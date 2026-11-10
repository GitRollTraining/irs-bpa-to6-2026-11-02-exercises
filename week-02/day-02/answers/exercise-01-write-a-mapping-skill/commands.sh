#!/bin/sh
# Exercise 1's answer, applied and checked with no model call: sh week-02/day-02/answers/exercise-01-write-a-mapping-skill/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ again, writes the answer's skill and the kept run's map, makes the two commits of
# cells 3 and 5, then runs the check (cell 6).
set -e
EX=week-02/day-02/exercise-01-write-a-mapping-skill
ANSWER=week-02/day-02/answers/exercise-01-write-a-mapping-skill
python3 reset.py exercise-01-write-a-mapping-skill
cp "$ANSWER/files/.agents/skills/map-codebase/SKILL.md" "$EX/lab/.agents/skills/map-codebase/SKILL.md"
cp "$ANSWER/files/CODEMAP.codex.md" "$EX/lab/CODEMAP.md"
(cd "$EX/lab" && git add -A && git commit -q -m "Map by Codex, as written")
cp "$ANSWER/files/CODEMAP.md" "$EX/lab/CODEMAP.md"
(cd "$EX/lab" && git add CODEMAP.md && git commit -q -m "Correct the map")
python3 "$EX/compare_map.py" pydeps payment_job --max-bacon 0
python3 "$EX/check.py"
