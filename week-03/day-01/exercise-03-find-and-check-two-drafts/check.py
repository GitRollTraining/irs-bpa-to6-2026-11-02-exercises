"""The done check for exercise 3. In Databricks, cell 4 of the notebook runs it with the entries of
cell 3 and reads each column's type, empty count, smallest and largest value again with spark.
Without Databricks, from the course folder:

    python3 week-03/day-01/exercise-03-find-and-check-two-drafts/check.py <values.json>
    python3 week-03/day-01/exercise-03-find-and-check-two-drafts/check.py --start

takes each column's facts from the setup's made-up rows, week-03/setup/day-01-course-data.py.
It checks the record, never the draft's wording, and calls no model.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
EMPTY_ENTRY = {"column": "", "draft": "", "type": "", "comment_and_tags": "", "empty": None,
               "smallest": None, "largest": None, "verdict": "", "reason": ""}
START = {"predict": "", "entries": [dict(EMPTY_ENTRY), dict(EMPTY_ENTRY)]}
SAYS_POSITIVE = re.compile(r"\b(always positive|never negative|positive|non-negative|nonnegative)\b", re.IGNORECASE)
SAYS_PRESENT = re.compile(r"\b(never empty|always present|always filled|not null|never null|required)\b", re.IGNORECASE)


def same(recorded: object, actual: object) -> bool:
    """Compare a value the learner typed with the column's value; numbers typed as text count."""
    if actual is None:
        return recorded in (None, "", "None", "null", "NULL")
    typed = str(recorded).strip().replace(",", "").lower()
    try:
        return float(typed) == float(actual)
    except (TypeError, ValueError):
        return typed == str(actual).strip().lower()


def entry_left(n: int, entry: dict, facts: dict | None) -> list[str]:
    """What is left in one entry.

    Args:
        n: the entry's number, 1 or 2.
        entry: the entry as cell 3 holds it.
        facts: the column's type, empty count, smallest and largest value; None when the column is not found.

    Returns:
        One line per problem.
    """
    column = (entry.get("column") or "").strip()
    if not column:
        return [f"Entry {n} names no column yet. Write table.column, as cell 1 shows it. Step 2."]
    if facts is None or not column.startswith("return_header."):
        return [f'Entry {n}: "{column}" is not a column of return_header. Write return_header.<column>, as cell 1 shows it. Step 2.']
    out = []
    if len((entry.get("draft") or "").split()) < 3:
        out.append(f"Entry {n} ({column}): copy the draft, word for word. Step 2.")
    if not same((entry.get("type") or "").lower(), facts["type"].lower()):
        out.append(f"Entry {n} ({column}): the type is not the one the catalog shows. Run cell 2 on it. Step 3.")
    if not (entry.get("comment_and_tags") or "").strip():
        out.append(f'Entry {n} ({column}): write the comment and tags cell 2 shows, such as "comment: none; tags: none". Step 3.')
    for key, fact in [("empty", "empty"), ("smallest", "min"), ("largest", "max")]:
        if not same(entry.get(key), facts[fact]):
            out.append(f"Entry {n} ({column}): {key} is not what cell 2 shows. Step 3.")
    verdict = (entry.get("verdict") or "").strip().lower()
    draft = entry.get("draft") or ""
    must_change = ((SAYS_POSITIVE.search(draft) and facts["min"] is not None and facts["min"] < 0)
                   or (SAYS_PRESENT.search(draft) and facts["empty"] > 0))
    if verdict not in ("keep", "change"):
        out.append(f"Entry {n} ({column}): write the verdict keep or change. Step 4.")
    elif must_change and verdict == "keep":
        out.append(f"Entry {n} ({column}): a value in cell 2 contradicts the draft. Read the first row of the verdict table in Step 4.")
    if len((entry.get("reason") or "").split()) < 4:
        out.append(f"Entry {n} ({column}): give the reason, 4 words or more: what in the facts decides it. Step 4.")
    return out


def left(values: dict, facts: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: predict and entries, as cells 2 and 3 hold them.
        facts: for each "table.column" of course.returns, its type, empty, min and max.
    """
    out = []
    if len((values.get("predict") or "").split()) < 5:
        out.append("Cell 2's predict has fewer than 5 words. Write it before you run cell 2. Step 3.")
    entries = values.get("entries") or []
    columns = [(e.get("column") or "").strip() for e in entries]
    if len(entries) < 2:
        out.append("Cell 3 needs two entries. Step 4.")
    elif columns[0] and columns[0] == columns[1]:
        out.append("Both entries name the same column. Check two columns. Step 4.")
    for n, entry in enumerate(entries[:2], 1):
        out += entry_left(n, entry, facts.get((entry.get("column") or "").strip()))
    return out


def report(values: dict, facts: dict) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(values, facts)
    if not out:
        said = ", ".join(f"{e['column']} ({e['verdict'].strip().lower()})" for e in values["entries"][:2])
        return f"Done: 2 entries, each with its check: {said}."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Read each entry's column from the catalog with spark, then return what cell 4 prints."""
    facts = {}
    for entry in values.get("entries") or []:
        column = (entry.get("column") or "").strip()
        if column.count(".") != 1:
            continue
        table, name = column.split(".")
        found = spark.sql(
            "SELECT data_type FROM course.information_schema.columns WHERE table_schema = 'returns' "
            f"AND table_name = '{table}' AND column_name = '{name}'").collect()
        if not found:
            continue
        row = spark.sql(f"SELECT count_if({name} IS NULL) AS empty, min({name}) AS low, max({name}) AS high "
                        f"FROM course.returns.{table}").first()
        facts[column] = {"type": found[0]["data_type"], "empty": row["empty"], "min": row["low"], "max": row["high"]}
    return report(values, facts)


def course_facts() -> dict:
    """Each column's facts, from the setup's made-up rows."""
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-01-course-data.py").read_text(encoding="utf-8"), data)
    return data["column_facts"]()


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given, course_facts()))
