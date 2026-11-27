"""The done check for exercise 2. In Databricks, cell 7 of the notebook runs it: it counts both
candidates' four cells at 0.5 again, from the scores cell 2 gave, and reads the newest run of each
name back from your experiment. Without Databricks, from the course folder:

    python3 week-04/day-03/exercise-02-precision-and-recall/check.py --start
    python3 week-04/day-03/exercise-02-precision-and-recall/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

NAMES = ("logistic-regression", "decision-tree")
START = {"guess": None,
         "by_hand": {n: {"precision": None, "recall": None} for n in NAMES},
         "counts": {"logistic-regression": {"TP": 34, "FP": 3, "FN": 6, "TN": 157},
                    "decision-tree": {"TP": 31, "FP": 12, "FN": 9, "TN": 148}},
         "logged": {}}


def plain(text) -> str:
    """A typed answer as the check reads it: lower case, with no spaces or full stop around it."""
    return str(text).strip().strip(".!").strip().lower()


def close(a, b) -> bool:
    if a is None or b is None or isinstance(a, str) or isinstance(b, str):  # a quoted division is not a number
        return False
    return abs(float(a) - float(b)) < 0.0005


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: guess, by_hand (the four divisions), counts (each candidate's four counts at
            0.5, counted again), and logged (the newest run of each name: threshold, precision, recall).

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    guess = f.get("guess")
    if not isinstance(guess, (int, float)) or isinstance(guess, bool) or not 0 <= guess <= 40:
        out.append("Cell 3: type your guess, a whole number from 0 to 40 with no quotes, in place of None. Step 2.")
    for name in NAMES:
        c, typed = f["counts"][name], f["by_hand"].get(name, {})
        want = {"precision": c["TP"] / (c["TP"] + c["FP"]), "recall": c["TP"] / (c["TP"] + c["FN"])}
        for measure, divide in (("precision", "TP + FP"), ("recall", "TP + FN")):
            if typed.get(measure) is None:
                out.append(f"Cell 5: type the {measure} of {name}. Step 3.")
            elif isinstance(typed[measure], str):
                out.append(f"Cell 5: type the {measure} of {name} with no quotes, such as 3 / 5, so Python "
                           "divides it. Step 3.")
            elif abs(float(typed[measure]) - want[measure]) < 0.006 and not close(typed[measure], want[measure]):
                top, bottom = c["TP"], c["TP"] + (c["FP"] if measure == "precision" else c["FN"])
                out.append(f"Cell 5: the {measure} of {name} is rounded. Type it as a division, such as "
                           f"`{top} / {bottom}`. Step 3.")
            elif not close(typed[measure], want[measure]):
                out.append(f"Cell 5: the {measure} of {name} is TP divided by {divide}, from cell 4's line for "
                           f"{name}. Step 3.")
    for name in NAMES:
        run = f["logged"].get(name)
        typed = f["by_hand"].get(name, {})
        if not run or run.get("precision") is None or run.get("recall") is None:
            out.append(f"Cell 6 has not logged precision and recall into the run {name}. Run cells 5 and 6. Step 4.")
        elif str(run.get("threshold")) != "0.5":
            out.append(f"The run {name} must hold the parameter threshold 0.5. Run cell 6 again. Step 4.")
        elif not (close(run["precision"], typed.get("precision")) and close(run["recall"], typed.get("recall"))):
            out.append(f"The run {name} holds other numbers than cell 5. Run cells 5 and 6 again. Step 4.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        parts = []
        for name in NAMES:
            c = f["counts"][name]
            parts.append(f"{name} precision {c['TP']} of {c['TP'] + c['FP']}, recall {c['TP']} of {c['TP'] + c['FN']}")
        return ("Done: at 0.5, " + "; ".join(parts) + ". Both are logged with the threshold in their runs. "
                f"Your guess at 0.4, written before you counted: {f['guess']} of the 40.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out])


def logged_of(g: dict) -> dict:
    """The newest run of each name in the notebook's experiment: its threshold, precision and recall."""
    if "experiment" not in g or "mlflow" not in g:
        return {}
    runs = g["mlflow"].search_runs(experiment_names=[g["experiment"]])
    out = {}
    for name in NAMES:
        found = runs[runs["tags.mlflow.runName"] == name] if len(runs) else runs
        if not len(found):
            continue
        run = found.iloc[0]
        value = lambda key: None if key not in run.index or run[key] is None or run[key] != run[key] else run[key]
        out[name] = {"threshold": value("params.threshold"), "precision": value("metrics.precision"),
                     "recall": value("metrics.recall")}
    return out


def facts_of(g: dict) -> dict:
    """The facts, from the notebook's values."""
    scores = g["scores"]
    examined = scores[scores["label"] != "never examined"]
    change = examined["label"] == "change"
    counts = {}
    for name, column in (("logistic-regression", "logistic_score"), ("decision-tree", "tree_score")):
        on = examined[column] >= 0.5
        counts[name] = {"TP": int((on & change).sum()), "FP": int((on & ~change).sum()),
                        "FN": int((~on & change).sum()), "TN": int((~on & ~change).sum())}
    number = lambda v: v if v is None or isinstance(v, str) else float(v)  # a quoted division stays text
    return {"guess": g.get("guess"),
            "by_hand": {n: {k: number(v) for k, v in m.items()} for n, m in g["by_hand"].items()},
            "counts": counts,
            "logged": {n: {k: (float(v) if k != "threshold" and v is not None else v) for k, v in r.items()}
                       for n, r in logged_of(g).items()}}


def in_notebook(g: dict) -> str:
    """Return what the check cell prints, from the notebook's values (cell 7 passes them)."""
    return report(facts_of(g))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
