"""Build this exercise's starting repository, lab/. Run it through the reset command:
python3 ~/practice/reset.py agent-boundary

lab/ is the week's lab repository after its first step, as the course team committed it: the
simulated notes, the field list and the route to the model; then the coding agent's configuration,
.claude/settings.json; then the data-rules check, passed. One file is added and not committed:
docs/boundary-proposal.md, with the cells you fill marked TODO.
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "lab-states").is_dir()) / "lab-states"))
from build_lab import build  # noqa: E402

build(HERE / "lab", "configured")
shutil.copy(HERE / "files" / "boundary-proposal.md", HERE / "lab" / "docs" / "boundary-proposal.md")
