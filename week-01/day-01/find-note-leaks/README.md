# 1.1 Find note leaks

Find and close three disclosure paths in an agent's change while preserving the extractor's behavior.

A teammate's coding agent added handling for bad model replies. All six tests pass, but the change exposes note data. Review it before it is merged. The “real note” in this scenario is fictional course data.

## Start

Follow the [Day 1 setup](../README.md). Work by hand, without AI tools. These commands create the workspace only if it is missing, then enter it:

```sh
test -d ~/practice/week-01/day-01/find-note-leaks/extractor/.git || python3 ~/practice/reset.py find-note-leaks
cd ~/practice/week-01/day-01/find-note-leaks/extractor
```

All paths below are relative to `extractor/`. The course team's version is on `main`; the agent's change is tagged `agent-draft`.

## Review and fix

```sh
git show --stat agent-draft
python3 -m pytest -q
```

Expect four changed files and `6 passed`. Passing tests do not establish that data is safe. Use section 1.1 of the notebook to explain each fix.

| Disclosure path | Change to make |
|---|---|
| The fallback in `extractor.py` sends notes to `inference.example.net`. | Replace the `ask_fallback` call with `ask(SYSTEM_PROMPT, message, SCHEMA)` and remove the unused fallback code and imports. |
| A failure log includes the whole note. | Log only `note_id(note_text)`, without note text or reply values. |
| `tests/fixtures/two_amounts.txt` represents a real note with identifiers removed. | Replace it with course note `notes/0122.txt`, preserving the two-amount test case. |

Save your changes, then commit and check:

```sh
git add -A
git commit -m "Close the paths in the agent's change"
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. The check uses a fake model and blocks network access.

## Reflect

Why did the tests pass with these leaks present? Where does a replaced fixture remain in Git history, and what would you do if the branch had already been pushed?

[Worked answer](../answers/find-note-leaks/) · [Start over](../../../README.md#start-an-exercise-again)
