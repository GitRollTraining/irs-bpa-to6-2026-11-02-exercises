"""Build this exercise's starting repository, lab/. Run it through the reset command:
python3 ~/practice/reset.py agent-boundary

lab/ is the week's lab repository after its run 2, as the course team committed it: the simulated
notes, the field list, the route to the model, the lab's agent configuration, the data-rules check,
the output schema and the extractor with its tests. Then the course team adds the pilot's facts,
docs/pilot.md (files/pilot.md); then a teammate commits the coding agents' configuration for the
pilot (files/claude-settings.json, files/mcp.json, files/codex-config.toml), tagged pilot-draft.
"""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "lab-states").is_dir()) / "lab-states"))
from build_lab import TEAM, build  # noqa: E402

REPO = HERE / "lab"
FILES = HERE / "files"
TEAMMATE = ["-c", "user.name=Teammate", "-c", "user.email=teammate@example.invalid"]


def git(who, *args):
    subprocess.run(["git", *who, *args], cwd=REPO, check=True, capture_output=True)


def place(source, target):
    (REPO / target).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(FILES / source, REPO / target)


build(REPO, "run2")
place("pilot.md", "docs/pilot.md")
git(TEAM, "add", "docs/pilot.md")
git(TEAM, "commit", "-q", "-m", "Add the pilot's facts: what an agent in this repository could reach")
place("claude-settings.json", ".claude/settings.json")
place("mcp.json", ".mcp.json")
place("codex-config.toml", ".codex/config.toml")
git(TEAMMATE, "add", ".claude/settings.json", ".mcp.json", ".codex/config.toml")
git(TEAMMATE, "commit", "-q", "-F", str(FILES / "teammate-commit.txt"))
git(TEAMMATE, "tag", "pilot-draft")
