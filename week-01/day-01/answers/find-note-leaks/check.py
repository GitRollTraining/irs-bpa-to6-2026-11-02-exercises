"""The done check for this exercise. In this folder, run: python3 check.py

It runs the extractor once on a reply that fails its check, for the course's note 0147, with a fake
model in place of the approved one and the network switched off. Then it looks where the note's text
went: the log (logs/extractor.log, which it leaves for you to read), any host the extractor tried to
reach, and the tests' fixtures. Last, it runs the tests, which should still pass. No model is called.
"""
import json
import logging
import pathlib
import re
import socket
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
KIT = next(p for p in HERE.parents if (p / "notes").is_dir())
COURSE_NOTES = {p.read_text().strip() for p in (KIT / "notes").glob("*.txt")}
NOTE_ID = "0147"
NOTE = (KIT / "notes" / f"{NOTE_ID}.txt").read_text()
# A reply that fails the schema: amount_in_question is missing.
BAD_REPLY = json.dumps({"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts below information returns",
                        "next_action": "Follow up on records request in 30 days"})
LOG_FILE = HERE / "logs" / "extractor.log"


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def holds_note_text(text, note, run=4):
    """True when `text` holds `run` words in a row from the note, after the note's "Note 0147" label."""
    note_words = words(note)[2:]
    found = " " + " ".join(words(text)) + " "
    return any(" " + " ".join(note_words[i:i + run]) + " " in found for i in range(len(note_words) - run + 1))


def network_off(host, *args, **kwargs):
    hosts.append(str(host))
    raise OSError("the network is switched off for this check")


problems, hosts = [], []
LOG_FILE.unlink(missing_ok=True)
socket.getaddrinfo = network_off
sys.path.insert(0, str(HERE))
try:
    import extractor
except Exception as failure:  # an edit that stops extractor.py loading is reported, not raised
    print(f"Not yet: extractor.py does not load ({type(failure).__name__}: {failure}).")
    sys.exit(1)

try:
    extractor.extract(NOTE_ID, NOTE, ask=lambda system_prompt, note_text, schema=None: BAD_REPLY)
    problems.append("a reply that fails its check came back as fields; extract should raise ExtractionFailed")
except extractor.ExtractionFailed:
    pass
except Exception as failure:
    problems.append(f"extract stopped with {type(failure).__name__} ({failure}) instead of ExtractionFailed")
logging.shutdown()

log_text = LOG_FILE.read_text() if LOG_FILE.exists() else ""
if holds_note_text(log_text, NOTE):
    problems.append("note text is written to the log, logs/extractor.log")
elif NOTE_ID not in log_text:
    problems.append("the failure is no longer logged; log which note failed, by its identifier, and why")
if hosts:
    problems.append("the note was sent to a host other than the approved model: " + ", ".join(sorted(set(hosts))))
fixtures = [p for p in sorted((HERE / "tests" / "fixtures").glob("*")) if p.is_file()]
if any(p.read_text().strip() not in COURSE_NOTES for p in fixtures):
    problems.append("a file in tests/fixtures/ is not one of the course's simulated notes")
tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "tests"], cwd=HERE, capture_output=True, text=True)
last = (tests.stdout.strip().splitlines() or ["no output"])[-1]
passed = re.search(r"(\d+) passed", last)
if tests.returncode != 0 or not passed or int(passed[1]) < 3:
    problems.append(f"the three tests should still pass; pytest ends: {last}")

if problems:
    print("Not yet: " + "; ".join(problems) + ".")
    sys.exit(1)
print("Done: a failed reply is logged by its note's identifier only and raised, not sent anywhere else; "
      "every fixture is a course note; the tests pass.")
