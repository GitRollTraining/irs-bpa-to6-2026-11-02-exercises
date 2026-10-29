# Exercise: Review a coding agent's change, and close every place a note leaks

After this exercise, you can close the paths that an agent's change opens for a note, and keep what the change was for.

**Scenario:** A teammate used a coding agent to change the case-notes extractor. The change makes the extractor handle bad replies from the model, and all its tests pass. But it opens three paths for a note. Fix the commit before anyone merges it into `main`.

**Success criterion:** from `extractor`, `python3 ../check.py` prints `Done:`.

**Where you work:** the folder `~/practice/week-01/day-01/find-note-leaks/extractor`, in VS Code and in a terminal. Each path in this exercise starts there. Do not use AI tools.

**Start from:** the folder `find-note-leaks`. Run `python3 ~/practice/reset.py find-note-leaks`. Then run `cd ~/practice/week-01/day-01/find-note-leaks/extractor`. To start again, run the same reset. The reset removes your commits.

**What you have:** in `extractor`, the course team's extractor on `main`, and the agent's commit on top of it, with the tag `agent-draft`. `../check.py` is the check. The week 1 chapter, section 1.1, has the rules.

## Steps

1. See the change. Run `git show --stat agent-draft` and `python3 -m pytest -q`. You should see one commit that changes four files, and `6 passed`.
2. Fix the three problems in the table by hand.
3. Commit, and run `python3 ../check.py`. You should see `Done:`. If you see `Not yet:`, fix what it names, and run the check again.

| Problem | The rule, in section 1.1 | Fix it by hand |
|---|---|---|
| 1. When a reply fails, `extractor.py` sends the note to `inference.example.net`, a model with no approval (lines 24 to 25, 59 to 63, and 77). | Federal taxpayer information is "Barred from unauthorized AI". | On line 77, call `ask(SYSTEM_PROMPT, message, SCHEMA)` in place of `ask_fallback(SYSTEM_PROMPT, message)`. Then remove lines 59 to 63, lines 24 to 25, and the lines `import urllib.request` and `import os`. |
| 2. When a reply fails, line 75 of `extractor.py` writes the whole note to `logs/extractor.log`. | "a log line that prints a whole note" is one of "the two paths the agent creates for you". | On line 75, remove the text of the note from the log line. Keep only `note_id(note_text)`. |
| 3. `tests/fixtures/two_amounts.txt` is a real note, with only its name and TIN removed. | A note without its name still "gives year, form, amount, date". | Replace the text of `tests/fixtures/two_amounts.txt` with the text of the course note `notes/0122.txt`. It also names two amounts, so the test still passes. |

**Answer:** `~/practice/week-01/day-01/answers/find-note-leaks/` holds the fixed files, and `commands.sh`, which ends with `Done:`.

## Afterwards, together

Which of the three paths would the agent never report? You replaced the real note in a new commit. Where is the real note still? What would you do if someone already pushed the branch?
