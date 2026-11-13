"""The done check for exercise 2. In Databricks, cell 4 of the notebook runs it with the text of
cells 1 to 3. It reads text only: no table, no query, no model. Without Databricks, from the course
folder:

    python3 week-03/day-01/exercise-02-your-question-and-its-data/check.py <values.json>
    python3 week-03/day-01/exercise-02-your-question-and-its-data/check.py --start
"""
import json
import re
import sys
from pathlib import Path

KINDS = ["the return's lines", "data to match against", "past outcomes"]
VERDICTS = ["needed", "not needed", "transformed"]
IDENTIFYING = re.compile(r"\b(names?|ssn|tin|ein|ids?|identif\w*|address)\b", re.IGNORECASE)
SELECTION = re.compile(r"\b(select\w*|random|sample|score\w*|chose|chosen)\b", re.IGNORECASE)
START = {
    "question": "\nUnit:\nTarget:\nTime:\n",
    "items": (
        "\n| Item | Kind | Question it serves | Verdict | Reason |\n|---|---|---|---|---|\n"
        "| Wages on the return | the return's lines | Did the return report all its wages? | needed |"
        " A first model starts with what the taxpayer reported directly. |\n"
        + "|  |  |  |  |  |\n" * 6
    ),
    "explain": "",
}


def question_left(question: str) -> list[str]:
    """What is missing from the question: a Unit, a Target and a Time line, each with words after it."""
    out = []
    for part in ["Unit", "Target", "Time"]:
        found = re.search(rf"^\s*{part}\s*:(.*)$", question or "", re.IGNORECASE | re.MULTILINE)
        if not found or len(found.group(1).split()) < 2:
            out.append(f"Cell 1: write the {part} line, two words or more after '{part}:'. Step 1.")
    return out


def rows(items: str) -> list[list[str]]:
    """Read the filled rows of the table in cell 2: each a list of five cells. Header and empty rows are skipped."""
    found = []
    for line in (items or "").splitlines():
        if not line.strip().startswith("|") or set(line.replace("|", "").strip()) <= {"-", " ", ":"}:
            continue
        cells = [c.replace("`", "").strip() for c in line.strip().strip("|").split("|")]
        if cells[:2] == ["Item", "Kind"] or not any(cells):
            continue
        found.append((cells + [""] * 5)[:5])
    return found


def items_left(items: str) -> list[str]:
    """What is missing from the list: six items, each kind, a verdict and a reason each, the two rules."""
    out = []
    table = rows(items)
    if len(table) < 6:
        out.append(f"Cell 2 has {len(table)} filled rows. Write 6 or more, two of each kind. Step 2.")
    for item, kind, serves, verdict, reason in table:
        label = item or "a row with no item"
        if not item:
            out.append("A row has no item. Write the piece of information in its first column. Step 2.")
        if kind.lower() not in KINDS:
            out.append(f'"{label}": its kind is "{kind}". Write one of: ' + ", ".join(KINDS) + ". Step 2.")
        if not serves:
            out.append(f'"{label}": name the question it serves, or "none". Step 2.')
        if verdict.lower() not in VERDICTS:
            out.append(f'"{label}": its verdict is "{verdict}". Write needed, not needed or transformed. Step 2.')
        if len(reason.split()) < 4:
            out.append(f'"{label}": give a reason of 4 words or more. Step 2.')
        if IDENTIFYING.search(item) and verdict.lower() == "needed":
            out.append(f'"{label}" identifies a person. Does the prediction need it? See the row for the taxpayer\'s name in Step 2\'s table. Step 2.')
    kinds = [kind.lower() for _, kind, _, _, _ in table]
    for kind in KINDS:
        if kinds.count(kind) < 2 and len(table) >= 6:
            out.append(f'Cell 2 has fewer than 2 items of the kind "{kind}". Step 2.')
    if table and not any(v.lower() == "not needed" for _, _, _, v, _ in table):
        out.append("No item is not needed. Which field would the prediction not use? Step 2.")
    outcomes = [i for i, k, _, _, _ in table if k.lower() == "past outcomes"]
    if outcomes and not any(SELECTION.search(i) for i in outcomes):
        out.append("No past-outcomes item records how the IRS selected each examined return. Step 2.")
    return out


def left(values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    out = question_left(values["question"]) + items_left(values["items"])
    if len((values["explain"] or "").split()) < 8:
        out.append("Cell 3's explain has fewer than 8 words. Step 3.")
    return out


def report(values: dict) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(values)
    if not out:
        n = len(rows(values["items"]))
        return f"Done: your question names its unit, target and time, and each of its {n} items has a kind, the question it serves, a verdict and a reason."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(values: dict) -> str:
    """Return what cell 4 prints. The notebook passes the text of cells 1 to 3."""
    return report(values)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
