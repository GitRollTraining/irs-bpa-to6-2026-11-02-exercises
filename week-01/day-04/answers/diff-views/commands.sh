# The answer to "4.3 Read every diff view".
# Run it from week-01/day-04/diff-views/lab, after python3 reset.py diff-views in the course folder:
#   sh ../../answers/diff-views/commands.sh
# It does the rows of the exercise's table, in order, and runs the check, which prints Done:.
# decisions.md gives the reason for each row.
set -e

cat docs/directing-prompt.md

git --no-pager diff --name-status          # Row 1. M extractor.py: only the change that is not staged
git --no-pager diff HEAD --name-status     # Row 2. All three files. The directing prompt allows two of them.

git restore --staged prompts/system.txt    # Its change stays on disk, in no commit.
git add extractor.py
git --no-pager diff --staged --name-status # Row 3. extractor.py and tests/test_extractor.py: what the commit holds
git commit -q -m "Fail a reply whose amount is negative"

git --no-pager diff HEAD^ HEAD --name-status   # Row 4. The same two files

python3 ../check.py
