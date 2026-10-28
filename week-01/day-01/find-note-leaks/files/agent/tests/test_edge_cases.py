"""Edge cases the course's notes do not cover, on a fixed model reply. No model is called.

tests/fixtures/two_amounts.txt is a note from a closed case, with the name and TIN taken out, so that
the two-amount case is realistic.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extractor import extract  # noqa: E402

REPLY = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below the 1099-K totals",
         "amount_in_question": 41750, "next_action": "Follow up in 21 days"}


def fixture(name):
    return (ROOT / "tests" / "fixtures" / name).read_text()


def fake_model(reply):
    """A model that always returns `reply`, and keeps what it was sent."""
    def ask(system_prompt, note_text, schema=None):
        ask.sent = note_text
        return json.dumps(reply)
    return ask


def test_both_amounts_reach_the_model():
    ask = fake_model(REPLY)
    fields = extract(fixture("two_amounts.txt"), ask=ask)
    assert "212,000" in ask.sent and "41,750" in ask.sent
    assert fields["amount_in_question"] == 41750
