#!/bin/sh
# Exercise 3's answer, checked with no Databricks and no model call:
#   sh week-03/day-02/answers/exercise-03-query-the-governed-batch-as-yourself/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting values
# (it prints Not yet), then on the kept answer, values.json beside this file (it ends with Done:).
# The batches come from the setup's made-up rows, week-03/setup/day-02-course-data.py.
# In Databricks, the notebook's check cell runs the same check against the live tables.
set -e
python3 week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/check.py --start
python3 week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/check.py week-03/day-02/answers/exercise-03-query-the-governed-batch-as-yourself/values-no-mask.json --plain
python3 week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/check.py week-03/day-02/answers/exercise-03-query-the-governed-batch-as-yourself/values.json
