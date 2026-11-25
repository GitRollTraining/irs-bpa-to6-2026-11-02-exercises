# Copied from scripts/week/check_exercise_self_contained.py in gitroll-dev/curriculum; do not edit here: change it there, then copy it again.
"""Fail an exercise that starts from the learner's own earlier work.

The exercise SOP, § Self-contained exercises: an exercise starts from a state the course supplies,
never from a notebook the learner filled, a value they typed, a table they wrote in their own
schema or a file they saved. Task Order 6 week 3 broke it in 10 of 16 exercises (the program
owner, 2026-11-24: "For some reason some of the exercises from week 3 are not self-contained");
week 2 did not, because each exercise there carries its start in its own folder.

Usage (the folder is an exercise repository, a week, a day or one exercise):
    python3 scripts/week/check_exercise_self_contained.py <folder>

An exercise is a folder directly in a day folder (`day-NN`, or a folder that holds `answers/` beside its
exercises, such as week 1's `codex/`) that is not the day's `answers/` or `figures/` and holds its own
`README.md` or a notebook, whatever it is named: the definition of `.github/check_repository.py` in the
exercise repository template. A day or week folder that holds folders of which none is recognised
fails, so a check that read nothing never prints ok. An exercise's learner text is its `README.md` and
the Markdown cells of its notebooks; its learner code is the code cells of its notebooks. A day folder `day-NN` also has what sits directly in it read, as text: its `README.md`
index, any other Markdown guide, and any notebook (a Program with one notebook per day; week 3's
`wednesday-tables.ipynb`). A finding there is named by the file's path, which holds the day.
Nothing else is read: no `.py` file, no file under `answers/`, no folder that is not an exercise
or a day.

Three kinds of finding, one line each, `<path>: <kind>: <the sentence or the name>`:

  own-work (a) one sentence that holds BOTH a reference to something the learner made or holds
           AND an earlier point in the course; PATTERNS below, roles "own" and "earlier". The
           exercise's own number and day are read from its path: "exercise 11" inside exercise 11
           is not earlier, "exercise 2" inside exercise 3 is. A sentence that says the earlier
           result is supplied here, or not needed, is skipped (roles "except").
  reads    (b) a notebook code cell uses a table of the learner's own schema (`{schema}.name`,
           `course.learner_NN.name`, with or without a catalog before it) by a literal name that
           no earlier line of the same notebook writes. A write under a name built at run time
           (`{schema}.{name}`) excuses every later use, because the name cannot be told.
  runs     (c) a notebook code cell runs another exercise's notebook (`%run ./exercise-01-x/...`).

What this does NOT cover, so a pass is not proof: files (a read of a file the course's setup does
not supply is not found), tables used under a name built at run time, a bare table name after
`USE <schema>`, tables of the shared course schemas (`course.returns.*` is supplied by the course
and never checked), reads in Python files, terminal commands or Markdown code blocks, a table whose
setup the exercise's guide names but whose code is not in a notebook, and any dependence the guide
states in words the PATTERNS do not describe, or splits over two sentences ("Open the notebook.
It is the one you saved yesterday." is found; "Yesterday you saved a notebook. Open it." is not).

Exits 0 when nothing is found, 1 on a finding, 2 on a missing or unreadable folder. Standard
library only. It builds no repository path: the folder is the argument.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday"]  # day-NN is the Nth of these
_DAY = "|".join(d.capitalize() for d in WEEKDAYS)
_MADE = (r"made|make|saved|save|wrote|write|written|built|build|created|create|typed|type|filled|fill|"
         r"ran|run|finished|finish|completed|exported|export|kept|keep|split|marked|produced|entered|"
         r"did|done|started|have|hold|own")
_EARLIER_EXERCISE = r"(?:previous|last|preceding|prior|earlier)\s+exercises?|exercises?\s+(?:above|before)|(?:the\s+)?one\s+before"

# One list, in four roles. A sentence is a finding when it matches at least one "own" pattern and
# at least one "earlier" pattern (a "earlier-*" role compares a number or a day with the
# exercise's own) and no "except" pattern. A "strip" pattern removes a phrase before the others
# run. Matched with the sentence's line breaks folded to spaces, ignoring case.
# (role, regular expression, the kind of wording it catches, one example)
PATTERNS = [
    # --- own: a reference to something the learner made or holds
    ("own", r"\byour\b",
     "any possessive for the learner's thing", "'your list', 'your notebook', 'your schema'"),
    ("own", r"\blearner['’]s\b",
     "the same, in the third person", "'the learner's own four notebooks'"),
    ("own", rf"\byou(?:['’]ve|['’]d)?\s+(?:\w+\s+){{0,2}}?(?:{_MADE})\b",
     "'you' then a verb of making, saving or holding",
     "'the table you created', 'the CSV you exported', 'After exercise 2 you have a table'"),
    ("own", r"\b(?:where\s+you\s+left\s+off|left\s+off|continu(?:e|es|ing)\s+(?:from|where|on)|"
            r"pick(?:s|ing)?\s+up\s+(?:from|where)|carry\s+on\s+(?:from|where)|builds?\s+on)\b",
     "going on from where something stopped", "'continue where you left off', 'pick up from exercise 2'"),
    ("own", rf"\b(?:from|of|in|left\s+by|made\s+by)\s+(?:the\s+)?(?:{_EARLIER_EXERCISE})\b",
     "a thing attributed to the exercise before, with no 'your'", "'uses df from the exercise above'"),
    ("own", rf"(?<!\bas\s)(?<!\bthan\s)\b(?:{_EARLIER_EXERCISE}|exercises?\s+\d+)\s+(?:it\s+)?"
            r"(?:wrote|made|built|saved|left|created|produced)\b",
     "an earlier exercise as the maker of the start (not a comparison: 'the same as exercise 2 made')",
     "'the tables the one before it wrote'"),
    ("own", r"\bexercises?\s+\d+['’]s\s+(?:tables?|output|results?|notebook|list|file|answers?|values?|"
            r"schema|features?|data)\b",
     "a numbered exercise's product", "'exercise 2's table'"),
    ("own", rf"\b(?:{_DAY})['’]s\s+(?:notebooks?|notes|records?|tables?|lists?|answers?|values?|schema|outputs?|results?)\b",
     "a named day's product, with no 'your'", "'Wednesday's tables', 'Monday's notebook'"),
    ("own", r"\b(?:notebooks?|notes|records?|tables?|lists?|answers?|values?|outputs?|results?|files?)\s+"
            r"(?:from|of|in|made\s+in)\s+(?:\w+['’]s\s+exercise|exercises?\s+\d+)\b",
     "a product named by the exercise it came from", "'the notebook from Monday's exercise 3', 'the table of exercise 2'"),
    # --- earlier: a point earlier in the course
    ("earlier", r"\b(?:yesterday|earlier|previously|this\s+morning|last\s+(?:week|night)|the\s+other\s+day)\b",
     "an earlier time named in words", "'yesterday', 'earlier today', 'last week'"),
    ("earlier", rf"\b(?:last|previous|preceding|prior)\s+(?:\w+\s+)?(?:exercises?|days?|weeks?|sessions?|class(?:es)?)\b|"
                rf"\b(?:{_EARLIER_EXERCISE})\b",
     "the exercise, day or class before", "'the last exercise', 'the previous exercise', 'the one before it'"),
    ("earlier-exercise", r"\bexercises?\s+(\d+)\b",
     "a numbered exercise lower than this one's own number", "'exercise 2' inside exercise 3"),
    ("earlier-day-level", r"\bexercise\s+notebooks?\b",
     "in a day-level file only: the notebooks of the day's own exercises", "'runs your four exercise notebooks'"),
    ("earlier-day", r"\bday\s+(\d+)\b",
     "a numbered day lower than this day", "'day 1' inside day 2"),
    ("earlier-weekday", rf"\b({_DAY})\b",
     "a weekday before this exercise's own day", "'Monday' inside a Tuesday exercise"),
    # --- except: the sentence says the earlier result is supplied, or not needed
    ("except", r"\b(?:supplied|provided|the\s+course(?:['’]s)?\s+(?:gives?|supplies|provides|file|table|copy|version)|"
              r"in\s+this\s+folder|this\s+folder|reset\.py|(?:cop(?:y|ies))\s+of|as\s+(?:exercise\s+\d+|the\s+one\s+before|"
              r"(?:\w+['’]s\s+)?exercise\s+\d+\s+ends|the\s+(?:previous|last)\s+exercise)\s+ends)\b",
     "the earlier result is supplied here", "'a copy of it is in this folder', 'the job as exercise 2 ends'"),
    ("except", r"\b(?:not\s+needed|no\s+need|need\s+nothing|need\s+not|(?:do(?:es)?\s+not|don['’]t)\s+need|"
              r"never\s+needs?|starts?\s+(?:blank|empty|fresh|from\s+scratch)|blank\s+on\s+purpose|nothing\s+from)\b",
     "the sentence says the earlier work is not needed", "'Your answer from exercise 2 is not needed'"),
    ("except", r"\b(?:your|the)\s+last\s+exercise\s+of\b",
     "'last' as the end of this day, not the one before", "'your last exercise of the day'"),
    # --- strip: a phrase that names a lesson, not the learner's work
    ("strip", r"\byour\s+(?:\w+['’]s\s+|\w+\s+)?(?:class|lesson|lecture|session|demo|talk|slides?|presentation|trainer)\b",
     "what a class or a lesson covered", "'Your Monday class covered keys'"),
    ("strip", r"\byour\s+(?:own\s+)?(?:team|company|organi[sz]ation|manager|colleagues?|teammates?|boss|client|"
              r"laptop|machine|browser|terminal|screen)\b",
     "a person or a place, not something the learner made", "'Your team keeps Tuesday's job in one repository'"),
]

# (b): a table of the learner's own schema, and how the text before it reads or writes it.
SCHEMA_TABLE = re.compile(r"\{\w*schema\w*\}\.(?P<name>\{?\w+\}?)|course\.learner_\w+\.(?P<lit>\w+)", re.I)
_CATALOG = r"(?:[\w{}$]+\.)*$"
WRITE_BEFORE = re.compile(
    rf"(?:saveAsTable|writeTo)\(\s*f?[\"']{_CATALOG}|CREATE\s+(?:OR\s+REPLACE\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?{_CATALOG}"
    rf"|INSERT\s+(?:INTO|OVERWRITE)\s+(?:TABLE\s+)?{_CATALOG}|(?:DROP|TRUNCATE)\s+TABLE\s+(?:IF\s+EXISTS\s+)?{_CATALOG}", re.I)
RUNS_EXERCISE = re.compile(r"%run\s+\S*exercise-\d+", re.I)

NOT_EXERCISES = {"answers", "figures"}
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z*`\"(\d])|\n\s*\n|\n(?=\s*(?:[-*]\s|\d+[.)]\s|#|\|))")


class Place:
    """Where a text sits: its exercise number and day number (None when unknown), and whether it is
    a day-level file, which has no exercise of its own."""

    def __init__(self, exercise: int | None = None, day: int | None = None, day_level: bool = False):
        self.exercise, self.day, self.day_level = exercise, day, day_level


def sentences(text: str) -> list[str]:
    return [re.sub(r"\s+", " ", part).strip() for part in SENTENCE_END.split(text) if part.strip()]


def is_earlier(role: str, match: re.Match, place: Place) -> bool:
    """Whether one "earlier-*" match is before this place. Unknown own numbers count as earlier."""
    if role == "earlier-exercise":
        return not place.day_level and (place.exercise is None or int(match.group(1)) < place.exercise)
    if role == "earlier-day-level":
        return place.day_level
    if role == "earlier-day":
        return place.day is None or int(match.group(1)) < place.day
    return place.day is None or WEEKDAYS.index(match.group(1).lower()) + 1 < place.day


def sentence_depends(sentence: str, place: Place) -> bool:
    """One sentence names something of the learner's AND an earlier point, and does not say the
    earlier result is supplied or not needed."""
    text = sentence
    for role, pattern, *_ in PATTERNS:
        if role == "strip":
            text = re.sub(pattern, " ", text, flags=re.I)
    if any(re.search(p, text, re.I) for r, p, *_ in PATTERNS if r == "except"):
        return False
    own = any(re.search(p, text, re.I) for r, p, *_ in PATTERNS if r == "own")
    earlier = any(is_earlier(r, m, place) if r.startswith("earlier-") else True
                  for r, p, *_ in PATTERNS if r.startswith("earlier")
                  for m in re.finditer(p, text, re.I))
    return own and earlier


def wording(text: str, place: Place | None = None) -> list[tuple[str, str]]:
    """The ("own-work", sentence) pairs of the sentences that depend on earlier learner work."""
    place = place or Place()
    found = []
    for sentence in sentences(text):
        if sentence_depends(sentence, place):
            pair = ("own-work", sentence if len(sentence) <= 170 else sentence[:167] + "...")
            if pair not in found:
                found.append(pair)
    return found


def notebook_cells(notebook: Path) -> list[tuple[str, str]]:
    """(cell type, source) of each cell of a notebook, in order."""
    cells = json.loads(notebook.read_text(encoding="utf-8")).get("cells", [])
    return [(c.get("cell_type", ""), "".join(c["source"]) if isinstance(c.get("source"), list)
             else str(c.get("source", ""))) for c in cells]


def reads_of_unwritten_tables(code: str) -> list[str]:
    """Learner-schema tables the code uses by a literal name before it writes them."""
    written: set[str] = set()
    dynamic_write = False
    found: list[str] = []
    for m in SCHEMA_TABLE.finditer(code):
        name = m.group("lit") or m.group("name")
        before = code[max(0, m.start() - 60):m.start()]
        if name.startswith("{"):
            dynamic_write = dynamic_write or bool(WRITE_BEFORE.search(before))
        elif WRITE_BEFORE.search(before):
            written.add(name)
        elif name not in written and not dynamic_write and name not in found:
            found.append(name)
    return found


def file_findings(texts: list[str], code: list[str], place: Place) -> list[tuple[str, str]]:
    """Every (kind, text) finding of the learner text and code of one exercise or one day-level file."""
    findings = list(dict.fromkeys(f for text in texts for f in wording(text, place)))
    joined = "\n".join(code)
    for name in reads_of_unwritten_tables(joined):
        findings.append(("reads", f"table {name} of the learner's schema, never written by this notebook"))
    for m in RUNS_EXERCISE.finditer(joined):
        findings.append(("runs", f"{m.group(0)}: runs another exercise's notebook"))
    return findings


def split_notebook(notebook: Path, texts: list[str], code: list[str]) -> None:
    for cell_type, source in notebook_cells(notebook):
        (code if cell_type == "code" else texts).append(source)


def number_in(name: str, prefix: str) -> int | None:
    m = re.match(rf"{prefix}-(\d+)", name)
    return int(m.group(1)) if m else None


def exercise_findings(folder: Path) -> list[tuple[str, str]]:
    """Every (kind, text) finding of one exercise folder."""
    texts, code = [], []
    readme = folder / "README.md"
    if readme.is_file():
        texts.append(readme.read_text(encoding="utf-8"))
    for notebook in sorted(folder.glob("*.ipynb")):
        split_notebook(notebook, texts, code)
    place = Place(number_in(folder.name, "exercise"), number_in(folder.resolve().parent.name, "day"))
    return file_findings(texts, code, place)


def holds_exercise_file(folder: Path) -> bool:
    """An exercise's own file: its README.md or a notebook (the test of `.github/check_repository.py`)."""
    return (folder / "README.md").is_file() or any(folder.glob("*.ipynb"))


def is_exercise_parent(folder: Path) -> bool:
    """A day folder `day-*`, or any folder that holds `answers/` beside its exercises (week 1's `codex/`)."""
    return folder.is_dir() and (folder.name.startswith("day-") or (folder / "answers").is_dir())


def exercise_candidates(parent: Path) -> list[Path]:
    """The folders directly in a day folder that are not its own support folders (`answers`, `figures`)."""
    return sorted(p for p in parent.iterdir()
                  if p.is_dir() and not p.name.startswith(".") and p.name not in NOT_EXERCISES)


def parents_under(root: Path) -> list[Path]:
    """The day folders at or under root, never one under answers/ or figures/."""
    found = [root] if is_exercise_parent(root) else []
    return found + sorted(p for p in root.rglob("*") if is_exercise_parent(p)
                          and not NOT_EXERCISES & set(p.relative_to(root).parts))


def exercise_folders(root: Path) -> list[Path]:
    """The exercise folders at or under root: a folder directly in a day folder, not answers/ or figures/,
    that holds its own README.md or a notebook. The definition of `.github/check_repository.py`
    (`NOT_EXERCISES`, and `exercise.ipynb` or `README.md`), whatever the folder is named."""
    if root.name not in NOT_EXERCISES and is_exercise_parent(root.parent) and holds_exercise_file(root):
        return [root]
    return sorted(c for parent in parents_under(root) for c in exercise_candidates(parent)
                  if holds_exercise_file(c))


def unrecognised_folders(root: Path) -> list[Path]:
    """The day folders, and week folders, that hold folders of which none was read as an exercise."""
    missed = [p for p in parents_under(root)
              if exercise_candidates(p) and not any(holds_exercise_file(c) for c in exercise_candidates(p))]
    weeks = [root] if root.name.startswith("week-") else sorted(p for p in root.rglob("week-*") if p.is_dir())
    missed += [w for w in weeks
               if exercise_candidates(w) and not any(is_exercise_parent(c) for c in exercise_candidates(w))]
    return missed


def day_files(root: Path) -> list[Path]:
    """The Markdown guides and notebooks that sit directly in each day folder at or under root."""
    days = [root] if root.name.startswith("day-") else sorted(p for p in root.rglob("day-*") if p.is_dir())
    return [f for d in days for f in sorted(d.iterdir()) if f.is_file() and f.suffix in {".md", ".ipynb"}]


def day_file_findings(path: Path) -> list[tuple[str, str]]:
    texts, code = [], []
    if path.suffix == ".ipynb":
        split_notebook(path, texts, code)
    else:
        texts.append(path.read_text(encoding="utf-8"))
    return file_findings(texts, code, Place(None, number_in(path.resolve().parent.name, "day"), day_level=True))


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not Path(argv[1]).is_dir():
        print(__doc__.split("Usage")[1].split("An exercise is")[0].strip(), file=sys.stderr)
        return 2
    root = Path(argv[1])
    exercises = exercise_folders(root)
    findings = 0
    flagged = 0
    for folder in exercises:
        found = exercise_findings(folder)
        flagged += bool(found)
        for kind, text in found:
            print(f"{folder}: {kind}: {text}")
        findings += len(found)
    unrecognised = unrecognised_folders(root)
    for folder in unrecognised:
        print(f"{folder}: no exercise recognised: it holds folders but none holds a README.md or a notebook "
              "(or, for a week, none is a day folder)")
    day_level = 0
    for path in day_files(root):
        for kind, text in day_file_findings(path):
            print(f"{path}: {kind}: {text}")
            day_level += 1
    findings += day_level + len(unrecognised)
    print(f"{'FAIL' if findings else 'ok'}: {len(exercises)} exercises checked, "
          f"{flagged} with findings, {findings} findings in all ({day_level} in day folders)"
          f"{f', {len(unrecognised)} folders with no exercise recognised' if unrecognised else ''}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
