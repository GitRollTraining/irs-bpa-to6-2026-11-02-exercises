"""The practice kit's route to the model the extractor calls.

    python3 ~/practice/model.py SYSTEM_PROMPT_FILE NOTE_FILE [--schema SCHEMA_FILE] [--model NAME]
    python3 ~/practice/model.py SYSTEM_PROMPT_FILE NOTE_FILE --functions FUNCTIONS_FILE

prints the model's reply as text. From Python: `from model import ask`, then
`ask(system_prompt, note_text, schema=None, model=None, functions=None)` returns the same text.

With `functions` (a list of function definitions, each with a name, a description, an
input_schema and, optionally, strict), the model may answer with calls to them, and the reply is
JSON: {"text": what the model wrote, "calls": [{"name": ..., "arguments": {...}}]}, with "calls"
empty when it made none. The reply is the model's first answer: no function is run here.

One setting decides where the request goes: model-route.json beside this file. The route the
hosted workspace uses is set there by the course team; nothing in an exercise names a route.
"""
import argparse
import json
import pathlib
import subprocess
import sys
import tempfile
import threading

SETTING = pathlib.Path(__file__).resolve().parent / "model-route.json"
SERVER_NAME = "kit"


def _route():
    return json.loads(SETTING.read_text())


def _claude_code(system_prompt, note_text, schema, model):
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


def _claude_code_functions(system_prompt, note_text, functions, model):
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


ROUTES = {"claude-code": _claude_code}
FUNCTION_ROUTES = {"claude-code": _claude_code_functions}


def ask(system_prompt, note_text, schema=None, model=None, functions=None):
    route = _route()
    if functions is not None:
        return FUNCTION_ROUTES[route["route"]](system_prompt, note_text, functions, model or route["model"])
    return ROUTES[route["route"]](system_prompt, note_text, schema, model or route["model"])


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
