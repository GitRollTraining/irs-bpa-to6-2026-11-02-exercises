#!/bin/sh
# Exercise 3's answer, applied and checked with no model call: sh week-02/day-02/answers/exercise-03-add-a-rule-test-first/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ again, installs the skill as step 2 does (this needs internet access), writes the
# kept run's rule and tests, makes the commit of cell 3, then runs the check (cell 4).
set -e
EX=week-02/day-02/exercise-03-add-a-rule-test-first
ANSWER=week-02/day-02/answers/exercise-03-add-a-rule-test-first
python3 reset.py exercise-03-add-a-rule-test-first
(cd "$EX/lab" && npx --yes skills@1.7.4 add https://github.com/openai/plugins/tree/main/plugins/superpowers/skills/test-driven-development --agent codex --yes > /dev/null)
cp "$ANSWER/files/payment_job/rules.py" "$EX/lab/payment_job/rules.py"
cp "$ANSWER/files/tests/test_rules.py" "$EX/lab/tests/test_rules.py"
(cd "$EX/lab" && git add payment_job/rules.py tests/test_rules.py && git commit -q -m "Add the relief rule, test first")
python3 "$EX/check.py"
