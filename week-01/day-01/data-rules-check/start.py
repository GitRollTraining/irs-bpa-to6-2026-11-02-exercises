"""Build this exercise's starting repository, lab/. Run it through the reset command:
python3 ~/practice/reset.py data-rules-check

lab/ is the week's lab repository at its first saved state: the simulated notes, the field list and
the route to the model, committed by the course team. One file is added and not committed:
docs/data-rules-check.md, the extractor's pilot, its approvals and its ten proposed uses, with the
answer cells left for the learner.
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "lab-states").is_dir()) / "lab-states"))
from build_lab import build  # noqa: E402

build(HERE / "lab", "base")
shutil.copy(HERE / "files" / "data-rules-check.md", HERE / "lab" / "docs" / "data-rules-check.md")
