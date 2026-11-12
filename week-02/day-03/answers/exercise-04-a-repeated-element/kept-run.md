# Exercise 4: the kept run

- Date: 2026-11-10, 13:26:12 to 13:26:36 UTC.
- Agent: Claude Code 2.1.322, model sonnet, stood in for Codex, which is not installed on that machine. Claude Code does not read `AGENTS.md` or `.agents/skills` by itself, so the run put `AGENTS.md` (and, for exercise 3, the skill's `SKILL.md`) in its system prompt.
- Where: a fresh build of `lab` in a checkout of this repository on a macOS laptop, Python 3.12, with the course environment active. Not yet in the class's hosted Workstation.
- Step 2 by hand: the test of `files/tests/test_form1040.py`; the tests then read `1 failed, 2 passed`.
- Command, in `lab`, for step 3 with Codex: `claude -p 'The new test in tests/test_form1040.py fails. Make it pass: write dependent_relationships in form1040.py, as its docstring says. Do not change the tests. Run the tests when you are done. Do not commit.'`. 7 turns.

## What it did

"`dependent_relationships` is written, and all 3 tests pass, including the new one." It returns "the `DependentRelationshipCd` text of each `DependentDetail`, in file order. A return with no dependent gives `[]`." Its `form1040.py` is `files/form1040.codex.py`. The commit and the check ran after it: `Done:`.
