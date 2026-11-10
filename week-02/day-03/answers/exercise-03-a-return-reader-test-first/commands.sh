#!/bin/sh
# Exercise 3's answer, applied and checked with no model call: sh week-02/day-03/answers/exercise-03-a-return-reader-test-first/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ again, installs the skill as step 2 does (this needs internet access), writes the
# reader and its tests, makes the commit of cell 2, then runs the check (cell 3).
set -e
EX=week-02/day-03/exercise-03-a-return-reader-test-first
ANSWER=week-02/day-03/answers/exercise-03-a-return-reader-test-first
python3 reset.py exercise-03-a-return-reader-test-first
(cd "$EX/lab" && npx --yes skills@1.7.4 add https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/test-driven-development --agent codex --yes > /dev/null)
cp "$ANSWER/files/form1040.py" "$EX/lab/form1040.py"
cp "$ANSWER/files/tests/test_form1040.py" "$EX/lab/tests/test_form1040.py"
(cd "$EX/lab" && git add form1040.py tests/test_form1040.py && git commit -q -m "Read three Form 1040 values, test first")
python3 "$EX/check.py"
