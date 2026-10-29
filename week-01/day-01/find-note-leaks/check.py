"""The done check for this exercise. From extractor/, run: python3 ../check.py

It runs extract on three replies for note 0147 that fail their check, with a fake model and the
network switched off. It looks where the note's text went, and it leaves logs/extractor.log for you
to read. Last it runs the tests, which must still hold the agent's tests. No model is called.
"""
import io
import json
import logging
import os
import pathlib
import re
import socket
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE / "extractor"
KIT = next(p for p in HERE.parents if (p / "notes").is_dir())
COURSE_NOTES = {p.stem: p.read_text().strip() for p in sorted((KIT / "notes").glob("*.txt"))}
NOTE_ID = "0147"
NOTE = COURSE_NOTES[NOTE_ID]
FIELDS = {"tax_year": 2023, "form": "1040", "issue": "Schedule C gross receipts lower than the information returns on file",
          "amount_in_question": 18400, "next_action": "Follow up in 30 days on the letter requesting business records"}
BAD_REPLIES = [
    json.dumps({**FIELDS, "amount_in_question": "18,400"}),  # the amount as text
    json.dumps({**FIELDS, "issue": ["Schedule C gross receipts", "lower than the information returns on file"]}),
    "Here are the fields: tax year 2023, Form 1040, Schedule C gross receipts lower than the information "
    "returns on file by 18,400.",  # not JSON
]
LOG_FILE = REPO / "logs" / "extractor.log"


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True)


def words(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def runs(text, length):
    w = words(text)
    return {" ".join(w[i:i + length]) for i in range(len(w) - length + 1)}


def found_in(text, phrases):
    have = " " + " ".join(words(text)) + " "
    return sorted(p for p in phrases if f" {p} " in have)


def pytest(folder, *args):
    # PY_COLORS=0: a notebook's kernel sets FORCE_COLOR, and colored output hides pytest's FAILED lines.
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=folder,
                          capture_output=True, text=True, timeout=300,
                          env={**os.environ, "EXTRACTOR_FALLBACK_URL": "http://127.0.0.1:9/", "PY_COLORS": "0"})


def test_names(folder):
    listed = pytest(folder, "--collect-only").stdout.splitlines()
    return {line.split("::")[-1].split("[")[0] for line in listed if "::" in line}


def stop(message):
    print("Not yet: " + message)
    sys.exit(1)


if not (REPO / ".git").is_dir():
    stop("there is no repository extractor/ yet. Run python3 ~/practice/reset.py find-note-leaks.")

# Run extract on each bad reply, with the network off and a fake model that keeps what it is sent.
hosts, sent = [], []


def network_off(host, *args, **kwargs):
    hosts.append(str(host))
    raise OSError("the network is switched off for this check")


def fake_model(reply):
    def ask(system_prompt, note_text, schema=None, **kwargs):
        sent.append(f"{system_prompt}\n{note_text}")
        return reply
    return ask


socket.getaddrinfo = network_off
socket.create_connection = lambda address, *args, **kwargs: network_off(address[0])
LOG_FILE.unlink(missing_ok=True)
sys.path = [str(REPO)] + [p for p in sys.path if pathlib.Path(p or ".").resolve() != HERE]
try:
    import extractor
except Exception as failure:  # an edit that stops extractor.py loading is reported, not raised
    stop(f"extractor.py does not load. Python reports {type(failure).__name__}: {failure}.")

problems = []
for reply in BAD_REPLIES:
    try:
        extractor.extract(NOTE, ask=fake_model(reply))
        problems.append("extract returned fields for a reply that fails its check. It should raise ExtractionFailed.")
    except extractor.ExtractionFailed:
        pass
    except Exception as failure:
        problems.append(f"extract stopped with {type(failure).__name__} ({failure}). It should raise ExtractionFailed.")
logging.shutdown()
problems = list(dict.fromkeys(problems))

if hosts:
    problems.append(f"extract tried to reach {', '.join(sorted(set(hosts)))}. "
                    "A note may go only to the model that model.py reaches.")
# A note is found by its label, or by six words in a row that no other course note and not the course
# team's system prompt holds.
shared = Counter(r for text in COURSE_NOTES.values() for r in runs(text, 6))
common = {r for r, n in shared.items() if n > 1} | runs((HERE / "files" / "course" / "prompts" / "system.txt").read_text(), 6)
if sent and not any(found_in(s, runs(NOTE, 6)) for s in sent):
    problems.append(f"the model did not get the text of note {NOTE_ID}. The extraction needs this text.")

log_text = LOG_FILE.read_text() if LOG_FILE.exists() else ""
from_note = runs(" ".join(words(NOTE)[2:]), 4)  # after its label, "Note 0147"
from_reply = set().union(*(runs(v if isinstance(v, str) else " ".join(v), 4)
                           for v in [FIELDS["issue"], FIELDS["next_action"], BAD_REPLIES[2]]))
leaked = found_in(log_text, from_note | from_reply) + re.findall(r"(?<![\d:])18,?400(?!\d)", log_text)
if leaked:
    problems.append("logs/extractor.log holds text or values from note 0147 or from the model's reply. Examples: "
                    + ", ".join(f'"{p}"' for p in sorted(set(leaked))[:3]))
if not log_text.strip():
    problems.append("logs/extractor.log is empty. The log should still show each failed reply, by its note.")
else:
    if log_text.count(NOTE_ID) < len(BAD_REPLIES):
        problems.append(f"logs/extractor.log does not name note {NOTE_ID} for each of the {len(BAD_REPLIES)} failures")

fixtures = sorted(p for p in (REPO / "tests" / "fixtures").rglob("*") if p.is_file()) \
    if (REPO / "tests" / "fixtures").is_dir() else []
for path in fixtures:
    if path.read_text().strip() not in COURSE_NOTES.values():
        problems.append(f"{path.relative_to(REPO)} is not one of the course's simulated notes")

# The tests: they pass, and they keep the agent's.
mine = pytest(REPO)
if log_text:
    LOG_FILE.write_text(log_text)  # what this check's three runs logged, without what the tests added
last = (mine.stdout.strip().splitlines() or ["no output"])[-1]
if mine.returncode != 0:
    problems.append(f"some of the tests fail. The last line from pytest is: {last}")
with tempfile.TemporaryDirectory() as draft:
    archive = git("archive", "--format=tar", "agent-draft")
    if archive.returncode != 0:
        stop("the tag agent-draft is missing. Run python3 ~/practice/reset.py find-note-leaks.")
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tar:
        try:
            tar.extractall(draft, filter="data")
        except TypeError:  # a Python without extraction filters
            tar.extractall(draft)
    gone = sorted(test_names(draft) - test_names(REPO))
    if gone:
        problems.append("the agent's tests " + ", ".join(gone) + " are gone. Keep what each test checks.")

if problems:
    print(f"Not yet: {len(problems)} left.")
    print("\n".join(f"- {p}" for p in problems))
    sys.exit(1)
print("Done: the log names each failed reply by its note only, and extract raises the failure. The note goes "
      "only to the approved model. Each fixture is a course note, and the tests pass.")
