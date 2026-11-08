# Exercise 1: the kept run

- Date: 2026-11-08 18:27 UTC.
- Where: a fresh clone of this repository on a macOS laptop, Python 3.12 and 3.10. Not yet in the class's hosted Workstation.
- Agent: Claude Code 2.1.319 stood in for Codex, which was not installed on that machine. One run, 13 turns.
- Command, in `week-02/day-01/exercise-01-fix-a-wrong-value/reference-app`: `claude -p "<the request in step 2, word for word>" --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Edit,Bash(pytest:*),Bash(python -m pytest:*)"`

## What it changed

```
templates/case.html:13
-  <dt>Balance due</dt><dd>{{ case.assessed | money }}</dd>
+  <dt>Balance due</dt><dd>{{ case.balance_due | money }}</dd>
```

## Its reply, in short

The template filled the Balance due row with the assessed amount. The calculation in `cases.py` was already right. It did not touch `data/cases.json`. It could not run the tests or load the page, because those commands were not approved in its run.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- Codex's permission prompts with `--sandbox read-only --ask-for-approval on-request`.
- `/quit`.
- Codex's own edit: the change above is Claude Code's.

## After the run

- The app on port 5055: the page of CS-2026-0001 shows `Balance due $12,250`.
- The notebook's cells, run in order in a kernel, with this change: cell 3 prints `Done:` on Python 3.12 and 3.10.
- After `reset.py exercise-01-fix-a-wrong-value`: cell 3 prints `Not yet: 1 left.`
- In a clone made before week 2 and given it by `git pull`: `Not yet: 1 left.` on the start, `Done:` with the change, `Not yet: 1 left.` after the reset.
