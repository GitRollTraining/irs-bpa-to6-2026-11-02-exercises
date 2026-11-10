#!/bin/sh
# Exercise 4's answer, applied and checked with no model call: sh week-02/day-03/answers/exercise-04-a-repeated-element/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ again, writes the test of step 2 and the function of step 3, makes the commit of
# cell 3, then runs the check (cell 4).
set -e
EX=week-02/day-03/exercise-04-a-repeated-element
ANSWER=week-02/day-03/answers/exercise-04-a-repeated-element
python3 reset.py exercise-04-a-repeated-element
cp "$ANSWER/files/tests/test_form1040.py" "$EX/lab/tests/test_form1040.py"
cp "$ANSWER/files/form1040.py" "$EX/lab/form1040.py"
(cd "$EX/lab" && git add form1040.py tests/test_form1040.py && git commit -q -m "Read each dependent's relationship, test first")
python3 "$EX/check.py"
