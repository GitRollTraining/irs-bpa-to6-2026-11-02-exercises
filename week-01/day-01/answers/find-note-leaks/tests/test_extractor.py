"""Tests for the extractor, on fixed model replies. No model is called.

Fixtures: note_0147.txt is the chapter's example note. note_no_amount.txt is the course's simulated
note 0104, which names no amount (in the answer, it replaces a note copied from a case).
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from extractor import extract  # noqa: E402

REPLY_0147 = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below information returns",
              "amount_in_question": 18400, "next_action": "Follow up on records request in 30 days"}
REPLY_NO_AMOUNT = {"tax_year": 2023, "form": "1040", "issue": "Records requested for a deduction",
                   "amount_in_question": None, "next_action": "Follow up in 45 days"}


def fixture(name):
    return (HERE / "fixtures" / name).read_text()


def fake_model(reply):
    """A model that always returns `reply`, and keeps the note it was sent."""
    def ask(system_prompt, note_text, schema=None):
        ask.sent = note_text
        return json.dumps(reply)
    return ask


def test_note_0147_gives_its_amount():
    assert extract("0147", fixture("note_0147.txt"), ask=fake_model(REPLY_0147))["amount_in_question"] == 18400


def test_note_is_sent_inside_note_tags():
    ask = fake_model(REPLY_0147)
    extract("0147", fixture("note_0147.txt"), ask=ask)
    assert ask.sent.startswith("<note>Note 0147.") and ask.sent.endswith("</note>")


def test_note_with_no_amount_gives_null():
    assert extract("no-amount", fixture("note_no_amount.txt"), ask=fake_model(REPLY_NO_AMOUNT))["amount_in_question"] is None
