"""Build this exercise's starting repository, lab/, from files/. Run it through the reset command,
in the course folder: python3 reset.py <this folder's name>

lab/ is a Git repository of its own, so your commits stay out of the course's clone. It holds one
commit, the course team's, tagged start. A lab/ that is already there is emptied in place first, so a
terminal open inside it keeps working.
"""
import pathlib
import shutil
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE / "lab"
TEAM = ["-c", "user.name=Course team", "-c", "user.email=course-team@example.invalid"]

LAB.mkdir(exist_ok=True)
for item in LAB.iterdir():
    shutil.rmtree(item) if item.is_dir() and not item.is_symlink() else item.unlink()
shutil.copytree(HERE / "files", LAB, dirs_exist_ok=True)
for args in (["init", "-q", "-b", "main"], ["add", "-A"],
             ["commit", "-q", "-m", "The sample return, as the course supplies it"], ["tag", "start"]):
    subprocess.run(["git", *TEAM, *args], cwd=LAB, check=True, capture_output=True)
