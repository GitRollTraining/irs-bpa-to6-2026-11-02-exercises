from datetime import date

import cases

TODAY = date(2026, 11, 9)


def make_case(**fields: object) -> cases.Case:
    """Return a test case, with any field replaced.

    Args:
        **fields: Fields to set, such as assessed=10000.

    Returns:
        One case with every field the app reads.
    """
    case = {
        "case_id": "CS-TEST-0001",
        "business_name": "Test Shop",
        "tax_year": 2023,
        "status": "Open",
        "opened": "2026-10-01",
        "closed": None,
        "assessed": 10000,
        "paid": 2500,
        "missed_filings": 0,
    }
    case.update(fields)
    return case


def test_balance_due_is_assessed_minus_paid() -> None:
    assert cases.balance_due(make_case(assessed=10000, paid=2500)) == 7500


def test_balance_due_is_zero_when_paid_in_full() -> None:
    assert cases.balance_due(make_case(assessed=4000, paid=4000)) == 0


def test_days_open_counts_to_today_for_an_open_case() -> None:
    assert cases.days_open(make_case(opened="2026-10-01"), TODAY) == 39


def test_days_open_counts_to_the_closing_date_for_a_closed_case() -> None:
    case = make_case(opened="2026-01-05", closed="2026-05-29", status="Closed")
    assert cases.days_open(case, TODAY) == 144


def test_selection_score_adds_the_three_factors() -> None:
    # balance 7,500 -> 7; 39 days -> 3; 2 missed filings -> 20
    case = make_case(assessed=10000, paid=2500, missed_filings=2)
    assert cases.selection_score(case, TODAY) == 30


def test_selection_score_caps_each_factor() -> None:
    case = make_case(assessed=500000, paid=0, opened="2020-01-01", missed_filings=9)
    assert cases.selection_score(case, TODAY) == 100


def test_find_case_returns_the_match_or_none() -> None:
    all_cases = [make_case(case_id="A"), make_case(case_id="B")]
    assert cases.find_case(all_cases, "B")["case_id"] == "B"
    assert cases.find_case(all_cases, "C") is None


def test_case_view_adds_the_computed_values() -> None:
    view = cases.case_view(make_case(assessed=10000, paid=2500), TODAY)
    assert view["balance_due"] == 7500
    assert view["days_open"] == 39
    assert view["score"] == cases.selection_score(make_case(), TODAY)


def test_case_list_puts_the_highest_score_first() -> None:
    low = make_case(case_id="LOW", assessed=1000, paid=1000)
    high = make_case(case_id="HIGH", missed_filings=3)
    ids = [v["case_id"] for v in cases.case_list([low, high], TODAY)]
    assert ids == ["HIGH", "LOW"]


def test_the_data_file_loads_with_unique_case_ids() -> None:
    all_cases = cases.load_cases()
    ids = [c["case_id"] for c in all_cases]
    assert 12 <= len(ids) <= 20
    assert len(ids) == len(set(ids))
