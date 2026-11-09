# Exercise 3: the kept run

- Date: 2026-11-08 18:37 UTC.
- Where: a fresh clone of this repository on a macOS laptop, Python 3.12 and 3.10, Node.js 24. Not yet in the class's hosted Workstation.
- The install ran for real: `npx skills@1.7.4 add OthmanAdi/planning-with-files --skill planning-with-files --agent codex --yes` printed `Installed 1 skill` and `Done!`. It put the skill in `reference-app/.agents/skills/planning-with-files` (with 22 scripts) and made `reference-app/skills-lock.json`.
- Agent: Claude Code 2.1.319 stood in for Codex, which was not installed on that machine. Claude Code does not read `.agents/skills` or `AGENTS.md`. So the request told it to read and follow the skill's `SKILL.md`. Its system prompt held the text of `AGENTS.md`. 33 turns.
- Command: `claude -p "Read .agents/skills/planning-with-files/SKILL.md and follow it to plan and make this change: on the case list page, show the words Review first next to each case whose selection score is 50 or more." --append-system-prompt "$(cat AGENTS.md)" --permission-mode acceptEdits --allowedTools "Read,Grep,Glob,Edit,Write,Bash(pytest),Bash(pytest *),Bash(python -m pytest*),Bash(python3 -m pytest*),Bash(ls*),Bash(date*)"`
- The run refused two of the skill's scripts (`init-session.sh`, `check-complete.sh`), as `sh` was not in the allowed commands. The agent wrote the three files from the skill's templates instead.

## What it wrote and changed

- `task_plan.md`, `findings.md`, `progress.md`.
- `cases.py`, `templates/list.html`, `templates/base.html`, `tests/test_cases.py` (two new tests).
- It ran `pytest`: 11 passed, then its 2 new tests failed before its change, then 13 passed.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- `$planning-with-files` in a Codex request.
- Codex reading `AGENTS.md` when a session starts.
- `/quit`.

## After the run

The cold read added a fourth check, the case list's label. We then checked again on 2026-11-09, in a fresh clone (Python 3.12) and in a clone given week 2 by `git pull` (Python 3.10):

- The start: `Not yet: 3 left.` (the skill, its three files, the label).
- `commands.sh` (the install, then the kept files): `Done:`.
- The notebook's cells in a kernel: `Done:`.
- After `reset.py exercise-03-use-a-skill`: `Not yet: 3 left.`, and `.agents/`, `skills-lock.json` and the three files are gone.

Written by hand, with the first three checks: only `task_plan.md` gave `Not yet: 1 left.` The three files in `.planning/2026-11-09-review-first/` gave `Done:`. A broken template gave `Not yet: 1 left.`, with the tests named.
