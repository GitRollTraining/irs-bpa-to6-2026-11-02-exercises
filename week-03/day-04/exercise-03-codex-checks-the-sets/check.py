"""The done check for exercise 3, Codex checks the three sets while the learner approves each command.

Run it in this folder on the Workstation:

    python3 check.py              reads notes.md beside it
    python3 check.py <notes file> reads another notes file (the answer's, for the course team)

It reads each command the learner copied and tests their four answers and their decision against
the command itself. It never runs a databricks command, never reads the catalog and calls no model.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOWN = 6  # the things left that one run prints, in the order of the steps
READS = {"list", "get", "get-run", "list-runs", "describe", "profiles", "-h", "--help"}
SAFEGUARD_OFF = {"--force", "-f"}
CATALOG_LINES = ("label_train", "label_valid", "label_test",
                 "tax_added_features", "tax_added_train", "tax_added_valid", "tax_added_test")
WHY_ABSENT = re.compile(r"\b(after|known|leak\w*|selection|selected|before)\b", re.IGNORECASE)
TRANSCRIPT_COMMANDS = 6


def read_notes(path: Path) -> dict[str, str]:
    """Read the "key: value" lines of a notes file.

    Args:
        path: the notes file.

    Returns:
        Each key with the text after its colon, stripped; an empty string when nothing is typed.
    """
    notes = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        found = re.match(r"^([a-z0-9_]+):(.*)$", line.strip())
        if found:
            notes[found.group(1)] = found.group(2).strip()
    return notes


def words(text: str) -> list[str]:
    """Split a text into lowercase words, without punctuation."""
    return re.findall(r"[a-z0-9_]+", text.lower())


def yes_no(text: str) -> str:
    """Return "yes" or "no" as the learner wrote it, or "" for anything else."""
    first = words(text)[:1]
    return first[0] if first and first[0] in ("yes", "no") else ""


def facts(command: str, learner: str) -> dict[str, str]:
    """What the command itself shows, for the four questions.

    Args:
        command: the command, as the learner copied it.
        learner: the learner's schema name, such as learner_07.

    Returns:
        reads_or_changes, profile, target and safeguard_removed, each as the notes write it, and the decision they give.
    """
    parts = command.strip("` ").split()
    verb = parts[2] if len(parts) > 2 else ""
    reads = "reads" if verb in READS else "changes"
    profile = "yes" if any(p in ("-p", "--profile") or p.startswith("--profile=") for p in parts) else "no"
    schemas = set(re.findall(r"learner_\d+", command))
    if schemas == {learner}:
        target = "yes"
    elif schemas or any(re.fullmatch(r"\d+", p) for p in parts):
        target = "no"  # another learner's schema, or an id the request never gave
    else:
        target = "either"  # no schema and no id, such as a catalog list: the learner judges it
    safeguard = "yes" if SAFEGUARD_OFF & set(parts) else "no"
    others_good = reads == "reads" and profile == "yes" and safeguard == "no"
    decision = {"yes": "approve" if others_good else "decline", "no": "decline",
                "either": "either" if others_good else "decline"}[target]
    return {"reads_or_changes": reads, "profile": profile, "target": target,
            "safeguard_removed": safeguard, "decision": decision}


def command_left(n: int, notes: dict[str, str], learner: str) -> list[str]:
    """What is left in one command's block.

    Args:
        n: the block's number.
        notes: the learner's notes.
        learner: the learner's schema name, such as learner_07.
    """
    command = notes.get(f"cmd_{n}", "")
    if not command.strip("` ").startswith("databricks "):
        return [f"cmd_{n}: copy the whole command, from databricks to its last option. Step 3."]
    shown = facts(command, learner)
    hints = {"reads_or_changes": "read the command word after the group",
             "profile": "look for -p or --profile",
             "target": "compare the schema, table or id with the ones you named",
             "safeguard_removed": "read each option"}
    out = []
    for key, hint in hints.items():
        written = notes.get(f"{key}_{n}", "").lower().strip()
        written = written if key == "reads_or_changes" else yes_no(written)
        if written != shown[key] and not (shown[key] == "either" and written in ("yes", "no")):
            out.append(f"{key}_{n}: it does not fit the command; {hint}. Step 3.")
    decision = notes.get(f"decision_{n}", "").lower().strip()
    expected = shown["decision"]
    if expected == "either":
        expected = "approve" if yes_no(notes.get(f"target_{n}", "")) == "yes" else "decline"
    if not out and decision != expected:
        out.append(f"decision_{n}: it does not follow your four answers: approve only when all four are good. Step 3.")
    if len(words(notes.get(f"reason_{n}", ""))) < 4:
        out.append(f"reason_{n}: give the reason, 4 words or more. Step 3.")
    return out


def left(notes: dict[str, str]) -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    out = []
    why = notes.get("why_absent", "")
    if len(words(why)) < 5 or not WHY_ABSENT.search(why):
        out.append("why_absent: write one sentence, 5 words or more: when is that column's value known? Step 1.")
    transcript = "transcript" in notes.get("source", "").lower()
    schema = notes.get("schema", "").strip("` ")
    if not re.fullmatch(r"course\.learner_\d+", schema):
        out.append("schema: write your schema, such as course.learner_07 (the transcript's: course.learner_07). Step 2.")
    if not transcript and len(words(notes.get("request", ""))) < 10:
        out.append("request: copy the request you gave Codex. Step 2.")
    blocks = sorted({int(k.split("_")[1]) for k in notes if re.fullmatch(r"cmd_\d+", k) and notes[k]})
    needed = TRANSCRIPT_COMMANDS if transcript else 2
    if len(blocks) < needed:
        out.append(f"Step 3: fill a block for each command: {needed} or more here, {len(blocks)} so far. "
                   "With no command to judge, use the fallback transcript.")
    for n in blocks:
        out += command_left(n, notes, schema.split(".")[-1])
    if len(words(notes.get("codex_answer", ""))) < 5:
        out.append("codex_answer: copy Codex's last answer. Step 4.")
    for line in CATALOG_LINES:
        if not yes_no(notes.get(line, "")):
            out.append(f"{line}: write yes or no, from the Columns tab in Catalog Explorer. Step 5.")
    if not yes_no(notes.get("agree", "")):
        out.append("agree: write yes or no. Step 5.")
    if len(words(notes.get("compared", ""))) < 5:
        out.append("compared: write one sentence, 5 words or more: what differs, or which commands the answer rests on. Step 5.")
    return out


def report(notes: dict[str, str]) -> str:
    """Return what the check prints: Done, or Not yet with each thing left."""
    out = left(notes)
    if out:
        shown = ["- " + line for line in out[:SHOWN]]
        more = [f"- and {len(out) - SHOWN} more, after these."] if len(out) > SHOWN else []
        return "\n".join([f"Not yet: {len(out)} left."] + shown + more)
    decided = [notes[k].lower() for k in notes if re.fullmatch(r"decision_\d+", k) and notes[k]]
    return (f"Done: {len(decided)} commands judged, {decided.count('decline')} declined; "
            "Codex's answer set beside Catalog Explorer.")


if __name__ == "__main__":
    print(report(read_notes(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "notes.md")))
