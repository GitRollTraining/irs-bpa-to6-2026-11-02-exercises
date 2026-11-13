#!/bin/sh
# Exercise 3's answer, checked with no Databricks, no Codex and no model call:
#   sh week-03/day-04/answers/exercise-03-codex-checks-the-sets/commands.sh
# Run it from the course folder. It runs the exercise's check on the starting notes (it prints
# Not yet), then on the kept answer, notes.md beside this file (it prints Done:). The kept answer
# judges the fallback transcript, week-03/setup/day-04-codex-transcript.md, the one run that does
# not vary; a learner's own Codex run is judged by the same rules.
set -e
python3 week-03/day-04/exercise-03-codex-checks-the-sets/check.py week-03/day-04/exercise-03-codex-checks-the-sets/notes.md
python3 week-03/day-04/exercise-03-codex-checks-the-sets/check.py week-03/day-04/answers/exercise-03-codex-checks-the-sets/notes.md
