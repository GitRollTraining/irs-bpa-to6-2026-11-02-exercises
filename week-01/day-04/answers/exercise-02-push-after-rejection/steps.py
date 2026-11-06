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
PROJECT = HOME / "practice" / "groceries"
SHARED = PROJECT.with_name("shared")  # origin, the shared copy
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


def git(*args, cwd=PROJECT, **env):
    return subprocess.run(["git", *args], cwd=cwd, env={**os.environ, **env}, capture_output=True, text=True).stdout


def build(n):
    """The project as Step n starts, with the steps before it done right."""
    os.chdir(HOME)
    shutil.rmtree(PROJECT, ignore_errors=True)
    shutil.rmtree(SHARED, ignore_errors=True)
    PROJECT.mkdir(parents=True)
    (PROJECT / "groceries.txt").write_text("milk 2.50\nbread 3.00\n")
    (PROJECT / "meals.txt").write_text("Monday: soup\n")
    git("init", "-q", "-b", "main")
    git("add", "-A")
    git("commit", "-q", "-m", "Start the grocery project")
    git("config", "advice.pushUpdateRejected", "false")  # no hint
    git("config", "pull.rebase", "false")  # pull merges, as Slide 16 says
    git("init", "-q", "--bare", "-b", "main", SHARED)
    git("remote", "add", "origin", "../shared")
    git("config", "remote.origin.followRemoteHEAD", "never")  # origin alone names no branch, on every Git
    git("push", "-q", "-u", "origin", "main")
    # Your housemate pushes first.
    theirs = PROJECT.with_name("housemate")
    git("clone", "-q", SHARED, theirs)
    (theirs / "meals.txt").write_text("Monday: soup\nWednesday: pasta\n")
    git("commit", "-q", "-am", DINNER, cwd=theirs, GIT_AUTHOR_NAME="Housemate", GIT_AUTHOR_EMAIL="housemate@example.com",
        GIT_COMMITTER_NAME="Housemate", GIT_COMMITTER_EMAIL="housemate@example.com", GIT_AUTHOR_DATE="2026-11-02T08:30:00+00:00")
    git("push", "-q", cwd=theirs)
    shutil.rmtree(theirs)
    (PROJECT / "groceries.txt").write_text("milk 2.50\nbread 3.00\neggs 3.20\n")
    git("commit", "-q", "-am", "Add eggs")
    if n >= 2:
        git("fetch", "-q")


DINNER = "Add a Wednesday dinner"
AGAIN = " Make the TODO line match the line shown above this cell, then run this cell again."


def check(n):
    """(right or not, the line that says so) after Step n's commands."""
    shown, shared = "".join(text for _, text in RUNS), git("log", "--format=%s", "main", cwd=SHARED)
    if n > 1 and ("'origin'" in shown or "merge: origin - not" in shown):  # origin alone names no branch
        return False, "PROBLEM: write origin/main as one name, with a slash." + AGAIN
    if any(code and "[rejected]" not in text for code, text in RUNS):  # Git's or the shell's own message is above: the TODO line has a slip
        return False, ("PROBLEM: a command stopped with an error: make the TODO line match the line shown "
                       "above this cell, then run this cell again.")
    if "[rejected]" in shown and n == 3:  # the merge took nothing from origin/main, or did not run
        return False, "PROBLEM: Git rejected your push: your merge did not add their commit." + AGAIN
    if "[rejected]" in shown:
        return False, "PROBLEM: Git rejected your push: origin holds a commit your work does not have." + AGAIN
    if "(forced update)" in shown:  # git push --force: Git did as told, and dropped their commit from origin
        return False, "PROBLEM: the forced push replaced their commit on origin with yours." + AGAIN
    if n == 1 and git("rev-list", "main..origin/main"):
        return True, "OK: fetch only downloads: their commit waits in origin/main; your work is unchanged."
    if n == 1 and git("rev-list", "--count", "main").strip() != "2":  # git pull merged their commit into main
        return False, "PROBLEM: pull also merged their commit into your work; fetch only downloads." + AGAIN
    if n == 2 and "Author: Housemate" in shown:
        if "Author: You" in shown:  # git show origin/main main: their commit, then yours
            return False, "PROBLEM: this also shows your own commit; show only origin/main, one name with a slash." + AGAIN
        return True, "OK: their commit changes only meals.txt; yours changes groceries.txt: both can be kept."
    if n == 3 and DINNER in shared and "Add eggs" in shared:
        return True, "OK: your push was sent: origin holds your commit and theirs."
    if n == 3 and "To ../shared" not in shown:  # the !git push line was changed or deleted
        return False, "PROBLEM: no push ran: the cell must end with !git push. Put it back, then run this cell again."
    if n == 2 and "Author: You" not in shown:  # a file, or nothing, was shown
        return False, "PROBLEM: their commit was not shown; it is in origin/main." + AGAIN
    return False, {1: "PROBLEM: their commit was not downloaded: use fetch.",
                   2: "PROBLEM: this is your own commit; their commit is in origin/main.",
                   3: "PROBLEM: origin does not hold both commits yet."}[n] + AGAIN


RESULTS = {}
REDO = {1: "fetch your housemate's commit. Redo Step 1.",
        2: "show origin/main. Redo Step 2.",
        3: "merge origin/main, then push. Redo Step 3."}


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
        print("Done: you read their commit, merged it and pushed both.")
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
