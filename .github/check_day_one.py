#!/usr/bin/env python3
"""Offline Day 1 regression check: .venv/bin/python .github/check_day_one.py.

Requires Git, sh, pytest and jsonschema. Copies only tracked course inputs (using
their current working-tree contents) into a disposable repository, never learner
workspaces. Does not run setup.py, notebooks, editors, agents or live models.
"""
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
DAY = pathlib.Path("week-01/day-01")
EXERCISES = {
    "find-note-leaks": ("extractor", (
        "extract tried to reach", "logs/extractor.log holds", "is not one of the course's simulated notes",
    )),
    "data-rules-check": ("lab", (
        "use 1:", "use 2:", "use 3:", "use 4:", "commit docs/data-rules-check.md",
    )),
    "agent-boundary": ("lab", (
        'Claude Code: .mcp.json still gives', 'Edit(/**)', 'Bash(git push *)',
        'web search tool', '[mcp_servers.case-files]', 'sandbox_mode = "workspace-write"',
        'web_search = "live"', 'does not yet name who must agree',
    )),
}

# Loaded by every child Python, including pytest subprocesses inside check.py.
# A live model invocation is an error even if exercise code catches the exception.
# Socket guards also prevent the deliberately unsafe starting extractor from
# reaching any service. These are regression guards, not a hostile-code sandbox.
GUARD = '''import os
import pathlib
import sys

def profile(frame, event, arg):
    if (event == "call" and frame.f_code.co_name == "ask"
            and pathlib.Path(frame.f_code.co_filename).name == "model.py"):
        pathlib.Path(os.environ["COURSE_MODEL_ATTEMPT"]).write_text("model.ask invoked")
        raise RuntimeError("Live model calls are forbidden in the Day 1 check")

def audit(event, args):
    if event in ("socket.connect", "socket.getaddrinfo", "socket.sendto"):
        raise OSError("Network disabled by the Day 1 check")

sys.setprofile(profile)
sys.addaudithook(audit)
'''


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(args, cwd, env, expected=0, contains=()):
    result = subprocess.run([str(a) for a in args], cwd=cwd, env=env,
                            capture_output=True, text=True, timeout=120)
    output = result.stdout + result.stderr
    require(result.returncode == expected and all(s in output for s in contains),
            f"Command failed validation: {args}\n"
            f"Expected exit {expected}, got {result.returncode}\n{output}")
    require(not pathlib.Path(env["COURSE_MODEL_ATTEMPT"]).exists(),
            f"Live model invocation detected: {args}")
    return output


def fingerprint(folder):
    """Include ignored files and nested Git history when checking preservation."""
    return {p.relative_to(folder).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in folder.rglob("*") if p.is_file()}


def main():
    # Fail before creating fixtures if this interpreter cannot run the checks.
    import pytest  # noqa: F401
    import jsonschema  # noqa: F401

    require(shutil.which("git") and shutil.which("sh"), "Git and sh are required")
    tracked = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-z", "--", str(DAY),
         "notes", "lab-states", "reset.py", "model.py", "model-route.json", ".gitignore"],
        capture_output=True, text=True, check=True,
    ).stdout.split("\0")
    sources = [ROOT / name for name in tracked if name]
    require(sources, "No tracked course inputs found")
    original = {p: p.read_bytes() for p in sources}

    with tempfile.TemporaryDirectory(prefix="course-day-one-") as tmp:
        base = pathlib.Path(tmp)
        course = base / "checkout with spaces"
        home = base / "home"
        guard = base / "guard"
        for folder in (course, home, guard):
            folder.mkdir()
        for source, content in original.items():
            dest = course / source.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
        (guard / "sitecustomize.py").write_text(GUARD)
        # Keep user Git configuration, hooks and identities out of test commits.
        (home / ".gitconfig").write_text("# must remain unchanged\n")
        (home / "learner-notes.txt").write_text("keep home data\n")
        home_before = fingerprint(home)
        env = {key: value for key, value in os.environ.items()
               if not key.startswith(("GIT_", "PYTHON", "CLAUDE", "CODEX"))}
        env.update({
            "HOME": str(home), "USERPROFILE": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "GIT_CONFIG_GLOBAL": str(home / ".gitconfig"), "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_AUTHOR_NAME": "Course check", "GIT_AUTHOR_EMAIL": "check@example.invalid",
            "GIT_COMMITTER_NAME": "Course check", "GIT_COMMITTER_EMAIL": "check@example.invalid",
            "GIT_TERMINAL_PROMPT": "0", "PYTHONPATH": str(guard),
            "PYTHONDONTWRITEBYTECODE": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PATH": str(pathlib.Path(sys.executable).parent) + os.pathsep + os.environ["PATH"],
            "EXTRACTOR_FALLBACK_URL": "http://127.0.0.1:9/", "NO_PROXY": "*",
            "COURSE_MODEL_ATTEMPT": str(base / "model-attempt"),
        })
        run([sys.executable, "-c", "import sitecustomize"], course, env)
        # Verify guards really load in the interpreter used by answer scripts.
        run(["python3", "-c",
             "import sys; assert sys.getprofile() is not None; import pytest, jsonschema"], course, env)
        run(["git", "init", "-q", "-b", "main"], course, env)
        run(["git", "add", "."], course, env)
        run(["git", "commit", "-qm", "Course check snapshot"], course, env)
        run(["git", "tag", "start"], course, env)

        # Deliberate learner data outside reset targets must survive every reset.
        notebook = course / DAY / "week-01-day-01.ipynb"
        notebook.write_bytes(notebook.read_bytes() + b"\n ")
        notebook_before = notebook.read_bytes()
        (course / "learner-notes.txt").write_text("untracked work outside exercises\n")
        preserved = {}
        for name, (workspace, findings) in EXERCISES.items():
            exercise = course / DAY / name
            repo = exercise / workspace
            run([sys.executable, course / "reset.py", name], course, env,
                contains=(f"{name} is back as it was supplied.",))
            if name == "find-note-leaks":
                run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"], repo, env,
                    contains=("6 passed",))
                print(f"{name}: initial tests: 6 passed", flush=True)
            run([sys.executable, "../check.py"], repo, env, expected=1,
                contains=(f"Not yet: {len(findings)} left.", *findings))
            print(f"{name}: initial check: {len(findings)} expected findings", flush=True)
            run(["sh", f"../../answers/{name}/commands.sh"], repo, env, contains=("Done:",))
            print(f"{name}: supplied answer: Done", flush=True)
            (repo / "learner-draft.txt").write_text("discard only on explicit reset\n")
            run([sys.executable, course / "reset.py", name], repo, env)
            require(not (repo / "learner-draft.txt").exists(), f"{name}: reset left learner draft")
            run([sys.executable, "../check.py"], repo, env, expected=1,
                contains=(f"Not yet: {len(findings)} left.", *findings))
            run(["sh", f"../../answers/{name}/commands.sh"], repo, env, contains=("Done:",))
            for other, before in preserved.items():
                require(fingerprint(other) == before, f"Reset changed unrelated exercise: {other.name}")
            # Preserve a completed exercise plus uncommitted learner work while
            # later exercises initialize/reset their own repositories.
            (repo / "learner-draft.txt").write_text("keep during other exercise resets\n")
            preserved[exercise] = fingerprint(exercise)
            require(notebook.read_bytes() == notebook_before, "Reset changed learner notebook")
            require((course / "learner-notes.txt").read_text() == "untracked work outside exercises\n",
                    "Reset changed unrelated learner file")
            require(fingerprint(home) == home_before, "Home configuration/data changed")
            print(f"{name}: reset, repeated answer and isolation: OK", flush=True)

    require(all(p.read_bytes() == content for p, content in original.items()),
            "Source course files changed during validation")
    print("OK: all 3 Day 1 exercises; offline answers and rebuilds pass; learner work preserved")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.SubprocessError) as failure:
        sys.exit(f"Day 1 check failed: {failure}")
