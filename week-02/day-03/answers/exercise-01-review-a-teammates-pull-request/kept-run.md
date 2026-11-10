# Exercise 1: the kept run

- Date: 2026-11-10, 13:23:57 to 13:24:42 UTC.
- Agent: Claude Code 2.1.322, model sonnet, stood in for Codex, which is not installed on that machine. Claude Code does not read `AGENTS.md` or `.agents/skills` by itself, so the run put `AGENTS.md` (and, for exercise 3, the skill's `SKILL.md`) in its system prompt.
- Where: a fresh build of `lab` in a checkout of this repository on a macOS laptop, Python 3.12, with the course environment active. Not yet in the class's hosted Workstation.
- Steps 2 and 3 ran as `commands.sh` runs them; then `teammate.py` pushed `add-penalty-cap`, and the review ran on that branch.
- Command, in `lab` on `add-penalty-cap`: `claude -p 'Review the changes on this branch against the base branch main (git diff main...HEAD), as a code reviewer. Report each issue you find, with where it is and why. Do not change any file.'`, allowed to read files and run `git diff`, `git log`, `git show` and pytest. 5 turns.

## What it found

Its verdict: "3 issues. Fix the missing test and the speculative class first." It cited the rules by number: rule 4, "the cap has no test"; rule 3, "the class builds things nothing uses"; rule 1, "A class is not how this file is built"; rule 2, that no account in the data can reach 500; and rule 5, "passes. 24 added lines, one change." The comments copied into `files/review.md` are these, shortened.

## Agent steps not tested with Codex

- Codex's question about trusting the folder.
- `/review` and its choice of a base branch: the run asked for a review against `main` in its prompt.
- Whether Codex's `/review` cites the rules of `AGENTS.md` by number as this run did.
- `/quit`.
