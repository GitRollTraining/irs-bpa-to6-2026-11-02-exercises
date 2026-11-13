"""The done check for exercise 5. In Databricks, cell 4 of the notebook runs it with what you recorded
in cells 1 and 3, runs Genie's query and your own query again with spark, and compares their
numbers. Without Databricks, from the course folder:

    python3 week-03/day-02/exercise-05-check-one-genie-answer/check.py <values.json>
    python3 week-03/day-02/exercise-05-check-one-genie-answer/check.py --start

runs both queries on the setup's made-up rows (week-03/setup/day-02-course-data.py) in SQLite.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
START = {"question": "", "genie_answer": "", "genie_query": "", "reads": "", "filters": "", "counts": "",
         "column": "wages_amt", "verdict": "", "deciding_line": ""}


def own_query(column: str) -> str:
    """Your own query for the question: per tax year of the clean batch, the returns and the column's total."""
    return (f"SELECT tax_year, count(DISTINCT return_id) AS returns, sum({column}) AS total "
            "FROM course.returns.batch_clean GROUP BY tax_year ORDER BY tax_year")


def safe(query: str) -> bool:
    """True for one query that only reads: it starts with SELECT or WITH and holds no second statement."""
    q = query.strip().rstrip(";")
    return q.upper().startswith(("SELECT", "WITH")) and ";" not in q


def numbers(rows: list) -> set:
    """Every number in a result, rounded to cents, so two results can be compared whatever their column names."""
    out = set()
    for row in rows:
        for value in row:
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                out.add(round(float(value), 2))
            elif value is not None and hasattr(value, "__float__"):  # a decimal from spark
                out.add(round(float(value), 2))
    return out


def left(values: dict, genie: list | None, own: list | None) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: what cells 1 and 3 hold.
        genie: the rows of Genie's query, or None when it does not run.
        own: the rows of your own query, or None when it does not run.
    """
    out = []
    column = (values.get("column") or "").strip()
    question = values.get("question") or ""
    if len(question.split()) < 6 or column not in question:
        out.append("In question, write the question you asked Genie, naming the column you set in cell 2. Step 1.")
    if len((values.get("genie_answer") or "").split()) < 3:
        out.append("In genie_answer, copy Genie's short answer. Step 1.")
    query = (values.get("genie_query") or "").strip()
    if genie is None:
        out.append("Genie's query does not run here. Paste the whole query from Show code. Step 1.")
    if own is None:
        out.append("Your own query does not run. In cell 2, set column to a column of the batch. Step 2.")
    flat = " ".join(query.replace("`", "").split())
    reads = (values.get("reads") or "").strip()
    if not reads or reads not in flat:
        out.append("In reads, write the table Genie's query reads, as its FROM line names it. Step 3.")
    if len((values.get("filters") or "").split()) < 1:
        out.append("In filters, copy the query's WHERE condition, or write none. Step 3.")
    if (values.get("counts") or "").strip().lower() not in ("returns", "rows"):
        out.append("In counts, write returns or rows: what the query's count counts. Step 3.")
    verdict = (values.get("verdict") or "").strip().lower()
    if verdict not in ("holds", "does not hold"):
        out.append("In verdict, write holds or does not hold. Step 4.")
    elif genie is not None and own is not None:
        same = numbers(genie) == numbers(own)
        if same and verdict != "holds":
            out.append("Genie's numbers and yours are the same. Read the two results again. Step 4.")
        if not same and verdict != "does not hold":
            out.append("Genie's numbers and yours differ. Read the two results again. Step 4.")
    line = " ".join((values.get("deciding_line") or "").replace("`", "").split())
    if len(line.split()) < 2 or line not in flat:
        out.append("In deciding_line, copy the one line of Genie's query that decides it, as it is. Step 4.")
    return out


def report(values: dict, genie: list | None, own: list | None) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(values, genie, own)
    if not out:
        return f"Done: Genie's answer {values['verdict'].strip().lower()}; the deciding line: {values['deciding_line'].strip()}"
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Run both queries with spark, then return what cell 4 prints."""
    def run(query: str) -> list | None:
        if not safe(query):
            return None
        try:
            return [tuple(r) for r in spark.sql(query.strip().rstrip(";")).collect()]
        except Exception:  # a query cut short, or a column the batch does not have
            return None
    return report(values, run(values.get("genie_query") or ""), run(own_query((values.get("column") or "").strip())))


def local_rows(values: dict) -> tuple:
    """Run both queries on the made-up rows in SQLite."""
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-02-course-data.py").read_text(encoding="utf-8"), data)
    db = data["local_db"]()

    def run(query: str) -> list | None:
        if not safe(query):
            return None
        try:
            return db.execute(data["local_sql"](query.strip().rstrip(";").replace("`", ""))).fetchall()
        except Exception:  # a query cut short, or a column the batch does not have
            return None
    return run(values.get("genie_query") or ""), run(own_query((values.get("column") or "").strip()))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given, *local_rows(given)))
