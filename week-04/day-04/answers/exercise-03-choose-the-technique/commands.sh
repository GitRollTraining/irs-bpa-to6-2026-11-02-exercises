#!/bin/sh
# Exercise 3's answer, checked with no Databricks and no model call:
#   sh week-04/day-04/answers/exercise-03-choose-the-technique/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting state
# (it prints Not yet), then on values.json beside this file (it prints Done:). values.json holds
# the text of the answer's cells 2 and 3, which is all the check reads. In Databricks, the
# notebook's cell 4 reads the same text from the notebook.
set -e
python3 week-04/day-04/exercise-03-choose-the-technique/check.py --start
python3 week-04/day-04/exercise-03-choose-the-technique/check.py week-04/day-04/answers/exercise-03-choose-the-technique/values.json
