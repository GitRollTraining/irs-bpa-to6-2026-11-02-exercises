#!/bin/sh
# Exercise 3's answer, applied and checked with no model call: sh week-02/day-01/answers/exercise-03-use-a-skill/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It installs the skill into the exercise's folder as step 2 does (this needs internet access and Node.js),
# copies the kept run's three plan files and changes, then runs the notebook's check (cell 4).
set -e
EX=week-02/day-01/exercise-03-use-a-skill
ANSWER=week-02/day-01/answers/exercise-03-use-a-skill
(cd "$EX/reference-app" && npx --yes skills@1.7.4 add OthmanAdi/planning-with-files --skill planning-with-files --agent codex --yes > /dev/null)
sleep 1
for f in task_plan.md findings.md progress.md cases.py templates/base.html templates/list.html tests/test_cases.py; do
  cp "$ANSWER/reference-app/$f" "$EX/reference-app/$f"
done
python - "$EX" <<'PY'
import json, os, sys
folder = sys.argv[1]
cell = next(c for c in json.load(open(f"{folder}/exercise.ipynb"))["cells"] if c["id"].endswith("-check"))
os.chdir(f"{folder}/reference-app")
sys.path.insert(0, os.getcwd())
exec("".join(line for line in cell["source"] if not line.startswith("%")))
PY
