"""Build this exercise's team repository and your clone of it, from files/. Run it through the
reset command, in the course folder: python3 reset.py <this folder's name>

remote/team.git stands for the team's repository on a Git host: a bare repository, with no account
and nothing online. lab/ is your clone of it, a Git repository of its own, so your commits stay out
of the course's clone. Both start from one commit, the course team's, tagged start. review.md, your
review, sits in lab/ and stays out of its commits. A folder that is already there is emptied in
place first, so a terminal open inside it keeps working.
"""
import pathlib
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE / "lab"
REMOTE = HERE / "remote" / "team.git"
TEAM = ["-c", "user.name=Course team", "-c", "user.email=course-team@example.invalid"]


def git(*args: str, cwd: pathlib.Path) -> None:
    """Run one Git command as the course team."""
    subprocess.run(["git", *TEAM, *args], cwd=cwd, check=True, capture_output=True)


def empty(folder: pathlib.Path) -> None:
    """Make the folder, or empty it in place."""
    folder.mkdir(parents=True, exist_ok=True)
    for item in folder.iterdir():
        shutil.rmtree(item) if item.is_dir() and not item.is_symlink() else item.unlink()


empty(REMOTE)
empty(LAB)
git("init", "-q", "--bare", "-b", "main", ".", cwd=REMOTE)
with tempfile.TemporaryDirectory() as tmp:
    seed = pathlib.Path(tmp)
    shutil.copytree(HERE / "files", seed, dirs_exist_ok=True)
    for args in (["init", "-q", "-b", "main"], ["add", "-A"],
                 ["commit", "-q", "-m", "The payment job, as the team keeps it"], ["tag", "start"],
                 ["push", "-q", str(REMOTE), "main", "start"]):
        git(*args, cwd=seed)
git("clone", "-q", str(REMOTE), ".", cwd=LAB)
git("tag", "-f", "start", "origin/main", cwd=LAB)
shutil.copy(HERE / "review.md", LAB / "review.md")
with open(LAB / ".git" / "info" / "exclude", "a", encoding="utf-8") as exclude:
    exclude.write("review.md\n")
