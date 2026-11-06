"""The practice folder for this exercise, and its %step and %done commands.

The notebook's first cell runs this file: %run steps.py. You do not need to read it.
%step N runs the cell's ! lines in practice/ (Step 1), in the repository you cloned there (Steps 2 to 4), or in
the meal plan from Exercise 2 (Step 5), never in the course folder, then prints OK or PROBLEM. %done prints Done,
or the first step to redo.
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
PRACTICE = HOME / "practice"  # Step 1 clones your repository in here
MEAL_PLAN = HOME.parent / "exercise-02-try-an-idea-on-a-branch" / "practice" / "meal-plan"  # made in Exercise 2
for name in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_COMMON_DIR",
             "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT"):
    os.environ.pop(name, None)  # set by a Git hook or a caller, these would point Git elsewhere or change its settings
# Your own Git: your name, your email and the GitHub sign-in you set up in a terminal. Git never opens an editor,
# never waits for typing (a notebook cannot answer it), and never looks above these practice folders for a repository.
os.environ.update(GIT_EDITOR="true", GIT_TERMINAL_PROMPT="0",
                  GIT_CEILING_DIRECTORIES=os.pathsep.join([str(PRACTICE), str(MEAL_PLAN.parent)]))
RUNS = []  # (exit code, output) of this step's ! lines
WHERE = [PRACTICE]  # the folder this step's ! lines run in; None while it does not exist


def run_line(command):
    """Run one ! line as a script would, so Git prints plain text: no colours, no progress."""
    if WHERE[0] is None:  # no folder to run in yet: the step's check says what to do first
        RUNS.append((1, ""))
        return
    try:
        done = subprocess.run(command, shell=True, cwd=WHERE[0], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print("The command took over 5 minutes, so it was stopped.")
        RUNS.append((1, ""))
        return
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
                   '%step 2 in Step 2, and so on. If you deleted or changed that line, put it back, '
                   'then run this cell again.")\n']
    if not any(line.lstrip().startswith(("!", "%step")) for line in lines):
        return lines  # not a step cell: the first cell, the check cell, or a cell of notes
    first = next(i for i, line in enumerate(lines) if line.strip() and not line.lstrip().startswith("#"))
    if not lines[first].lstrip().startswith("%step"):  # no %step line, or a line above it that would run first
        return nothing_ran
    number = lines[first].strip()[len("%step"):].lstrip()
    digits = number[:len(number) - len(number.lstrip("0123456789"))]
    joined = number[len(digits):].strip()  # a command joined onto the %step line, by one Backspace too many
    if digits not in ("1", "2", "3", "4", "5") or joined[:1] not in ("", "!", "#") and joined.split()[0] not in COMMANDS:
        return nothing_ran  # the number is gone or names no step, or other text was typed onto the line
    lines = [f"%step {digits}\n"] + ([joined + "\n"] if joined else []) + lines[first + 1:]
    return [line if line.strip()[:1] in ("", "%", "#") else "!" + line.lstrip().lstrip("!") for line in lines]


COMMANDS = ("git", "echo")  # the commands step cells run


def git(*args, cwd):
    return subprocess.run(["git", *args], cwd=cwd, stdin=subprocess.DEVNULL, capture_output=True, text=True).stdout


def repository():
    """The repository Step 1 cloned into practice/, or None."""
    found = [p for p in PRACTICE.iterdir() if (p / ".git").is_dir()] if PRACTICE.is_dir() else []
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def build(n):
    """Step 1 starts from an empty practice/ folder; Steps 2 to 4 go on in your clone; Step 5 in Exercise 2's meal plan."""
    os.chdir(HOME)
    if n == 1:
        shutil.rmtree(PRACTICE, ignore_errors=True)
        PRACTICE.mkdir(parents=True, exist_ok=True)
        WHERE[0] = PRACTICE
    elif n == 5:
        WHERE[0] = MEAL_PLAN if (MEAL_PLAN / ".git").is_dir() else None
    else:
        WHERE[0] = repository()


FILE = "hello.txt"
AGAIN = " Make the TODO line match the line shown above this cell, then run this cell again."
ERROR = ("PROBLEM: a command stopped with an error: make the TODO line match the line shown above this cell, "
         "then run this cell again.")
SIGN_IN_FAILED = ("PROBLEM: Git could not sign in to GitHub: sign in from a terminal first, as your instructor "
                  "showed you, then run this cell again.")
REFUSED = "PROBLEM: GitHub refused the push: use a repository of your own, which you can push to."


def committed(where):
    """hello.txt is in your clone's last commit."""
    return subprocess.run(["git", "cat-file", "-e", f"HEAD:{FILE}"], cwd=where, capture_output=True).returncode == 0


def pushed(where):
    """Your commit with hello.txt is on GitHub: your branch and GitHub's are the same commit."""
    head, upstream = (git("rev-parse", "-q", "--verify", ref, cwd=where).strip() for ref in ("HEAD", "@{upstream}"))
    return committed(where) and bool(head) and head == upstream


def address(url):
    """A repository's address without the parts that may differ: the case, a last slash, .git."""
    url = url.strip().lower().rstrip("/")
    return url[:-len(".git")] if url.endswith(".git") else url


def check(n):
    """(right or not, the line that says so) after Step n's commands."""
    shown = "".join(text for _, text in RUNS)
    failed = any(code for code, _ in RUNS)
    where = repository()
    signing = "could not read Username" in shown or "Authentication failed" in shown
    refused = "error: 403" in shown or "Permission to" in shown
    if n == 1:
        if where:
            return True, f"OK: your repository is cloned into practice/{where.name}, and its address is saved as origin."
        if "'URL' does not exist" in shown:
            return False, "PROBLEM: nothing was cloned: change URL to your repository's address." + AGAIN
        if "Permission denied (publickey)" in shown:
            return False, "PROBLEM: that is an SSH address: copy the HTTPS one, which starts with https://." + AGAIN
        if signing:
            return False, SIGN_IN_FAILED
        if "not found" in shown:
            return False, ("PROBLEM: GitHub found no repository at that address: copy it from the green Code "
                           "button on your repository's page." + AGAIN)
        return False, ERROR if failed else "PROBLEM: nothing was cloned." + AGAIN
    if n == 5:
        if WHERE[0] is None:
            return False, "PROBLEM: there is no meal plan from Exercise 2 yet: do Exercise 2 first, then run this cell again."
        if "'URL' does not appear to be a git repository" in shown:
            return False, "PROBLEM: nothing was pushed: change URL to your repository's address." + AGAIN
        if signing:
            return False, SIGN_IN_FAILED
        if refused:
            return False, REFUSED
        if failed:
            return False, ERROR
        if "veggie-week -> veggie-week" not in shown and "Everything up-to-date" not in shown:
            return False, "PROBLEM: veggie-week was not pushed." + AGAIN
        sent_to = [line[3:].strip() for line in shown.splitlines() if line.startswith("To ")]
        origin = git("remote", "get-url", "origin", cwd=where) if where else ""
        if sent_to and origin and address(sent_to[0]) != address(origin):
            return False, (f"PROBLEM: veggie-week went to {sent_to[0]}, not to the repository you cloned, "
                           f"{origin.strip()}: use that address." + AGAIN)
        return True, "OK: veggie-week is on GitHub, with the commits you made in Exercise 2."
    if where is None:
        return False, "PROBLEM: there is no clone of your repository in practice/ yet: do Step 1 first."
    staged = git("diff", "--cached", "--name-only", cwd=where).split()
    if n == 2:
        if FILE in staged:
            return True, "OK: hello.txt is staged: git status lists it under Changes to be committed."
        if "pathspec 'FILE'" in shown:
            return False, "PROBLEM: nothing was staged: change FILE to hello.txt." + AGAIN
        if committed(where) and not git("status", "--porcelain", FILE, cwd=where).strip():
            return True, "OK: hello.txt has no new change: it is already in your last commit."
        return False, ERROR if failed else "PROBLEM: hello.txt is not staged." + AGAIN
    if n == 3:
        if committed(where) and FILE not in staged:
            return True, "OK: your commit holds hello.txt: git log lists it first."
        if "empty commit message" in shown:
            return False, ("PROBLEM: no commit was made: Git stops a commit with an empty message. "
                           "Type Add hello.txt between the quotes, then run this cell again.")
        if "Please tell me who you are" in shown:
            return False, ('PROBLEM: Git does not know your name yet: in a terminal, run git config --global '
                           'user.name "Your Name" and git config --global user.email "you@example.com", '
                           "then run this cell again.")
        if FILE not in staged:
            return False, "PROBLEM: hello.txt is not staged: do Step 2 first."
        return False, ERROR if failed else "PROBLEM: no commit was made." + AGAIN
    if pushed(where):
        return True, "OK: your commit is on GitHub: git status says your branch is up to date with origin."
    if not committed(where):
        return False, "PROBLEM: there is no commit with hello.txt to push yet: do Step 3 first."
    if signing:
        return False, SIGN_IN_FAILED
    if refused:
        return False, REFUSED
    if "[rejected]" in shown:
        return False, ("PROBLEM: GitHub holds a commit that your clone does not. Pull it first, as in Exercise 3: "
                       "add the line !git pull above !git push, then run this cell again.")
    return False, ERROR if failed else "PROBLEM: your commit is not on GitHub yet." + AGAIN


RESULTS = {}
DONE = "Done: hello.txt and your Exercise 2 branch, veggie-week, are on GitHub: open your repository's page to see them."


def step(line):
    """%step N: run Step N's cell in its folder; after the cell, print OK or PROBLEM."""
    n = int(line)
    build(n)
    RUNS.clear()

    def after(result):
        shell.events.unregister("post_run_cell", after)
        RESULTS[n], text = check(n)
        print(text)

    shell.events.register("post_run_cell", after)


def done(line):
    """%done: Done, or Not yet with the first step to redo, from what is in your clone and on GitHub."""
    where = repository()
    if where is None:
        print("Not yet: clone your repository. Redo Step 1.")
    elif not committed(where):
        print("Not yet: stage and commit hello.txt. Redo Steps 2 and 3.")
    elif not pushed(where):
        print("Not yet: push your commit. Redo Step 4.")
    elif not RESULTS.get(5):
        print("Not yet: push veggie-week from Exercise 2. Redo Step 5.")
    else:
        print(DONE)


shell = get_ipython()
shell.system = run_line
shell.register_magic_function(step, "line", "step")
shell.register_magic_function(done, "line", "done")
cleanup = shell.input_transformers_cleanup  # what IPython does to each cell's text before it runs it
cleanup[:] = [t for t in cleanup if getattr(t, "__name__", "") != "as_command"] + [as_command]
PRACTICE.mkdir(parents=True, exist_ok=True)
