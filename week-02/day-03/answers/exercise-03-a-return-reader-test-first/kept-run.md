# Exercise 3: the kept run

- Date: 2026-11-10, 13:20:33 to 13:21:17 UTC.
- Agent: Claude Code 2.1.322, model sonnet, stood in for Codex, which is not installed on that machine. Claude Code does not read `AGENTS.md` or `.agents/skills` by itself, so the run put `AGENTS.md` (and, for exercise 3, the skill's `SKILL.md`) in its system prompt.
- Where: a fresh build of `lab` in a checkout of this repository on a macOS laptop, Python 3.12, with the course environment active. Not yet in the class's hosted Workstation.
- Install: the `npx` command of step 2, in `lab`. It printed `Installed 1 skill` and `Done!`.
- Command, in `lab`: the folded request of step 3, word for word, with the skill's `SKILL.md` in the system prompt, allowed to read and edit files and run pytest. 12 turns.

## What it did

"All 3 tests failed first with `NotImplementedError`, the stub's own error. After the implementation, all 3 passed." It added a third test of its own, a return whose Form 1040 has no `WagesAmt`, because "The sample's W-2 ... also has a `WagesAmt` of 52340, so an unscoped search would wrongly return it." Its files are `files/form1040.py` and `files/tests/test_form1040.codex.py`; `files/tests/test_form1040.py` is the two tests the steps ask for. The commit of cell 2 and the check ran after it: `Done:`.

## The gate

A second, fresh reader did the exercise from the notebook alone, on 2026-11-10: the tests went red, then green, and were committed, and it put a learner's time at 17 to 21 minutes of the 25.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- `$test-driven-development`, which makes Codex load the skill from `.agents/skills`.
- `/quit`.
