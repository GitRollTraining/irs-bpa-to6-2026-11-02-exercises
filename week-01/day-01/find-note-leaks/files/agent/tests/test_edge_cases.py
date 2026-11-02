"""Edge cases the course's notes do not cover, on a fixed model reply. No model is called.

tests/fixtures/two_amounts.txt is a note from a closed case, with the name and TIN taken out, so that
the two-amount case is realistic.
"""
import json
import pathlib
import sys
from collections.abc import Callable

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from extractor import extract  # noqa: E402

REPLY = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below the 1099-K totals",
         "amount_in_question": 41750, "next_action": "Follow up in 21 days"}


def fixture(name: str) -> str:
    """Return the text of a file in tests/fixtures/.

    Args:
        name: the file's name, such as "two_amounts.txt".

    Returns:
        The file's text.
    """
    return (ROOT / "tests" / "fixtures" / name).read_text()


def fake_model(reply: dict) -> Callable[[str, str, dict | None], str]:
    """A model that always returns `reply`, and keeps what it was sent.

    Args:
        reply: the fields the model replies with.

    Returns:
        A function to pass to extract as its ask.
    """
    def ask(system_prompt: str, note_text: str, schema: dict | None = None) -> str:
        """Return `reply` as JSON, and keep the message in ask.sent.

        Args:
            system_prompt: the extractor's system prompt.
            note_text: the message the extractor sends.
            schema: the output schema.

        Returns:
            The reply's text.
        """
        ask.sent = note_text
        return json.dumps(reply)
    return ask


def test_both_amounts_reach_the_model() -> None:
    ask = fake_model(REPLY)
    note = fixture("two_amounts.txt")
    fields = extract(note, ask=ask)
    assert ask.sent == f"<note>{note.strip()}</note>"
    assert fields["amount_in_question"] == REPLY["amount_in_question"]
