"""The done check for exercise 1. In Databricks, cell 4 of the notebook runs it with the values of
cells 1 to 3 and counts the table's rows again with spark. Without Databricks, from the course folder:

    python3 week-03/day-01/exercise-01-tour-the-workspace/check.py <values.json>
    python3 week-03/day-01/exercise-01-tour-the-workspace/check.py --start

reads the values from a JSON file (or the notebook's starting values) and takes the table's row count
from the setup's made-up rows, week-03/setup/day-01-course-data.py. No model is called.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
TABLE = "course.returns.return_header"
START = {"full_name": "", "notebook_count": None, "sql_editor_count": None, "explain": ""}


def plain(name: str) -> str:
    """Write a full name without backticks or spaces, in lower case."""
    return name.replace("`", "").strip().lower()


def left(values: dict, true_count: int) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: full_name, notebook_count, sql_editor_count and explain, as the cells hold them.
        true_count: the number of rows the table holds.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    name = plain(values["full_name"] or "")
    if not name:
        out.append("Cell 1 has no full name yet. Copy it from Catalog Explorer. Step 1.")
    elif name.count(".") != 2:
        out.append(f'"{values["full_name"]}" is not a full name: it needs three parts, catalog.schema.table. Step 1.')
    elif name != TABLE:
        out.append(f'"{values["full_name"]}" is not the return table. Open the catalog course, the schema returns, then return_header. Step 1.')
    if values["notebook_count"] != true_count:
        out.append("Cell 2 has not counted the return table yet. Run cell 2, on the compute of step 2. Step 2.")
    sql = values["sql_editor_count"]
    if sql is None:
        out.append("Cell 3 has no SQL editor count yet. Type the number the SQL editor showed. Step 3.")
    elif isinstance(sql, str):
        out.append(f'The SQL editor count, "{sql}", is text in quotes. Type the digits only, with no quotes. Step 3.')
    elif sql != true_count:
        out.append(f"The SQL editor count, {sql}, is not the table's count. Run the query on the full name of step 1. Step 3.")
    if len((values["explain"] or "").split()) < 8:
        out.append("Cell 3's explain has fewer than 8 words. Write 8 words or more on why the counts match or differ. Step 3.")
    return out


def report(values: dict, true_count: int) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(values, true_count)
    if not out:
        return f"Done: {plain(values['full_name'])} has {true_count} rows, in the notebook and in the SQL editor."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Count the return table's rows with spark, then return what cell 4 prints."""
    true_count = spark.sql(f"SELECT COUNT(*) AS row_count FROM {TABLE}").first()["row_count"]
    return report(values, true_count)


def course_count() -> int:
    """The return table's row count, from the setup's made-up rows."""
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-01-course-data.py").read_text(encoding="utf-8"), data)
    return data["column_facts"]()["return_header.return_id"]["rows"]


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given, course_count()))
