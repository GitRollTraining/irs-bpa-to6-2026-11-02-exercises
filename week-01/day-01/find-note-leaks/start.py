"""Build this exercise's starting repository, extractor/. Run it through the reset command:
python3 ~/practice/reset.py find-note-leaks

extractor/ holds, on main, the course team's two commits: the simulated notes, the field list and the
route to the model; then the extractor, its output schema, its system prompt and its tests on
recorded replies (files/course/). On the branch agent/robust-extractor, checked out, it holds one
commit more, tagged agent-draft: a teammate's coding agent's change (files/agent/), which the
learner reviews. REVIEW.md is added and not committed, for the learner's findings.
"""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "lab-states").is_dir()) / "lab-states"))
from build_lab import TEAM, build  # noqa: E402

REPO = HERE / "extractor"
TEAMMATE = ["-c", "user.name=Teammate", "-c", "user.email=teammate@example.invalid"]


def git(who, *args):
    subprocess.run(["git", *who, *args], cwd=REPO, check=True, capture_output=True)


build(REPO, "base")
shutil.copytree(HERE / "files" / "course", REPO, dirs_exist_ok=True)
git(TEAM, "add", "-A")
git(TEAM, "commit", "-q", "-m", "Add the extractor, its output schema, its system prompt and its tests")
git(TEAM, "switch", "-q", "-c", "agent/robust-extractor")
shutil.copytree(HERE / "files" / "agent", REPO, dirs_exist_ok=True)
git(TEAMMATE, "add", "-A")
git(TEAMMATE, "commit", "-q", "-F", str(HERE / "files" / "agent-commit.txt"))
git(TEAMMATE, "tag", "agent-draft")
shutil.copy(HERE / "files" / "REVIEW.md", REPO / "REVIEW.md")
