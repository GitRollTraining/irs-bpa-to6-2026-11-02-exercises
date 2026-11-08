"""The compliance case-selection workbench: a case list and a page per case."""
from datetime import date

from flask import Flask, abort, render_template

import cases

app = Flask(__name__)


@app.template_filter("money")
def money(amount):
    return f"${amount:,.0f}"


@app.route("/")
def case_list():
    all_cases = cases.case_list(cases.load_cases(), date.today())
    return render_template("list.html", cases=all_cases)


@app.route("/cases/<case_id>")
def case_page(case_id):
    case = cases.find_case(cases.load_cases(), case_id)
    if case is None:
        abort(404)
    return render_template("case.html", case=cases.case_view(case, date.today()))
