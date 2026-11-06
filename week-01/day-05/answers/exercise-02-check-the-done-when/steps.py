"""The practice project for this exercise, and its %step and %done commands.

The notebook's first cell runs this file: %run steps.py. You do not need to read it.
%step N builds the project as Step N starts, runs the cell's ! lines inside the project (never in the
course folder), then prints OK or PROBLEM. %done prints Done, or the first step to redo.
"""
import builtins

# IPython, which runs the notebook, adds get_ipython to Python's builtins; plain Python does not.
get_ipython = getattr(builtins, "get_ipython", None)
if get_ipython is None:
    raise SystemExit("Run this file from the notebook's first cell: %run steps.py")

import os
import pathlib
import shutil
import subprocess
import sys

HOME = pathlib.Path(__file__).resolve().parent  # the notebook's folder, which holds this file
PROJECT = HOME / "practice" / "groceries"
# Git as on a new computer, the same on every run: your name is You, and no editor opens.
os.environ.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_EDITOR="true",
                  GIT_AUTHOR_NAME="You", GIT_AUTHOR_EMAIL="you@example.com",
                  GIT_COMMITTER_NAME="You", GIT_COMMITTER_EMAIL="you@example.com",
                  GIT_AUTHOR_DATE="2026-11-02T09:00:00+00:00", GIT_COMMITTER_DATE="2026-11-02T09:00:00+00:00",
                  XDG_CONFIG_HOME=os.devnull, GIT_CEILING_DIRECTORIES=str(PROJECT.parent))
for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_COMMON_DIR",
             "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT"):
    os.environ.pop(name, None)  # set by a Git hook or a caller, these would point Git elsewhere or change its settings
# python3 with pytest; plain output.
os.environ.update(PATH=os.path.dirname(sys.executable) + os.pathsep + os.environ["PATH"], NO_COLOR="1")
RUNS = []  # (exit code, output) of this step's ! lines


def run_line(command):
    """Run one ! line as a script would, so Git prints plain text: no colours, no progress."""
    done = subprocess.run(command, shell=True, cwd=PROJECT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, timeout=60)
    lines = done.stdout.splitlines(keepends=True)
    # A mistyped option adds Git's whole usage text: show only the error.
    print("".join(lines[:1] if done.returncode and len(lines) > 15 else lines), end="")
    RUNS.append((done.returncode, done.stdout))


def as_command(lines):
    """In a step cell, each line runs as a command, even with its ! left out, doubled or after a space."""
    nothing_ran = ['print("PROBLEM: nothing ran. Commands run only below a %step line: %step 1 in Step 1, '
                   '%step 2 in Step 2, %step 3 in Step 3. If you deleted or changed that line, put it back, '
                   'then run this cell again.")\n']
    if not any(line.lstrip().startswith(("!", "%step")) for line in lines):
        return lines  # not a step cell: the first cell, the check cell, or a cell of notes
    first = next(i for i, line in enumerate(lines) if line.strip() and not line.lstrip().startswith("#"))
    if not lines[first].lstrip().startswith("%step"):  # no %step line, or a line above it that would run first
        return nothing_ran
    number = lines[first].strip()[len("%step"):].lstrip()
    digits = number[:len(number) - len(number.lstrip("0123456789"))]
    joined = number[len(digits):].strip()  # a command joined onto the %step line, by one Backspace too many
    if digits not in ("1", "2", "3") or joined[:1] not in ("", "!", "#") and joined.split()[0] not in COMMANDS:
        return nothing_ran  # the number is gone or names no step, or other text was typed onto the line
    lines = [f"%step {digits}\n"] + ([joined + "\n"] if joined else []) + lines[first + 1:]
    return [line if line.strip()[:1] in ("", "%", "#") else "!" + line.lstrip().lstrip("!") for line in lines]


COMMANDS = ("git", "echo", "cat", "python3")  # the commands step cells run


def git(*args):
    return subprocess.run(["git", *args], cwd=PROJECT, capture_output=True, text=True).stdout


FILES = {"groceries.txt": "milk 2.50\neggs 3.20\nbread\n",
         "total.py": """def total(lines):
    return sum(float(line.split()[1]) for line in lines)
""",
         "test_total.py": """import pytest
from total import total


def test_adds_prices():
    assert total(["milk 2.50", "eggs 3.20"]) == 5.70


def test_bad_price_stops():
    with pytest.raises(ValueError):
        total(["rice two"])


def test_no_price_adds_zero():
    assert total(["milk 2.50", "eggs 3.20", "bread"]) == 5.70
""",
         "pytest.ini": "[pytest]\n", ".gitignore": "__pycache__/\n.pytest_cache/\n",
         ".gitattributes": "*.py diff=plain\n"}


def build(n):
    """The project as Step n starts; Steps 1 and 2 only read."""
    os.chdir(HOME)
    shutil.rmtree(PROJECT, ignore_errors=True)
    PROJECT.mkdir(parents=True)
    for name, text in FILES.items():
        (PROJECT / name).write_text(text)
    git("init", "-q", "-b", "main")
    git("config", "diff.plain.xfuncname", "x^")  # nothing after @@
    git("add", "-A")
    git("commit", "-q", "-m", "Start the grocery project")
    # The agent's made-up run: bread costs 1.00, and a test changed to match.
    (PROJECT / "total.py").write_text(FILES["total.py"].replace("line.split()", '(line.split() + ["1.00"])'))
    (PROJECT / "test_total.py").write_text(FILES["test_total.py"].replace('"bread"]) == 5.70', '"bread"]) == 6.70'))


LINE = {2: "!git diff test_total.py", 3: "!git restore total.py test_total.py"}  # each edit step's right line
AGAIN = " Make the TODO line read {}, then run this cell again."


def check(n):
    """(right or not, the line that says so) after Step n's commands."""
    failed, shown = any(code for code, _ in RUNS), "".join(text for _, text in RUNS)
    if n == 1:
        return False, ("PROBLEM: 3 tests pass, but the agent changed test_total.py, not only total.py. "
                       "Steps 2 and 3 fix this." if "3 passed" in shown else
                       "PROBLEM: pytest did not run your tests: read the message above.")
    again = AGAIN.format(LINE[n])
    if n == 3 and len(RUNS) > 2:  # a line was added: the cell started with two commands
        return False, ("PROBLEM: this cell has more command lines than it started with: put your edit on the "
                       "TODO line and delete the extra line, then run this cell again.")
    if failed:  # Git's or the shell's own message is above: the TODO line has a slip
        return False, "PROBLEM: a command stopped with an error." + again
    if n == 2:
        if "diff --git a/total.py" in shown:
            return False, "PROBLEM: that shows total.py, the code." + again
        if "diff --git a/test_total.py" in shown and "6.70" in shown:
            return True, ("OK: you found the cheat: test_no_price_adds_zero now expects 6.70, not 5.70, "
                          "because the agent's code counts bread as 1.00.")
        return False, "PROBLEM: this does not show test_total.py's changed lines." + again
    # Each file against how it began: a commit keeps the agent's change, so it does not count.
    left = [name for name in ("test_total.py", "total.py")
            if not (PROJECT / name).is_file() or (PROJECT / name).read_text() != FILES[name]]
    if left:
        return False, f"PROBLEM: the agent's change is still in {' and '.join(left)}." + again
    return True, "OK: both files are back as they were, so you can ask the agent again."


RESULTS = {}
REDO = {2: "read test_total.py's diff. Redo Step 2.",
        3: "restore both files the agent changed. Redo Step 3."}


def step(line):
    """%step N: start Step N from the same point each time; after the cell, print OK or PROBLEM."""
    n = int(line)
    build(n)
    RUNS.clear()

    def after(result):
        shell.events.unregister("post_run_cell", after)
        RESULTS[n], text = check(n)
        print(text)

    shell.events.register("post_run_cell", after)


def done(line):
    """%done: Done, or Not yet with the first step to redo, or with the steps not run since the first cell."""
    wrong = [n for n in REDO if not RESULTS.get(n)]
    unrun = [str(n) for n in wrong if n not in RESULTS]  # skipped, or the first code cell ran again
    if not wrong:
        print("Done: you read the test file's diff and restored both files.")
    elif wrong[0] in RESULTS:
        print("Not yet: " + REDO[wrong[0]])
    elif len(unrun) == 1:
        print(f"Not yet: run Step {unrun[0]}; it has not run since you last ran the first code cell.")
    else:
        print(f"Not yet: run Steps {', '.join(unrun[:-1])} and {unrun[-1]}; they have not run since you last ran the first code cell.")


shell = get_ipython()
shell.system = run_line
shell.register_magic_function(step, "line", "step")
shell.register_magic_function(done, "line", "done")
cleanup = shell.input_transformers_cleanup  # what IPython does to each cell's text before it runs it
cleanup[:] = [t for t in cleanup if getattr(t, "__name__", "") != "as_command"] + [as_command]
build(1)
