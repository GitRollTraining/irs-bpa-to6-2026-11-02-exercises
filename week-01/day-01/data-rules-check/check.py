"""The done check for this exercise. From lab/, run: python3 ../check.py

It reads docs/data-rules-check.md and docs/requirements.md: every Permitted? answer is the one the
course's check gives, every reason is there and, where the answer is not Yes, names the chapter
section its rule is in; the TODO cells are filled, each requirement names where a reviewer checks it
in backticks, and each open question names the role the chapter gives it. Then it reads the history:
both files are committed, and no commit an AI tool made comes before them. It counts a commit as an
AI tool's when its author, or a Co-authored-by line in its message, names one (Claude Code adds such
a line to the commits it makes). It never judges how good a reason is; the class talks that through.
"""
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parent / "lab"
CHECK, NOTE = "docs/data-rules-check.md", "docs/requirements.md"
ANSWERS = ["yes", "no", "no", "no", "not mine to decide", "yes"]
ROLES = [("May the extractor be used", "accountable", "the accountable official"),
         ("May simulated or synthetic", "privacy", "the privacy contact")]
AI_TOOLS = ("claude", "codex", "copilot", "openai", "anthropic")


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def table(text, header):
    """The rows of the Markdown table whose header row starts with `header`, as lists of cells."""
    lines = text.splitlines()
    start = next((n for n, line in enumerate(lines) if line.startswith(header)), None)
    rows = []
    for line in lines[start + 2:] if start is not None else []:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def words(text):
    return len(re.findall(r"[A-Za-z0-9]+", text))


def permitted(cell):
    answer = " ".join(re.findall(r"[a-z]+", cell.lower()))
    return "not mine to decide" if answer in ("not yours to decide", "not ours to decide") else answer


problems = []
check_rows = table((REPO / CHECK).read_text(), "| Information |") if (REPO / CHECK).exists() else []
if len(check_rows) != 6:
    problems.append(f"{CHECK} should hold its six rows; it holds {len(check_rows)}")
empty = [row for row in check_rows if not row[2] or words(row[3] if len(row) > 3 else "") < 4]
if empty:
    problems.append(f"in {CHECK}, {len(empty)} of the six rows still need Permitted? and a reason in Why")
for row, answer in zip(check_rows, ANSWERS):
    if row in empty:
        continue
    if permitted(row[2]) != answer:
        problems.append(f'"{row[0]}" in "{row[1]}" is not answered as the course\'s check answers it; '
                        "compare the table in section 1.2")
    elif answer != "yes" and not re.search(r"section\s+1\.[123]\b", row[3], re.I):
        problems.append(f'"{row[0]}" in "{row[1]}": its reason does not end with the section its rule is in, '
                        "such as (section 1.1)")

note_text = (REPO / NOTE).read_text() if (REPO / NOTE).exists() else ""
requirements = table(note_text, "| What the protected surface triggers |")[3:]
todo = [row for row in requirements if "TODO" in " ".join(row) or len(row) < 3]
if todo or len(requirements) != 3:
    problems.append(f"in {NOTE}, {len(todo)} of the three new requirement rows are still TODO")
for row in requirements:
    if row in todo:
        continue
    if words(row[1]) < 6:
        problems.append(f'the requirement for "{row[0]}" is not yet a line a reviewer can check')
    elif not re.search(r"`[^`]+`", row[2]):
        problems.append(f'the requirement for "{row[0]}" does not name, in backticks, where a reviewer checks it')
questions = table(note_text, "| Question |")
unrouted = 0
for (start, role, name) in ROLES:
    row = next((r for r in questions if r[0].startswith(start)), None)
    if row is None or "TODO" in row[-1] or not row[-1]:
        unrouted += 1
    elif role not in row[-1].lower():
        problems.append(f'the open question "{start} ..." goes to another role; see section 1.2, the fifth move')
if unrouted:
    problems.append(f"in {NOTE}, {unrouted} of the two open questions name no role yet")

uncommitted = [path for path in (CHECK, NOTE) if git("ls-files", "--error-unmatch", path).returncode != 0
               or git("diff", "--quiet", "HEAD", "--", path).returncode != 0]
if uncommitted:
    problems.append(" and ".join(uncommitted) + (" are" if len(uncommitted) > 1 else " is")
                    + " not committed yet, as they stand now")
commits = git("rev-list", "--reverse", "HEAD").stdout.split()
for index, commit in enumerate(commits):
    who = git("log", "-1", "--format=%an %ae%n%(trailers:key=Co-authored-by,valueonly)", commit).stdout.lower()
    if not any(tool in who for tool in AI_TOOLS):
        continue
    late = []
    for path in (CHECK, NOTE):
        added = git("log", "--diff-filter=A", "--format=%H", "--", path).stdout.split()
        if not added or commits.index(added[-1]) > index:
            late.append(path)
    if late:
        subject = git("log", "-1", "--format=%h %s", commit).stdout.strip()
        problems.append(f'an AI tool made commit {subject} before {" and ".join(late)} '
                        f'{"were" if len(late) > 1 else "was"} committed')
    break

if problems:
    print("Not yet: " + "; ".join(problems) + ".")
    sys.exit(1)
print("Done: the data-rules check is passed and committed with your requirements note, "
      "before any commit an AI tool made.")
