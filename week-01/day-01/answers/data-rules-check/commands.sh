# The answer to "Classify four uses of AI tools with the data-rules check". Run it from
# ~/practice/week-01/day-01/data-rules-check/lab, after python3 ~/practice/reset.py data-rules-check:
#   sh ../../answers/data-rules-check/commands.sh
# As the exercise's steps do, it writes the answers, commits them, and runs the check, which prints Done:.
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

# The answers: the file as supplied, with Permitted?, Who decides and Why filled in for each use.
cp "$ANSWER/data-rules-check.md" docs/data-rules-check.md
git add docs/data-rules-check.md
git commit -q -m "Answer the data-rules check"
git log --oneline   # your commit above the course team's

python3 ../check.py
