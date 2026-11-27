"""The done check for exercise 1. In Databricks, cell 8 of the notebook runs it: it counts the label
exam_changed_tax again in the training set that cell 2 loaded (course.returns.model_train, or the same
rows from the course's setup file), counts how often each column of fields.csv agrees with it, and reads
your origin, your column of cell 6, your trace and your marks. Without Databricks, from the course folder:

    python3 week-04/day-02/exercise-01-labels-and-marks/check.py --start
    python3 week-04/day-02/exercise-01-labels-and-marks/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

LABEL = "exam_changed_tax"
FILE = "fields.csv"
GIVEN = {"tax_to_agi": "before", "deduction_amt": "before", "deduction_missing": "before",
         "tax_added_by_exam": "after"}  # Monday's record marks these four; cell 7 gives them
EXAMINER = ("exam", "auditor", "agent")  # "exam" covers examiner and examination
# Stages of the tax work that change the tax on an account after the return is filed
STEPS_AFTER_FILING = ("exam", "audit", "assess", "adjust", "amend", "aur", "underreport", "cp2000", "cp 2000",
                      "notice", "posting", "posted", "correction", "math error", "collection")
MADE_BY = ("course", "synthetic", "made up", "made-up", "simulated", "fake", "not real", "generated", "invented")
START = {"label_column": "refund_held",
         "origin": {"decision": "", "made by": "", "when": ""},
         "beside": "refund-held.csv", "agreement_label": "refund_held", "agreement": {"refund_hold_days": 16},
         "labelled": 16, "suspect": "", "file_agreement": {},
         "trace": {"which table holds it": "refund-held.csv", "which stage wrote it": ""},
         "marks": dict({name: [mark, "given in cell 7"] for name, mark in GIVEN.items()}, **{"": ["", ""]}),
         "counts": {"no": 320, "yes": 80}, "empty": 100}


def plain(text) -> str:
    """An answer as the check reads it: lower case, with no spaces or full stop around it."""
    return str(text).strip().strip(".").strip().lower()


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: label_column, origin, beside (the file cell 5 read), agreement_label (the
            label cell 5 used), suspect, trace, marks, file_agreement (how often each column of fields.csv
            agrees with exam_changed_tax, counted by the check), and the counts of exam_changed_tax in train.

    Returns:
        One line per problem; an empty list when the exercise is done. No line names the column that
        gives the label away before cell 6 names it.
    """
    out = []
    if f["label_column"] != LABEL:
        out.append(f"Cell 3 counts {f['label_column']}. Type {LABEL} in its place, then run cell 3. Step 2.")
    origin = {k: plain(v) for k, v in f["origin"].items()}
    decision, missing = origin.get("decision", ""), []
    if not ("exam" in decision or "audit" in decision or ("tax" in decision and "chang" in decision)):
        missing.append("decision (which decision: the examination's result)")
    if not any(word in origin.get("made by", "") for word in MADE_BY + EXAMINER):
        missing.append("made by (who made these labels)")
    if len(origin.get("when", "").split()) < 2:
        missing.append("when (two words or more)")
    if missing:
        out.append("Cell 4: answer " + "; ".join(missing) + ". Then run cell 4. Step 3.")
    if f["beside"] != FILE or f["agreement_label"] != LABEL:
        out.append(f"Cell 5 has not put the columns of {FILE} beside {LABEL} yet. Type {FILE} in cell 5, then "
                   "run cells 3 and 5. Step 4.")
    found = f.get("file_agreement") or {}
    leak = max(found, key=found.get) if found else None
    if f["suspect"] != leak:
        out.append(f"Cell 6: type the name of the column of {FILE} that agrees with {LABEL} on nearly every "
                   "return, as cell 5 counted it. Step 5.")
    trace = {k: plain(v) for k, v in f["trace"].items()}
    if not any(w in trace.get("which stage wrote it", "") for w in STEPS_AFTER_FILING):
        out.append("Cell 6: answer which stage of the tax work wrote the column: what changes the tax on an account "
                   "after a return is filed? Then run cell 6. Step 5.")
    wanted = dict(GIVEN, **{column: ("after" if column == leak else "before") for column in found})
    wrong = set()
    for name, right in wanted.items():
        mark, reason = (list(f["marks"].get(name, ["", ""])) + ["", ""])[:2]
        if plain(mark) != right or len(str(reason).split()) < 3:
            wrong.add(name)
    given_changed, file_wrong = bool(wrong & set(GIVEN)), bool(wrong - set(GIVEN))
    if file_wrong or not found:
        out.append(f"Cell 7: give each column of {FILE} its name, the mark its timing says, before or after, and a "
                   "reason of three words or more. Then run cell 7. Step 6.")
    if given_changed:
        out.append("Cell 7: the four rows of Monday's record are given. Set them back as the course gives them. "
                   "Step 6.")
    return out


def note(f: dict) -> str:
    """One line when cell 4 names an examiner: right for a real return, but these labels are the course's."""
    made_by = plain(f["origin"].get("made by", ""))
    if any(w in made_by for w in EXAMINER) and not any(w in made_by for w in MADE_BY):
        return ("\nNote: on a real return an examiner makes this label; in this course no examiner did, and the "
                "labels themselves are made up by the course.")
    return ""


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        counts, n = f["counts"], sum(f["counts"].values())
        return (f"Done: {LABEL} counts no {counts.get('no', 0)}, yes {counts.get('yes', 0)}, and {f['empty']} empty, "
                f"not counted. Of the columns of {FILE}, {f['suspect']} agrees with it on "
                f"{f['file_agreement'][f['suspect']]} of {n} returns; you traced it to a stage after selection and "
                "marked it after, beside tax_added_by_exam."
                + note(f))
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out]) + note(f)


def facts_of(values: dict, folder: str) -> dict:
    """The facts, from the notebook's values: the label counted again in the training set, and each
    column of fields.csv put beside it by this check, not taken from cell 5."""
    import pandas as pd
    values = dict(values)
    train = values.pop("train")
    facts = dict(START, **values)
    facts["marks"] = {k: list(v) if isinstance(v, (tuple, list)) else [v, ""] for k, v in facts["marks"].items()}
    labels = train[LABEL]
    facts["counts"] = {str(k): int(v) for k, v in labels[labels.notna()].value_counts().items()}
    facts["empty"] = int(labels.isna().sum())
    columns = [c for c in pd.read_csv(f"{folder}/{FILE}", comment="#", nrows=1).columns if c != "return_id"]
    labelled = train[labels.notna()]
    facts["file_agreement"] = {c: int(((labelled[c] > 0) == (labelled[LABEL] == "yes")).sum()) for c in columns}
    return facts


def in_notebook(values: dict, folder: str) -> str:
    """Return what the check cell prints, from the notebook's values (cell 8 passes them).

    Args:
        values: train (the DataFrame cell 2 loaded), label_column, origin, beside, agreement_label,
            agreement, labelled, suspect, trace and marks, as the cells hold them.
        folder: the exercise's folder, where fields.csv is.
    """
    return report(facts_of(values, folder))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
