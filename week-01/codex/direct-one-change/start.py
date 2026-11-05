"""Build this exercise's project, work/, from files/. In this folder, run: python3 start.py

work/ is a Git repository of its own with one commit: the checkpoint before Codex starts. The script
keeps that commit's id in work/.git/info/exercise-start, so that check.py finds every commit after
it, and lists record.md in work/.git/info/exclude, so that Git ignores your notes. It reads nothing
outside this folder. If work/ exists already, it stops and changes nothing.
"""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "work"
# The start commit's author, so that the start works before you set your own name in Git.
AUTHOR = ["-c", "user.name=Course start", "-c", "user.email=course-start@example.invalid",
          "-c", "commit.gpgsign=false"]


def git(*args: str) -> str:
    """Run one Git command in work/ and return what it prints.

    Args:
        *args: The Git command's arguments, for example "add", "-A".

    Returns:
        The command's output, without the line end.

    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    done = subprocess.run(["git", *args], cwd=WORK, check=True, capture_output=True, text=True)
    return done.stdout.strip()


def main() -> None:
    """Copy files/ to work/, make it a Git repository with one commit, and keep that commit's id."""
    if WORK.exists():
        sys.exit("work/ exists already, so nothing changed. To start again, rename it first, "
                 "for example: mv work work-old")
    shutil.copytree(HERE / "files", WORK, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    git("init", "-q")
    info = WORK / ".git" / "info"
    info.mkdir(exist_ok=True)
    with open(info / "exclude", "a") as exclude:
        exclude.write("record.md\n")
    git("add", "-A")
    git(*AUTHOR, "commit", "-q", "-m", "Start: parse_duration and its tests")
    (info / "exercise-start").write_text(git("rev-parse", "HEAD") + "\n")
    print("work/ is ready, with one commit: your checkpoint. Next: cd work")


if __name__ == "__main__":
    main()
