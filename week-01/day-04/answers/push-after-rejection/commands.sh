# The answer to "4.2 Push after a rejection".
# Run it from week-01/day-04/push-after-rejection/extractor, after
# python3 reset.py push-after-rejection in the course folder:
#   sh ../../answers/push-after-rejection/commands.sh
# It runs the commands of the steps in order. Then it runs the check, which prints Done:.
# decisions.md gives each answer, its reason, and what else the check accepts.
set -e

# Review: your commit, with one file changed: tests/test_extractor.py.
git show --stat HEAD

# Check the remote: the (fetch) line names shared.git, the (push) line mirror.git.
git remote -v
# Set the push line.
git remote set-url --push origin ../shared.git
git remote -v
# Push: the lab's remote rejects it, as your teammate pushed first.
if git push; then echo "Not expected: the push was not rejected."; exit 1; fi
# Fetch, read what came in, merge, and push again.
git fetch
git show --stat origin/main
git merge --no-edit origin/main
git push

# Check.
python3 ../check.py
