# The answer to "Classify ten uses of AI tools proposed for the extractor's pilot, and route the ones
# not yours to decide". Run it from ~/practice/week-01/day-01/data-rules-check/lab, after
# python3 ~/practice/reset.py data-rules-check:
#   sh ../../answers/data-rules-check/commands.sh
# As the exercise's steps do, it writes the answers, commits them before any AI tool touches the
# repository, and runs the check, which prints Done:.
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

# The answers: the file as supplied, with Permitted?, Who decides and Why written for each use.
cp "$ANSWER/data-rules-check.md" docs/data-rules-check.md
git add docs/data-rules-check.md
git commit -q -m "Answer the data-rules check for the pilot's ten proposed uses, before any AI tool"
git log --oneline   # your commit above the course team's, and no commit an AI tool made before it

python3 ../check.py
