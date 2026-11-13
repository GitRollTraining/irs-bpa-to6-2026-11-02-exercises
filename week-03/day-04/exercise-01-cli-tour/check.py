"""The done check for exercise 1, the Databricks CLI tour.

Run it in this folder on the Workstation:

    python3 check.py              reads notes.md beside it
    python3 check.py <notes file> reads another notes file (the answer's, for the course team)

It reads what the learner wrote in notes.md and compares the two columns with the made-up rows of
Monday's setup, week-03/setup/day-01-course-data.py. It never runs a databricks command and calls
no model.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEEDED_CATALOG = "course"
NEEDED_RETURNS_TABLES = ("return_header", "return_summary")
LOWEST_VERSION = (0, 205, 0)
SHOWN = 6  # the things left that one run prints, in the order of the steps


def read_notes(path: Path) -> dict[str, str]:
    """Read the "key: value" lines of a notes file.

    Args:
        path: the notes file.

    Returns:
        Each key with the text after its colon, stripped; an empty string when nothing is typed.
    """
    notes = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        found = re.match(r"^([a-z0-9_]+):(.*)$", line.strip())
        if found:
            notes[found.group(1)] = found.group(2).strip()
    return notes


def return_header_columns() -> dict[str, tuple[str, str | None]]:
    """Each column of course.returns.return_header: its type and its comment (None for no comment).

    Returns:
        The column name, with its SQL type and comment, from Monday's setup file.
    """
    data = {"__name__": "course_data"}
    setup = HERE.parents[1] / "setup" / "day-01-course-data.py"
    exec(setup.read_text(encoding="utf-8"), data)
    return {name: (kind, comment) for name, kind, comment in data["COLUMNS"]["return_header"]}


def words(text: str) -> list[str]:
    """Split a text into lowercase words, without punctuation."""
    return re.findall(r"[a-z0-9_]+", text.lower())


def is_none(text: str) -> bool:
    """Say whether the learner wrote that there is no comment."""
    return text.strip().strip("`\"'").lower() in ("none", "no comment", "null", "-")


def comment_fits(written: str, comment: str | None) -> bool:
    """Say whether the comment the learner wrote is the one the catalog holds.

    Args:
        written: what the learner wrote.
        comment: the catalog's comment, or None when the column has none.

    Returns:
        True when both say there is no comment, or the written text holds the comment's first five words.
    """
    if comment is None:
        return is_none(written)
    first = words(comment)[:5]
    return " ".join(first) in " ".join(words(written))


def version_left(notes: dict[str, str]) -> list[str]:
    """What is left in steps 1 and 2."""
    out = []
    found = re.search(r"(\d+)\.(\d+)\.(\d+)", notes.get("version", ""))
    if not found:
        out.append("version: write the version number that databricks -v prints. Step 1.")
    elif tuple(int(n) for n in found.groups()) < LOWEST_VERSION:
        out.append("version: it is below 0.205.0. Tell the trainer before you go on. Step 1.")
    if notes.get("version_exit") != "0":
        out.append("version_exit: write the number that echo $? prints after databricks -v. Step 1.")
    if "not found" not in notes.get("miss_message", "").lower():
        out.append("miss_message: copy the line that databrick -v prints. Step 2.")
    if not re.fullmatch(r"\d+", notes.get("miss_exit", "")) or notes.get("miss_exit") == "0":
        out.append("miss_exit: write the number that echo $? prints after databrick -v. Step 2.")
    return out


def sign_in_left(notes: dict[str, str]) -> list[str]:
    """What is left in steps 3 and 4."""
    out = []
    if not notes.get("profile"):
        out.append("profile: write the profile name you typed. Step 3.")
    if notes.get("login_exit") != "0":
        out.append("login_exit: the sign-in has no exit status 0 yet. Sign in again, or ask the trainer. Step 3.")
    if notes.get("profile_valid", "").upper() != "YES":
        out.append("profile_valid: databricks auth profiles must show your profile as valid. Step 3.")
    if len(words(notes.get("predicted_catalogs", ""))) < 3:
        out.append("predicted_catalogs: before you list them, write the catalogs you expect, and why. Step 4.")
    if NEEDED_CATALOG not in words(notes.get("listed_catalogs", "")):
        out.append("listed_catalogs: the course's catalog is not in it. Copy the whole list; "
                   "if it is not there, ask the trainer for the grant. Step 4.")
    if notes.get("catalogs_exit") != "0":
        out.append("catalogs_exit: write the number that echo $? prints after the catalog list. Step 4.")
    if len(words(notes.get("catalogs_match", ""))) < 5:
        out.append("catalogs_match: write one sentence, 5 words or more, on why the list matches your prediction or not. Step 4.")
    return out


def tables_left(notes: dict[str, str]) -> list[str]:
    """What is left in step 5."""
    out = []
    listed = words(notes.get("returns_tables", ""))
    if not all(name in listed for name in NEEDED_RETURNS_TABLES):
        out.append("returns_tables: write every table name that the list of course returns shows. Step 5.")
    if notes.get("returns_exit") != "0":
        out.append("returns_exit: write the number that echo $? prints after that list. Step 5.")
    if not re.fullmatch(r"course\.learner_\d+", notes.get("my_schema", "").strip("`")):
        out.append("my_schema: write your schema as course.learner_ and your number. Step 5.")
    if not notes.get("my_tables"):
        out.append("my_tables: write the table names your schema shows, or none. Step 5.")
    if notes.get("my_tables_exit") != "0":
        out.append("my_tables_exit: write the number that echo $? prints after the list of your schema. Step 5.")
    return out


def columns_left(notes: dict[str, str], columns: dict[str, tuple[str, str | None]]) -> list[str]:
    """What is left in step 6."""
    out = []
    if notes.get("get_exit") != "0":
        out.append("get_exit: write the number that echo $? prints after databricks tables get. Step 6.")
    second = notes.get("column_2", "").strip("`").removeprefix("return_header.")
    for n, name in ((1, "total_income"), (2, second)):
        if n == 2 and (name not in columns or name == "total_income"):
            out.append("column_2: write the other column of return_header that you checked on Monday. Step 6.")
            continue
        kind, comment = columns[name]
        if notes.get(f"column_{n}_type", "").strip("`").upper() != kind:
            out.append(f"column_{n}_type: it is not the type_name that tables get prints for {name}. Step 6.")
        if not comment_fits(notes.get(f"column_{n}_comment", ""), comment):
            out.append(f"column_{n}_comment: it is not the comment that tables get prints for {name} "
                       "(write none when its entry has no comment). Step 6.")
        if len(words(notes.get(f"column_{n}_monday", ""))) < 2:
            out.append(f"column_{n}_monday: write what your Monday entry says for {name}. Step 6.")
    if len(words(notes.get("difference", ""))) < 4:
        out.append("difference: write one sentence, 4 words or more: what differs, or no difference and what you compared. Step 6.")
    return out


def report(notes: dict[str, str], columns: dict[str, tuple[str, str | None]]) -> str:
    """Return what the check prints: Done, or Not yet with each thing left.

    Args:
        notes: the learner's notes, from read_notes.
        columns: return_header's columns, from return_header_columns.
    """
    left = version_left(notes) + sign_in_left(notes) + tables_left(notes) + columns_left(notes, columns)
    if left:
        shown = ["- " + line for line in left[:SHOWN]]
        more = [f"- and {len(left) - SHOWN} more, after these."] if len(left) > SHOWN else []
        return "\n".join([f"Not yet: {len(left)} left."] + shown + more)
    return (f"Done: profile {notes['profile']} is valid; the catalogs, two schemas and two columns of "
            "return_header are read, each command with its exit status.")


if __name__ == "__main__":
    notes_file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "notes.md"
    print(report(read_notes(notes_file), return_header_columns()))
