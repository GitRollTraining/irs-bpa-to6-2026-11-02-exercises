"""The done check for exercise 3. In Databricks, cell 4 of the notebook runs it with the text of cells
2 and 3. It reads text only: no table, no query, no model. Without Databricks, from the course folder:

    python3 week-04/day-04/exercise-03-choose-the-technique/check.py --start
    python3 week-04/day-04/exercise-03-choose-the-technique/check.py <values.json>
"""
import json
import re
import sys
from pathlib import Path

LINES = ("Labelled data", "Cost", "Risk", "Choice", "Decided by")
EMPTY = "\n" + "\n".join(f"{name}:" for name in LINES) + "\n"
START = {"late_exams": EMPTY.replace("Cost:", "Cost: training once; then each new examination costs almost nothing to "
                                     "score, every week"), "drafts": EMPTY}
NEGATED = re.compile(r"\b(not|rather than|instead of|no)\s+(a\s+)?(trained model|model trained|prompting|prompts?)\b")
ROW = re.compile(r"\blabel|\bcost|\bcalls?\b|\brisk", re.I)
TASKS = (("late_exams", "Cell 2", "a trained model",
          "What are the many past examinations, each labelled on time or late, for?"),
         ("drafts", "Cell 3", "prompting",
          "Is there a store of approved answers for a model to learn from?"))


def line(text: str, name: str) -> str:
    """Return the words after `name:` in the text, or an empty string."""
    found = re.search(rf"^\s*{name}\s*:(.*)$", text or "", re.I | re.M)
    return found.group(1).strip() if found else ""


def choice(text: str) -> str:
    """Return the technique a Choice line names: a trained model, prompting, both, or an empty string.
    A technique the line rules out, such as "not prompting", does not count as named."""
    said = NEGATED.sub("", text.lower())
    trained, prompt = bool(re.search(r"\btrain", said)), "prompt" in said
    return "both" if trained and prompt else "a trained model" if trained else "prompting" if prompt else ""


def left(values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: late_exams and drafts, the text of cells 2 and 3.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    for name, cell, right, question in TASKS:
        text = values.get(name) or ""
        for row in ("Labelled data", "Cost", "Risk"):
            if len(line(text, row).split()) < 3:
                out.append(f"{cell}: answer {row} in three words or more, after '{row}:'. Step {cell[-1]}.")
        chosen = choice(line(text, "Choice"))
        if chosen == "both":
            out.append(f"{cell}: your Choice line names both a trained model and prompting. Keep only the one you "
                       f"choose. Step {cell[-1]}.")
        elif not chosen:
            out.append(f"{cell}: after 'Choice:', write a trained model or prompting. Step {cell[-1]}.")
        elif chosen != right:
            out.append(f"{cell}: look at your Labelled data line again. {question} Step {cell[-1]}.")
        decided = line(text, "Decided by")
        if len(decided.split()) < 6:
            out.append(f"{cell}: after 'Decided by:', write one sentence of six words or more. Step {cell[-1]}.")
        elif not ROW.search(decided):
            out.append(f"{cell}: the reason after 'Decided by:' names one of the three rows: labelled data, cost "
                       f"or risk. Which row does your reason belong to? Step {cell[-1]}.")
    risk = line(values.get("drafts") or "", "Risk")
    if len(risk.split()) >= 3 and "against" not in risk.lower():
        out.append("Cell 3: in the Risk line, say who catches a wrong draft, and against what, with the word "
                   "against. Step 3.")
    return out


def report(values: dict) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(values)
    if not out:
        return ("Done: each task has the three answers, a choice, and the row that decided it; your draft answers' "
                "Risk line says who catches a wrong draft, and against what.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out])


def in_notebook(g: dict) -> str:
    """Return what cell 4 prints, from the notebook's values (cell 4 passes them)."""
    return report({"late_exams": g.get("late_exams"), "drafts": g.get("drafts")})


def facts_of(g: dict) -> dict:
    """The facts the check reads: the text of cells 2 and 3."""
    return {"late_exams": g.get("late_exams"), "drafts": g.get("drafts")}


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
