"""The done check for week 3, day 1, exercise 1. In the notebook it is cell 3. In a terminal in the
course folder: python3 week-03/day-01/exercise-01-the-question-the-list-each-verdict/check.py

It reads record.json, which cell 2 writes beside this file, and checks the question, the target line
and each field's kind, verdict and reason. No model is called.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KINDS = {"line item", "compare", "outcome", "none"}
VERDICTS = {"needed", "not needed", "transform"}
# Each field: the kind, the verdict, and why, as the guide in step 2 gives them.
ANSWER = {
    "wages_amt": ("line item", "needed", "a line item the ranking compares with similar returns"),
    "total_income_amt": ("line item", "needed", "a line item the ranking compares with similar returns"),
    "w2_wages_amt": ("compare", "needed", "a third-party report to compare with the wages on the return"),
    "exam_changed_tax": ("outcome", "needed", "it is the target: the answer the model learns from"),
    "exam_picked_by": ("outcome", "needed", "it records which outcomes came from a random sample and which from a score"),
    "taxpayer_name": ("none", "not needed", "a name tells the ranking nothing it needs"),
    "tin": ("none", "transform", "it joins the tables, and Tuesday replaces it"),
    "street_address": ("none", "not needed", "an address identifies a person and tells the ranking nothing it needs"),
}


def question_left(question: str) -> list[str]:
    """Return what is missing from the question.

    Args:
        question: the sentence the learner typed in cell 2.

    Returns:
        One line for each part the question does not name yet; empty when it names all three.
    """
    q = question.lower()
    if not q.strip():
        return ["question is empty. Write it in one sentence. Step 1."]
    left = []
    if "return" not in q:
        left.append("The question does not name its unit: one return. Step 1.")
    if "chang" not in q or "tax" not in q:
        left.append("The question does not name its target: whether an examination changes the tax. Step 1.")
    if "year" not in q and not any(ch.isdigit() for ch in q):
        left.append("The question does not name its time, such as this year's returns. Step 1.")
    return left


def target_left(target: str) -> list[str]:
    """Return what is missing from the target line.

    Args:
        target: the line the learner typed in cell 2.

    Returns:
        One line for each part not yet written; empty when the line is complete.
    """
    t = target.lower()
    if not t.strip():
        return ["target is empty. Write the target you chose, why, and what you considered. Step 3."]
    left = []
    if "chang" not in t:
        left.append("The target line does not say the target: a change to the tax, yes or no. Step 3.")
    if "amount" not in t:
        left.append("The target line does not name what you considered: predicting the amount. Step 3.")
    return left


def fields_left(rows: dict) -> list[str]:
    """Return what is not yet right in the field rows.

    Args:
        rows: field name to a dict with the keys kind, verdict and reason.

    Returns:
        One line for each field that is not yet right.
    """
    left = []
    with open(HERE / "fields.csv", newline="", encoding="utf-8") as file:
        names = [row["field"] for row in csv.DictReader(file)]
    for name in names:
        row = rows.get(name) or {}
        kind = (row.get("kind") or "").strip().lower()
        verdict = (row.get("verdict") or "").strip().lower()
        reason = (row.get("reason") or "").strip()
        want_kind, want_verdict, why = ANSWER[name]
        if not (kind or verdict or reason):
            left.append(f"{name}: fill in its kind, verdict and reason. Step 2.")
            continue
        if kind not in KINDS:
            left.append(f'{name}: kind is "{kind or "empty"}". Use line item, compare, outcome or none. Step 2.')
        elif kind != want_kind:
            left.append(f'{name}: the kind "{kind}" does not fit what the field holds. Step 2.')
        if verdict not in VERDICTS:
            left.append(f'{name}: verdict is "{verdict or "empty"}". Use needed, not needed or transform. Step 2.')
        elif verdict != want_verdict:
            left.append(f'{name}: the verdict "{verdict}" is not the one the rule gives: {why}. Step 2.')
        if len(reason.split()) < 3:
            left.append(f"{name}: write a reason of three words or more. Step 2.")
    return left


def check(path: Path = HERE / "record.json") -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        path: the record to check; cell 2 writes it beside this file.

    Returns:
        The lines still to fix; an empty list when the record is done.
    """
    if not path.is_file():
        return ["record.json is not there yet. Type your values in cell 2 and run it."]
    record = json.loads(path.read_text(encoding="utf-8"))
    return (question_left(record.get("question", ""))
            + fields_left(record.get("fields", {}))
            + target_left(record.get("target", "")))


def main() -> None:
    """Print Done: when the record is complete, else Not yet: and each thing left.

    A path given on the command line is checked instead of record.json; the answer's commands.sh uses it.
    """
    left = check(Path(sys.argv[1])) if len(sys.argv) > 1 and sys.argv[1].endswith(".json") else check()
    if left:
        print("Not yet:")
        for line in left:
            print("-", line)
    else:
        print("Done: your question names its unit, target and time; each field has its kind, verdict and reason; "
              "your target line names what you considered.")


if __name__ == "__main__":
    main()
