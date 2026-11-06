"""Tests of model.py's route through Codex, with no call to a model: uv run .github/test_model.py.

A fake codex records each command line it gets, then answers as the course's stand-in does
(tools/stand-ins/codex), so the tests see both what model.py sends and how it reads the reply.
"""
import importlib.util
import json
import os
import pathlib
import shutil
import sys
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
STAND_IN = ROOT / "tools" / "stand-ins" / "codex"
FUNCTIONS = [{"name": "lookup_form", "description": "Gives the title of a tax form.",
              "input_schema": {"type": "object", "properties": {"form_number": {"type": "string"}},
                               "required": ["form_number"], "additionalProperties": False}}]
NOTE = "<note>Note 0147. Synthetic filer. Tax year 2023, Form 1040. Follow up in 30 days.</note>"


class CodexRouteTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="model-route-")
        self.addCleanup(temp.cleanup)
        self.root = pathlib.Path(temp.name)
        kit = self.root / "kit with spaces"
        kit.mkdir()
        shutil.copy(ROOT / "model.py", kit / "model.py")
        shutil.copy(ROOT / "model-route.json", kit / "model-route.json")
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.calls = self.root / "calls.jsonl"
        self.fake("")
        # HOME is a folder of the test's own, so no ~/.local/bin/codex of this machine is found.
        env = {"PATH": str(self.bin) + os.pathsep + os.environ["PATH"], "CODEX_STUB_STATE": str(self.root / "state"),
               "HOME": str(self.root / "home")}
        patch = mock.patch.dict(os.environ, env)
        patch.start()
        self.addCleanup(patch.stop)
        for name in ("CODEX_STUB_REPLIES", "CLAUDE_STUB_REPLIES"):
            os.environ.pop(name, None)
        spec = importlib.util.spec_from_file_location("model_under_test", kit / "model.py")
        self.model = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.model)

    def fake(self, before):
        """A codex that records its arguments, runs `before` (Python), then is the stand-in."""
        script = self.bin / "codex"
        script.write_text(f"""#!{sys.executable}
import json, os, sys
folder = sys.argv[sys.argv.index("-C") + 1] if "-C" in sys.argv else None
with open({str(self.calls)!r}, "a") as log:
    log.write(json.dumps({{"args": sys.argv[1:], "folder": os.listdir(folder) if folder else None}}) + "\\n")
{before}
os.execv({sys.executable!r}, [{sys.executable!r}, {str(STAND_IN)!r}] + sys.argv[1:])
""")
        script.chmod(0o755)

    def sent(self):
        return [json.loads(line)["args"] for line in self.calls.read_text().splitlines()]

    def setting(self, args, key):
        return next(json.loads(args[i + 1].split("=", 1)[1]) for i, arg in enumerate(args)
                    if arg == "-c" and args[i + 1].startswith(key + "="))

    def test_a_plain_request_with_the_setting_and_the_system_prompt(self):
        reply = json.loads(self.model.ask('Say "hi".\nThen stop.', NOTE))
        self.assertEqual(reply["tax_year"], 2023)
        args = self.sent()[0]
        route = json.loads((ROOT / "model-route.json").read_text())
        self.assertEqual(args[:1], ["exec"])
        for flag in ("--ephemeral", "--ignore-user-config", "--skip-git-repo-check"):
            self.assertIn(flag, args)
        self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
        self.assertEqual(args[args.index("-m") + 1], route["model"])
        self.assertEqual(self.setting(args, "model_reasoning_effort"), route["effort"])
        self.assertEqual(self.setting(args, "developer_instructions"), 'Say "hi".\nThen stop.')
        self.assertEqual(args[args.index("--") + 1], NOTE)
        self.assertEqual(json.loads(self.calls.read_text().splitlines()[0])["folder"], [])  # an empty folder

    def test_a_schema_goes_without_its_draft_line(self):
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object",
                  "properties": {"amount_in_question": {"type": ["integer", "null"]}}}
        seen = self.root / "schema-seen.json"
        self.fake(f"""import shutil
shutil.copy(sys.argv[sys.argv.index("--output-schema") + 1], {str(seen)!r})""")
        reply = json.loads(self.model.ask("Extract.", NOTE, schema))
        self.assertIn("amount_in_question", reply)
        self.assertEqual(json.loads(seen.read_text()), {k: v for k, v in schema.items() if k != "$schema"})

    def test_functions_come_back_as_the_first_calls(self):
        reply = json.loads(self.model.ask("Answer.", NOTE, functions=FUNCTIONS))
        self.assertEqual(reply["calls"], [{"name": "lookup_form", "arguments": {"form_number": "<form_number>"}}])
        args = self.sent()[0]
        self.assertIn("--json", args)
        self.assertEqual(self.setting(args, "mcp_servers.kit.args")[1:2], ["--serve"])

    def test_a_failed_sign_in_is_the_route_failing(self):
        self.fake('sys.stderr.write("Error: Not logged in. Run codex login.\\n"); sys.exit(1)')
        with self.assertRaisesRegex(RuntimeError, "the model route failed: .*codex login"):
            self.model.ask("Extract.", NOTE)
        with self.assertRaisesRegex(RuntimeError, "the model route failed: .*codex login"):
            self.model.ask("Answer.", NOTE, functions=FUNCTIONS)

    def test_codex_in_local_bin_when_path_lacks_it(self):
        # A notebook's kernel often has no ~/.local/bin on PATH, where the course's installer puts codex.
        local = pathlib.Path(os.environ["HOME"]) / ".local" / "bin"
        local.mkdir(parents=True)
        (self.bin / "codex").rename(local / "codex")
        with mock.patch.dict(os.environ, {"PATH": "/usr/bin:/bin"}):  # no folder that holds a codex
            reply = json.loads(self.model.ask("Extract.", NOTE))
        self.assertEqual(reply["tax_year"], 2023)
        self.assertEqual(self.sent()[0][:1], ["exec"])

    def test_no_codex_says_where_to_install_it(self):
        (self.bin / "codex").unlink()
        with mock.patch.dict(os.environ, {"PATH": str(self.bin)}):
            with self.assertRaisesRegex(RuntimeError, "codex is not installed"):
                self.model.ask("Extract.", NOTE)
            with self.assertRaisesRegex(RuntimeError, "codex is not installed"):
                self.model.ask("Answer.", NOTE, functions=FUNCTIONS)


if __name__ == "__main__":
    unittest.main()
