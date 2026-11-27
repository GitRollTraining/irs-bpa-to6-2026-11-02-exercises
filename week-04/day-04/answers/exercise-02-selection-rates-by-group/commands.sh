#!/bin/sh
# Exercise 2's answer, checked with no Databricks and no model call:
#   sh week-04/day-04/answers/exercise-02-selection-rates-by-group/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting state
# (it prints Not yet), then on values.json beside this file (it prints Done:), then on
# values-without-proxy-step.json, the same answer with the optional last step (proxy segment) cut (it prints Done: too).
# Each JSON file holds the facts the check reads from the answer's run, as a stand-in in plain
# Python computed them from the course's week 4 tables (week-04/setup/day-01-course-data.py).
# In Databricks, the notebook's cell 5 reads the same facts from the notebook.
set -e
python3 week-04/day-04/exercise-02-selection-rates-by-group/check.py --start
python3 week-04/day-04/exercise-02-selection-rates-by-group/check.py week-04/day-04/answers/exercise-02-selection-rates-by-group/values.json
python3 week-04/day-04/exercise-02-selection-rates-by-group/check.py week-04/day-04/answers/exercise-02-selection-rates-by-group/values-without-proxy-step.json
