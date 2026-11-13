#!/bin/sh
# Exercise 1's answer, applied and checked with no model call: sh week-03/day-01/answers/exercise-01-the-question-the-list-each-verdict/commands.sh
# Run it from the course folder. It runs the exercise's check on the kept record, files/record.json,
# and leaves the exercise folder as the course gives it.
set -e
python3 week-03/day-01/exercise-01-the-question-the-list-each-verdict/check.py week-03/day-01/answers/exercise-01-the-question-the-list-each-verdict/files/record.json
