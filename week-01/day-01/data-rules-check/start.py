"""Build this exercise's starting repository, lab/. Run it through the reset command:
python3 ~/practice/reset.py data-rules-check

lab/ is the week's lab repository at its first saved state: the simulated notes, the field list and
the route to the model, committed by the course team. One file is added and not committed:
docs/data-rules-check.md, the four uses to classify, with the answer cells left for the learner. Two uses
send exports/case-2231.txt, a case note that a teammate exported. Git ignores exports/, so no commit can
hold the note.
"""
import pathlib
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "lab-states").is_dir()) / "lab-states"))
from build_lab import build  # noqa: E402

build(HERE / "lab", "base")
shutil.copy(HERE / "files" / "data-rules-check.md", HERE / "lab" / "docs" / "data-rules-check.md")
(HERE / "lab" / "exports").mkdir()
shutil.copy(HERE / "files" / "case-2231.txt", HERE / "lab" / "exports" / "case-2231.txt")
with open(HERE / "lab" / ".git" / "info" / "exclude", "a") as exclude:
    exclude.write("exports/\n")
