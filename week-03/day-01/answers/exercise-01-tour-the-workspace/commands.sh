#!/bin/sh
# Exercise 1's answer, checked with no Databricks and no model call:
#   sh week-03/day-01/answers/exercise-01-tour-the-workspace/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting values
# (it prints Not yet), then on the kept answer, values.json beside this file (it prints Done:).
# The table facts come from the setup's made-up rows, week-03/setup/day-01-course-data.py.
# In Databricks, the notebook's check cell runs the same check against the live tables.
set -e
python3 week-03/day-01/exercise-01-tour-the-workspace/check.py --start
python3 week-03/day-01/exercise-01-tour-the-workspace/check.py week-03/day-01/answers/exercise-01-tour-the-workspace/values.json
