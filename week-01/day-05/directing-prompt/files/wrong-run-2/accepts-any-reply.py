"""A wrong run 2, for check.py. It is the extractor of the course's run 2, lab-states/run2/extractor.py,
with one change: check_reply does not check a reply against the output schema. So the extractor
accepts each reply that is JSON, and the run 2 test test_reply_missing_amount_is_a_failure fails.
"""
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
    """Read the model's reply as JSON.

    Args:
        reply_text: the reply's text, which should be JSON.

    Returns:
        The fields the reply holds.

    Raises:
        ExtractionFailed: the reply is not JSON.
    """
    try:
        fields = json.loads(reply_text)
    except json.JSONDecodeError as err:
        raise ExtractionFailed(f"the reply is not JSON ({err.msg})") from None
    problems = []  # The one change: no check against the schema.
    if problems:
        raise ExtractionFailed("; ".join(problems))
    return fields


def extract(note_text: str, ask: Callable[[str, str, dict], str] | None = None) -> dict:
    """Extract the five fields of one case note.

    Args:
        note_text: the text of the note, as in notes/0147.txt.
        ask: the model: a function that takes the system prompt, the message and the output
            schema, and returns the reply's text. None: model.ask, the route in model-route.json.

    Returns:
        The fields the reply holds.

    Raises:
        ExtractionFailed: the reply is not JSON.
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
