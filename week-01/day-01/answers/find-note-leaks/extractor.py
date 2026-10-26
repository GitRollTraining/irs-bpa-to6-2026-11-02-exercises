"""The case-notes extractor, first draft: one note in, its five fields out, checked against a schema.

A coding agent wrote this draft from the task "extract the fields from one case note, and make it
robust". Its tests pass.

    from extractor import extract
    fields = extract("0147", note_text)

The model is reached through the practice kit's model.py, the route to the model the extractor is
approved to call. The tests pass in a fake model instead, so they never call one.

The answer: a failed reply is logged by its note's identifier and the problem only, never the note's
text; it is raised as a failure, never sent to a second model; the fallback model and its address
are gone.
"""
import json
import logging
import pathlib
import sys

import jsonschema

HERE = pathlib.Path(__file__).resolve().parent
LOG_FILE = HERE / "logs" / "extractor.log"

SCHEMA = {
    "type": "object",
    "properties": {
        "tax_year": {"type": "integer"},
        "form": {"type": "string"},
        "issue": {"type": "string"},
        "amount_in_question": {"type": ["integer", "null"]},
        "next_action": {"type": "string"},
    },
    "required": ["tax_year", "form", "issue", "amount_in_question", "next_action"],
    "additionalProperties": False,
}
SYSTEM_PROMPT = (
    "You extract fields from one case note. Return only the fields in the schema you are given. "
    "Use only what the note says. If the note states no amount, return null for amount_in_question."
)


class ExtractionFailed(Exception):
    """The model's reply was not JSON that matches the schema."""


def _log():
    LOG_FILE.parent.mkdir(exist_ok=True)
    log = logging.getLogger("extractor")
    if not log.handlers:
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        log.addHandler(handler)
        log.setLevel(logging.INFO)
    return log


def check_reply(reply_text):
    try:
        fields = json.loads(reply_text)
    except json.JSONDecodeError as err:
        raise ExtractionFailed(f"the reply is not JSON ({err.msg})") from None
    problems = [error.message for error in jsonschema.Draft202012Validator(SCHEMA).iter_errors(fields)]
    if problems:
        raise ExtractionFailed("; ".join(problems))
    return fields


def _approved_model():
    sys.path.insert(0, str(next(p for p in HERE.parents if (p / "model.py").exists())))  # the kit's model.py
    from model import ask
    return ask


def extract(note_id, note_text, ask=None):
    ask = ask or _approved_model()
    reply = ask(SYSTEM_PROMPT, f"<note>{note_text.strip()}</note>", SCHEMA)
    try:
        return check_reply(reply)
    except ExtractionFailed as failure:
        # Which note failed and why: its identifier and the problem, never its text.
        _log().warning("note %s failed its check: %s", note_id, failure)
        raise
