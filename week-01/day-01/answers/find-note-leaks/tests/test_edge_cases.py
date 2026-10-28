"""Edge cases, on a fixed model reply and the course's simulated notes. No model is called.

Note 0122 names two amounts, the gross receipts and the difference, and only the difference is in
question. (In the answer it replaces a fixture copied from a case, with its name and TIN taken out.)
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extractor import extract  # noqa: E402

REPLY = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below the 1099-K total",
         "amount_in_question": 7500, "next_action": "Follow up in 30 days"}


def note(number):
    return (ROOT / "notes" / f"{number}.txt").read_text()


def fake_model(reply):
    """A model that always returns `reply`, and keeps what it was sent."""
    def ask(system_prompt, note_text, schema=None):
        ask.sent = note_text
        return json.dumps(reply)
    return ask


def test_both_amounts_reach_the_model():
    ask = fake_model(REPLY)
    fields = extract(note("0122"), ask=ask)
    assert "64,000" in ask.sent and "7,500" in ask.sent
    assert fields["amount_in_question"] == 7500
