"""The done check for this exercise. From extractor/, run: python3 ../check.py

It reads the repository extractor/ through Git. It checks that no commit and not the staging area holds
the change to model.py or the log directory, logs/. It checks that the last commit holds each change that
you asked the agent for (agent-session.txt), as the agent made it. Last, it checks that a committed
.gitignore keeps logs/ out of Git. It runs no test, calls no model and starts no agent.
"""
import json
import os
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
KIT = next(p for p in HERE.parents if (p / "lab-states").is_dir())  # the course folder
RESET_PY = os.path.relpath(KIT / "reset.py")  # the reset, as a path from where this runs
REPO = HERE / "extractor"
# start.py records the Git id of each changed file, as the course committed it and as the agent left it.
RECORD = REPO / ".git" / "info" / "agent-run.json"
# The kept answer, which the exercise's table gives: commit the three changes that the request asks for,
# leave out model.py, the debugging print that writes the whole note to logs/extractor.log, and add logs/
# to .gitignore. Each line of the check names its file, what to do, and the notebook line.
ASKED = ("extractor.py", "tests/test_extractor.py", "README.md")
LEFT_OUT = "model.py"
LOGS = "logs"
LOG_FILES = [p.relative_to(HERE / "files").as_posix()
             for p in sorted((HERE / "files" / LOGS).rglob("*")) if p.is_file()]
RESET = f"python3 {RESET_PY} commit-three-of-four"
TABLE = "Skipping staging lets an agent's stray edit in."
WHO_CHOOSES = f'Section 4.1, the table under "{TABLE}", row Who chooses: "You choose which changes go in".'
STAY_OUT = (f'Section 4.1, the table under "{TABLE}", row The debugging print: with git add, then git commit, '
            'it "Can stay out".')
IGNORE = ('Section 4.1, the heading "Keep the logs out: a pushed commit is very hard to take back." Below it: '
          '"A .gitignore file lists patterns of files Git will not offer to add."')
STAGING = ('Section 4.1, the heading "The staging area lets you keep three changes, leave the fourth." Below it: '
           '"git add copies a file into the staging area, the draft of the next commit."')


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def stop(message):
    print("Not yet: 1 left.")
    print("- " + message)
    sys.exit(1)


def blob(rev, path):
    """The Git id of what rev holds at path (rev "" is the staging area), or None where it holds nothing."""
    found = git("rev-parse", "-q", "--verify", f"{rev}:{path}")
    return found.stdout.strip() if found.returncode == 0 else None


def on_disk(path):
    """The Git id that the file on disk gets when you stage it, or None where there is no file."""
    found = git("hash-object", "--", path) if (REPO / path).is_file() else None
    return found.stdout.strip() if found and found.returncode == 0 else None


def unstage(path):
    """How to take path out of the staging area: in the notebook with cell 2, in a terminal with Git."""
    return (f"Unstage it. In the notebook, take it out of files and run cell 2 again. In a terminal, run git restore "
            f"--staged {path}.")


if not (REPO / ".git").is_dir() or not RECORD.is_file() or git("rev-parse", "-q", "--verify", "HEAD").returncode:
    stop(f"there is no repository extractor/ yet. Run {RESET}.")
record = json.loads(RECORD.read_text())
agent, course = record["agent"], record["course"]

problems = []

# model.py and the log directory: in no commit of the history, and not staged. A stash is not part of the
# history, so it is not read. Their lines come first, as a commit takes all that the staging area holds.
commits = git("rev-list", "HEAD", "--branches", "--tags", "--remotes").stdout.split()
staged = git("diff", "--cached", "--name-only").stdout.split()
held = []  # what the two lines below say to unstage
if any(blob(commit, LEFT_OUT) != course[LEFT_OUT] for commit in commits):
    problems.append(f"a commit holds the change to {LEFT_OUT}, the debugging print that you did not ask for. The "
                    f"exercise's table leaves it out. A commit stays in the history. To start again, run {RESET}. "
                    f"{STAY_OUT}")
elif LEFT_OUT in staged:
    held.append(LEFT_OUT)
    problems.append(f"the staging area holds the change to {LEFT_OUT}, the debugging print. The exercise's table "
                    f"leaves it out. {unstage(LEFT_OUT)} {STAY_OUT}")
if any(git("cat-file", "-e", f"{commit}:{LOGS}").returncode == 0 for commit in commits):
    problems.append(f"a commit holds {LOGS}/, with a whole note in its log. The exercise's table keeps it out. A "
                    f"commit stays in the history. To start again, run {RESET}. {IGNORE}")
elif any(path.startswith(LOGS + "/") for path in staged):
    held.append(LOGS + "/")
    problems.append(f"the staging area holds {LOGS}/. The exercise's table keeps it out. {unstage(LOGS + '/')} "
                    f"{IGNORE}")
# The move that commits a change. While the lines above say to unstage model.py or logs/, it says that first, and
# says "commit" with no "it", which could read as a commit of that file.
THEN_COMMIT = f"Unstage {' and '.join(held)}. Then commit." if held else "Then commit it."
COMMIT = THEN_COMMIT if held else "Commit it."

# The changes that you asked for: each one in the last commit, as the agent made it. One line for each.
for path in ASKED:
    head = blob("HEAD", path)
    if head == agent[path]:
        continue
    if head == course[path]:
        line = f"the change to {path} is not in a commit yet. You asked for it in ../agent-session.txt."
    else:
        # The last commit holds the file with an edit that the agent did not make, or holds no such file.
        line = (f"the last commit does not hold {path} as the agent left it. You asked for the agent's change in "
                "../agent-session.txt.")
    if blob("", path) == agent[path]:
        # The commit takes the copy that you staged, so a later edit on disk does not matter here.
        line += f" The staging area holds it. {COMMIT}"
    elif on_disk(path) == agent[path]:
        line += f" Stage it. {THEN_COMMIT}"
    else:
        # No commit, not the staging area and not the disk holds the agent's change now: only the reset gets it back.
        if head == course[path]:
            line += f" {path} is not as the agent left it."
        line += f" To get the agent's change back, run {RESET}."
    problems.append(f"{line} {WHO_CHOOSES}")

# .gitignore: a line in it keeps every file of logs/ out of Git, and a commit holds it.
lines = git("check-ignore", "--no-index", "--verbose", "--non-matching", "--", *LOG_FILES).stdout.splitlines()
kept_out = len(lines) == len(LOG_FILES) and all(
    line.split(":", 1)[0] == ".gitignore" and not line.split("\t", 1)[0].split(":", 2)[-1].startswith("!")
    for line in lines)
if not kept_out:
    problems.append(f".gitignore has no line that keeps {LOGS}/ out yet. Add {LOGS}/ on a new line at its end, as "
                    f"the exercise's table says. Save .gitignore. Stage it. {THEN_COMMIT} {IGNORE}")
elif git("status", "--porcelain", "--", ".gitignore").stdout.strip():
    if ".gitignore" in staged:
        problems.append(f"the staging area holds your line in .gitignore, but no commit holds it yet. {COMMIT} "
                        f"{STAGING}")
    else:
        problems.append(f"your line in .gitignore is not in a commit yet. Stage .gitignore. {THEN_COMMIT} {STAGING}")

if problems:
    print(f"Not yet: {len(problems)} left.")
    print("\n".join(f"- {problem}" for problem in problems))
    sys.exit(1)
print("Done: the history holds the changes to extractor.py, tests/test_extractor.py and README.md, and your line "
      "in .gitignore, which keeps logs/ out of Git. No commit holds the debugging print in model.py or logs/.")
