"""Build this exercise's starting repository, lab/. Run it through the reset command:
python3 ~/practice/reset.py data-rules-check

lab/ is the week's lab repository at its first saved state: the simulated notes, the field list and
the route to the model, committed by the course team. Two files are added and not committed:
docs/data-rules-check.md and docs/requirements.md, each with the cells you fill left empty or TODO.
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "lab-states").is_dir()) / "lab-states"))
from build_lab import build  # noqa: E402

build(HERE / "lab", "base")
for name in ("data-rules-check.md", "requirements.md"):
    shutil.copy(HERE / "files" / name, HERE / "lab" / "docs" / name)
