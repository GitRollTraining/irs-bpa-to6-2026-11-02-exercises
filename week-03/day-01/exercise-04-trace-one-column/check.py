"""The done check for exercise 4. In Databricks, cell 3 of the notebook runs it with the values of
cells 1 and 2. It compares them with how the setup notebook built course.returns.return_summary
(week-03/setup/day-01-course-data.py): it reads no lineage itself, so it gives the same answer
whether or not the lineage system tables are open to you. Without Databricks, from the course folder:

    python3 week-03/day-01/exercise-04-trace-one-column/check.py <values.json>
    python3 week-03/day-01/exercise-04-trace-one-column/check.py --start
"""
import json
import sys
from pathlib import Path

# non_wage_income is total_income - wages_amt in one SQL query, so lineage sees both sources.
# income_band comes from a Python function the query calls; what the graph shows for it is recorded,
# not judged: "Use of user-defined functions (UDFs) can obscure the mapping".
SOURCES = {"return_header.total_income", "return_header.wages_amt"}
START = {"non_wage_income_sources": [], "non_wage_income_stops_at": "", "predict": "", "income_band_trace": ""}


def short(name: str) -> str:
    """Keep the last two parts of a column's name, table.column, in lower case."""
    return ".".join(name.replace("`", "").strip().lower().split(".")[-2:])


def left(values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: non_wage_income_sources, non_wage_income_stops_at, predict and income_band_trace,
            as cells 1 and 2 hold them.
    """
    out = []
    given = {short(s) for s in values.get("non_wage_income_sources") or [] if s.strip()}
    given.discard("return_header.return_id")
    if not given:
        out.append("Cell 1 lists no source column yet. Write each column the graph highlights for non_wage_income. Step 1.")
    else:
        if SOURCES - given:
            out.append("non_wage_income_sources lacks a column the graph highlights in return_header. Step 1.")
        for extra in sorted(given - SOURCES):
            out.append(f'"{extra}" is not a source of non_wage_income. Keep only the columns the graph highlights, as table.column. Step 1.')
    stops = (values.get("non_wage_income_stops_at") or "").lower()
    if len(stops.split()) < 4 or "return_header" not in stops:
        out.append("non_wage_income_stops_at: write the table at the left end of the trace and what the graph shows to its left, in 4 words or more. Step 1.")
    if len((values.get("predict") or "").split()) < 5:
        out.append("Cell 2's predict has fewer than 5 words. Write yes or no and the reason, before you select income_band. Step 2.")
    if len((values.get("income_band_trace") or "").split()) < 4:
        out.append("income_band_trace: write what the graph shows for income_band, in 4 words or more. Step 2.")
    return out


def report(values: dict) -> str:
    """Return what cell 3 prints: Done, or Not yet with each thing left."""
    out = left(values)
    if not out:
        return ("Done: non_wage_income traces to return_header.total_income and return_header.wages_amt, "
                "and stops at return_header; your income_band trace is recorded beside your prediction.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(values: dict) -> str:
    """Return what cell 3 prints. The notebook passes the values of cells 1 and 2."""
    return report(values)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
