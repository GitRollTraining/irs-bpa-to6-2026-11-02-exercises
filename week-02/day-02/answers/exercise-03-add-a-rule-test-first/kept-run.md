# Exercise 3: the kept run

- Date: 2026-11-09, 16:09 to 16:10 UTC.
- Where: a fresh build of `lab` in a checkout of this repository on a macOS laptop, Python 3.12, with the course environment active. Not yet in the class's hosted Workstation.
- Install: the `npx` command of step 2, in `lab`. It printed `Installed 1 skill` and `Done!`, and wrote `.agents/skills/test-driven-development/` (`SKILL.md`, `writing-good-tests.md`, `agents/openai.yaml`) and `skills-lock.json`.
- Agent: Claude Code 2.1.319 stood in for Codex, which was not installed on that machine. Claude Code does not read `.agents/skills`, so the run put the skill's `SKILL.md` in its system prompt.
- Command, in `lab`: `claude -p '$test-driven-development Add this rule to penalty_for ... Do not commit.' --append-system-prompt "<SKILL.md>" --permission-mode acceptEdits --allowedTools "Read,Glob,Grep,Write,Edit,Bash(python -m pytest*),Bash(pytest*),Bash(python3 -m pytest*)"`. 9 turns.
- A try before it, with the course environment not active, wrote the test and stopped: it could not run pytest, so it could not watch the test fail. We set it aside and built `lab` again.

## What it did

It wrote the test first and ran it: "the new test failed with `80.0 == 0` before the rule existed." Then it added the rule to `penalty_for`, and all 9 tests passed. It said that the older `penalty_for` test now reads the real `data/relief_areas.txt`. Its request named only "the test", so it stubbed only the new one. The request in step 3 now says "every test that calls `penalty_for`".

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- `$test-driven-development`, which makes Codex load the skill from `.agents/skills`.
- `/quit`.
