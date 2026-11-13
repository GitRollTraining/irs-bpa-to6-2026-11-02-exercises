"""The done check for exercise 2. In Databricks, cell 4 of the notebook runs it with the record of
cell 2 and the explanation of cell 3, reads the batch's columns with spark, and builds the prepared
data again from the record, as cell 3 does. Without Databricks, from the course folder:

    python3 week-03/day-02/exercise-02-field-record-and-case-key/check.py <values.json>
    python3 week-03/day-02/exercise-02-field-record-and-case-key/check.py --start

takes the batch's columns from the setup, week-03/setup/day-02-course-data.py. It checks the
record and what the prepared data holds, never the wording of a reason.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
CLASSES = ("sensitive but unclassified", "personally identifiable", "neither")
ACTIONS = ("keep", "remove", "transform")
MONDAY = ("needed", "not needed", "transformed", "not listed")
TRANSFORMS = {"tin": "filer_key", "zip_code": "zip3"}
NAMES_A_PERSON = ("tin", "taxpayer_name", "street_address", "loaded_by")
FILLED = {
    "tin": {"field": "tin", "monday": "transformed", "needed": "no", "class": "sensitive but unclassified",
            "action": "transform",
            "reason": "FTI. The model needs no number, but Wednesday matches a filer's returns, so a case key replaces it."},
    "filing_status": {"field": "filing_status", "monday": "not listed", "needed": "yes", "class": "sensitive but unclassified",
                      "action": "keep", "reason": "FTI from the return. The use needs it to compare like returns."},
}
FIELDS = ["return_id", "tin", "taxpayer_name", "street_address", "zip_code", "filing_status", "wages_amt",
          "agi_amt", "total_income", "total_tax_amt", "tax_year", "received_date", "loaded_by", "batch_id"]
START = {"record": [dict(FILLED[f]) if f in FILLED else
                    {"field": f, "monday": "", "needed": "", "class": "", "action": "", "reason": ""} for f in FIELDS],
         "explain": ""}


def prepared_columns(columns: list[str], record: list[dict]) -> list[str]:
    """The columns the prepared data has after cell 3: removed fields dropped, transformed ones replaced.

    Args:
        columns: the batch's columns.
        record: the field record, as cell 2 holds it.

    Returns:
        The prepared data's columns, in order.
    """
    act = {(r.get("field") or "").strip(): (r.get("action") or "").strip().lower() for r in record}
    out = [c for c in columns if act.get(c) not in ("remove", "transform")]
    return out + [TRANSFORMS[c] for c in columns if act.get(c) == "transform" and c in TRANSFORMS]


def row_left(row: dict) -> list[str]:
    """What is left in one row of the record."""
    field = (row.get("field") or "").strip()
    out = []
    if (row.get("monday") or "").strip().lower() not in MONDAY:
        out.append(f"{field}: write Monday's verdict (needed, not needed, transformed) or not listed. Step 2.")
    if (row.get("needed") or "").strip().lower() not in ("yes", "no"):
        out.append(f"{field}: does the use need it? Write yes or no. Step 2.")
    klass = (row.get("class") or "").strip().lower()
    if klass not in CLASSES:
        out.append(f"{field}: its class is sensitive but unclassified, personally identifiable, or neither. Step 2.")
    elif field in NAMES_A_PERSON and klass == "neither":
        out.append(f"{field}: it names a person. Read the guide's class rows again. Step 2.")
    action = (row.get("action") or "").strip().lower()
    if action not in ACTIONS:
        out.append(f"{field}: its action is keep, remove or transform. Step 2.")
    elif action == "transform" and field not in TRANSFORMS:
        out.append(f"{field}: cell 3 has no transform for it. Choose keep or remove. Step 2.")
    elif action == "keep" and (row.get("needed") or "").strip().lower() == "no":
        out.append(f"{field}: the use does not need it, so it does not stay as it is. Step 2.")
    elif action == "keep" and field in NAMES_A_PERSON:
        out.append(f"{field}: it names a person, so it does not stay as it is. Read the guide again. Step 2.")
    if len((row.get("reason") or "").split()) < 4:
        out.append(f"{field}: give the reason, 4 words or more. Step 2.")
    return out


def left(values: dict, columns: list[str]) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: the record and the explanation, as cells 2 and 3 hold them.
        columns: the batch's columns.
    """
    record = values.get("record") or []
    fields = [(r.get("field") or "").strip() for r in record]
    out = [f"The record has no row for {c}. Add one. Step 2." for c in columns if c not in fields]
    for row in record:
        problems = row_left(row)
        if len(problems) >= 4:
            out.append(f"{(row.get('field') or '').strip()}: its row is not filled yet. Step 2.")
        elif problems:
            out.append(" ".join(problems))
    act = {(r.get("field") or "").strip(): (r.get("action") or "").strip().lower() for r in record}
    gone = {c for c in columns if act.get(c) in ("remove", "transform")}
    kept = prepared_columns(columns, record)
    if gone & set(kept):
        out.append("A removed field is still in the prepared data. Run cell 3 again. Step 3.")
    if act.get("tin") == "transform" and "filer_key" not in kept:
        out.append("The prepared data has no filer_key. Run cell 3 again. Step 3.")
    if len((values.get("explain") or "").split()) < 8:
        out.append("In explain, write why the case key can stay when the number goes, in 8 words or more. Step 3.")
    return out


def report(values: dict, columns: list[str]) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(values, columns)
    if not out:
        kept = prepared_columns(columns, values["record"])
        return f"Done: {len(values['record'])} fields recorded; the prepared data has {len(kept)} columns: {', '.join(kept)}."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Read the batch's columns with spark, then return what cell 4 prints."""
    return report(values, spark.table("course.returns.batch_dirty").columns)


def course_columns() -> list[str]:
    """The batch's columns, from the setup."""
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-02-course-data.py").read_text(encoding="utf-8"), data)
    return data["NAMES"]


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given, course_columns()))
