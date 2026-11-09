#!/bin/sh
# Exercise 2's answer, applied and checked with no model call: sh week-02/day-01/answers/exercise-02-write-agents-md/commands.sh
# Run it from the course folder, with week 2's environment active (source reference-app/.venv/bin/activate).
# It copies the kept run's AGENTS.md and changes into the exercise's folder, runs pytest there as the
# kept run's agent did after its change, then runs the notebook's check (cell 4).
set -e
EX=week-02/day-01/exercise-02-write-agents-md
ANSWER=week-02/day-01/answers/exercise-02-write-agents-md
cp "$ANSWER/reference-app/AGENTS.md" "$EX/reference-app/AGENTS.md"
cp "$ANSWER/reference-app/templates/list.html" "$EX/reference-app/templates/list.html"
cp "$ANSWER/reference-app/tests/test_cases.py" "$EX/reference-app/tests/test_cases.py"
sleep 1
(cd "$EX/reference-app" && python -m pytest -q > /dev/null)
python - "$EX" <<'PY'
import json, os, sys
folder = sys.argv[1]
cell = next(c for c in json.load(open(f"{folder}/exercise.ipynb"))["cells"] if c["id"].endswith("-check"))
os.chdir(f"{folder}/reference-app")
sys.path.insert(0, os.getcwd())
exec("".join(line for line in cell["source"] if not line.startswith("%")))
PY
