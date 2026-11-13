"""The done check for exercise 3. In Databricks, cell 5 of the notebook runs it with what you recorded
in cells 1 and 4, and queries course.returns.batch_governed again as you, with spark. Without
Databricks, from the course folder:

    python3 week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/check.py <values.json>
    python3 week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/check.py <values.json> --plain
    python3 week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/check.py --start

reads the setup's made-up rows (week-03/setup/day-02-course-data.py) as the learners' group sees
them, or, with --plain, as a workspace with no mask and no filter shows them. It checks what you
recorded against what the table gives you, never the wording of a sentence.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
YEARS_IN_BATCH = {2019, 2021, 2022, 2023}
START = {"predict": "", "rows_per_year": {}, "identifier_seen": "", "grants": "", "why_differs": "", "fallback": ""}


def left(values: dict, seen: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: what cells 1 and 4 hold.
        seen: what the table gives you: "per_year" (year to row count) and "identifiers" (the values of tin).
    """
    out = []
    if len((values.get("predict") or "").split()) < 5:
        out.append("Write your prediction in cell 1, 5 words or more, before you run cell 2. Step 1.")
    typed = {str(k).strip(): v for k, v in (values.get("rows_per_year") or {}).items()}
    actual = {str(k): v for k, v in seen["per_year"].items()}
    if not typed:
        out.append("rows_per_year is empty. Copy each tax year and its row count from cell 2. Step 2.")
    elif set(typed) != set(actual) or any(str(typed[k]).strip() != str(actual[k]) for k in actual):
        out.append("rows_per_year is not what cell 2 shows you. Run cell 2 again and copy each year and count. Step 2.")
    if (values.get("identifier_seen") or "").strip() not in seen["identifiers"]:
        out.append("identifier_seen is not a value of tin that cell 2 shows you. Copy one, as it is. Step 2.")
    if "select" not in (values.get("grants") or "").lower() or len((values.get("grants") or "").split()) < 3:
        out.append("In grants, write who holds SELECT on the table, as cell 3 shows it. Step 3.")
    controlled = set(seen["per_year"]) != YEARS_IN_BATCH or not any(any(c.isdigit() for c in i) for i in seen["identifiers"])
    if controlled and len((values.get("why_differs") or "").split()) < 8:
        out.append("In why_differs, write why what you see differs from the trainer's demo, 8 words or more. Step 4.")
    if not controlled and len((values.get("fallback") or "").split()) < 10:
        out.append("You see every year and the full number: this table has no mask or filter for you. "
                   "In fallback, write which group could read the number, and why, 10 words or more. Step 4.")
    return out


def report(values: dict, seen: dict) -> str:
    """Return what cell 5 prints: Done, or Not yet with each thing left."""
    out = left(values, seen)
    if not out:
        years = ", ".join(f"{k}: {v}" for k, v in sorted(seen["per_year"].items()))
        return f"Done: you see {years}; the identifier as {values['identifier_seen'].strip()}."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Query the governed batch as you, then return what cell 5 prints."""
    table = "course.returns.batch_governed"
    per_year = {r["tax_year"]: r["n"] for r in spark.sql(f"SELECT tax_year, count(*) AS n FROM {table} GROUP BY tax_year").collect()}
    identifiers = {r["tin"] for r in spark.sql(f"SELECT DISTINCT tin FROM {table}").collect()}
    return report(values, {"per_year": per_year, "identifiers": identifiers})


def local_seen(view: str) -> dict:
    """What the made-up rows give a learner: "learner" with the mask and the filter, "plain" without."""
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-02-course-data.py").read_text(encoding="utf-8"), data)
    db = data["local_db"](view)
    per_year = dict(db.execute("SELECT tax_year, count(*) FROM batch_governed GROUP BY tax_year").fetchall())
    identifiers = {r[0] for r in db.execute("SELECT DISTINCT tin FROM batch_governed").fetchall()}
    return {"per_year": per_year, "identifiers": identifiers}


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--plain"]
    given = START if args == ["--start"] else json.loads(Path(args[0]).read_text(encoding="utf-8"))
    print(report(given, local_seen("plain" if "--plain" in sys.argv else "learner")))
