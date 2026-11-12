#!/bin/sh
# Exercise 2's answer, applied and checked with no model call: sh week-02/day-03/answers/exercise-02-read-a-return-by-its-paths/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ again, writes the kept run's paths with the labels of step 3, writes the broken copy
# of step 4 and the parser's line, then runs the check (cell 4).
set -e
EX=week-02/day-03/exercise-02-read-a-return-by-its-paths
ANSWER=week-02/day-03/answers/exercise-02-read-a-return-by-its-paths
python3 reset.py exercise-02-read-a-return-by-its-paths
cp "$ANSWER/files/paths.csv" "$EX/lab/paths.csv"
cp "$ANSWER/files/broken.xml" "$EX/lab/broken.xml"
cp "$ANSWER/files/parse-error.txt" "$EX/lab/parse-error.txt"
python3 "$EX/check.py"
