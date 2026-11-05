# Direct Codex through one change

Have Codex add one feature with a test to a small Python project, then review and commit the change.

## What this measures

Whether you can steer Codex from prompt to commit: a four-part prompt, a yes or no to each command, your own read of the diff, and a commit.

## Prerequisites

- The Codex CLI, signed in.
- Git, with your name and email set.
- The course's Python environment, made with uv in the [setup](../../../README.md#set-up-once). It holds pytest.

## Setup

In a new terminal in the course folder, build the project if it is missing, then enter it:

```sh
source .venv/bin/activate
cd week-01/codex/direct-one-change
test -d work/.git || python3 start.py
cd work
```

`work/` is a small Git project: `durations.py`, where `parse_duration("1h30m")` returns 5400, and its tests. Its one commit is your checkpoint. Paths below start in `work/`. Your notes go in `record.md`, which Git ignores.

## Concepts

- **Four-part prompt:** goal, context, constraints, done when (deck 1.5).
- **Approval modes:** what Codex may do without asking you first (1.5).
- **`/diff`:** the Git diff inside Codex, read before you commit (1.4).
- **Git checkpoints:** a commit before and after a task, so you can go back (1.5).

## Direct the change

1. Run `codex --version`, then `codex`. If Codex asks whether you trust this folder, answer yes.
2. Type `/status`. Copy its model, approval policy and sandbox into `record.md`. If the approval is not Ask for approval, type `/permissions` and select the mode your screen calls Ask for approval (some versions say Auto).
3. Type `/init`. Make sure the `AGENTS.md` it drafts has this line: `Run the tests before you say a change is done.` Codex reads `AGENTS.md` when it starts, so the line guides later sessions.
4. Type `/plan`, then a prompt in four parts. Goal: `parse_duration` also accepts days, `d`, so `"2d"` returns 172800. Write the other three parts yourself; paste the prompt into `record.md`. Read the plan. If Codex asks to carry it out, say yes; if not, press Shift+Tab to leave plan mode and type `Carry out the plan.`
5. Read each command Codex asks to run. Say yes to reading files and running tests; say no to anything outside `work/`.
6. Type `/diff`. In `record.md`, write one thing it showed that you checked.
7. Type `!python3 -m pytest -q`. Copy its last line into `record.md`.
8. Type `/exit`, then commit and check:

```sh
git status --short
git add -A
git commit -m "Accept days in parse_duration"
python3 ../check.py
```

Finish when the check prints `Done:`.

## Reflect

Why commit before Codex starts and again after it finishes? What did `/diff` show that Codex's own summary did not?

[Worked answer](../answers/direct-one-change/) · Start over: from the exercise folder, `mv work work-old`, then `python3 start.py`.
