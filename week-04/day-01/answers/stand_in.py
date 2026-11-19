"""Run one of Monday's exercise notebooks with no Databricks, against a stand-in for Spark.

    uv run --no-project --python 3.12 --with duckdb==1.4.3 --with pandas==3.1.1 python week-04/day-01/answers/stand_in.py exercise-02-baseline-accuracy

Run it from the course folder. It loads the week's five tables into DuckDB, an in-process SQL
database, under the same names as in Databricks (course.returns.model_returns and the rest, from
week-04/setup/day-01-course-data.py), and gives each notebook a `spark` with the calls Monday's
cells use: spark.sql, spark.table, spark.createDataFrame and the table writer. Then it runs every
code cell of the exercise's starting notebook (its check prints Not yet), and of the answer's
notebook (its check prints Done:). Nothing is sent to a model or to Databricks. DuckDB reads the
cells' SQL as Databricks does for the statements Monday uses; the run in Databricks is still a
trainer gap.
"""
import contextlib
import io
import json
import os
import sys
from pathlib import Path

import duckdb
import pandas as pd

DAY = Path(__file__).resolve().parents[1]
COURSE = DAY.parents[1]
SETUP = COURSE / "week-04" / "setup" / "day-01-course-data.py"


class Row(dict):
    """One row of a result, read by name as row["n"] or row.n, as a Spark Row is."""

    def __getattr__(self, name: str) -> object:
        try:
            return self[name]
        except KeyError as missing:
            raise AttributeError(name) from missing


class Frame:
    """The part of a Spark DataFrame that Monday's cells use, over a pandas table."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    @property
    def columns(self) -> list[str]:
        return list(self.data.columns)

    def count(self) -> int:
        return len(self.data)

    def collect(self) -> list[Row]:
        clean = self.data.astype(object).where(self.data.notna(), None)
        return [Row(r) for r in clean.to_dict("records")]

    def first(self) -> Row | None:
        rows = self.collect()
        return rows[0] if rows else None

    def show(self, n: int = 20, truncate: bool = True) -> None:
        print(self.data.head(n).astype(object).where(self.data.notna(), "NULL").to_string(index=False))

    @property
    def write(self) -> "Writer":
        return Writer(self)


class Writer:
    """frame.write.mode(...).option(...).saveAsTable(name), as Databricks writes a table."""

    def __init__(self, frame: Frame) -> None:
        self.frame = frame

    def mode(self, _: str) -> "Writer":
        return self

    def option(self, *_: object) -> "Writer":
        return self

    def saveAsTable(self, name: str) -> None:
        data = self.frame.data
        STAND_IN.db.register("_written", data)
        STAND_IN.db.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM _written")
        STAND_IN.db.unregister("_written")


class Catalog:
    """spark.catalog.tableExists(name)."""

    def tableExists(self, name: str) -> bool:
        catalog, schema, table = name.split(".")
        found = STAND_IN.db.execute(
            "SELECT COUNT(*) FROM information_schema.tables WHERE table_catalog = ? AND table_schema = ? AND table_name = ?",
            [catalog, schema, table]).fetchone()[0]
        return found > 0


class Spark:
    """The stand-in session: Databricks' three-part names over one DuckDB database per catalog."""

    def __init__(self) -> None:
        self.db = duckdb.connect()
        self.catalog = Catalog()

    def sql(self, statement: str) -> Frame:
        result = self.db.execute(statement)
        return Frame(result.df() if result.description else pd.DataFrame())

    def table(self, name: str) -> Frame:
        return self.sql(f"SELECT * FROM {name}")

    def createDataFrame(self, rows: list, schema: str) -> Frame:
        names = [part.split()[0] for part in schema.split(",")]
        return Frame(pd.DataFrame([list(r) for r in rows], columns=names, dtype=object))


STAND_IN = Spark()


def load_tables() -> None:
    """Load the five week 4 tables, and one learner's schema, course.learner_00."""
    course = {"__name__": "course_data"}
    exec(SETUP.read_text(encoding="utf-8"), course)
    db = STAND_IN.db
    db.execute("ATTACH ':memory:' AS course")
    db.execute("CREATE SCHEMA course.returns")
    db.execute("CREATE SCHEMA course.learner_00")
    tables = {"model_returns": (course["RETURN_COLUMNS"], course["returns"]()),
              "model_features": (course["FEATURE_COLUMNS"], course["feature_rows"]())}
    tables.update({name: (course["FEATURE_COLUMNS"], course["set_rows"](name)) for name in course["SETS"]})
    kinds = {"INT": "Int64", "STRING": "object", "DOUBLE": "float64"}
    for name, (columns, rows) in tables.items():
        data = pd.DataFrame([[r[c] for c, _, _ in columns] for r in rows], columns=[c for c, _, _ in columns])
        data = data.astype({c: kinds[k] for c, k, _ in columns})
        db.register("_rows", data)
        db.execute(f"CREATE TABLE course.returns.{name} AS SELECT * FROM _rows")
        db.unregister("_rows")


def run(notebook: Path) -> str:
    """Run every code cell of one notebook in order, in its own folder, and return what it printed."""
    cells = ["".join(c["source"]) for c in json.loads(notebook.read_text(encoding="utf-8"))["cells"]
             if c["cell_type"] == "code"]
    names = {"spark": STAND_IN, "__name__": "__main__"}
    here = os.getcwd()
    out = io.StringIO()
    os.chdir(notebook.parent)
    try:
        with contextlib.redirect_stdout(out):
            for cell in cells:
                exec(compile(cell, str(notebook), "exec"), names)
    finally:
        os.chdir(here)
    return out.getvalue()


if __name__ == "__main__":
    exercise = sys.argv[1]
    load_tables()
    for label, path in (("start", DAY / exercise / "exercise.ipynb"), ("answer", DAY / "answers" / exercise / "exercise.ipynb")):
        printed = run(path)
        print(f"== {label}: {path.relative_to(COURSE)}")
        print(printed.rstrip())
