#!/bin/sh
# Exercise 1's answer, checked with no Databricks and no model call:
#   sh week-03/day-02/answers/exercise-01-tests-that-fail-the-dirty-batch/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting values
# (it prints Not yet), then on the kept answer, values.json beside this file (it ends with Done:).
# The batches come from the setup's made-up rows, week-03/setup/day-02-course-data.py.
# In Databricks, the notebook's check cell runs the same check against the live tables.
set -e
python3 week-03/day-02/exercise-01-tests-that-fail-the-dirty-batch/check.py --start
python3 week-03/day-02/exercise-01-tests-that-fail-the-dirty-batch/check.py week-03/day-02/answers/exercise-01-tests-that-fail-the-dirty-batch/values.json
