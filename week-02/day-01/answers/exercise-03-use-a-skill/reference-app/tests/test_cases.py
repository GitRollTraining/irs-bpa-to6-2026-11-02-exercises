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


def test_case_view_flags_review_first_from_a_score_of_50() -> None:
    # 39 days -> 3; 2 missed filings -> 20; balance 26,500 -> 26 (49) or 27,500 -> 27 (50)
    at_49 = cases.case_view(make_case(assessed=26500, paid=0, missed_filings=2), TODAY)
    at_50 = cases.case_view(make_case(assessed=27500, paid=0, missed_filings=2), TODAY)
    assert (at_49["score"], at_49["review_first"]) == (49, False)
    assert (at_50["score"], at_50["review_first"]) == (50, True)


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


def test_case_list_page_shows_balance_due_after_status() -> None:
    from app import app

    html = app.test_client().get("/").get_data(as_text=True)
    assert "<th>Status</th><th>Balance due</th>" in html
    first = cases.case_list(cases.load_cases(), date.today())[0]
    assert f"${first['balance_due']:,}" in html


def test_case_list_page_shows_review_first_only_for_scores_of_50_or_more() -> None:
    from app import app

    html = app.test_client().get("/").get_data(as_text=True)
    views = cases.case_list(cases.load_cases(), date.today())
    flagged = sum(1 for v in views if v["score"] >= 50)
    assert 0 < flagged < len(views)  # the data covers both cases
    assert html.count("Review first") == flagged
    for row in html.split("<tr>")[2:]:
        score = int(row.split('<td class="number">')[-1].split("<")[0])
        assert ("Review first" in row) == (score >= 50)
