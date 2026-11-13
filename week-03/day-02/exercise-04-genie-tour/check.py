"""The done check for exercise 4. In Databricks, cell 2 of the notebook runs it with what you recorded
in cell 1, and runs the query you copied from Genie again, with spark, to see that it is the whole
query. Without Databricks, from the course folder:

    python3 week-03/day-02/exercise-04-genie-tour/check.py <values.json>
    python3 week-03/day-02/exercise-04-genie-tour/check.py --start

runs the query on the setup's made-up rows (week-03/setup/day-02-course-data.py) in SQLite. It
never judges Genie's answer: exercise 5 does that.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
QUESTION = "How many returns are in the clean batch for each filing status?"
START = {"answer": "", "result_table": "", "query": "", "table_read": "", "second": "", "what_changed": ""}


def left(values: dict, runs: bool) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: what cell 1 holds.
        runs: True when the copied query ran.
    """
    out = []
    if len((values.get("answer") or "").split()) < 3:
        out.append("In answer, copy Genie's short answer. Step 2.")
    if not any(ch.isdigit() for ch in values.get("result_table") or ""):
        out.append("In result_table, copy the rows of Genie's result table. Step 2.")
    query = (values.get("query") or "").strip()
    if not query.upper().startswith(("SELECT", "WITH")):
        out.append("In query, paste the whole query from Show code: it starts with SELECT or WITH. Step 3.")
    elif not runs:
        out.append("The query you pasted does not run. Copy it again from Show code, all of it. Step 3.")
    elif "course.returns." not in query.replace("`", ""):
        out.append("The query names no table of course.returns. Copy the whole query from Show code. Step 3.")
    table = (values.get("table_read") or "").strip()
    if not table or table not in query.replace("`", ""):
        out.append("In table_read, write the table the query reads, as its FROM line names it. Step 3.")
    second = (values.get("second") or "").strip().lower()
    if second not in ("same", "changed"):
        out.append("Ask the question again. In second, write same or changed. Step 4.")
    elif second == "changed" and len((values.get("what_changed") or "").split()) < 4:
        out.append("In what_changed, write what changed: the answer, the table or the query. Step 4.")
    return out


def report(values: dict, runs: bool) -> str:
    """Return what cell 2 prints: Done, or Not yet with each thing left."""
    out = left(values, runs)
    if not out:
        return f"Done: Genie read {values['table_read'].strip()}; the second answer was {values['second'].strip().lower()}."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def safe(query: str) -> bool:
    """True for one query that only reads: it starts with SELECT or WITH and holds no second statement."""
    q = query.strip().rstrip(";")
    return q.upper().startswith(("SELECT", "WITH")) and ";" not in q


def in_notebook(spark: object, values: dict) -> str:
    """Run the copied query with spark, then return what cell 2 prints."""
    query = values.get("query") or ""
    runs = False
    if safe(query):
        try:
            spark.sql(query.strip().rstrip(";")).collect()
            runs = True
        except Exception:  # a query cut short, or changed by hand
            runs = False
    return report(values, runs)


def local_runs(query: str) -> bool:
    """Run the copied query on the made-up rows in SQLite."""
    if not safe(query):
        return False
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-02-course-data.py").read_text(encoding="utf-8"), data)
    try:
        data["local_db"]().execute(data["local_sql"](query.strip().rstrip(";").replace("`", ""))).fetchall()
        return True
    except Exception:  # a query cut short, or changed by hand
        return False


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given, local_runs(given.get("query") or "")))
