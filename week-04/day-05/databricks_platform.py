#!/usr/bin/env python3
"""Native Databricks operations. Local files are configuration/receipts, never solutions."""
import argparse
import asyncio
import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from datetime import timedelta

ROOT = Path(__file__).resolve().parent
# The Challenge's folder in the learner's fork of the exercise repository; submitted files go here.
FOLDER = 'week-04/day-05/'
STATE = ROOT / '.platform'
KIT = ROOT / '.tools/ai-dev-kit'
PIN = '07f8e1ccf3dfc09a794eaf86fd15a5848f9d63d4'
INPUT_SCHEMA = 'training.to6_challenge4_inputs'
INPUT_TABLES = ('closed_returns', 'new_returns')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def repo_parts(url):
    m = re.fullmatch(r'https://github\.com/([A-Za-z0-9-]+)/([A-Za-z0-9_.-]+)', url)
    require(m is not None, 'Use the base https://github.com/owner/repository URL.')
    owner, repo = m.groups()
    require(repo not in ('.', '..') and not repo.endswith('.git'), 'Use the repository base URL, without .git.')
    return owner, repo


def identity_config(username, repo, profile='TO6'):
    require(bool(username) and '/' not in username and '\\' not in username and username not in ('.', '..'),
            'Workspace identity is not a valid personal notebook path.')
    owner, name = repo_parts(repo)
    require(isinstance(profile, str) and bool(profile.strip()), 'A named Databricks authentication profile is required.')
    return {'profile': profile, 'username': username, 'repository': repo,
            'owner': owner, 'repo': name, 'branch': 'main',
            'workspace_path': f'/Users/{username}/to6-challenge4/notebook',
            'input_schema': INPUT_SCHEMA,
            'output_schema': 'training.to6_c4_' + digest(username.encode())[:12]}


def save(name, value):
    STATE.mkdir(exist_ok=True)
    target = STATE / name
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(target)


def load(name):
    return json.loads((STATE / name).read_text())


def unpack(result):
    require(not result.get('isError'), 'MCP operation failed; inspect the operation in Databricks. No credentials are printed.')
    if result.get('structuredContent') is not None:
        return result['structuredContent']
    for block in result.get('content', []):
        if block.get('type') == 'text':
            try:
                return json.loads(block['text'])
            except json.JSONDecodeError:
                return block['text']
    raise ValueError('MCP returned no readable result.')


def verify_readback(result, expected):
    """GitHub MCP text rendering may omit a final LF; Git blob SHA binds exact bytes."""
    value = unpack(result)
    if isinstance(value, dict) and value.get('encoding') == 'base64':
        require(base64.b64decode(value['content']) == expected, 'GitHub content differs from native export.')
        return
    if isinstance(value, str):
        m = re.match(r'successfully downloaded text file \(SHA: ([0-9a-f]{40})\)\n', value)
        require(m is not None and m[1] == blob_sha(expected), 'GitHub blob hash differs or cannot be verified.')
        return
    raise ValueError('Unsupported GitHub readback format; no successful submission receipt written.')


def native_files(payload, source):
    require(isinstance(payload, dict) and isinstance(payload.get('files'), dict),
            'Notebook must exit JSON with files: {SUBMISSION.md: text, outputs/name.json: text}.')
    files = payload['files']
    require('SUBMISSION.md' in files, 'Native handoff SUBMISSION.md is required.')
    for name, content in files.items():
        p = PurePosixPath(name)
        require(name == 'SUBMISSION.md' or (name.startswith('outputs/') and len(p.parts) > 1
                and '..' not in p.parts and '\\' not in name and str(p) == name),
                'Only SUBMISSION.md and files below outputs/ can be submitted.')
        require(isinstance(content, str), 'Native output files must be text.')
    require('outputs/native-run.json' not in files, 'outputs/native-run.json is reserved for the run receipt.')
    return {'notebook.py': source.decode('utf-8'), **files}


def validate_execution(last, source, state, config):
    require(last.get('success') is True, 'The latest attempted execution did not succeed; execute successfully before submitting.')
    require(last.get('source_sha256') == digest(source), 'Native source changed since successful execution; execute again.')
    require(last.get('workspace_path') == config['workspace_path'], 'Execution belongs to another notebook.')
    require(state == 'SUCCESS', 'Databricks does not report the bound run as successful.')


async def managed(w, service, name, args):
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client
    url = w.config.host.rstrip('/') + '/ai-gateway/mcp-services/system.ai.' + service
    async with streamablehttp_client(url, headers=w.config.authenticate()) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            return (await session.call_tool(name, args)).model_dump(mode='json')


async def github(w, cfg, tool, args):
    return await managed(w, 'github', tool, {'owner': cfg['owner'], 'repo': cfg['repo'], **args})


async def verify_github_owner(w, cfg):
    identity = unpack(await managed(w, 'github', 'get_me', {}))
    require(isinstance(identity, dict) and isinstance(identity.get('login'), str)
            and identity['login'].lower() == cfg['owner'].lower(),
            'GitHub connection is not the owner of your personal submission repository.')
    return identity['login']


def export_source(w, cfg):
    from databricks.sdk.service.workspace import ExportFormat
    return base64.b64decode(w.workspace.export(cfg['workspace_path'], format=ExportFormat.SOURCE).content)


def native_environment(cfg):
    env = {k: v for k, v in os.environ.items() if not k.startswith('DATABRICKS_')}
    env['DATABRICKS_CONFIG_PROFILE'] = cfg['profile']
    return env


async def execute(w, cfg, request):
    require(set(request) == {'code'} and isinstance(request['code'], str) and request['code'].strip(),
            'execute accepts only JSON {"code": "inline notebook source"}; file_path is not supported.')
    require(subprocess.check_output(['git', '-C', str(KIT), 'rev-parse', 'HEAD'], text=True).strip() == PIN,
            'ai-dev-kit does not match the pinned revision; repeat setup.')
    require(not subprocess.check_output(['git', '-C', str(KIT), 'status', '--porcelain', '--untracked-files=no'], text=True).strip(),
            'ai-dev-kit has modified tracked files; restore the pinned installation.')
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    code = request['code']
    if not code.startswith('# Databricks notebook source\n'):
        code = '# Databricks notebook source\n' + code
    save('last-execution.json', {'success': False, 'state': 'STARTED', 'workspace_path': cfg['workspace_path']})
    # Credential values stay with SDK profile authentication, not in notebook code or receipts.
    env = native_environment(cfg)
    params = StdioServerParameters(command=sys.executable,
                                   args=[str(KIT / 'databricks-mcp-server/run_server.py')], env=env)
    with (STATE / 'server.log').open('a') as err:
        async with stdio_client(params, errlog=err) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=420)) as session:
                await session.initialize()
                response = await session.call_tool('execute_code', {
                    'code': code, 'compute_type': 'serverless', 'workspace_path': cfg['workspace_path'],
                    'run_name': 'TO6 Challenge 4', 'timeout': 300})
    result = unpack(response.model_dump(mode='json'))
    require(isinstance(result, dict), 'Unexpected execution response.')
    record = {'success': False, 'workspace_path': cfg['workspace_path'],
              'run_id': result.get('run_id'), 'run_url': result.get('run_url')}
    save('last-execution.json', record)
    if record.get('run_id'):
        save(f"run-{record['run_id']}.json", record)
    if result.get('success') is not True or not result.get('run_id'):
        print(json.dumps(record))
        raise ValueError('Execution did not finish successfully; inspect the native run, then execute again.')
    run = w.jobs.get_run(result['run_id'])
    require(run.state.result_state.value == 'SUCCESS', 'Run has not reached SUCCESS.')
    source = export_source(w, cfg)
    require(source.rstrip(b'\n') == code.encode().rstrip(b'\n'), 'Native source differs from the inline request.')
    record.update(success=True, source_sha256=digest(source))
    save('last-execution.json', record)
    # Retain rejection and successful run references without storing a local solution.
    save(f"run-{result['run_id']}.json", record)
    return record


async def submit(w, cfg):
    await verify_github_owner(w, cfg)
    last = load('last-execution.json')
    require(last.get('success') is True, 'Latest execution was not successful.')
    run = w.jobs.get_run(last['run_id'])
    source = export_source(w, cfg)
    validate_execution(last, source, run.state.result_state.value, cfg)
    require(len(run.tasks or []) == 1, 'Expected one notebook task; refusing ambiguous output.')
    output = w.jobs.get_run_output(run.tasks[0].run_id)
    require(output.notebook_output and not output.notebook_output.truncated, 'Native notebook output missing or truncated.')
    files = native_files(json.loads(output.notebook_output.result), source)
    files['outputs/native-run.json'] = json.dumps({**last, 'output_schema': cfg['output_schema']}, indent=2) + '\n'
    # Recheck just before the remote commit. A concurrent native edit forces a new run.
    require(export_source(w, cfg) == source, 'Notebook changed during export; execute again.')
    pushed = unpack(await github(w, cfg, 'push_files', {'branch': 'main',
        'message': 'Submit native Databricks notebook and handoff',
        'files': [{'path': FOLDER + name, 'content': text} for name, text in files.items()]}))
    sha = pushed['object']['sha']
    require(re.fullmatch(r'[0-9a-f]{40}', sha) is not None, 'Invalid commit SHA returned.')
    # Persist pending commit immediately: a failed readback must not hide that a push occurred.
    receipt = {'verified': False, 'repository': cfg['repository'], 'commit': sha,
               'branch': 'main', 'run_id': last['run_id'], 'files': {n: blob_sha(t.encode()) for n, t in files.items()}}
    save('submission.json', receipt)
    for name, text in files.items():
        response = await github(w, cfg, 'get_file_contents', {'path': FOLDER + name, 'sha': sha})
        verify_readback(response, text.encode())
    receipt['verified'] = True
    save('submission.json', receipt)
    return receipt


async def main(args):
    from databricks.sdk import WorkspaceClient
    # Reject credential overrides: the named profile must determine the learner identity.
    require(not any(k in os.environ for k in ('DATABRICKS_TOKEN', 'DATABRICKS_CLIENT_SECRET', 'DATABRICKS_HOST')),
            'Unset Databricks credential/host environment overrides; use your saved login profile.')
    if args.command == 'init':
        require(not (STATE / 'config.json').exists(), 'Already initialized; inspect .platform/config.json instead of replacing it.')
        profile = args.profile
        cfg = None
    else:
        cfg = load('config.json')
        profile = cfg['profile']
    w = WorkspaceClient(profile=profile)
    username = w.current_user.me().user_name
    if args.command == 'init':
        cfg = identity_config(username, args.repository, profile)
        cfg['host'] = w.config.host
        save('config.json', cfg)
        return cfg
    expected = identity_config(username, cfg['repository'], profile)
    require({k: cfg[k] for k in expected} == expected
            and cfg['host'] == w.config.host, 'Profile identity/config changed; do not use another learner configuration.')
    if args.command == 'check':
        github_owner = await verify_github_owner(w, cfg)
        descriptions = []
        for name in INPUT_TABLES:
            table = w.tables.get(INPUT_SCHEMA + '.' + name)
            require(bool(table.comment) and bool(table.columns), 'Input table needs columns and description.')
            descriptions.append(table.full_name)
        w.schemas.get(cfg['output_schema'])
        w.workspace.get_status('/Users/' + username)
        unpack(await github(w, cfg, 'get_file_contents', {'path': FOLDER + 'README.md', 'ref': 'main'}))
        return {'identity': username, 'host': cfg['host'], 'inputs': descriptions,
                'output_schema': cfg['output_schema'], 'github_read': True, 'github_identity': github_owner,
                'limits': 'Read checks only. Native write/compute, MLflow logging, GitHub write, ACL isolation and session capture require the walkthrough.'}
    if args.command == 'execute':
        return await execute(w, cfg, json.load(sys.stdin))
    if args.command == 'sql':
        if args.statement_id:
            return unpack(await managed(w, 'dbsql', 'poll_sql_result', {'statement_id': args.statement_id}))
        request = json.load(sys.stdin)
        require(set(request) == {'query'} and isinstance(request['query'], str), 'sql expects JSON {"query":"SQL"}.')
        # No prefix filter can sandbox SQL. Unity Catalog grants are the authority.
        return unpack(await managed(w, 'dbsql', 'execute_sql', request))
    if args.command == 'submit':
        return await submit(w, cfg)
    if args.command == 'read':
        receipt = load('submission.json')
        require(args.path in receipt['files'], 'Path is not part of the submitted file set.')
        result = await github(w, cfg, 'get_file_contents', {'path': FOLDER + args.path, 'sha': receipt['commit']})
        return {'commit': receipt['commit'], 'file': args.path, 'result': unpack(result)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest='command', required=True)
    init_parser = subs.add_parser('init')
    init_parser.add_argument('--repository', required=True)
    init_parser.add_argument('--profile', default='TO6')
    for command in ('check', 'execute', 'submit'):
        subs.add_parser(command)
    subs.add_parser('sql').add_argument('--statement-id')
    subs.add_parser('read').add_argument('path')
    try:
        print(json.dumps(asyncio.run(main(parser.parse_args())), indent=2))
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except Exception as error:
        # Auth/HTTP errors can contain headers. Do not echo their values into a captured session.
        print(f'{type(error).__name__}: operation failed; inspect the native platform status. No successful completion is claimed.', file=sys.stderr)
        sys.exit(1)
