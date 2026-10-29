"""The extractor's tests, on model replies recorded in tests/recorded/. No model is called."""
import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extractor import ExtractionFailed, extract  # noqa: E402


def note(number):
    return (ROOT / "notes" / f"{number}.txt").read_text()


def recorded(name):
    """A fake model that returns the reply recorded in tests/recorded/<name>.json, and keeps what it was sent."""
    reply = (ROOT / "tests" / "recorded" / f"{name}.json").read_text()

    def ask(system_prompt, note_text, schema=None):
        ask.sent = note_text
        return reply

    return ask


def test_note_0147_gives_its_amount():
    fields = extract(note("0147"), ask=recorded("0147"))
    assert fields["tax_year"] == 2023
    assert fields["form"] == "1040"
    assert fields["amount_in_question"] == 18400


def test_note_with_no_amount_gives_null():
    assert extract(note("0102"), ask=recorded("0102"))["amount_in_question"] is None


def test_note_is_sent_inside_note_tags():
    ask = recorded("0147")
    extract(note("0147"), ask=ask)
    assert ask.sent.startswith("<note>Note 0147.") and ask.sent.endswith("</note>")


def test_reply_missing_amount_is_a_failure():
    fields = json.loads((ROOT / "tests" / "recorded" / "0147.json").read_text())
    del fields["amount_in_question"]
    with pytest.raises(ExtractionFailed):
        extract(note("0147"), ask=lambda system_prompt, note_text, schema=None: json.dumps(fields))


def test_reply_that_is_not_json_is_a_failure():
    with pytest.raises(ExtractionFailed):
        extract(note("0147"), ask=lambda system_prompt, note_text, schema=None: "Here are the fields: ...")
