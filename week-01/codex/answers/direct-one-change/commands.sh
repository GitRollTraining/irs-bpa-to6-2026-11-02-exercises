# The answer to "Direct Codex through one change". Not yet run in the workstation.
# It stands in for the Codex session with the files Codex would leave, commits them, and runs the
# check, which prints Done:.
# Run it from week-01/codex/direct-one-change/work, after python3 start.py in the exercise folder.
# The command:
#   sh ../../answers/direct-one-change/commands.sh
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

# The Codex session. No coding agent runs in this file. The copies stand in for /init's AGENTS.md,
# with the tests line kept, and for the change Codex makes after /plan: days in durations.py and a
# test for them. record.md holds the notes of the steps, as an example.
cp "$ANSWER/AGENTS.md" "$ANSWER/durations.py" "$ANSWER/test_durations.py" .
cp "$ANSWER/record.md" record.md

# The step inside Codex, !python3 -m pytest -q, run here in the terminal.
python3 -m pytest -q

# The commit after the task: the second checkpoint.
git status --short
git add -A
git commit -q -m "Accept days in parse_duration"
python3 ../check.py
