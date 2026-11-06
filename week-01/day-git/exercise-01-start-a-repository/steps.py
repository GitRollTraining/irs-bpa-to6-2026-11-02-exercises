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

HOME = pathlib.Path(__file__).resolve().parent  # the notebook's folder, which holds this file
PROJECT = HOME / "practice" / "meal-plan"
for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_COMMON_DIR",
             "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT"):
    os.environ.pop(name, None)  # set by a Git hook or a caller, these would point Git elsewhere or change its settings
# Git as on a new computer, the same on every run: your name is You, no editor opens, a new repository's
# first branch is main, as on GitHub, and Git never looks above practice/ for a repository.
os.environ.update(GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1", GIT_EDITOR="true",
                  GIT_AUTHOR_NAME="You", GIT_AUTHOR_EMAIL="you@example.com",
                  GIT_COMMITTER_NAME="You", GIT_COMMITTER_EMAIL="you@example.com",
                  GIT_AUTHOR_DATE="2026-11-02T09:00:00+00:00", GIT_COMMITTER_DATE="2026-11-02T09:00:00+00:00",
                  XDG_CONFIG_HOME=os.devnull, GIT_CEILING_DIRECTORIES=str(PROJECT.parent),
                  GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0="init.defaultBranch", GIT_CONFIG_VALUE_0="main")
RUNS = []  # (exit code, output) of this step's ! lines


def run_line(command):
    """Run one ! line as a script would, so Git prints plain text: no colours, no progress."""
    done = subprocess.run(command, shell=True, cwd=PROJECT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True, timeout=60)
    lines = done.stdout.splitlines(keepends=True)
    usage = [i for i, line in enumerate(lines) if line.startswith("usage: ")]
    if done.returncode and usage:  # a missing or mistyped part adds Git's whole usage text: stop at its first line
        lines = lines[:usage[0] + 1]
    elif done.returncode and len(lines) > 15:
        lines = lines[:1]
    print("".join(lines), end="")
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


COMMANDS = ("git", "echo", "cat")  # the commands step cells run


def git(*args):
    return subprocess.run(["git", *args], cwd=PROJECT, capture_output=True, text=True).stdout


def build(n):
    """The project as Step n starts, with the steps before it done right."""
    os.chdir(HOME)
    shutil.rmtree(PROJECT, ignore_errors=True)
    PROJECT.mkdir(parents=True)
    (PROJECT / "meals.txt").write_text("Monday: soup\nTuesday: pasta\n")
    (PROJECT / "groceries.txt").write_text("milk 2.50\nbread 3.00\n")
    if n >= 2:
        git("init", "-q")
    if n >= 3:
        git("add", "meals.txt", "groceries.txt")


FILES = ["groceries.txt", "meals.txt"]
AGAIN = " Make the TODO line match the line shown above this cell, then run this cell again."
ERROR = ("PROBLEM: a command stopped with an error: make the TODO line match the line shown above this cell, "
         "then run this cell again.")


def check(n):
    """(right or not, the line that says so) after Step n's commands."""
    failed = any(code for code, _ in RUNS)
    shown = "".join(text for _, text in RUNS)
    if n == 1:
        if not (PROJECT / ".git").is_dir() or git("rev-parse", "--is-inside-work-tree").strip() != "true":
            return False, "PROBLEM: meal-plan is not yet a Git repository, so git status cannot work in it." + AGAIN
        if failed:  # git init ran, but after a git status: the second line was changed, not the TODO line
            return False, ("PROBLEM: git status stopped with an error: change status to init on the TODO line, "
                           "the first ! line, keep !git status below it, then run this cell again.")
        if "Untracked files" not in shown:
            return False, "PROBLEM: git status did not run after git init: keep the line !git status below the TODO line." + AGAIN
        return True, "OK: meal-plan is a Git repository: git status lists your 2 files as untracked."
    if n == 2:
        if "did not match any files" in shown:  # a misspelt name: git add then stages no file at all
            return False, ("PROBLEM: git add found no file with one of the names you typed, so it staged no file. "
                           "Check both names against the line shown above this cell, then run this cell again.")
        if failed:
            return False, ERROR
        left = [name for name in FILES if name not in git("ls-files").split()]
        if len(left) == 2:
            return False, "PROBLEM: no file is staged: git status lists both under Untracked files." + AGAIN
        if left:
            return False, f"PROBLEM: {left[0]} is not staged: git status lists it under Untracked files." + AGAIN
        if "Changes to be committed" not in shown:
            return False, "PROBLEM: git status did not run: keep the line !git status below the TODO line." + AGAIN
        return True, "OK: both files are staged: git status lists them under Changes to be committed."
    if not git("rev-parse", "-q", "--verify", "HEAD").strip():  # no commit yet
        if "empty commit message" in shown:
            return False, ("PROBLEM: no commit was made: Git stops a commit with an empty message. "
                           "Type Start the meal plan between the quotes, then run this cell again.")
        return False, ERROR if failed else "PROBLEM: no commit was made." + AGAIN
    if failed:
        return False, ERROR
    if sorted(git("ls-tree", "--name-only", "HEAD").split()) != FILES:  # a file name after the message
        return False, "PROBLEM: your commit does not hold both files: type only the message between the quotes." + AGAIN
    return True, "OK: your first commit holds both files: git log shows its message, author and date."


RESULTS = {}
REDO = {1: "turn meal-plan into a Git repository with git init. Redo Step 1.",
        2: "stage both files with git add. Redo Step 2.",
        3: "commit them with a message. Redo Step 3."}
DONE = "Done: you made meal-plan a Git repository, staged both files, and committed them."


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
        print(DONE)
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
