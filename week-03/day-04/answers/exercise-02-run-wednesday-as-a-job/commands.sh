#!/bin/sh
# Exercise 2's answer, checked with no Databricks and no model call:
#   sh week-03/day-04/answers/exercise-02-run-wednesday-as-a-job/commands.sh
# Run it from the course folder. It runs the exercise's check on the starting notes and job file
# (it prints Not yet), then makes the answer's job file, the start's with the two values a learner
# changes (learner 07; a made-up user name), and runs the check on it and the kept notes,
# notes.md beside this file (it prints Done:). The counts and the run id in notes.md are a
# stand-in: on the Workstation they come from the class workspace.
set -e
exercise=week-03/day-04/exercise-02-run-wednesday-as-a-job
answer=week-03/day-04/answers/exercise-02-run-wednesday-as-a-job
python3 "$exercise/check.py" "$exercise/notes.md" "$exercise/job.json"
work=$(mktemp -d)
sed -e 's/learner_NN/learner_07/' -e 's/YOUR_USER_NAME/learner-07@example.org/' "$exercise/job.json" > "$work/job.json"
python3 -m json.tool "$work/job.json" > /dev/null
python3 "$exercise/check.py" "$answer/notes.md" "$work/job.json"
