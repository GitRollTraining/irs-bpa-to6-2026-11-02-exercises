"""The done check for exercise 4. In Databricks, cell 3 of the notebook runs it with the values of
cells 1 and 2. It compares them with how the setup notebook built case_features
(week-03/day-01/setup/course_data.py): it reads no lineage itself, so it gives the same answer
whether or not the lineage system tables are open to you. Without Databricks, from the course folder:

    python3 week-03/day-01/exercise-04-trace-one-column/check.py <values.json>
    python3 week-03/day-01/exercise-04-trace-one-column/check.py --start
"""
import json
import sys
from pathlib import Path

# How the setup notebook built the two columns. income_gap: one SQL query, so lineage sees both
# sources. income_band: computed in Python, then written to income_bands; no query links it to returns.
INCOME_GAP_SOURCES = {"returns.wages", "third_party_reports.wages_reported"}
SOURCE_TABLES = {"returns", "third_party_reports"}
BAND_STOPS_AT = "income_bands"
START = {"CATALOG": "workspace", "income_gap_sources": [], "income_gap_stops_at": "", "predict": "",
         "income_band_stops_at": ""}


def short(name: str) -> str:
    """Keep the last two parts of a column's name, table.column, in lower case."""
    return ".".join(name.replace("`", "").strip().lower().split(".")[-2:])


def left(values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: income_gap_sources, income_gap_stops_at, predict and income_band_stops_at, as cells 1 and 2 hold them.
    """
    out = []
    given = {short(s) for s in values.get("income_gap_sources") or [] if s.strip()}
    given.discard("returns.return_id")
    given.discard("third_party_reports.return_id")
    if not given:
        out.append("Cell 1 lists no source column yet. Select income_gap in the lineage graph. Step 1.")
    else:
        for missing in sorted(INCOME_GAP_SOURCES - given):
            out.append(f"income_gap_sources lacks a column the graph highlights, in the table {missing.split('.')[0]}. Step 1.")
        for extra in sorted(given - INCOME_GAP_SOURCES):
            out.append(f'"{extra}" is not a source of income_gap. Write each highlighted column as table.column. Step 1.')
    stops = (values.get("income_gap_stops_at") or "").lower()
    if len(stops.split()) < 4 or not all(t in stops for t in SOURCE_TABLES):
        out.append("income_gap_stops_at: name the tables where the trace stops, and why, in 4 words or more. Step 1.")
    if len((values.get("predict") or "").split()) < 5:
        out.append("Cell 2's predict has fewer than 5 words. Write it before you select income_band. Step 2.")
    band = (values.get("income_band_stops_at") or "").lower()
    if BAND_STOPS_AT not in band:
        out.append("income_band_stops_at: name the table where the income_band trace stops, as the graph shows it. Step 2.")
    return out


def report(values: dict) -> str:
    """Return what cell 3 prints: Done, or Not yet with each thing left."""
    out = left(values)
    if not out:
        return ("Done: income_gap traces to returns.wages and third_party_reports.wages_reported, and "
                "stops at those two tables; income_band stops at income_bands.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(values: dict) -> str:
    """Return what cell 3 prints. The notebook passes the values of cells 1 and 2."""
    return report(values)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
