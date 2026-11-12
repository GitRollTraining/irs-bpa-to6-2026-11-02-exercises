#!/bin/sh
# Exercise 1's answer, applied and checked with no model call: sh week-02/day-03/answers/exercise-01-review-a-teammates-pull-request/commands.sh
# Run it from the course folder, with the course environment active (source .venv/bin/activate).
# It builds lab/ and the team repository again, commits the rules on review-rules and pushes them
# (step 2), makes the teammate's requested change and squash-merges (step 3), has the teammate push
# add-penalty-cap and fetches it, writes the kept review (step 4), then runs the check (step 5).
set -e
EX=week-02/day-03/exercise-01-review-a-teammates-pull-request
ANSWER=week-02/day-03/answers/exercise-01-review-a-teammates-pull-request
python3 reset.py exercise-01-review-a-teammates-pull-request
cd "$EX/lab"
git switch -q -c review-rules
cp "../../../../$ANSWER/files/AGENTS.first-commit.md" AGENTS.md
git commit -q -am "Add Code Review Rules"
git push -q -u origin review-rules
cp "../../../../$ANSWER/files/AGENTS.md" AGENTS.md
git commit -q -am "Add a rule on pull request size"
git push -q
git switch -q main
git merge -q --squash review-rules
git commit -q -m "Add Code Review Rules"
git push -q
python3 ../teammate.py
git fetch -q
git switch -q add-penalty-cap
cp "../../../../$ANSWER/files/review.md" review.md
cd ../../../..
python3 "$EX/check.py"
