#!/bin/sh
# Exercise 2's answer, applied and checked with no model call: sh week-02/day-02/answers/exercise-02-test-plan-to-branch-coverage/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ again, writes the answer's test plan and the kept run's tests (with the plan's
# corrected row), runs coverage as cell 4 does, then runs the check (cell 5).
set -e
EX=week-02/day-02/exercise-02-test-plan-to-branch-coverage
ANSWER=week-02/day-02/answers/exercise-02-test-plan-to-branch-coverage
python3 reset.py exercise-02-test-plan-to-branch-coverage
cp "$ANSWER/files/TEST_PLAN.md" "$EX/lab/TEST_PLAN.md"
cp "$ANSWER/files/tests/test_rules.py" "$EX/lab/tests/test_rules.py"
(cd "$EX/lab" && python3 -m coverage run --branch -m pytest -q -p no:cacheprovider > /dev/null && python3 -m coverage report)
python3 "$EX/check.py"
