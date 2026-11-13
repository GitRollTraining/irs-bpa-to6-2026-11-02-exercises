#!/bin/sh
# Exercise 4's answer, checked with no Databricks and no model call:
#   sh week-03/day-03/answers/exercise-04-selection-day-and-split/commands.sh
# Run it from the course folder. It runs the exercise's check on the notebook's starting state
# (it prints Not yet), then on values.json beside this file (it prints Done:). values.json holds
# the facts the check reads from the answer's tables, as a stand-in in plain Python computed them
# from the course's return files (week-03/setup/day-03-course-data.py). In Databricks, the
# notebook's check cell reads the same facts from the tables in your schema.
set -e
python3 week-03/day-03/exercise-04-selection-day-and-split/check.py --start
python3 week-03/day-03/exercise-04-selection-day-and-split/check.py week-03/day-03/answers/exercise-04-selection-day-and-split/values.json
