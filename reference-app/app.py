"""The compliance case-selection workbench: a case list and a page per case."""
from datetime import date

from flask import Flask, abort, render_template

import cases

app = Flask(__name__)


@app.template_filter("money")
def money(amount: int) -> str:
    """Format a whole-dollar amount for a page.

    Args:
        amount: An amount in whole US dollars.

    Returns:
        The amount with a dollar sign and thousands commas, such as "$12,250".
    """
    return f"${amount:,.0f}"


@app.route("/")
def case_list() -> str:
    """Show every case, highest selection score first.

    Returns:
        The case list page as HTML.
    """
    all_cases = cases.case_list(cases.load_cases(), date.today())
    return render_template("list.html", cases=all_cases)


@app.route("/cases/<case_id>")
def case_page(case_id: str) -> str:
    """Show one case's details.

    Args:
        case_id: The case number in the address, such as "CS-2026-0001".

    Returns:
        The case page as HTML.

    Raises:
        NotFound: No case has this case number (the page answers 404).
    """
    case = cases.find_case(cases.load_cases(), case_id)
    if case is None:
        abort(404)
    return render_template("case.html", case=cases.case_view(case, date.today()))
