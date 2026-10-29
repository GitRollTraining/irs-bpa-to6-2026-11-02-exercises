# The answer to "Review a coding agent's change, and close every place a note leaks".
# Run it from extractor/, after python3 ~/practice/reset.py find-note-leaks:
#   sh ../../answers/find-note-leaks/commands.sh
# Each part ends in a commit, as the exercise's steps do; the last command prints Done:.
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

# Close each path, keeping the retry (through the approved model) and the edge-case test, whose fixture is now course note 0122.
cp "$ANSWER/extractor.py" extractor.py
cp notes/0122.txt tests/fixtures/two_amounts.txt
git add extractor.py tests/fixtures/two_amounts.txt
git commit -q -m "Send the note only to the approved model, and log a failure by its note only"


python3 ../check.py
