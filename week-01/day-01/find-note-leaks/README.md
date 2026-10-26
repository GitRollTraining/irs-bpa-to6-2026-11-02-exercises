# Exercise: Find and close the three places a note leaks from the extractor

After this you can find where a coding agent's draft lets a case note's text out, to a log, a model that is not approved or a test fixture, and close each path.

**Success criterion:** in the folder, `python3 check.py` prints `Done:`. It runs your `extract` on a failing reply for note 0147 with the network off, and passes when `extract` raises `ExtractionFailed` and tries no host, the log it writes, `logs/extractor.log`, names note 0147 and holds none of its text, every fixture is a course note, unchanged, and the tests pass. Until then it prints `Not yet:` and what is left.

**Where you work:** VS Code in your hosted workspace: `extractor.py` and `tests/fixtures/` in the folder `find-note-leaks`, and the terminal. AI tools: none.

**Start from:** the folder `find-note-leaks` in the practice kit: `cd ~/practice/week-01/day-01/find-note-leaks`, then `python3 check.py`, which prints `Not yet:` and the three places the note's text went. To get it again: `python3 ~/practice/reset.py find-note-leaks`.

## Steps

1. Find what wrote note 0147's text into `logs/extractor.log`, close that path, and run the check. You should see: `Not yet:` no longer naming the log.
2. Find what sends the note to the host the check names, close that path, and run the check. You should see: `Not yet:` naming only a fixture.
3. Find the fixture that is not a course note and close that path, keeping what its test checks; run `python3 -m pytest -q`. You should see: `3 passed`.
4. Run `python3 check.py`, then read `logs/extractor.log`. You should see: `Done:`, and a line naming note 0147 and why it failed, with none of its text.

**Answer:** your trainer has it, and shows it at the debrief.

## Afterwards, together

Which of the three paths would the agent never have raised on its own? Which of your searches could a machine run before every commit?
