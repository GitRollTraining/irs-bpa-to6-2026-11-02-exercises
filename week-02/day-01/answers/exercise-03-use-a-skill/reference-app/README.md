# Case workbench: the reference application

A simulated compliance case-selection workbench. A reviewer sees a list of tax compliance cases, ranked by a selection score, and opens one to see its details. The course uses this one application all week.

Every business, case number and amount in it is fictional.

## What is in it

| Path | What it holds |
|---|---|
| `app.py` | The Flask app: the case list at `/` and a page per case at `/cases/<case_id>` |
| `cases.py` | Loads the cases and computes the values the pages show: balance due, days open, selection score |
| `data/cases.json` | The fictional cases |
| `templates/` | The HTML pages: `base.html`, `list.html`, `case.html` |
| `tests/test_cases.py` | Unit tests of `cases.py` |
| `tests/e2e/` | End-to-end tests, added later in the course |

The selection score runs from 0 to 100 and adds three factors: 1 point per $1,000 of balance due (up to 40), 1 point per 10 days open (up to 30), and 10 points per missed filing (up to 30).

## Run it

Needs Python 3.10 or later. From this folder (`reference-app`), in a terminal:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run
```

Open http://127.0.0.1:5000 in a browser. Stop the app with Ctrl+C.

## Run its tests

With `.venv` active, from this folder:

```sh
pytest
```
