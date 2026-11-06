"""Isolated tests of the setup check: uv run .github/test_setup.py.

Uses temporary courses, synthetic identities, a fake model, and a fake Codex CLI. No test opens a
network connection beyond this machine; the notebook kernels talk to the check on loopback only.
"""
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import nbformat

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON = sys.executable
REAL_RUN = subprocess.run
FAKE_CODEX = """#!/bin/sh
case "$1 $2" in
  "--version "*) echo "codex-cli 0.0.0-test" ;;
  "login status")
    if [ -n "$FAKE_CODEX_SIGNED_OUT" ]; then echo "Not logged in" >&2; exit 1; fi
    echo "Logged in using ChatGPT" >&2 ;;
  *) exit 3 ;;
esac
"""


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class SetupCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="course-setup-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name) / "checkout with spaces"
        self.root.mkdir()
        self.home = self.root.parent / "home"
        self.home.mkdir()
        self.global_config = self.home / ".gitconfig"
        self.global_config.write_text("# leave untouched\n")
        tools = self.root.parent / "bin"
        tools.mkdir()
        (tools / "codex").write_text(FAKE_CODEX)
        (tools / "codex").chmod(0o755)
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("GIT_", "PYTHON", "CLAUDE", "CODEX", "VIRTUAL_ENV", "JUPYTER"))}
        self.env.update(HOME=str(self.home), USERPROFILE=str(self.home),
                        GIT_CONFIG_GLOBAL=str(self.global_config), GIT_CONFIG_NOSYSTEM="1",
                        PATH=os.pathsep.join([str(pathlib.Path(PYTHON).parent), str(tools), os.environ["PATH"]]),
                        PYTHONDONTWRITEBYTECODE="1")
        shutil.copy(ROOT / "check_setup.py", self.root / "check_setup.py")
        shutil.copytree(ROOT / "tools", self.root / "tools")
        (self.root / "model.py").write_text('''import os
from pathlib import Path
Path(__file__).with_name("model-imported").touch()
def ask(*args):
    Path(__file__).with_name("model-called").touch()
    if os.environ.get("FAKE_MODEL_FAIL"):
        raise RuntimeError("synthetic provider unavailable")
    return "ready"
''')
        (self.root / "model-route.json").write_text(json.dumps({"model": "fake"}))
        # No test may reach the network; a kernel and the check meet on loopback only.
        guard = self.root.parent / "guard"
        guard.mkdir()
        (guard / "sitecustomize.py").write_text('''import sys
LOOPBACK = {"127.0.0.1", "::1", "localhost", None, ""}
def audit(event, args):
    if event == "socket.connect" and isinstance(args[1], tuple) and args[1][0] not in LOOPBACK:
        raise RuntimeError("test network access forbidden")
    if event == "socket.getaddrinfo" and args[0] not in LOOPBACK:
        raise RuntimeError("test network access forbidden")
sys.addaudithook(audit)
''')
        self.env["PYTHONPATH"] = str(guard)
        self.git("init", "-q", "-b", "main")
        self.notebook("print('hello')")

    def git(self, *args, folder=None):
        return REAL_RUN(["git", "-C", str(folder or self.root), *args],
                        env=self.env, check=True, capture_output=True, text=True).stdout.strip()

    def notebook(self, *sources):
        """A day's notebook with these code cells, committed, as the course's notebooks are."""
        folder = self.root / "week-01/day-01"
        folder.mkdir(parents=True, exist_ok=True)
        nb = nbformat.v4.new_notebook()
        nb.cells = [nbformat.v4.new_markdown_cell("# Day 1")] + [nbformat.v4.new_code_cell(s) for s in sources]
        nbformat.write(nb, folder / "week-01-day-01.ipynb")
        self.git("add", "-A")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-qm", "The course")

    def identity(self):
        self.git("config", "--global", "user.name", "Learner")
        self.git("config", "--global", "user.email", "learner@example.invalid")

    def check(self, *args, expected=0, env=None, cwd=None):
        result = REAL_RUN([PYTHON, str(self.root / "check_setup.py"), *args],
                          env=env or self.env, cwd=cwd or self.root.parent,
                          capture_output=True, text=True, timeout=300)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_ready_from_another_folder_runs_the_notebook_without_the_model(self):
        self.identity()
        out = self.check()
        self.assertIn("Setup OK", out)
        self.assertIn("codex-cli 0.0.0-test, signed in", out)
        self.assertIn("all 1 cells of the 1 notebooks ran", out)
        self.assertFalse((self.root / "model-imported").exists())
        self.assertFalse((self.root / "week-01/day-01/.ipynb_checkpoints").exists())

    def test_missing_identity_is_actionable_and_read_only(self):
        out = self.check(expected=1)
        self.assertIn('git config --global user.name "Your Name"', out)
        self.assertIn('git config --global user.email "you@example.com"', out)
        self.assertEqual(self.global_config.read_text(), "# leave untouched\n")

    def test_codex_missing_or_signed_out_is_actionable(self):
        self.identity()
        env = dict(self.env, FAKE_CODEX_SIGNED_OUT="1")
        out = self.check(expected=1, env=env)
        self.assertIn("Codex CLI is not signed in (Not logged in): run codex login", out)
        env = dict(self.env, PATH=os.pathsep.join(p for p in self.env["PATH"].split(os.pathsep)
                                                  if not (pathlib.Path(p) / "codex").exists()))
        out = self.check(expected=1, env=env)
        self.assertIn("Codex CLI: install it with curl -fsSL https://chatgpt.com/codex/install.sh | sh", out)

    def test_model_probe_alone_succeeds_and_fails(self):
        out = self.check("--check-model")
        self.assertIn("Model OK: fake answered 'ready'", out)
        self.assertNotIn("notebooks", out)
        self.assertTrue((self.root / "model-called").exists())
        env = dict(self.env, FAKE_MODEL_FAIL="1")
        self.assertIn("synthetic provider unavailable", self.check("--check-model", expected=1, env=env))

    def test_missing_packages_and_git_are_actionable(self):
        self.identity()
        loaded = module(self.root / "check_setup.py", "check_packages")
        with mock.patch.dict(os.environ, self.env, clear=True), \
             mock.patch.object(loaded.importlib.metadata, "version",
                               side_effect=importlib.metadata.PackageNotFoundError):
            missing = []
            self.assertFalse(loaded.check_python(missing, []))
        for name in loaded.PACKAGES:
            self.assertIn(f"{name}: run uv sync in the course folder, then uv run check_setup.py", missing)
        with mock.patch.dict(os.environ, self.env, clear=True), \
             mock.patch.object(loaded, "git", side_effect=FileNotFoundError):
            missing = []
            self.assertFalse(loaded.check_git(missing, []))
        self.assertIn("Git: install Git 2.28 or later", missing)

    @unittest.skipIf(os.name == "nt", "Unix notebook shell interpreter check")
    def test_another_python_on_path(self):
        self.identity()
        shell = self.root.parent / "shell"
        shell.mkdir()
        fake = shell / "python3"
        fake.write_text("#!/bin/sh\necho /different/python/environment\n")
        fake.chmod(0o755)
        env = dict(self.env, PATH=str(shell) + os.pathsep + self.env["PATH"])
        self.assertIn("python3 on PATH is another Python", self.check(expected=1, env=env))

    def test_an_exercise_without_an_identity_is_named(self):
        self.git("config", "--local", "user.name", "Learner")
        self.git("config", "--local", "user.email", "learner@example.invalid")
        folder = self.root / "week-01/day-01/example"
        folder.mkdir()
        (folder / "start.py").touch()
        (folder / "lab").mkdir()
        self.git("init", "-q", "-b", "main", folder=folder / "lab")
        out = self.check(expected=1)
        self.assertIn("week-01/day-01/example/lab has no Git name or email", out)

    def test_a_failing_cell_is_named_and_your_work_is_left_alone(self):
        self.identity()
        self.notebook("print('fine')", "1 / 0", "!cat no-such-file.txt",
                      "!echo Done: nothing to check  # check.py")
        draft = self.root / "week-01/day-01/week-01-day-01.ipynb"
        draft.write_text(draft.read_text().replace("print('fine')", "print('my own edit')"))
        before = draft.read_text()
        out = self.check(expected=1)
        self.assertIn("week-01/day-01: cell", out)
        self.assertIn("stopped with an error: ZeroDivisionError", out)
        self.assertIn("reports a missing file", out)
        self.assertIn("does not print Not yet: before any work", out)
        self.assertEqual(draft.read_text(), before)
        self.assertNotIn("my own edit", out)


if __name__ == "__main__":
    unittest.main()
