"""Isolated setup regression tests: .venv/bin/python .github/test_setup.py.

Uses temporary repositories, synthetic identities and a fake model. The setup
orchestration test stubs package installation and kernel registration only.
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

ROOT = pathlib.Path(__file__).resolve().parents[1]
PYTHON = sys.executable
REAL_RUN = subprocess.run


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="course-setup-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name) / "checkout with spaces"
        self.root.mkdir()
        self.home = self.root.parent / "home"
        self.home.mkdir()
        self.global_config = self.home / ".gitconfig"
        self.global_config.write_text("# leave untouched\n")
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith(("GIT_", "PYTHON", "CLAUDE", "CODEX"))}
        self.env.update(HOME=str(self.home), USERPROFILE=str(self.home),
                        GIT_CONFIG_GLOBAL=str(self.global_config), GIT_CONFIG_NOSYSTEM="1",
                        PATH=str(pathlib.Path(PYTHON).parent) + os.pathsep + os.environ["PATH"],
                        PYTHONDONTWRITEBYTECODE="1")
        for name in ("check_setup.py", "setup.py"):
            shutil.copy(ROOT / name, self.root / name)
        (self.root / "lab-states").mkdir()
        shutil.copy(ROOT / "lab-states/build_lab.py", self.root / "lab-states/build_lab.py")
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
        # No test is allowed to open a network connection, including subprocesses.
        guard = self.root.parent / "guard"
        guard.mkdir()
        (guard / "sitecustomize.py").write_text('''import sys
def audit(event, args):
    if event in ("socket.connect", "socket.getaddrinfo", "socket.sendto"):
        raise RuntimeError("test network access forbidden")
sys.addaudithook(audit)
''')
        self.env["PYTHONPATH"] = str(guard)
        self.git("init", "-q", "-b", "main")

    def git(self, *args, folder=None):
        return REAL_RUN(["git", "-C", str(folder or self.root), *args],
                        env=self.env, check=True, capture_output=True, text=True).stdout.strip()

    def identity(self):
        self.git("config", "--local", "user.name", "Learner")
        self.git("config", "--local", "user.email", "learner@example.invalid")

    def check(self, *args, expected=0, env=None, cwd=None):
        result = REAL_RUN([PYTHON, str(self.root / "check_setup.py"), *args],
                          env=env or self.env, cwd=cwd or self.root.parent,
                          capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def exercise(self):
        folder = self.root / "week-01/day-01/example"
        folder.mkdir(parents=True)
        (folder / "start.py").touch()
        repo = folder / "lab"
        repo.mkdir()
        self.git("init", "-q", "-b", "main", folder=repo)
        (repo / "learner-draft.txt").write_text("preserve me\n")
        return repo

    def test_offline_from_arbitrary_directory_without_model_import(self):
        self.identity()
        self.assertIn("Setup OK (offline)", self.check())
        self.assertFalse((self.root / "model-imported").exists())
        self.assertEqual(self.global_config.read_text(), "# leave untouched\n")

    def test_missing_identity_actionable_and_read_only(self):
        out = self.check(expected=1)
        self.assertIn("git config --local user.name", out)
        self.assertIn("git config --local user.email", out)
        self.assertEqual(self.global_config.read_text(), "# leave untouched\n")
        self.assertFalse((self.root / "model-imported").exists())

    def test_existing_global_identity_is_accepted(self):
        self.global_config.write_text("[user]\n name = Existing Learner\n email = existing@example.invalid\n")
        before = self.global_config.read_bytes()
        self.assertIn("Setup OK (offline)", self.check())
        self.assertEqual(self.global_config.read_bytes(), before)

    def test_explicit_model_probe_success_and_failure(self):
        self.identity()
        self.assertIn("including live model probe", self.check("--check-model"))
        self.assertTrue((self.root / "model-called").exists())
        env = dict(self.env, FAKE_MODEL_FAIL="1")
        self.assertIn("synthetic provider unavailable", self.check("--check-model", expected=1, env=env))

    def test_missing_packages_and_git_are_actionable(self):
        self.identity()
        loaded = module(self.root / "check_setup.py", "readiness_packages")
        with mock.patch.dict(os.environ, self.env, clear=True), \
             mock.patch.object(sys, "argv", ["check_setup.py"]), \
             mock.patch.object(loaded.importlib.metadata, "version",
                               side_effect=importlib.metadata.PackageNotFoundError), \
             mock.patch("builtins.print") as output:
            self.assertEqual(loaded.main(), 1)
        printed = "\n".join(str(call.args[0]) for call in output.call_args_list)
        for name in ("pytest", "jsonschema", "ipykernel"):
            self.assertIn(name + ": run setup.py", printed)
        with mock.patch.dict(os.environ, self.env, clear=True), \
             mock.patch.object(sys, "argv", ["check_setup.py"]), \
             mock.patch.object(loaded, "git", side_effect=FileNotFoundError), \
             mock.patch("builtins.print") as output:
            self.assertEqual(loaded.main(), 1)
        self.assertTrue(any("install Git 2.28" in str(call) for call in output.call_args_list))

    @unittest.skipIf(os.name == "nt", "Unix notebook shell interpreter check")
    def test_shell_environment_mismatch(self):
        self.identity()
        shell = self.root.parent / "shell"
        shell.mkdir()
        fake = shell / "python3"
        fake.write_text("#!/bin/sh\necho /different/python/environment\n")
        fake.chmod(0o755)
        env = dict(self.env, PATH=str(shell) + os.pathsep + self.env["PATH"])
        self.assertIn("different environment", self.check(expected=1, env=env))

    def test_nested_identity_propagation_preserves_work_and_overrides(self):
        self.identity()
        repo = self.exercise()
        self.assertIn("example/lab needs user.name", self.check(expected=1))
        loaded = module(self.root / "lab-states/build_lab.py", "lab_identity")
        with mock.patch.dict(os.environ, self.env, clear=True):
            loaded.configure_identity(repo)
        self.git("add", ".", folder=repo)
        self.git("commit", "-qm", "Learner commit", folder=repo)
        self.assertEqual(self.git("show", "-s", "--format=%an <%ae>", folder=repo),
                         "Learner <learner@example.invalid>")
        self.git("config", "--local", "user.name", "Explicit Override", folder=repo)
        with mock.patch.dict(os.environ, self.env, clear=True):
            loaded.configure_identity(repo)
        self.assertEqual(self.git("config", "--get", "user.name", folder=repo), "Explicit Override")
        self.assertEqual((repo / "learner-draft.txt").read_text(), "preserve me\n")
        self.assertIn("Setup OK (offline)", self.check(cwd=repo))
        self.assertEqual(self.global_config.read_text(), "# leave untouched\n")

    def test_missing_venv_support_has_repair_guidance(self):
        loaded = module(self.root / "setup.py", "setup_venv_failure")
        def run(args, **kwargs):
            args = [str(a) for a in args]
            if args[1:3] == ["-m", "venv"]:
                raise subprocess.CalledProcessError(1, args)
            return REAL_RUN(args, **kwargs)
        with mock.patch.dict(os.environ, self.env, clear=True), \
             mock.patch.object(sys, "argv", ["setup.py"]), \
             mock.patch.object(subprocess, "run", side_effect=run), \
             self.assertRaisesRegex(SystemExit, "python3-venv"):
            loaded.main()

    def test_setup_repeatable_local_identity_and_offline_final_check(self):
        repo = self.exercise()
        loaded = module(self.root / "setup.py", "course_setup")
        # Reuse the test interpreter; do not install packages or register a user kernel.
        loaded.PYTHON = pathlib.Path(PYTHON)
        loaded.BIN = pathlib.Path(PYTHON).parent
        loaded.VENV = pathlib.Path(sys.prefix)
        installs = []

        def run(args, **kwargs):
            args = [str(a) for a in args]
            if args[1:3] in (["-m", "pip"], ["-m", "ipykernel"]):
                installs.append(args)
                return subprocess.CompletedProcess(args, 0)
            return REAL_RUN(args, **kwargs)

        with mock.patch.dict(os.environ, self.env, clear=True), \
             mock.patch.object(sys, "argv", ["setup.py"]), \
             mock.patch.object(subprocess, "run", side_effect=run), \
             mock.patch("builtins.input", side_effect=["Learner", "learner@example.invalid"]):
            self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                     "commit", "--allow-empty", "-qm", "Fixture")
            self.assertEqual(loaded.main(), 0)
            baseline = self.git("rev-parse", "start")
            self.assertEqual(loaded.main(), 0)
            self.assertEqual(self.git("rev-parse", "start"), baseline)
        self.assertEqual(len(installs), 4)
        kernel = next(args for args in installs if args[2] == "ipykernel")
        self.assertIn(str(loaded.BIN) + os.pathsep + self.env["PATH"], kernel)
        self.assertEqual(self.git("config", "--local", "user.name"), "Learner")
        self.assertEqual(self.git("config", "--local", "user.email", folder=repo), "learner@example.invalid")
        self.assertEqual((repo / "learner-draft.txt").read_text(), "preserve me\n")
        self.assertEqual(self.global_config.read_text(), "# leave untouched\n")
        self.assertFalse((self.root / "model-imported").exists())


if __name__ == "__main__":
    unittest.main()
