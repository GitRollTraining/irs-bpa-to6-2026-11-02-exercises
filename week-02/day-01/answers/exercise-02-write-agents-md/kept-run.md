# Exercise 2: the kept run

- Date: 2026-11-08 18:33 UTC.
- Where: a fresh clone of this repository on a macOS laptop, Python 3.12 and 3.10. Not yet in the class's hosted Workstation.
- Agent: Claude Code 2.1.319 stood in for Codex, which was not installed on that machine. Claude Code does not read `AGENTS.md`. So the run put the file's text in its system prompt. Codex reads the file at the start of a session in the same way.
- Command, in `week-02/day-01/exercise-02-write-agents-md/reference-app`, after cell 2 wrote `AGENTS.md`: `claude -p "On the case list page, add a Balance due column after Status." --append-system-prompt "$(cat AGENTS.md)" --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Edit,Bash(pytest),Bash(pytest *),Bash(python -m pytest*),Bash(python3 -m pytest*)"`. 8 turns.
- A first try made the same kind of change but could not run the tests. Its allowed commands had no `python3 -m pytest`, so the run refused each of its three test runs. We set that try aside and put the folder back to the start.

## What it changed

- `templates/list.html`: a Balance due header after Status, and a cell for it in each row.
- `tests/test_cases.py`: one new test of the case list page.

## Its reply, in short

The case list has a Balance due column after Status. It ran `pytest` after the change, without a request: all 11 tests pass. No Python code changed.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- Codex reading `AGENTS.md` when a session starts.
- Codex's Auto setting in this folder.
- `/quit`.

## After the run

- Cell 4 prints `Done:` on Python 3.12 and 3.10.
- Written by hand: no test run gives `Not yet: 1 left.` A test run after the change gives `Done:`. A change after the test run gives `Not yet: 1 left.`
- After `reset.py exercise-02-write-agents-md`: `Not yet: 3 left.`
- In a clone made before week 2 and given it by `git pull`: the same results.
