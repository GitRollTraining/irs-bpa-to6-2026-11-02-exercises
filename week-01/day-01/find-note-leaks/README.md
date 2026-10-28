# Exercise: Review a coding agent's change, and close every place a note leaks

After this you can find every path an agent's change opens for a note's text or values, close each while keeping what the change was for, and guard them with a test.

**Scenario:** A teammate's coding agent made the case-notes extractor "robust to bad model replies", and its tests pass. Review and fix its commit before it merges, as if the extractor were about to run on real notes. From: the chapter's case-notes extractor.

**Success criterion:** from `extractor`, `python3 ../check.py` prints `Done:`. Once your review is committed, it runs `extract` on three bad replies for note 0147 with a fake model and no network, and checks where the note's text went, that the agent's tests still pass, and that a test you added fails on `agent-draft`.

**Where you work:** VS Code in your hosted workspace: the repository `extractor`, and the terminal, inside it. AI tools: none.

**Start from:** the folder `find-note-leaks`: `python3 ~/practice/reset.py find-note-leaks`, which prints `find-note-leaks is back as it was supplied.` and leaves you on the agent's branch, `agent/robust-extractor`; then `cd ~/practice/week-01/day-01/find-note-leaks/extractor`. To get it again: the same reset; it removes your commits.

**What you have:** in `extractor`, the course team's extractor on `main` and the agent's commit, tagged `agent-draft`; `notes/`, the course's simulated notes, each marked "Synthetic filer"; `model.py`, the one approved model's route; `REVIEW.md`, your review; `../check.py`, the check. The week 1 chapter, sections 1.1, "Keep taxpayer and personal data out of every prompt, log and test fixture", and 1.2, "Work out what a federal rule requires of this task, and who decides".

## Steps

1. See what you review: `git log --oneline main..`, `git show --stat agent-draft`, `python3 -m pytest -q`. You should see: one commit, six files changed, `6 passed`.
2. Review before the check does: read `git diff main` and list in `REVIEW.md` each place a note's text or values leave other than through `model.py`, with file and line, destination and rule broken. Commit, then run `python3 ../check.py`. You should see: `Not yet:` and its findings; compare.
3. Close each path, keeping what the change was for where a rule allows; failures stay traceable to note and field. Commit as you go. You should see: `Not yet:` and one line, about your tests.
4. Make the rule machine-enforced: add a test that fails on `agent-draft` and passes on your fixes; commit; run the check. You should see: `Done:`, and a log you would accept on real notes.

**Answer:** `~/practice/week-01/day-01/answers/find-note-leaks/`: the kept review, fixed files and `commands.sh`, ending `Done:`.

## Afterwards, together

How many paths did your review find before the check? Which would the agent never have raised? Where else does your code repeat a value it rejects?
