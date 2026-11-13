#!/bin/sh
# Exercise 1's answer, checked with no Databricks and no model call:
#   sh week-03/day-04/answers/exercise-01-cli-tour/commands.sh
# Run it from the course folder. It runs the exercise's check on the starting notes (it prints
# Not yet), then on the kept answer, notes.md beside this file (it prints Done:).
# The column facts come from the setup's made-up rows, week-03/setup/day-01-course-data.py.
# On the Workstation, the learner runs the same check in the exercise folder: python3 check.py
set -e
python3 week-03/day-04/exercise-01-cli-tour/check.py week-03/day-04/exercise-01-cli-tour/notes.md
python3 week-03/day-04/exercise-01-cli-tour/check.py week-03/day-04/answers/exercise-01-cli-tour/notes.md
