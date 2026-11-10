# Exercise 2: the kept run

- Date: 2026-11-10, 13:25:32 to 13:26:02 UTC.
- Agent: Claude Code 2.1.322, model sonnet, stood in for Codex, which is not installed on that machine. Claude Code does not read `AGENTS.md` or `.agents/skills` by itself, so the run put `AGENTS.md` (and, for exercise 3, the skill's `SKILL.md`) in its system prompt.
- Where: a fresh build of `lab` in a checkout of this repository on a macOS laptop, Python 3.12, with the course environment active. Not yet in the class's hosted Workstation.
- Command, in `lab`: `claude -p 'In paths.csv, write the path of each of the three fields in its path column, for returns/sample-return.xml. Write each path in ElementTree path syntax, from the root element Return, one step per element, with the prefixes efile: and course: that AGENTS.md gives. Check each path with ElementTree find, but print only the tag each path reaches, never a value. Leave the label column empty.'`, allowed to read and edit files and run `python -c`. 7 turns.

## What it did

It wrote the three paths of `files/paths.csv`, word for word, and left the labels empty. It noted the second `WagesAmt`: "the XML has a second `WagesAmt`, under `IRSW2`. The path goes through `IRS1040`, so it reaches the Form 1040 one." Its own check of the paths did not run, as its command fell outside what the run allowed; cell 2 and the check found each path reaches its field. The labels, `broken.xml` and `parse-error.txt` are the learner's, written by hand.

## Agent steps not tested with Codex

- Codex's question about trusting the folder, and `/quit`.
