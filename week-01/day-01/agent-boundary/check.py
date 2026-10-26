"""The done check for this exercise. From lab/, run: python3 ../check.py

It reads docs/boundary-proposal.md: its first line says it is a proposal and not an approval; every
row names the rule it rests on, as a quoted phrase or the words course proposal, and the role who
decides; and the combination the proposal removes is written. It checks that each is there and in
that shape, never how good it is; the class talks that through.
"""
import pathlib
import re
import sys

PROPOSAL = pathlib.Path(__file__).resolve().parent / "lab" / "docs" / "boundary-proposal.md"
SETTINGS = ["Which tool", "Where it runs", "Network", "What it may change", "Approvals", "Record"]
ROLES = ("accountable", "cybersecurity", "contracting officer", "privacy")
QUOTED = re.compile(r'"[^"]{12,}"|“[^”]{12,}”')


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


problems = []
text = PROPOSAL.read_text() if PROPOSAL.exists() else ""
first = text.splitlines()[0].lower() if text else ""
if "todo" in first or "proposal" not in first or not re.search(r"not (an )?approval", first):
    problems.append("the first line should say that this is a proposal and not an approval")
rows = {row[0]: row for row in table(text, "| Setting |")}
todo = [s for s in SETTINGS if s in rows and len(rows[s]) >= 5 and "TODO" in rows[s][3] + rows[s][4]]
if todo:
    problems.append(f"{len(todo)} of the six rows still have TODO in Rule or Who decides")
for setting in SETTINGS:
    row = rows.get(setting)
    if row is None or len(row) < 5:
        problems.append(f'the row "{setting}" is missing')
        continue
    if setting in todo:
        continue
    rule, who = row[3], row[4]
    if not (QUOTED.search(rule) or re.search(r"course'?s? proposal", rule, re.I)):
        problems.append(f'"{setting}": Rule should quote a phrase of the rule in double quotes, or say course proposal')
    if not any(role in who.lower() for role in ROLES):
        problems.append(f'"{setting}": Who decides should name a role the chapter names')
removes = re.search(r"^The combination this proposal removes, and why:(.*)$", text, re.M)
if not removes or "TODO" in removes[1] or len(re.findall(r"[A-Za-z]+", removes[1])) < 6:
    problems.append("the combination the proposal removes, and why, is not written yet")

if problems:
    print("Not yet: " + "; ".join(problems) + ".")
    sys.exit(1)
print("Done: the proposal says what it is, and every row names its rule and who decides; "
      "the combination it removes is written.")
