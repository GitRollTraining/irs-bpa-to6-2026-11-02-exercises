"""The case-notes extractor: one note in, its five fields out, checked against the output schema.

    python3 extractor.py notes/0147.txt

prints the fields as JSON, or the reason the model's reply failed its check. The model is reached
through model.py; the tests pass in a recorded reply instead, so they never call the model. A reply
that fails its check is logged and tried once more through a second provider, then reported as a
failure and never repaired.
"""
import json
import logging
import os
import pathlib
import re
import sys
import urllib.request

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent
SCHEMA = json.loads((ROOT / "schema" / "output.schema.json").read_text())
SYSTEM_PROMPT = (ROOT / "prompts" / "system.txt").read_text()
LOG_FILE = ROOT / "logs" / "extractor.log"
# A second provider, tried once when a reply fails its check. Set EXTRACTOR_FALLBACK_URL to change it.
FALLBACK_URL = os.environ.get("EXTRACTOR_FALLBACK_URL", "https://inference.example.net/v1/complete")


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


def check_reply(reply_text):
    try:
        fields = json.loads(reply_text)
    except json.JSONDecodeError as err:
        raise ExtractionFailed(f"the reply is not JSON ({err.msg})") from None
    problems = [error.message for error in jsonschema.Draft202012Validator(SCHEMA).iter_errors(fields)]
    if problems:
        raise ExtractionFailed("; ".join(problems))
    return fields


def ask_fallback(system_prompt, message):
    body = json.dumps({"system": system_prompt, "input": message, "format": "json"}).encode()
    request = urllib.request.Request(FALLBACK_URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read())["output"]


def extract(note_text, ask=None):
    if ask is None:
        from model import ask
    message = f"<note>{note_text.strip()}</note>"
    reply = ask(SYSTEM_PROMPT, message, SCHEMA)
    try:
        return check_reply(reply)
    except ExtractionFailed as failure:
        # Keep the note with the failure, so a bad extraction can be reproduced.
        _log().warning("note %s: reply failed its check. The note: %s", note_id(note_text), note_text.strip())
        try:
            return check_reply(ask_fallback(SYSTEM_PROMPT, message))
        except (OSError, ValueError, KeyError, ExtractionFailed):
            raise failure from None


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 extractor.py NOTE_FILE")
    try:
        print(json.dumps(extract(pathlib.Path(sys.argv[1]).read_text())))
    except ExtractionFailed as failure:
        sys.exit(f"Failed: {failure}")


if __name__ == "__main__":
    main()
