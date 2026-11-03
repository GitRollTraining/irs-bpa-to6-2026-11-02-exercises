"""The case-notes extractor: one note in, its five fields out, checked against the output schema.

    python3 extractor.py notes/0147.txt

prints the fields as JSON, or the reason the model's reply failed its check. The model is reached
through model.py; the tests pass in a recorded reply instead, so they never call the model. A reply
that fails its check is reported as a failure and never repaired.
"""
import datetime
import json
import pathlib
import sys
from collections.abc import Callable

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "schema" / "output.schema.json").read_text())
SYSTEM_PROMPT = (ROOT / "prompts" / "system.txt").read_text()


class ExtractionFailed(Exception):
    """The model's reply was not JSON that matches the output schema."""


def check_reply(reply_text: str) -> dict:
    """Check the model's reply against the output schema.

    Args:
        reply_text: the reply's text, which should be JSON.

    Returns:
        The fields the reply holds.

    Raises:
        ExtractionFailed: the reply is not JSON, or does not match the schema.
    """
    try:
        fields = json.loads(reply_text)
    except json.JSONDecodeError as err:
        raise ExtractionFailed(f"the reply is not JSON ({err.msg})") from None
    problems = [error.message for error in jsonschema.Draft202012Validator(SCHEMA).iter_errors(fields)]
    if problems:
        raise ExtractionFailed("; ".join(problems))
    if fields["tax_year"] > datetime.date.today().year:
        raise ExtractionFailed("the tax year is after this year")
    return fields


def extract(note_text: str, ask: Callable[[str, str, dict], str] | None = None) -> dict:
    """Extract the five fields of one case note.

    Args:
        note_text: the text of the note, as in notes/0147.txt.
        ask: the model: a function that takes the system prompt, the message and the output
            schema, and returns the reply's text. None: model.ask, the route in model-route.json.

    Returns:
        The fields, checked against the output schema.

    Raises:
        ExtractionFailed: the reply is not JSON that matches the output schema.
    """
    if ask is None:
        from model import ask
    reply = ask(SYSTEM_PROMPT, f"<note>{note_text.strip()}</note>", SCHEMA)
    return check_reply(reply)


def main() -> None:
    """Extract the note named on the command line and print its fields as JSON.

    Exits with the reason when the reply fails its check.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractor.py NOTE_FILE")
    try:
        print(json.dumps(extract(pathlib.Path(sys.argv[1]).read_text())))
    except ExtractionFailed as failure:
        sys.exit(f"Failed: {failure}")


if __name__ == "__main__":
    main()
