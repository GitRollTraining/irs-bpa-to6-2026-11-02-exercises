"""The practice kit's route to the model the extractor calls.

    python3 model.py SYSTEM_PROMPT_FILE NOTE_FILE [--schema SCHEMA_FILE] [--model NAME]
    python3 model.py SYSTEM_PROMPT_FILE NOTE_FILE --functions FUNCTIONS_FILE

prints the model's reply as text. From Python: `from model import ask`, then
`ask(system_prompt, note_text, schema=None, model=None, functions=None)` returns the same text.

With `functions` (a list of function definitions, each with a name, a description, an
input_schema and, optionally, strict), the model may answer with calls to them, and the reply is
JSON: {"text": what the model wrote, "calls": [{"name": ..., "arguments": {...}}]}, with "calls"
empty when it made none. The reply is the model's first answer: no function is run here.

One setting decides where the request goes: model-route.json beside this file, which names the
route, the model and, for Codex, the reasoning level. The route the hosted workspace uses is set
there by the course team; nothing in an exercise names a route. Two routes: "codex", the Codex CLI
the course setup installs (codex exec), and "claude-code", Claude Code's print mode (claude -p).
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import threading

SETTING = pathlib.Path(__file__).resolve().parent / "model-route.json"
SERVER_NAME = "kit"


def _route():
    return json.loads(SETTING.read_text())


def _said(errors):
    """The last lines a failed run wrote: where Codex and Claude Code say what went wrong."""
    lines = [line.strip() for line in errors.splitlines() if line.strip()]
    return " ".join(lines[-2:])


def _codex_cli():
    """The codex command: the one on PATH, else the one in ~/.local/bin, where the course's install command
    puts it. A notebook's kernel, which the editor starts, often has no ~/.local/bin on its PATH: the
    installer adds that folder in the shell's start-up file, which only a terminal reads."""
    found = shutil.which("codex")
    if found:
        return found
    local = pathlib.Path.home() / ".local" / "bin" / "codex"
    return str(local) if local.is_file() and os.access(local, os.X_OK) else "codex"


def _codex_command(system_prompt, model, effort, folder):
    # Codex's non-interactive mode, as one plain request: none of the user's own settings, no
    # session kept, no shell and no web search, in an empty folder it may only read, so the reply
    # depends on the system prompt and the note alone. The system prompt goes in as Codex's
    # developer instructions, the message the model reads before the note.
    cmd = [_codex_cli(), "exec", "--ephemeral", "--ignore-user-config", "--skip-git-repo-check",
           "--sandbox", "read-only", "--color", "never", "-C", str(folder), "-m", model,
           "-c", "features.shell_tool=false", "-c", 'web_search="disabled"',
           "-c", "developer_instructions=" + json.dumps(system_prompt, ensure_ascii=False)]
    if effort:
        cmd += ["-c", "model_reasoning_effort=" + json.dumps(effort)]
    return cmd


def _run(cmd, **kwargs):
    """Start a route's command; a missing command or a run past 180 seconds is the route's failure."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=180,
                              **kwargs)
    except FileNotFoundError:
        raise RuntimeError(f"the model route failed: {pathlib.Path(cmd[0]).name} is not installed (the course "
                           "README, Set up once)") from None
    except subprocess.TimeoutExpired:
        raise RuntimeError("the model route failed: no reply in 180 seconds") from None


def _codex(system_prompt, note_text, schema, model, effort=None):
    with tempfile.TemporaryDirectory() as tmp:
        files, folder = pathlib.Path(tmp), pathlib.Path(tmp) / "work"
        folder.mkdir()
        cmd = _codex_command(system_prompt, model, effort, folder)
        if schema is not None:
            # As on Claude Code's route, the draft line is dropped and the rest is sent as written.
            (files / "schema.json").write_text(json.dumps({k: v for k, v in schema.items() if k != "$schema"}))
            cmd += ["--output-schema", str(files / "schema.json")]
        reply = files / "reply.txt"
        result = _run(cmd + ["-o", str(reply), "--", note_text])
        if result.returncode != 0 or not reply.is_file() or not reply.read_text().strip():
            raise RuntimeError(f"the model route failed: {_said(result.stderr) or 'no reply'}")
        return reply.read_text().strip()


def _codex_functions(system_prompt, note_text, functions, model, effort=None):
    # Codex offers functions to the model only as MCP tools, so this file serves the definitions as a
    # small MCP server (see _serve_functions) for one run, as on Claude Code's route. MCP has no strict
    # setting, so `strict` is not sent: on this route it has no effect, and the kit's tests check each
    # recorded call against the input schema in your own code.
    with tempfile.TemporaryDirectory() as tmp:
        files, folder = pathlib.Path(tmp), pathlib.Path(tmp) / "work"
        folder.mkdir()
        served = files / "functions.json"
        served.write_text(json.dumps(functions))
        server = [str(pathlib.Path(__file__).resolve()), "--serve", str(served)]
        cmd = _codex_command(system_prompt, model, effort, folder) + [
            "-c", f"mcp_servers.{SERVER_NAME}.command=" + json.dumps(sys.executable),
            "-c", f"mcp_servers.{SERVER_NAME}.args=" + json.dumps(server), "--json", "--", note_text]
        with open(files / "errors.txt", "w+") as errors:
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=errors, stdin=subprocess.DEVNULL,
                                        text=True)
            except FileNotFoundError:
                raise RuntimeError("the model route failed: codex is not installed (the course README, Set "
                                   "up once)") from None
            watchdog = threading.Timer(180, proc.kill)
            watchdog.start()
            text, calls, seen, error = [], [], set(), None
            try:
                for line in proc.stdout:
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    kind, item = event.get("type"), event.get("item") or {}
                    if item.get("type") == "mcp_tool_call" and item.get("server") == SERVER_NAME:
                        if item.get("id") not in seen:
                            seen.add(item.get("id"))
                            calls.append({"name": item.get("tool"), "arguments": item.get("arguments") or {}})
                        if kind == "item.completed":
                            break  # the first call came back: the model's first answer was its calls
                    elif kind == "item.completed" and item.get("type") == "agent_message":
                        text.append(item.get("text", ""))
                    elif kind in ("turn.failed", "error"):
                        error = (event.get("error") or {}).get("message") or event.get("message") or "the run failed"
                        break
                    elif kind == "turn.completed":
                        break
            finally:
                watchdog.cancel()
                proc.kill()
                proc.wait(timeout=30)
                proc.stdout.close()
                errors.seek(0)
                said = _said(errors.read())
        if error or (not text and not calls):
            raise RuntimeError(f"the model route failed: {error or said or 'no reply'}")
    return json.dumps({"text": "\n".join(t for t in text if t).strip(), "calls": calls})


def _claude_code(system_prompt, note_text, schema, model, effort=None):
    # Claude Code's print mode, with no tools and none of the user's own settings, so the reply
    # depends on the system prompt and the note alone.
    cmd = ["claude", "-p", "--safe-mode", "--model", model, "--system-prompt", system_prompt,
           "--tools", "", "--no-session-persistence", "--output-format", "json"]
    if schema is not None:
        # This route's schema check does not load the 2020-12 draft a "$schema" line may name; the
        # draft line is dropped and the rest of the schema is sent as written.
        cmd += ["--json-schema", json.dumps({k: v for k, v in schema.items() if k != "$schema"})]
    result = subprocess.run(cmd + [note_text], capture_output=True, text=True, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(f"the model route failed: {result.stderr.strip() or result.stdout.strip()}")
    reply = json.loads(result.stdout)
    if reply.get("is_error"):
        raise RuntimeError(f"the model route returned an error: {reply.get('result')}")
    return reply["result"]


def _claude_code_functions(system_prompt, note_text, functions, model, effort=None):
    # Claude Code offers functions to the model only as MCP tools, so this file serves the
    # definitions as a small MCP server (see _serve_functions) for one print-mode call. Safe mode
    # turns MCP servers off; empty setting sources and --strict-mcp-config keep the user's own
    # settings, instructions and servers out instead. MCP has no strict setting, so `strict` is
    # not sent: on this route it has no effect, and the kit's tests check each recorded call
    # against the input schema in your own code.
    with tempfile.TemporaryDirectory() as tmp:
        served = pathlib.Path(tmp) / "functions.json"
        served.write_text(json.dumps(functions))
        server = {"command": sys.executable, "args": [str(pathlib.Path(__file__).resolve()), "--serve", str(served)]}
        # --mcp-config takes several values, so it comes before the other options, not last.
        cmd = ["claude", "-p", "--mcp-config", json.dumps({"mcpServers": {SERVER_NAME: server}}),
               "--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands",
               "--model", model, "--system-prompt", system_prompt, "--tools", "", "--no-session-persistence",
               "--output-format", "stream-json", "--verbose", note_text]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        watchdog = threading.Timer(180, proc.kill)
        watchdog.start()
        text, calls, error = [], [], None
        try:
            for line in proc.stdout:
                event = json.loads(line)
                if event.get("type") == "assistant":
                    for block in event["message"]["content"]:
                        if block.get("type") == "text":
                            text.append(block["text"])
                        elif block.get("type") == "tool_use":
                            calls.append({"name": block["name"].removeprefix(f"mcp__{SERVER_NAME}__"),
                                          "arguments": block["input"]})
                elif event.get("type") == "user" and calls:
                    break  # the model's first answer was a call; stop before Claude Code goes on
                elif event.get("type") == "result":
                    if event.get("is_error"):
                        error = event.get("result") or event.get("subtype")
                    break
        finally:
            watchdog.cancel()
            proc.kill()
            stderr = proc.communicate(timeout=30)[1]
        if error or (not text and not calls):
            raise RuntimeError(f"the model route failed: {error or stderr.strip() or 'no reply'}")
    return json.dumps({"text": "\n".join(text).strip(), "calls": calls})


def _serve_functions(path):
    # A minimal MCP server over standard input and output, offering the definitions in `path`.
    # It never runs a function: a call that reaches it gets an error, as the route stops first.
    functions = json.loads(pathlib.Path(path).read_text())
    tools = [{"name": f["name"], "description": f.get("description", ""), "inputSchema": f["input_schema"]}
             for f in functions]

    def send(message_id, result=None, error=None):
        reply = {"jsonrpc": "2.0", "id": message_id}
        reply.update({"error": error} if error else {"result": result})
        sys.stdout.write(json.dumps(reply) + "\n")
        sys.stdout.flush()

    for line in sys.stdin:
        if not line.strip():
            continue
        message = json.loads(line)
        method, message_id = message.get("method"), message.get("id")
        if message_id is None:
            continue
        if method == "initialize":
            send(message_id, {"protocolVersion": message["params"].get("protocolVersion", "2025-06-18"),
                              "capabilities": {"tools": {}}, "serverInfo": {"name": SERVER_NAME, "version": "1"}})
        elif method == "tools/list":
            send(message_id, {"tools": tools})
        elif method == "tools/call":
            send(message_id, {"content": [{"type": "text", "text": "Not run: the practice kit records calls only."}],
                              "isError": True})
        elif method == "ping":
            send(message_id, {})
        else:
            send(message_id, error={"code": -32601, "message": f"{method} is not supported"})


# Claude Code's route takes no level: the setting's "effort" is Codex's reasoning level.
ROUTES = {"codex": _codex, "claude-code": _claude_code}
FUNCTION_ROUTES = {"codex": _codex_functions, "claude-code": _claude_code_functions}


def ask(system_prompt, note_text, schema=None, model=None, functions=None):
    route = _route()
    model, effort = model or route["model"], route.get("effort")
    if functions is not None:
        return FUNCTION_ROUTES[route["route"]](system_prompt, note_text, functions, model, effort)
    return ROUTES[route["route"]](system_prompt, note_text, schema, model, effort)


def main():
    if sys.argv[1:2] == ["--serve"]:
        _serve_functions(sys.argv[2])
        return
    parser = argparse.ArgumentParser(description="Send one note to the model the extractor calls.")
    parser.add_argument("system_prompt_file")
    parser.add_argument("note_file")
    parser.add_argument("--schema", help="a JSON Schema file the reply must match")
    parser.add_argument("--functions", help="a JSON file listing the function definitions the model may call")
    parser.add_argument("--model", help="a model name, in place of the one model-route.json names")
    args = parser.parse_args()
    schema = json.loads(pathlib.Path(args.schema).read_text()) if args.schema else None
    functions = json.loads(pathlib.Path(args.functions).read_text()) if args.functions else None
    print(ask(pathlib.Path(args.system_prompt_file).read_text(), pathlib.Path(args.note_file).read_text(),
              schema, args.model, functions))


if __name__ == "__main__":
    main()
