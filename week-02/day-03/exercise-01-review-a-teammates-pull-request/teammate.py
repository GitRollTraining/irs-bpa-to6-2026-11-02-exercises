"""Your teammate opens their pull request: python3 teammate.py, in this exercise's folder.

It plays the teammate. It takes the team repository's main as it is now, makes the teammate's one
change on a new branch, add-penalty-cap, and pushes that branch to remote/team.git. It changes
nothing in lab/: there, git fetch brings the branch in. Run it once; a second run says the branch is
there already.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
REMOTE = HERE / "remote" / "team.git"
BRANCH = "add-penalty-cap"
MATE = ["-c", "user.name=Your teammate", "-c", "user.email=teammate@example.invalid"]


def git(*args: str, cwd: pathlib.Path) -> str:
    """Run one Git command as the teammate and return what it printed."""
    return subprocess.run(["git", *MATE, *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


if not REMOTE.is_dir():
    sys.exit(f"The team repository is not there yet. In the course folder, run python3 reset.py {HERE.name}.")
if git("branch", "--list", BRANCH, cwd=REMOTE).strip():
    sys.exit(f"Your teammate's branch {BRANCH} is there already. In lab: git fetch, then git switch {BRANCH}.")
with tempfile.TemporaryDirectory() as tmp:
    work = pathlib.Path(tmp)
    git("clone", "-q", str(REMOTE), ".", cwd=work)
    git("switch", "-q", "-c", BRANCH, cwd=work)
    shutil.copy(HERE / "teammate" / "rules.py", work / "payment_job" / "rules.py")
    git("commit", "-q", "-am", "Cap each account's penalty at 500 dollars", cwd=work)
    git("push", "-q", "origin", BRANCH, cwd=work)
print(f"Your teammate pushed {BRANCH}: one commit, 'Cap each account's penalty at 500 dollars'.")
print(f"In lab: git fetch, then git switch {BRANCH}.")
