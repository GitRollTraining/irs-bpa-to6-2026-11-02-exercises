"""The done check for this exercise. From lab/, run: python3 ../check.py

It reads your answers in docs/data-rules-check.md, and compares each with the course's answer. It
compares the answer in Permitted?, and for the use that is not yours to decide, the role in Who decides.
Each answer needs a reason in Why that ends with its section. The check does not judge the reason
further. The class talks the reasons through. Your answers count only after you commit them. It calls
no model.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE / "lab"
RECORD = "docs/data-rules-check.md"
USES = range(1, 5)
# For each use: the answer in Permitted?, and the role that Who decides must name. The answer file,
# with a reason for each use, is in answers/data-rules-check/.
ACCEPTED = {1: ("yes", None), 2: ("no", None), 3: ("not mine", "accountable"), 4: ("no", None)}
# Shown for a use whose answer the course does not accept: where to look again, in the file and in the notebook.
LOOK_AGAIN = {
    1: "Look again at the first line of notes/0147.txt, and at The approval on file. Then find its row in the "
       "data-rules check in section 1.2.",
    2: "Look again at what exports/case-2231.txt still gives without its name. Section 1.1 says what that means.",
    3: "Look again at what the approval covers, and at move 5 in section 1.2.",
    4: "Look again at the warning of the policy about public AI tools, in section 1.1.",
}


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)


def stop(message):
    print("Not yet: " + message)
    sys.exit(1)


def answers(text):
    """The answer table's rows by use: {use: (Permitted?, Who decides, Why)}."""
    lines = text.splitlines()
    start = next((n for n, line in enumerate(lines) if line.replace(" ", "").startswith("|Use|")), None)
    found = {}
    for line in lines[start + 2:] if start is not None else []:
        if not line.strip().startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 6 and cells[0].isdigit():
            found[int(cells[0])] = (cells[3], cells[4], " ".join(cells[5:]))
    return found


def permitted(cell):
    words = re.findall(r"[a-z]+", cell.lower())
    if words[:1] == ["not"] and len(words) > 1:  # Not mine (or yours, or ours) to decide
        return "not mine"
    return words[0] if words[:1] in (["yes"], ["no"]) else None


def roles(cell):
    return {role for role in ("accountable", "privacy") if role in cell.lower()}


def unfinished(answer, who, why):
    """What one row still needs, whatever its answer is. None when it needs nothing."""
    if not answer.strip() and not why.strip():
        return "fill in Permitted? and Why."
    if permitted(answer) is None:
        return "in Permitted?, write Yes, No or Not mine to decide."
    if permitted(answer) == "not mine" and not roles(who):
        return "in Who decides, write the role that decides."
    if len(re.findall(r"[A-Za-z]+", why)) < 6:
        return "in Why, write the rule that your answer rests on."
    if not re.search(r"sections?\s+1\.[123]\b", why, re.I):
        return "end Why with the section of the rule, such as (section 1.1)."
    return None


def judge(use, answer, who):
    """None when the course accepts this answer. Otherwise, what differs."""
    want, role = ACCEPTED[use]
    if permitted(answer) != want:
        return f"in Permitted?, the course does not accept your answer. {LOOK_AGAIN[use]}"
    if role and role not in roles(who):
        return f"in Who decides, the course does not accept the role. {LOOK_AGAIN[use]}"
    return None


if not (REPO / ".git").is_dir():
    stop("there is no repository lab/ yet. Run python3 ~/practice/reset.py data-rules-check.")
if not (REPO / RECORD).exists():
    stop(f"{RECORD} is missing. Run python3 ~/practice/reset.py data-rules-check to get it again.")

found = answers((REPO / RECORD).read_text())
problems = []
for use in USES:
    row = found.get(use, ("", "", ""))
    differs = unfinished(*row) or judge(use, row[0], row[1])
    if differs:
        problems.append(f"use {use}: {differs}")
committed = git("ls-files", "--error-unmatch", RECORD).returncode == 0 and \
    git("diff", "--quiet", "HEAD", "--", RECORD).returncode == 0
if not committed:
    problems.append(f"commit {RECORD} as it is now. Your answers count only after you commit them.")

if problems:
    print(f"Not yet: {len(problems)} left.")
    print("\n".join(f"- {p}" for p in problems))
    sys.exit(1)
print("Done: the course accepts your answer for each of the four uses. Each answer gives its rule and its section.")
