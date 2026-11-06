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
import re
import shutil
import subprocess

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


def build(n):
    """The project as Step n starts, with the steps before it done right."""
    os.chdir(HOME)
    shutil.rmtree(PROJECT, ignore_errors=True)
    PROJECT.mkdir(parents=True)
    (PROJECT / "groceries.txt").write_text("milk 2.50\n")
    (PROJECT / "budget.txt").write_text("week 40.00\n")
    git("init", "-q", "-b", "main")
    git("add", "-A")
    git("commit", "-q", "-m", "Start the grocery project")
    (PROJECT / "groceries.txt").write_text("milk 2.80\n")
    git("add", "groceries.txt")
    (PROJECT / "budget.txt").write_text("week 40.00\nparty 15.00\n")
    if n >= 3:
        git("commit", "-q", "-m", "Milk now costs 2.80")


AGAIN = " Edit the TODO line, then run this cell again."
NOTES = {"TODO: add --staged after diff", "TODO: replace 0.00 with milk's new price", "TODO: change HEAD to HEAD^ HEAD"}
GIVEN = {1: "git diff", 2: 'git commit -m "Milk now costs 0.00"', 3: "git diff HEAD"}  # each TODO line's command
NEW_PRICE = r"^(?!.*(?<![\d.,])0[.,]00).*(?<![\d.,])2[.,]80?(?![.,]?\d)"  # 2.80 (or 2.8, 2,80) on its own, and no 0.00
SAYS = {  # Step n's diff: (right, only budget.txt, anything else)
    1: ("OK: --staged shows your next commit: groceries.txt.",
        "PROBLEM: git diff alone hides what you staged: it shows budget.txt, not groceries.txt.",
        "PROBLEM: this should show only your next commit, groceries.txt: use exactly git diff --staged."),
    3: ("OK: HEAD^ HEAD shows what your commit changed: groceries.txt.",
        "PROBLEM: git diff HEAD compares your files with your new commit, so it shows budget.txt.",
        "PROBLEM: this should show only what your commit changed, milk 2.50 to 2.80 in groceries.txt: use exactly HEAD^ HEAD."),
}


def check(n, cell):
    """(right or not, the line that says so) after Step n's commands."""
    shown = "".join(text for _, text in RUNS)
    files = re.findall(r"^diff --git a/(\S+)", shown, re.M)
    message = git("log", "-1", "--format=%s").strip()
    typed = [line.split("#")[0].strip().lstrip("!").strip() for line in cell.splitlines()]  # each command, without its note
    if len([command for command in typed if command and command[0] != "%"]) > (2 if n == 2 else 1):
        return False, ("PROBLEM: this cell has more command lines than it started with: put your edit on the TODO line "
                       "and delete the extra line, then run this cell again.")
    if any(code for code, _ in RUNS):  # Git's or the shell's own message is above: the TODO line has a slip
        where = "in Show the answer" if n == 2 else "shown above this cell"
        return False, (f"PROBLEM: a command stopped with an error: make the TODO line match the line {where}, "
                       "then run this cell again.")
    if n == 2 and "budget.txt" in git("diff", "--name-only", "HEAD~1", "HEAD").split():  # -a took the unstaged file too
        return False, "PROBLEM: budget.txt went into your commit: commit only what you staged, without -a." + AGAIN
    if n == 2 and re.search(NEW_PRICE, message):
        return True, "OK: milk went from 2.50 (the - line) to 2.80 (the + line)."
    if n != 2 and set(files) == {"groceries.txt"} and "+milk 2.80" in shown:
        return True, SAYS.get(n, SAYS[3])[0]
    if set(re.findall(r"# *(.*\S)", cell)) - NOTES and GIVEN.get(n) in typed:  # the command is as given; the note is not
        return False, "PROBLEM: you typed after #, in the note: undo it, then do what the note says." + AGAIN
    if n == 2 and any(re.search(r"\$\d", command) for command in typed):  # in "$2.80" the shell reads $2 as a name, empty
        return False, ("PROBLEM: in a command, $ and the digit after it are dropped. "
                       "Type the price without $ on the TODO line, then run this cell again.")
    if n == 2:
        old = ", not 0.00" if re.search(r"(?<![\d.])0\.00", message) else ""
        return False, f'PROBLEM: your message "{message}" needs milk\'s new price, from the + line{old}.' + AGAIN
    return False, SAYS.get(n, SAYS[3])[1 if set(files) == {"budget.txt"} else 2] + AGAIN


RESULTS = {}
REDO = {1: "use --staged. Redo Step 1.", 2: "commit only groceries.txt, with milk's new price in the message. Redo Step 2.",
        3: "use HEAD^ HEAD. Redo Step 3."}


def step(line):
    """%step N: start Step N from the same point each time; after the cell, print OK or PROBLEM."""
    n = int(line)
    build(n)
    RUNS.clear()

    def after(result):
        shell.events.unregister("post_run_cell", after)
        RESULTS[n], text = check(n, result.info.raw_cell)
        print(text)

    shell.events.register("post_run_cell", after)


def done(line):
    """%done: Done, or Not yet with the first step to redo, or with the steps not run since the first cell."""
    wrong = [n for n in REDO if not RESULTS.get(n)]
    unrun = [str(n) for n in wrong if n not in RESULTS]  # skipped, or the first code cell ran again
    if not wrong:
        print("Done: you read each diff view.")
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
