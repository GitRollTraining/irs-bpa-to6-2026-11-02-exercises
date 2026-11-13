"""The done check for exercise 2, Wednesday's notebook run as a one-off job.

Run it in this folder on the Workstation:

    python3 check.py                          reads notes.md and job.json beside it
    python3 check.py <notes file> [<job file>] reads other files (the answer's, for the course team)

It reads what the learner wrote and the job file they changed. It never runs a databricks command
and calls no model.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHOWN = 6  # the things left that one run prints, in the order of the steps
WHY_SAME = re.compile(r"\b(same|overwrit\w*|rewrit\w*|replac\w*|files?)\b", re.IGNORECASE)


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


def number(text: str) -> int | None:
    """Read a whole number the learner typed, commas allowed; None when it is not one."""
    typed = text.replace(",", "").strip("` ")
    return int(typed) if re.fullmatch(r"\d+", typed) else None


def job_left(path: Path) -> list[str]:
    """What is left in the job file (step 2).

    Args:
        path: job.json.

    Returns:
        One line per problem.
    """
    try:
        job = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"job.json is not valid JSON ({error.msg}, line {error.lineno}). Step 2."]
    tasks = job.get("tasks") or [{}]
    task = tasks[0].get("notebook_task") or {}
    path_text = str(task.get("notebook_path", ""))
    out = []
    if not re.search(r"learner_\d+$", str(job.get("run_name", ""))):
        out.append("job.json: run_name still needs your learner number in place of NN. Step 2.")
    if "YOUR_USER_NAME" in path_text or not path_text.startswith("/Workspace/Users/"):
        out.append("job.json: notebook_path still needs your user name in place of YOUR_USER_NAME. Step 2.")
    if len(tasks) != 1 or tasks[0].get("task_key") != "features" or "/week-03/day-03/" not in path_text \
            or task.get("source") != "WORKSPACE":
        out.append("job.json: change only the two values. Run git restore job.json and start step 2 again.")
    return out


def run_left(notes: dict[str, str]) -> list[str]:
    """What is left in steps 1 and 3 to 5 of notes.md."""
    out = []
    if number(notes.get("features_before", "")) is None:
        out.append("features_before: write the count the SQL editor shows, before the run. Step 1.")
    predict = notes.get("predict_after", "")
    if len(words(predict)) < 5 or not WHY_SAME.search(predict):
        out.append("predict_after: write your prediction and why, 5 words or more, from how the notebook writes its tables. Step 1.")
    if notes.get("json_exit") != "0":
        out.append("json_exit: write the number that echo $? prints after the JSON check. Step 2.")
    if number(notes.get("run_id", "")) is None:
        out.append("run_id: write the run id that jobs submit prints, digits only. Step 3.")
    if notes.get("submit_exit") != "0":
        out.append("submit_exit: write the number that echo $? prints after jobs submit. Step 3.")
    if notes.get("final_state", "").upper() != "TERMINATED":
        out.append("final_state: the run has not ended yet. Run jobs get-run again until state is TERMINATED. Step 4.")
        return out
    code = notes.get("end_code", "").upper()
    if not code:
        out.append("end_code: write the code under termination_details. Step 4.")
    elif code != "SUCCESS":
        if not notes.get("failed_task"):
            out.append("failed_task: write the task_key of the task that did not succeed. Step 4.")
        if len(words(notes.get("error", ""))) < 5:
            out.append("error: copy the message that tells why the run ended. Step 4.")
        return out
    for key in ("failed_task", "error"):
        if notes.get(key, "").strip("` ").lower() != "none":
            out.append(f"{key}: the run ended with SUCCESS, so write none. Step 4.")
    if number(notes.get("features_after", "")) is None:
        out.append("features_after: write the count the SQL editor shows after the run. Step 5.")
    if len(words(notes.get("compare", ""))) < 5:
        out.append("compare: write one sentence, 5 words or more: the same count or not, and why. Step 5.")
    return out


def report(notes: dict[str, str], job_file: Path) -> str:
    """Return what the check prints: Done, or Not yet with each thing left.

    Args:
        notes: the learner's notes, from read_notes.
        job_file: the job file the learner changed.
    """
    left = job_left(job_file) + run_left(notes)
    if left:
        shown = ["- " + line for line in left[:SHOWN]]
        more = [f"- and {len(left) - SHOWN} more, after these."] if len(left) > SHOWN else []
        return "\n".join([f"Not yet: {len(left)} left."] + shown + more)
    if notes["end_code"].upper() != "SUCCESS":
        return (f"Done: run {notes['run_id']} ended with {notes['end_code']}; you have its task and its error. "
                "Show them to the trainer.")
    return (f"Done: run {notes['run_id']} ended with SUCCESS; features held {notes['features_before']} rows "
            f"before and {notes['features_after']} after.")


if __name__ == "__main__":
    notes_file = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "notes.md"
    job_file = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "job.json"
    print(report(read_notes(notes_file), job_file))
