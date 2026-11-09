#!/bin/sh
# Exercise 1's answer, applied and checked with no model call: sh week-02/day-01/answers/exercise-01-fix-a-wrong-value/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It copies the kept run's change into the exercise's folder, then runs the notebook's check (cell 3).
set -e
EX=week-02/day-01/exercise-01-fix-a-wrong-value
ANSWER=week-02/day-01/answers/exercise-01-fix-a-wrong-value
cp "$ANSWER/reference-app/templates/case.html" "$EX/reference-app/templates/case.html"
python - "$EX" <<'PY'
import json, os, sys
folder = sys.argv[1]
cell = next(c for c in json.load(open(f"{folder}/exercise.ipynb"))["cells"] if c["id"].endswith("-check"))
os.chdir(f"{folder}/reference-app")
sys.path.insert(0, os.getcwd())
exec("".join(line for line in cell["source"] if not line.startswith("%")))
PY
