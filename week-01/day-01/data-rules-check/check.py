"""The done check for this exercise. From lab/, run: python3 ../check.py

It reads your answers in docs/data-rules-check.md and shows nothing of the course's until all ten
are filled in and committed, so that they are your own. Then it compares each with the course's: a
use the rules settle one way has one answer it accepts, and a use two careful readers could answer
two ways has each of them, some only with the reason that answer rests on. It never judges how good
a reason is beyond that; the class talks the reasons through. It also checks that no commit an AI
tool made comes before your answers: it counts a commit as an AI tool's when its author, or a
Co-authored-by line in its message, names one. No model is called.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE / "lab"
RECORD = "docs/data-rules-check.md"
USES = range(1, 11)
AI_TOOLS = ("claude", "codex", "copilot", "openai", "anthropic")

# The answers the course accepts for each use: (Permitted?, the roles Who decides may name, a pattern
# the reason must match). The kept answer, with the reason for each, is in answers/data-rules-check/.
FROM_REAL_NOTES = r"real|actual|associat|identif|taxpayer|return information"
CONTRACTOR_RULE = r"cybersecurity|contracting officer"
ACCEPTED = {
    1: [("yes", None, None)],
    2: [("no", None, None), ("not mine", {"accountable", "privacy"}, None)],
    3: [("no", None, None)],
    4: [("yes", None, None)],
    5: [("not mine", {"privacy"}, None), ("no", None, FROM_REAL_NOTES)],
    6: [("no", None, None)],
    7: [("not mine", {"cybersecurity and contracting officer"}, None), ("no", None, CONTRACTOR_RULE)],
    8: [("no", None, None)],
    9: [("no", None, None), ("not mine", {"accountable", "privacy"}, None)],
    10: [("yes", None, None), ("not mine", {"privacy"}, None)],
}
# Shown only once your answers are committed, for a use whose answer the course does not accept.
LOOK_AGAIN = {
    1: "what the approvals on file cover, and what a use inside them requires (section 1.3)",
    2: "what each line of the list says about a return, against the statute's definition of return "
       "information (section 1.1)",
    3: "what the guide still is once the names are out, and which tools may be used at all (sections 1.1 "
       "and 1.3)",
    4: "what the approvals on file cover (section 1.3)",
    5: "where the notes came from, and who answers questions about synthetic data (sections 1.1 and 1.2)",
    6: "which tools may be used for work at all, whatever the text (section 1.3)",
    7: "who Sam works for, and the rule for that (section 1.3)",
    8: "what the log holds now, and who may read return information (sections 1.2 and 1.3)",
    9: "which tools are approved (sections 1.1 and 1.3)",
    10: "the statute's exception for data that cannot be associated with a taxpayer (section 1.1)",
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
    text = cell.lower()
    named = {role for role in ("accountable", "privacy") if role in text}
    cyber, officer = "cybersecurity" in text, "contracting officer" in text
    if cyber and officer:
        named.add("cybersecurity and contracting officer")
    elif cyber or officer:
        named.add("one of two")
    return named


def unfinished(found):
    """What is still missing from the answers, as (use, what), whatever the answers are."""
    missing = []
    for use in USES:
        answer, who, why = found.get(use, ("", "", ""))
        if not answer.strip() and not why.strip():
            missing.append((use, "empty"))
        elif permitted(answer) is None:
            missing.append((use, "write Yes, No or Not mine to decide in Permitted?"))
        elif permitted(answer) == "not mine" and not roles(who):
            missing.append((use, "name, in Who decides, the role whose decision it is"))
        elif len(re.findall(r"[A-Za-z]+", why)) < 6:
            missing.append((use, "write the reason in Why"))
        elif not re.search(r"sections?\s+1\.[123]\b", why, re.I):
            missing.append((use, "end Why with the section its rule is in, such as (section 1.3)"))
    return missing


def judge(use, answer, who, why):
    """None when the course accepts this answer; otherwise what differs."""
    answer, named = permitted(answer), roles(who)
    options = [option for option in ACCEPTED[use] if option[0] == answer]
    if not options:
        return "Permitted? is not an answer the course accepts for this use"
    for _, owners, reason in options:
        if owners is not None and not (named and named <= owners):
            continue
        if reason and not re.search(reason, f"{who} {why}", re.I):
            continue
        return None
    owners = options[0][1]
    if owners is not None and "one of two" in named:
        return "Who decides names one of the two roles the rule names; name both"
    if owners is not None and named & owners:
        return ("Who decides names, beside the role whose decision it is, one whose it is not; keep only "
                "the one")
    if owners is not None:
        return "Who decides is not a role the course accepts for this use"
    return f"{answer.capitalize()} is accepted for this use only with the reason it rests on, which Why does not give"


def matched(found):
    return sum(judge(use, *found[use]) is None for use in USES)


def ai_made(commit):
    who = git("log", "-1", "--format=%an %ae%n%(trailers:key=Co-authored-by,valueonly)", commit).stdout.lower()
    return any(tool in who for tool in AI_TOOLS)


if not (REPO / ".git").is_dir():
    stop("there is no repository lab/ yet; run python3 ~/practice/reset.py data-rules-check")
if not (REPO / RECORD).exists():
    stop(f"{RECORD} is missing; run python3 ~/practice/reset.py data-rules-check to get it again")

# Your answers come first, and are your own: nothing is compared until they are filled in and committed.
found = answers((REPO / RECORD).read_text())
missing = unfinished(found)
committed = git("ls-files", "--error-unmatch", RECORD).returncode == 0 and \
    git("diff", "--quiet", "HEAD", "--", RECORD).returncode == 0
if missing or not committed:
    empty = [use for use, what in missing if what == "empty"]
    lines = [f"{len(empty)} of the ten uses still need Permitted? and Why"] if empty else []
    lines += [f"use {use}: {what}" for use, what in missing if what != "empty"]
    lines += [] if committed else [f"{RECORD} is not committed yet, as it stands now"]
    stop(f"{RECORD}, your answers for the ten uses, is not filled in and committed yet.\n"
         + "".join(f"- {line}\n" for line in lines)
         + "The check compares your answers with the course's only once they are committed, so that "
           "they are your own.")

# Your first committed answers, for the debrief, and that they came before any commit an AI tool made.
commits = git("rev-list", "--reverse", "HEAD").stdout.split()
first = None
for commit in git("rev-list", "--reverse", "HEAD", "--", RECORD).stdout.split():
    then = answers(git("show", f"{commit}:{RECORD}").stdout)
    if not unfinished(then):
        first = (commit, matched(then))
        break
problems = []
ai = next((commit for commit in commits if ai_made(commit)), None)
if ai and (first is None or commits.index(first[0]) >= commits.index(ai)):
    subject = git("log", "-1", "--format=%h %s", ai).stdout.strip()
    problems.append(f"an AI tool made commit {subject} before your answers were committed; they come "
                    "first, before any AI tool touches the repository")

for use in USES:
    differs = judge(use, *found[use])
    if differs:
        problems.append(f"use {use}: {differs}. Look again at {LOOK_AGAIN[use]}")

so_far = f"Your first committed answers matched {first[1]} of the ten." if first else ""
if problems:
    print(f"Not yet: {len(problems)} left.")
    print("\n".join(f"- {problem}" for problem in problems))
    print(so_far)
    sys.exit(1)
print("Done: each of your ten answers is one the course accepts, with its reason and its section, "
      "committed before any commit an AI tool made. " + so_far)
