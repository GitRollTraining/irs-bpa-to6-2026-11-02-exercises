# The answer to "Review a coding agent's change, and close every place a note leaks".
# Run it from extractor/, after python3 ~/practice/reset.py find-note-leaks:
#   sh ../../answers/find-note-leaks/commands.sh
# Each part ends in a commit, as the exercise's steps do; the last command prints Done:.
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

# The review, committed before the check shows anything.
cp "$ANSWER/REVIEW.md" REVIEW.md
git add REVIEW.md
git commit -q -m "Review agent-draft: five places a note's text or values leave the extractor"

# Close each path, keeping the retry (through the approved model) and the edge-case test (on note 0122);
# the prompt and the test the agent changed go back to main's.
cp "$ANSWER/extractor.py" extractor.py
cp "$ANSWER/tests/test_edge_cases.py" tests/test_edge_cases.py
git checkout main -- prompts/system.txt tests/test_extractor.py
git rm -q tests/fixtures/two_amounts.txt
git add extractor.py tests/test_edge_cases.py
git commit -q -m "Send only the note, and only to the approved model; log a failure by note and field"

# The rule, enforced by tests that fail on agent-draft.
cp "$ANSWER/tests/test_no_leaks.py" tests/test_no_leaks.py
git add tests/test_no_leaks.py
git commit -q -m "Test that a note reaches the approved model only, and no log, host or fixture"

python3 ../check.py
