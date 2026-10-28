"""The case-notes extractor: one note in, its five fields out, checked against the output schema.

    python3 extractor.py notes/0147.txt

prints the fields as JSON, or the reason the model's reply failed its check. The model is reached
through model.py; the tests pass in a recorded reply instead, so they never call the model. A reply
that fails its check is logged and asked for once more, through the same model, then reported as a
failure and never repaired.

The answer: the note goes to the model model.py reaches and nowhere else, with nothing from another
note beside it; a failure is logged by the note's identifier, the field and the rule it broke, never
by a value, because the validator's own message repeats the value it rejected.
"""
import json
import logging
import pathlib
import re
import sys

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "schema" / "output.schema.json").read_text())
SYSTEM_PROMPT = (ROOT / "prompts" / "system.txt").read_text()
LOG_FILE = ROOT / "logs" / "extractor.log"
ATTEMPTS = 2


class ExtractionFailed(Exception):
    """The model's reply was not JSON that matches the output schema."""


def _log():
    LOG_FILE.parent.mkdir(exist_ok=True)
    log = logging.getLogger("extractor")
    if not log.handlers:
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
    return log


def note_id(note_text):
    found = re.match(r"\s*Note (\d+)", note_text)
    return found[1] if found else "unknown"


def problem(error):
    """The field and the rule it broke, never the value it held: a value from a note is return information."""
    if error.validator == "required":
        return "missing " + ", ".join(name for name in error.validator_value if name not in error.instance)
    field = ".".join(str(part) for part in error.absolute_path) or "the reply"
    return f"{field} fails {error.validator}"


def check_reply(reply_text):
    try:
        fields = json.loads(reply_text)
    except json.JSONDecodeError:
        raise ExtractionFailed("the reply is not JSON") from None
    problems = [problem(error) for error in jsonschema.Draft202012Validator(SCHEMA).iter_errors(fields)]
    if problems:
        raise ExtractionFailed("; ".join(problems))
    return fields


def extract(note_text, ask=None):
    if ask is None:
        from model import ask
    for attempt in range(1, ATTEMPTS + 1):
        reply = ask(SYSTEM_PROMPT, f"<note>{note_text.strip()}</note>", SCHEMA)
        try:
            return check_reply(reply)
        except ExtractionFailed as failure:
            # Which note failed and why, by its identifier and the field, never its text or the reply.
            _log().warning("note %s: reply %d of %d failed its check: %s", note_id(note_text), attempt, ATTEMPTS, failure)
            if attempt == ATTEMPTS:
                raise


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractor.py NOTE_FILE")
    try:
        print(json.dumps(extract(pathlib.Path(sys.argv[1]).read_text())))
    except ExtractionFailed as failure:
        sys.exit(f"Failed: {failure}")


if __name__ == "__main__":
    main()
