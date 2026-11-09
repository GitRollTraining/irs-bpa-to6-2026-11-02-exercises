# Exercise 2: the kept run

- Date: 2026-11-09, 16:07 UTC.
- Where: a fresh build of `lab` in a checkout of this repository on a macOS laptop, Python 3.12. Not yet in the class's hosted Workstation.
- Agent: Claude Code 2.1.319 stood in for Codex, which was not installed on that machine.
- Command, in `lab` after the answer's plan was written (with its `penalty_for` row at 40): `claude -p '<the folded request of step 3>' --permission-mode acceptEdits --allowedTools "Read,Glob,Grep,Write,Edit,Bash(python -m pytest*),Bash(pytest*)"`. The run could not start pytest, as the course environment was not active in its shell.

## What it wrote

`tests/test_rules.py`, the file `files/tests/test_rules.codex.py`: one test with six `pytest.param` rows, one test with `pytest.raises` for -1 months, and one test of `penalty_for`. Each expected value is the plan's, 40 among them. With the plan's row at 40, 1 test failed and 7 passed. With the row at 80, all 8 pass, and `coverage report` shows 100 percent of the lines and branches of `rules.py`. On a copy with the cap at 9 months, 2 tests fail.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- `/quit`.
