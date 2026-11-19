#!/bin/sh
# Exercise 2's answer, checked with no Databricks and no model call:
#   sh week-04/day-01/answers/exercise-02-baseline-accuracy/commands.sh
# Run it from the course folder. It loads the week's five tables into DuckDB, a stand-in for Spark
# (week-04/day-01/answers/stand_in.py), and runs every code cell of the exercise's starting
# notebook (its check prints Not yet), then of exercise.ipynb beside this file (it prints Done:).
# In Databricks, the notebook's check cell runs the same check.py against the live tables.
set -e
uv run --no-project --python 3.12 --with duckdb==1.4.3 --with pandas==3.1.1 python week-04/day-01/answers/stand_in.py exercise-02-baseline-accuracy
