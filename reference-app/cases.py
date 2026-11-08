"""Load the workbench's cases and compute the values its pages show.

Every function here is pure except load_cases, which reads data/cases.json.
Amounts are whole US dollars. All cases are fictional.
"""
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "cases.json"


def load_cases(path=DATA_FILE):
    """Return every case in the data file, as a list of dicts."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_case(cases, case_id):
    """Return the case with this case_id, or None."""
    for case in cases:
        if case["case_id"] == case_id:
            return case
    return None


def balance_due(case):
    """Assessed amount minus the amount paid."""
    return case["assessed"] - case["paid"]


def days_open(case, today):
    """Days from opening to closing, or to today while the case is still open."""
    opened = date.fromisoformat(case["opened"])
    end = date.fromisoformat(case["closed"]) if case["closed"] else today
    return (end - opened).days


def selection_score(case, today):
    """A 0-100 score for which case to review first; higher means sooner.

    Three factors, each capped:
      balance due:     1 point per $1,000, up to 40
      days open:       1 point per 10 days, up to 30
      missed filings: 10 points each, up to 30
    """
    balance_points = min(balance_due(case) // 1000, 40)
    age_points = min(days_open(case, today) // 10, 30)
    filing_points = min(case["missed_filings"] * 10, 30)
    return balance_points + age_points + filing_points


def case_view(case, today):
    """The case's stored fields plus the computed values a page shows."""
    return {
        **case,
        "balance_due": balance_due(case),
        "days_open": days_open(case, today),
        "score": selection_score(case, today),
    }


def case_list(cases, today):
    """Every case with its computed values, highest score first."""
    views = [case_view(case, today) for case in cases]
    return sorted(views, key=lambda v: v["score"], reverse=True)
