"""Load the workbench's cases and compute the values its pages show.

Every function here is pure except load_cases, which reads data/cases.json.
Amounts are whole US dollars. All cases are fictional.
"""
import json
from datetime import date
from pathlib import Path
from typing import Any

Case = dict[str, Any]

DATA_FILE = Path(__file__).parent / "data" / "cases.json"

REVIEW_FIRST_SCORE = 50  # a case scoring this or more is marked "Review first"


def load_cases(path: Path = DATA_FILE) -> list[Case]:
    """Return every case in the data file.

    Args:
        path: The JSON file that holds the cases.

    Returns:
        Every case, as a list of dicts.
    """
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_case(cases: list[Case], case_id: str) -> Case | None:
    """Return the case with this case number.

    Args:
        cases: The cases to search.
        case_id: The case number, such as "CS-2026-0001".

    Returns:
        The matching case, or None when no case has that number.
    """
    for case in cases:
        if case["case_id"] == case_id:
            return case
    return None


def balance_due(case: Case) -> int:
    """Return the amount still owed: the assessed amount minus the amount paid.

    Args:
        case: One case.

    Returns:
        The balance due, in whole US dollars.
    """
    return case["assessed"] - case["paid"]


def days_open(case: Case, today: date) -> int:
    """Return the days from opening to closing, or to today while the case is still open.

    Args:
        case: One case.
        today: The date to count to when the case is open.

    Returns:
        The number of days.
    """
    opened = date.fromisoformat(case["opened"])
    end = date.fromisoformat(case["closed"]) if case["closed"] else today
    return (end - opened).days


def selection_score(case: Case, today: date) -> int:
    """Return a 0-100 score for which case to review first; higher means sooner.

    Three factors, each capped:
      balance due:     1 point per $1,000, up to 40
      days open:       1 point per 10 days, up to 30
      missed filings: 10 points each, up to 30

    Args:
        case: One case.
        today: The date to count days open to.

    Returns:
        The selection score.
    """
    balance_points = min(balance_due(case) // 1000, 40)
    age_points = min(days_open(case, today) // 10, 30)
    filing_points = min(case["missed_filings"] * 10, 30)
    return balance_points + age_points + filing_points


def case_view(case: Case, today: date) -> Case:
    """Return the case's stored fields plus the computed values a page shows.

    Args:
        case: One case.
        today: The date to count days open to.

    Returns:
        The case with balance_due, days_open, score and review_first added.
    """
    score = selection_score(case, today)
    return {
        **case,
        "balance_due": balance_due(case),
        "days_open": days_open(case, today),
        "score": score,
        "review_first": score >= REVIEW_FIRST_SCORE,
    }


def case_list(cases: list[Case], today: date) -> list[Case]:
    """Return every case with its computed values, highest score first.

    Args:
        cases: The cases to show.
        today: The date to count days open to.

    Returns:
        Each case as case_view gives it, sorted by score.
    """
    views = [case_view(case, today) for case in cases]
    return sorted(views, key=lambda v: v["score"], reverse=True)
