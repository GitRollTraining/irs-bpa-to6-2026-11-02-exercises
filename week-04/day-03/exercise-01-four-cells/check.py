"""The done check for exercise 1. In Databricks, cell 8 of the notebook runs it: it sorts the ten
returns at 0.5 and counts the 200 examined returns again, from the scores cell 2 gave, and compares
what you typed with that. Without Databricks, from the course folder:

    python3 week-04/day-03/exercise-01-four-cells/check.py --start
    python3 week-04/day-03/exercise-01-four-cells/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

CELLS = ("TP", "FP", "FN", "TN")
NAMES = {"tp": "TP", "true positive": "TP", "fp": "FP", "false positive": "FP",
         "fn": "FN", "false negative": "FN", "tn": "TN", "true negative": "TN"}
TEN = {205: (0.997, "change"), 224: (0.983, "change"), 123: (0.964, "change"), 905: (0.942, "no change"),
       463: (0.652, "no change"), 37: (0.474, "no change"), 471: (0.179, "change"), 50: (0.071, "change"),
       4: (0.058, "no change"), 11: (0.0, "no change")}
GIVEN = {205: "TP", 224: "TP", 123: "TP", 50: "FN", 4: "TN", 11: "TN"}  # cell 4 sorts these six for the learner
START = {"ten": {str(k): list(v) for k, v in TEN.items()}, "my_cells": {str(k): GIVEN.get(k, "") for k in TEN},
         "meaning": {"FP": "", "FN": ""}, "guess": None, "all_counts": {c: None for c in CELLS},
         "expected_all": {"TP": 34, "FP": 3, "FN": 6, "TN": 157}}


def plain(text) -> str:
    """A typed answer as the check reads it: lower case, with no spaces or full stop around it."""
    return str(text).strip().strip(".!").strip().lower()


def cell_of(score: float, label: str, threshold: float = 0.5) -> str:
    """One return's cell at the threshold. A score equal to the threshold goes on the list."""
    on, change = score >= threshold, label == "change"
    return {(True, True): "TP", (True, False): "FP", (False, True): "FN", (False, False): "TN"}[(on, change)]


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: ten (each return's score and label, by case_id), my_cells, meaning, guess,
            all_counts, and expected_all (the 200 examined returns' four counts, counted again).

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    blank, wrong = [], []
    for case, (score, label) in f["ten"].items():
        typed = plain(f["my_cells"].get(case, ""))
        if not typed:
            blank.append(case)
        elif NAMES.get(typed) != cell_of(score, label):
            wrong.append(case)
    if blank:
        out.append(f"Cell 4: type the cell of case {', '.join(blank)}. Step 2.")
    if wrong:
        out.append(f"Cell 4: look again at case {', '.join(wrong)}: is its score at or above 0.5, and what does "
                   "its label say? Step 2.")
    short = [c for c in ("FP", "FN") if len(str(f["meaning"].get(c, "")).split()) < 4]
    if short:
        out.append(f"Cell 5: write what {' and '.join(short)} {'mean' if len(short) > 1 else 'means'} for an examiner, "
                   "four words or more. Step 3.")
    guess = f.get("guess")
    if not isinstance(guess, (int, float)) or isinstance(guess, bool) or not 0 <= guess <= 6:
        out.append("Cell 6: type your guess, a whole number from 0 to 6 with no quotes, in place of None. Step 4.")
    if any(f["all_counts"].get(c) is None for c in CELLS):
        out.append("Cell 7: type the four counts of cell 6's table. Step 5.")
    elif {c: f["all_counts"][c] for c in CELLS} != f["expected_all"]:
        out.append("Cell 7: a count is not where the table puts it. Its rows are the labels: first change, then "
                   "no change. Check the two sums: 200 and 40. Step 5.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        m = {c: 0 for c in CELLS}
        for score, label in f["ten"].values():
            m[cell_of(score, label)] += 1
        a = f["all_counts"]
        return (f"Done: at 0.5, the ten returns are {m['TP']} TP, {m['FP']} FP, {m['FN']} FN, {m['TN']} TN; "
                f"the 200 examined returns are {a['TP']} TP, {a['FP']} FP, {a['FN']} FN, {a['TN']} TN. "
                f"Your guess, written before you counted: {f['guess']} of the {a['FN']} missed scoring above 0.4.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out])


def facts_of(g: dict) -> dict:
    """The facts, from the notebook's values."""
    scores = g["scores"]
    examined = scores[scores["label"] != "never examined"]
    expected = {c: 0 for c in CELLS}
    for score, label in zip(examined["logistic_score"], examined["label"]):
        expected[cell_of(float(score), label)] += 1
    ten = scores[scores["case_id"].isin(list(TEN))]
    number = lambda v: None if v is None else int(v)
    return {"ten": {str(int(c)): [float(s), l] for c, s, l in zip(ten["case_id"], ten["logistic_score"], ten["label"])},
            "my_cells": {str(k): v for k, v in g["my_cells"].items()},
            "meaning": dict(g["meaning"]),
            "guess": g.get("guess"),
            "all_counts": {c: number(g["all_counts"].get(c)) for c in CELLS},
            "expected_all": expected}


def in_notebook(g: dict) -> str:
    """Return what the check cell prints, from the notebook's values (cell 8 passes them)."""
    return report(facts_of(g))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
