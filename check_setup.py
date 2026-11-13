"""Check the course setup: uv run check_setup.py, from the course folder.

It checks Python and the course's packages, Git with your name and email, and the Codex CLI with its
sign-in. Then it runs every cell of every day's notebook, as Run All does, in a temporary copy of the
course as committed. Stand-ins answer for the model, the coding agents and the editor (tools/stand-ins),
so nothing is sent to a model, no agent starts, and your own work is not touched. Continue when it
prints Setup OK.

uv run check_setup.py --check-model checks only the route to the model, with one short live request.
"""
import argparse
import importlib.metadata
import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time

KIT = pathlib.Path(__file__).resolve().parent
STAND_INS = KIT / "tools" / "stand-ins"
PACKAGES = ("flask", "pytest", "jsonschema", "ipykernel", "nbclient", "nbformat", "coverage", "pydeps", "lxml")
MISSING_FILE = re.compile(r"No such file or directory|can't open file|not a git repository", re.I)
CODEX_INSTALL = "curl -fsSL https://chatgpt.com/codex/install.sh | sh"


def git(*args, folder=KIT):
    return subprocess.run(["git", "-C", str(folder), *args], capture_output=True, text=True)


def check_python(missing, found):
    """Python 3.10 or later, the course's packages, and python3 on PATH from the same environment."""
    found.append(f"Python {sys.version.split()[0]}")
    print(f"Python: {sys.executable}")
    ready = sys.version_info >= (3, 10)
    if not ready:
        missing.append("Python 3.10 or later: run uv sync in the course folder, then uv run check_setup.py")
    for name in PACKAGES:
        try:
            found.append(f"{name} {importlib.metadata.version(name)}")
        except importlib.metadata.PackageNotFoundError:
            missing.append(f"{name}: run uv sync in the course folder, then uv run check_setup.py")
            ready = False
    # An exercise's terminal commands, and a notebook's !python3 lines, use the python3 on PATH.
    shell = shutil.which("python3")
    if not shell:
        missing.append("python3 on PATH: in each new terminal, run source .venv/bin/activate")
    else:
        probe = subprocess.run([shell, "-c", "import sys; print(sys.prefix)"], capture_output=True, text=True)
        if probe.returncode or pathlib.Path(probe.stdout.strip()).resolve() != pathlib.Path(sys.prefix).resolve():
            missing.append("python3 on PATH is another Python: in each new terminal, run source .venv/bin/activate")
    return ready


def check_git(missing, found):
    """Git 2.28 or later, and a name and email for your commits, here and in each exercise built so far."""
    try:
        version = re.search(r"(\d+)\.(\d+)", git("--version").stdout)
    except FileNotFoundError:
        version = None
    if not version:
        missing.append("Git: install Git 2.28 or later")
        return False
    if (int(version[1]), int(version[2])) < (2, 28):
        missing.append(f"Git 2.28 or later (this is {version[0]})")
        return False
    found.append(f"Git {version[0]}")
    unset = [key for key in ("user.name", "user.email") if not git("config", "--get", key).stdout.strip()]
    for key in unset:
        example = "Your Name" if key == "user.name" else "you@example.com"
        missing.append(f'Git {key}: run git config --global {key} "{example}", with your own')
    if not unset:
        for start in sorted(KIT.glob("week-*/day-*/*/start.py")):
            for name in ("lab", "extractor"):
                repo = start.parent / name
                if (repo / ".git").exists() and any(not git("config", "--get", key, folder=repo).stdout.strip()
                                                    for key in ("user.name", "user.email")):
                    missing.append(f"{repo.relative_to(KIT)} has no Git name or email: run the git config "
                                   "--global commands for user.name and user.email")
    return True


def check_codex(missing, found):
    """The Codex CLI answers, and is signed in. Nothing is sent to a model."""
    codex = shutil.which("codex")
    if not codex:
        missing.append(f"Codex CLI: install it with {CODEX_INSTALL}, open a new terminal, "
                       "then sign in with codex login")
        return
    try:
        version = subprocess.run([codex, "--version"], capture_output=True, text=True, timeout=60)
        status = subprocess.run([codex, "login", "status"], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as failure:
        missing.append(f"Codex CLI did not answer ({failure}): install it again with {CODEX_INSTALL}")
        return
    said = (version.stdout.strip() or version.stderr.strip()).splitlines()
    if version.returncode or not said:
        missing.append(f"Codex CLI did not give its version: install it again with {CODEX_INSTALL}")
        return
    if status.returncode:
        reason = (status.stderr.strip() or status.stdout.strip() or "no status").splitlines()[-1]
        missing.append(f"Codex CLI is not signed in ({reason}): run codex login, or in a hosted "
                       "workspace codex login --device-auth")
    else:
        found.append(f"{said[0]}, signed in")


def output_of(cell):
    """What a code cell printed, errors included."""
    parts = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            parts.append(out.get("text", ""))
        elif out.get("output_type") == "error":
            parts.append(f"{out.get('ename')}: {out.get('evalue')}\n")
        elif out.get("output_type") in ("execute_result", "display_data"):
            parts.append(str(out.get("data", {}).get("text/plain", "")) + "\n")
    # A shell's own start-up noise is not the cell's output.
    return "\n".join(line for line in "".join(parts).splitlines() if ".zshenv" not in line)


def check_notebooks(missing, found):
    """Run All of each day's notebook in a temporary copy of the course, with the stand-ins first on PATH."""
    if git("rev-parse", "HEAD").returncode:
        missing.append("the notebooks: run this check in a Git clone of the course")
        return
    with tempfile.TemporaryDirectory(prefix="course-check-") as tmp:
        tmp = pathlib.Path(tmp)
        course = tmp / "course"
        course.mkdir()
        archive = subprocess.run(["git", "-C", str(KIT), "archive", "--format=tar", "HEAD"],
                                 capture_output=True, check=True)
        with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
            if sys.version_info >= (3, 12):
                tar.extractall(course, filter="data")
            else:
                tar.extractall(course)
        # A clone of its own, with the start tag that reset.py restores from.
        for step in (["init", "-q", "-b", "main"], ["config", "user.name", "Course check"],
                     ["config", "user.email", "course-check@example.invalid"], ["add", "-A"],
                     ["commit", "-qm", "The course, for the check"], ["tag", "start"]):
            if git(*step, folder=course).returncode:
                missing.append(f"the notebooks: could not set up the temporary copy (git {step[0]})")
                return
        # The kernel is this environment's Python, started in the notebook's folder, as the editor's is.
        spec = tmp / "jupyter" / "kernels" / "course-check"
        spec.mkdir(parents=True)
        spec.joinpath("kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
            "display_name": "course check", "language": "python"}))
        env = dict(os.environ, JUPYTER_PATH=str(tmp / "jupyter"), CODEX_STUB_STATE=str(tmp / "stand-in"),
                   CLAUDE_STUB_STATE=str(tmp / "stand-in"),
                   PATH=os.pathsep.join([str(STAND_INS), str(pathlib.Path(sys.executable).parent),
                                         os.environ.get("PATH", "")]))
        for name in ("CODEX_STUB_REPLIES", "CLAUDE_STUB_REPLIES"):
            env.pop(name, None)
        # This process finds the kernel by JUPYTER_PATH too; it is set back when the run ends.
        before = os.environ.get("JUPYTER_PATH")
        os.environ["JUPYTER_PATH"] = env["JUPYTER_PATH"]
        try:
            run_notebooks(course, env, missing, found)
        finally:
            if before is None:
                os.environ.pop("JUPYTER_PATH", None)
            else:
                os.environ["JUPYTER_PATH"] = before


def run_notebooks(course, env, missing, found):
    """Each notebook from its first cell to its last; a problem names its day and its cell."""
    import nbclient
    import nbformat


    # A notebook whose metadata names the platform databricks runs only in Databricks (week 3): skipped here.
    notebooks = [p for p in sorted(course.glob("week-*/day-*/week-*-day-*.ipynb"))
                 + sorted(course.glob("week-*/day-*/exercise-*/exercise.ipynb"))
                 if any(c.cell_type == "code" for c in nbformat.read(p, as_version=4).cells)
                 and nbformat.read(p, as_version=4).metadata.get("platform") != "databricks"]
    if not notebooks:
        missing.append("the notebooks: none found; run this check in the course folder")
        return
    print(f"Running every cell of the {len(notebooks)} notebooks with code, in a temporary copy "
          "of the course. This takes a minute or two.", flush=True)
    cells = 0
    for path in notebooks:
        day = path.parent
        where = day.relative_to(course).as_posix()
        began = time.time()
        # An exercise notebook whose start.py builds lab/ runs after its reset, as a learner's does.
        if path.name == "exercise.ipynb" and (day / "start.py").is_file():
            subprocess.run([sys.executable, "reset.py", day.name], cwd=course, capture_output=True, env=env)
        nb = nbformat.read(path, as_version=4)
        client = nbclient.NotebookClient(nb, kernel_name="course-check", timeout=600, allow_errors=True,
                                         resources={"metadata": {"path": str(day)}})
        try:
            # The kernel's own log (a cell's output is not in it) would only alarm: it warns of TCP on loopback.
            client.execute(cwd=str(day), env=env, stderr=subprocess.DEVNULL)
        except Exception as failure:
            missing.append(f"{where}: the notebook did not run ({type(failure).__name__}: {failure})")
            continue
        problems = []
        for cell in (c for c in nb.cells if c.cell_type == "code"):
            cells += 1
            out = output_of(cell)
            last = " | ".join(out.strip().splitlines()[-3:])[:200]
            # In a command notebook's %step cell, git status before git init prints "not a git repository" on
            # purpose: the step teaches it, and prints OK or PROBLEM itself. Any other missing file still counts.
            seen = re.sub(r"(?m)^fatal: not a git repository.*$", "", out) if cell.source.startswith("%step") else out
            if any(o.get("output_type") == "error" for o in cell.get("outputs", [])):
                problems.append(f"cell {cell.get('id')} stopped with an error: {last}")
            elif MISSING_FILE.search(seen):
                problems.append(f"cell {cell.get('id')} reports a missing file: {last}")
            elif "check.py" in cell.source and "Not yet" not in out:
                problems.append(f"check cell {cell.get('id')} does not print Not yet: before any work: {last}")
        for start in sorted(day.glob("*/start.py")):
            if not any((start.parent / name / ".git").is_dir() for name in ("lab", "extractor")):
                problems.append(f"the first cell of {start.parent.name} did not build its workspace")
        missing.extend(f"{where}: {problem}" for problem in problems)
        print(f"{where}: {'OK' if not problems else f'{len(problems)} problems'} "
              f"({time.time() - began:.0f} s)", flush=True)
    found.append(f"all {cells} cells of the {len(notebooks)} notebooks ran")


def check_model():
    """One short live request through model.py, by the route model-route.json names."""
    try:
        from model import ask
        route = json.loads((KIT / "model-route.json").read_text())
        reply = ask("Reply with the single word ready.", "Are you there?")
    except Exception as failure:
        print(f"Missing:\n- model access: {failure}; check model-route.json, and on its codex route sign in "
              "with codex login")
        return 1
    print(f"Model OK: {route['model']} answered {reply.strip()[:20]!r}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check-model", action="store_true",
                        help="check only the route to the model, with one short live request")
    args = parser.parse_args()
    if args.check_model:
        return check_model()
    missing, found = [], []
    python_ready = check_python(missing, found)
    git_ready = check_git(missing, found)
    check_codex(missing, found)
    if python_ready and git_ready:
        check_notebooks(missing, found)
    else:
        missing.append("the notebooks were not run: fix the items above first")
    if missing:
        print("Missing:\n" + "\n".join(f"- {item}" for item in missing))
        print("Fix each item, then run uv run check_setup.py again.")
        return 1
    print("Setup OK: " + "; ".join(found))
    print("Open a day's notebook, select the .venv kernel, and run its first cell. Before the model "
          "exercises on Day 2, run uv run check_setup.py --check-model.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
