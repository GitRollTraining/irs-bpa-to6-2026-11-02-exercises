import asyncio
import base64
import importlib.util
import json
import io
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace as NS
import tempfile
import unittest
from unittest.mock import AsyncMock, patch

spec = importlib.util.spec_from_file_location('to6_platform', Path(__file__).parent / 'databricks_platform.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


def response(value):
    return {'content': [{'type': 'text', 'text': value}], 'isError': False}


class BoundaryTests(unittest.TestCase):
    def test_direct_cli_sdk_import_does_not_shadow_stdlib_platform(self):
        try:
            sdk_available = importlib.util.find_spec('databricks.sdk') is not None
        except ModuleNotFoundError:
            sdk_available = False
        if not sdk_available:
            self.skipTest('Install requirements to exercise direct CLI SDK import.')
        command = Path(__file__).parent / 'databricks_platform.py'
        result = subprocess.run([sys.executable, str(command), 'check'], capture_output=True,
                                text=True, env={**os.environ, 'DATABRICKS_HOST': 'https://localhost.invalid'})
        self.assertEqual(result.returncode, 1)
        self.assertIn('Unset Databricks credential/host environment overrides', result.stderr)
        self.assertNotIn('AttributeError', result.stderr)
        self.assertFalse((command.parent / 'platform.py').exists())

    def test_saved_profile_reaches_sdk_and_native_child_without_drift(self):
        cfg = p.identity_config('alice@example.test', 'https://github.com/alice/work', 'EXISTING_COURSE')
        cfg['host'] = 'https://workspace.example.test'
        with patch.dict(os.environ, {'DATABRICKS_CONFIG_PROFILE': 'WRONG_PROFILE',
                                    'DATABRICKS_TOKEN': 'unused-test-value'}, clear=True):
            child = p.native_environment(cfg)
            self.assertEqual(child['DATABRICKS_CONFIG_PROFILE'], 'EXISTING_COURSE')
            self.assertNotIn('DATABRICKS_TOKEN', child)
        try:
            import databricks.sdk
        except ImportError:
            self.skipTest('Install requirements to exercise SDK profile dispatch.')
        w = NS(current_user=NS(me=lambda: NS(user_name='alice@example.test')),
               config=NS(host=cfg['host']))
        with tempfile.TemporaryDirectory() as directory, patch.object(p, 'STATE', Path(directory)), \
             patch.dict(os.environ, {}, clear=True), \
             patch('databricks.sdk.WorkspaceClient', return_value=w) as client, \
             patch.object(p, 'execute', new=AsyncMock(return_value={'success': True})) as execute, \
             patch('sys.stdin', io.StringIO('{"code":"print(1)"}')):
            p.save('config.json', cfg)
            asyncio.run(p.main(NS(command='execute')))
            client.assert_called_once_with(profile='EXISTING_COURSE')
            self.assertEqual(execute.call_args.args[1]['profile'], 'EXISTING_COURSE')

    def test_repo_requires_base_url(self):
        for bad in ('https://github.com/a/b/tree/main', 'https://evil.com/a/b', 'git@github.com:a/b',
                    'https://github.com/a/b.git', 'https://github.com/a/..'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                p.repo_parts(bad)

    def test_output_scopes_are_identity_bound(self):
        a = p.identity_config('alice@example.test', 'https://github.com/alice/work')
        b = p.identity_config('bob@example.test', 'https://github.com/bob/work')
        self.assertNotEqual(a['output_schema'], b['output_schema'])
        self.assertEqual(a['workspace_path'], '/Users/alice@example.test/to6-challenge4/notebook')
        with self.assertRaises(ValueError):
            p.identity_config('../bob', 'https://github.com/alice/work')

    def test_browser_scaffold_uses_the_same_authenticated_schema(self):
        notebook = (Path(__file__).parent / 'notebook.py').read_text()
        setup = notebook.split('# MAGIC ## 1.')[0]  # the setup cell only; later cells need Databricks
        for username in ('alice@example.test', 'Learner.MixedCase@example.test'):
            spark = NS(sql=lambda query: NS(first=lambda: {'username': username}))
            path = f'/Users/{username}/fork/week-04/day-05/notebook'
            context = NS(notebookPath=lambda: NS(get=lambda: path))
            dbutils = NS(notebook=NS(entry_point=NS(getDbutils=lambda: NS(notebook=lambda: NS(getContext=lambda: context)))))
            scope = {'spark': spark, 'dbutils': dbutils, 'print': lambda *args: None}
            exec(compile(setup, 'notebook.py', 'exec'), scope)
            self.assertEqual(scope['TASK_ROOT'].as_posix(), f'/Workspace/Users/{username}/fork/week-04/day-05')
            expected = p.identity_config(username, 'https://github.com/alice/work')
            self.assertEqual(scope['OUTPUT_SCHEMA'], expected['output_schema'])
            self.assertEqual(scope['INPUT_SCHEMA'], expected['input_schema'])
            self.assertEqual(scope['EXPERIMENT'], f'/Users/{username}/week-04-challenge')

    def test_native_files_reject_traversal_and_source_replacement(self):
        for bad in ('outputs/../secret', 'outputs//x', 'outputs/x/../../x', 'notebook.py',
                    'README.md', '/tmp/x', 'outputs/x\\y', 'outputs/native-run.json'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                p.native_files({'files': {'SUBMISSION.md': 'x', bad: 'bad'}}, b'code')

    def test_native_handoff_required_and_readme_never_overwritten(self):
        with self.assertRaises(ValueError):
            p.native_files({'files': {'outputs/a.json': '{}'}}, b'code')
        files = p.native_files({'files': {'SUBMISSION.md': 'handoff', 'outputs/a.json': '{}'}}, b'code')
        self.assertEqual(files['notebook.py'], 'code')
        self.assertEqual(files['SUBMISSION.md'], 'handoff')
        self.assertNotIn('README.md', files)

    def test_native_source_must_match_latest_success_and_live_run(self):
        cfg = {'workspace_path': '/Users/alice/n'}
        last = {**cfg, 'success': True, 'source_sha256': p.digest(b'source')}
        p.validate_execution(last, b'source', 'SUCCESS', cfg)
        for updated, source, state in [({**last, 'success': False}, b'source', 'SUCCESS'),
                                       (last, b'edited', 'SUCCESS'), (last, b'source', 'FAILED'),
                                       ({**last, 'workspace_path': '/Users/bob/n'}, b'source', 'SUCCESS')]:
            with self.assertRaises(ValueError):
                p.validate_execution(updated, source, state, cfg)

    def test_readback_hash_checks_exact_bytes_including_final_newline(self):
        data = b'hello\n'
        result = response('successfully downloaded text file (SHA: ' + p.blob_sha(data) + ')\nhello')
        p.verify_readback(result, data)
        with self.assertRaises(ValueError):
            p.verify_readback(result, b'hello')
        encoded = {'structuredContent': {'encoding': 'base64', 'content': base64.b64encode(data).decode()}}
        p.verify_readback(encoded, data)
        with self.assertRaises(ValueError):
            p.verify_readback({'isError': True}, data)

    def test_execute_refuses_local_file_input_before_any_connection(self):
        with self.assertRaises(ValueError):
            asyncio.run(p.execute(None, {}, {'file_path': '/tmp/notebook.py'}))
        with self.assertRaises(ValueError):
            asyncio.run(p.execute(None, {}, {'code': 'print(1)', 'file_path': '/tmp/notebook.py'}))

    def test_operator_github_identity_cannot_submit_for_learner(self):
        with patch.object(p, 'managed', new=AsyncMock(return_value={'structuredContent': {'login': 'operator'}})):
            with self.assertRaises(ValueError):
                asyncio.run(p.verify_github_owner(None, {'owner': 'learner'}))

    def test_failed_readback_records_remote_mutation_but_not_verified(self):
        source = b'# Databricks notebook source\nprint(1)\n'
        cfg = {'workspace_path': '/Users/alice/n', 'repository': 'https://github.com/alice/work',
               'output_schema': 'training.to6_c4_abc'}
        last = {**cfg, 'success': True, 'run_id': 1, 'source_sha256': p.digest(source)}
        w = NS(jobs=NS(get_run=lambda _: NS(state=NS(result_state=NS(value='SUCCESS')), tasks=[NS(run_id=2)]),
                        get_run_output=lambda _: NS(notebook_output=NS(truncated=False,
                            result=json.dumps({'files': {'SUBMISSION.md': 'handoff'}})))))
        sha = 'a' * 40
        with tempfile.TemporaryDirectory() as directory, patch.object(p, 'STATE', Path(directory)), \
             patch.object(p, 'verify_github_owner', new=AsyncMock(return_value='alice')), \
             patch.object(p, 'export_source', return_value=source), \
             patch.object(p, 'github', new=AsyncMock(side_effect=[{'structuredContent': {'object': {'sha': sha}}},
                                                                response('unsupported')])) as gh:
            p.save('last-execution.json', last)
            with self.assertRaises(ValueError):
                asyncio.run(p.submit(w, cfg))
            receipt = p.load('submission.json')
            self.assertFalse(receipt['verified'])
            self.assertEqual(receipt['commit'], sha)
            self.assertEqual(gh.call_args_list[1].args[3]['sha'], sha)
            self.assertEqual(gh.call_args_list[1].args[3]['path'], 'week-04/day-05/notebook.py')


if __name__ == '__main__':
    unittest.main()
