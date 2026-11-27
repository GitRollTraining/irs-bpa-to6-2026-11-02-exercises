#!/bin/sh
# Exercise 1's answer, checked with no Databricks and no model call:
#   sh week-04/day-04/answers/exercise-01-explain-case-123/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting state
# (it prints Not yet), then on values.json beside this file (it prints Done:). values.json holds
# the facts the check reads from the answer's run, as a stand-in in plain Python computed them
# from the course's week 4 tables (week-04/setup/day-01-course-data.py). In Databricks, the
# notebook's cell 7 reads the same facts from the notebook.
set -e
python3 week-04/day-04/exercise-01-explain-case-123/check.py --start
python3 week-04/day-04/exercise-01-explain-case-123/check.py week-04/day-04/answers/exercise-01-explain-case-123/values.json
