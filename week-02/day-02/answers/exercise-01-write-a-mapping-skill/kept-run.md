# Exercise 1: the kept run

- Date: 2026-11-09, 16:04 to 16:05 UTC.
- Where: a fresh build of `lab` (`python3 start.py`) in a checkout of this repository on a macOS laptop, Python 3.12. Not yet in the class's hosted Workstation.
- Agent: Claude Code 2.1.319 stood in for Codex, which was not installed on that machine. Claude Code does not read `.agents/skills`, so the run put the skill's text in its system prompt.
- Command, in `lab` after the answer's `SKILL.md` was written: `claude -p '$map-codebase Map this codebase.' --append-system-prompt "<the skill's text>" --permission-mode acceptEdits --allowedTools "Read,Glob,Grep,Write,Edit"`. 15 turns.
- Two tries before it were set aside: one in a folder the agent may not write to, and one on an earlier `writer.py` that had no import inside a function.

## What it wrote

`CODEMAP.md`, the file `files/CODEMAP.codex.md`, with the five sections. Its `## Imports` had all 7 arrows, the import inside `write_report` among them. Its `## Risky spots` named `settings.py`.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- `$map-codebase`, which makes Codex load the skill from `.agents/skills`.
- `/quit`.
