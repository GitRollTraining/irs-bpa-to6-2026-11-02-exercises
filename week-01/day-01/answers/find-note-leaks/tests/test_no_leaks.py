"""Where a note's text may go, checked on every test run. No model is called and no network is used.

A case note's text, or a value taken from it, goes to one place only: the model model.py reaches,
with nothing from another note beside it. It is never written to a log or sent to another host, and
every fixture is one of the course's simulated notes.
"""
import json
import logging
import pathlib
import re
import socket
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import extractor  # noqa: E402

NOTES = {p.stem: p.read_text().strip() for p in (ROOT / "notes").glob("*.txt")}
NOTE = NOTES["0147"]
FIELDS = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts lower than the information returns",
          "amount_in_question": 18400, "next_action": "Follow up in 30 days"}
BAD = json.dumps({**FIELDS, "amount_in_question": "18,400"})


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def shares_four_words(text, source):
    have, w = " " + " ".join(words(text)) + " ", words(source)
    return any(f" {' '.join(w[i:i + 4])} " in have for i in range(len(w) - 3))


@pytest.fixture
def hosts(monkeypatch):
    """The hosts extract tries to reach; every try is refused."""
    tried = []

    def refuse(host, *args, **kwargs):
        tried.append(host)
        raise OSError("no network in the tests")

    monkeypatch.setattr(socket, "getaddrinfo", refuse)
    monkeypatch.setattr(socket, "create_connection", lambda address, *args, **kwargs: refuse(address[0]))
    return tried


@pytest.fixture
def log_text(tmp_path, monkeypatch, hosts):
    """What extract logs for a reply that fails its check."""
    log = logging.getLogger("extractor")

    def detach():
        for handler in log.handlers[:]:
            log.removeHandler(handler)
            handler.close()

    detach()
    monkeypatch.setattr(extractor, "LOG_FILE", tmp_path / "extractor.log")
    with pytest.raises(extractor.ExtractionFailed):
        extractor.extract(NOTE, ask=lambda system_prompt, note_text, schema=None: BAD)
    detach()
    written = tmp_path / "extractor.log"
    return written.read_text() if written.exists() else ""


def test_a_failure_is_logged_by_its_note_and_field(log_text):
    assert "0147" in log_text and "amount_in_question" in log_text


def test_a_failure_logs_no_text_or_value_from_the_note(log_text):
    assert not shares_four_words(log_text, " ".join(words(NOTE)[2:]))  # after its label, "Note 0147"
    assert not re.search(r"(?<![\d:])18,?400(?!\d)", log_text)


def test_a_failed_reply_sends_the_note_to_no_other_host(hosts):
    with pytest.raises(extractor.ExtractionFailed):
        extractor.extract(NOTE, ask=lambda system_prompt, note_text, schema=None: BAD)
    assert hosts == []


def test_nothing_but_the_note_goes_to_the_model():
    sent = []

    def ask(system_prompt, note_text, schema=None):
        sent.append(system_prompt + note_text)
        return json.dumps(FIELDS)

    extractor.extract(NOTE, ask=ask)
    assert [n for n in NOTES if n != "0147" and f"Note {n}." in sent[0]] == []


def test_every_fixture_is_a_course_note():
    fixtures = ROOT / "tests" / "fixtures"
    for path in sorted(fixtures.rglob("*")) if fixtures.is_dir() else []:
        if path.is_file():
            assert path.read_text().strip() in NOTES.values(), path.name
