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


FILES = {"groceries.txt": "milk 2.50\neggs 3.20\nbread\nrice two\n",
         "total.py": """import sys


def total(lines):
    return sum(float(line.split()[1]) for line in lines)


if __name__ == "__main__":
    sys.tracebacklimit = 0  # an error prints one line, not the code around it
    print(f"Total: {total(open(sys.argv[1]).read().splitlines()):.2f}")
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
         "pytest.ini": "[pytest]\naddopts = --tb=no\n"}
BRANCHES = {"run-a": 'in lines if " " in line)', "run-b": "in lines if line[-1].isdigit())"}


def build(n):
    """The project as Step n starts, with the steps before it done right."""
    os.chdir(HOME)
    shutil.rmtree(PROJECT, ignore_errors=True)
    PROJECT.mkdir(parents=True)
    for name, text in FILES.items():
        (PROJECT / name).write_text(text)
    git("init", "-q", "-b", "main")
    git("add", "-A")
    git("commit", "-q", "-m", "Start the grocery project")
    for branch, change in BRANCHES.items():
        git("switch", "-qc", branch, "main")
        (PROJECT / "total.py").write_text(FILES["total.py"].replace("in lines)", change))
        git("commit", "-qam", branch)
    git("switch", "-q", "run-b" if n > 1 else "main")


AGAIN = " Edit the TODO line, then run this cell again."


def check(n):
    """(right or not, the line that says so) after Step n's commands."""
    shown = "".join(text for _, text in RUNS)
    if n == 1:  # no TODO line: anything but run B's total means the cell's lines were changed
        if "Total: 5.70" in shown:
            return False, ('PROBLEM: run B skipped "rice two" with no error, against your constraints. '
                           "Step 2 finds this; Step 3 checks run A.")
        return False, ("PROBLEM: this cell has no TODO line; its lines must read !git switch run-b, "
                       "!cat groceries.txt and !python3 total.py groceries.txt. Then run this cell again.")
    if n == 2:
        if "1 failed, 2 passed" in shown:
            return True, 'OK: your whole done-when ran; DID NOT RAISE means run B did not stop at "rice two".'
        if "deselected" in shown:
            return False, "PROBLEM: -k ran only some of your 3 tests, not your whole done-when." + AGAIN
        return False, "PROBLEM: pytest did not run your tests: the line must read !python3 -m pytest -q." + AGAIN
    if "3 passed" in shown:
        return True, "OK: run A passes your done-when: anyone can check it."
    if "Already on 'run-b'" in shown:
        return False, "PROBLEM: run B does not pass your done-when; switch to run-a." + AGAIN
    return False, ("PROBLEM: your done-when did not run on run A: the lines must read !git switch run-a "
                   "and !python3 -m pytest -q. Then run this cell again.")


RESULTS = {}
REDO = {2: "run the whole done-when. Redo Step 2.", 3: "check run A. Redo Step 3."}


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
        print("Done: your done-when rejects run B; run A passes it.")
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
