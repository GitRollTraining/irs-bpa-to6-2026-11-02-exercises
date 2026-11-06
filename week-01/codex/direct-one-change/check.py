"""The done check for this exercise. From work/, run: python3 ../check.py

It reads Git and record.md in work/, and runs the project's tests. It prints Done: when a commit after
the start holds AGENTS.md with the tests line, a changed test file and days in parse_duration; the
tests pass; nothing is left uncommitted; and each line of record.md is filled in. Otherwise it names
the first thing missing. It starts no coding agent, calls no model and needs no network. It does not
ask who wrote the code.
"""
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE / "work"
START = WORK / ".git" / "info" / "exercise-start"
RECORD = WORK / "record.md"
LINE = "Run the tests before you say a change is done."
FIELDS = ("Model", "Approval", "Sandbox", "Prompt", "Checked in /diff", "Test result")
DAYS = ("2d", 172800)  # the feature: a duration in days, and its seconds


def run(*command: str) -> subprocess.CompletedProcess:
    """Run one command in work/ and keep what it prints.

    Args:
        *command: The program and its arguments.

    Returns:
        The finished command, with its exit code, output and errors.
    """
    return subprocess.run(command, cwd=WORK, capture_output=True, text=True)


def plain(text: str) -> str:
    """Text in lower case, without Markdown marks, quotes or full stops, and with single spaces."""
    return " ".join(re.sub(r"[`*_\"'.]", "", text).lower().split())


def record_fields(text: str) -> dict:
    """Each line of record.md, as {name: what follows its colon, with the lines below it}."""
    values, name = {}, None
    for line in text.splitlines():
        found = next((f for f in FIELDS if line.strip().lower().startswith(f.lower() + ":")), None)
        if found:
            name = found
            values[name] = line.strip()[len(found) + 1:].strip()
        elif name and line.strip():
            values[name] = (values[name] + " " + line.strip()).strip()
    return values


def first_missing() -> str | None:
    """The first thing the exercise still needs, in words, or None when nothing is missing."""
    if not START.is_file() or run("git", "cat-file", "-e", START.read_text().strip() + "^{commit}").returncode:
        return "there is no work/ from the start. From the exercise folder, run: python3 start.py"
    start = START.read_text().strip()
    if run("git", "rev-parse", "HEAD").stdout.strip() == start:
        return "work/ has no commit after the start. Commit the change: git add -A, then git commit."
    if run("git", "merge-base", "--is-ancestor", start, "HEAD").returncode:
        return ("the last commit does not follow the start commit. From the exercise folder, rename work/ "
                "(mv work work-old) and run python3 start.py.")
    agents = run("git", "show", "HEAD:AGENTS.md")
    if agents.returncode:
        return "the last commit has no AGENTS.md. Type /init in Codex, keep the file, and commit it."
    if plain(LINE) not in plain(agents.stdout):
        return f'AGENTS.md in the last commit does not have the line "{LINE}" Add it, and commit.'
    changed = run("git", "diff", "--name-only", start, "HEAD").stdout.split()
    if not any(pathlib.PurePath(path).name.startswith("test_") for path in changed):
        return "the commits after the start change no test file. Ask Codex for a test of days, and commit it."
    days = run(sys.executable, "-c", f"from durations import parse_duration; print(parse_duration({DAYS[0]!r}))")
    if days.stdout.strip() != str(DAYS[1]):
        got = days.stdout.strip() or (days.stderr.strip().splitlines() or ["nothing"])[-1]
        return f'parse_duration("{DAYS[0]}") should return {DAYS[1]}; it gave: {got}'
    tests = run(sys.executable, "-m", "pytest", "-q")
    if "No module named pytest" in tests.stderr:
        return ("this Python has no pytest. In the course folder, run source .venv/bin/activate, "
                "then run the check again.")
    if tests.returncode:
        last = (tests.stdout.strip().splitlines() or ["no output"])[-1]
        return f"the tests fail: {last} Run python3 -m pytest -q to see which."
    left = [line[3:] for line in run("git", "status", "--porcelain").stdout.splitlines() if line.strip()]
    if left:
        return f"work/ has changes that are not committed: {', '.join(left)}. Commit them, or undo them."
    if not RECORD.is_file():
        return "record.md is missing. Copy it again: cp ../files/record.md record.md"
    values = record_fields(RECORD.read_text(encoding="utf-8", errors="replace"))
    for name in FIELDS:
        if not values.get(name):
            return f'record.md: fill in the line "{name}:".'
    return None


def main() -> None:
    """Print Done: when nothing is missing; otherwise print the first thing missing and exit 1."""
    missing = first_missing()
    if missing:
        print("Not yet: " + missing)
        sys.exit(1)
    print("Done: a commit after the start adds days with a test, holds AGENTS.md, and the tests pass; "
          "record.md is filled in.")


if __name__ == "__main__":
    main()
