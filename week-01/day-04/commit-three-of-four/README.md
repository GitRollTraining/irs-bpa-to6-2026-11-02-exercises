# 4.1 Commit three of four changes

Commit only the three changes that you asked a coding agent for, and keep the extractor's log out of the history.

You asked a coding agent to log each failed reply by the note's number only. The agent changed four files and ran the extractor once.

## Start

Follow the [Day 4 setup](../README.md). Work by hand, without AI tools. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-04/commit-three-of-four/extractor/.git || python3 reset.py commit-three-of-four
cd week-01/day-04/commit-three-of-four/extractor
```

All paths below are relative to `extractor/`. `../agent-session.txt` holds your request and the agent's report.

## Stage and commit

```sh
git status --short
code ../agent-session.txt logs/extractor.log .gitignore
```

Expect four files marked `M`, changed, and `?? logs/`, which no commit holds. Use section 4.1 of the notebook to explain each change.

| Change | What to do |
|---|---|
| `extractor.py`, `tests/test_extractor.py`, `README.md`: a log line for each failed reply, its test and a `README.md` row, which you asked for. | Stage each. |
| `model.py`: a debugging print that you did not ask for. It wrote the whole note to `logs/extractor.log`. | Do not stage it. |
| `logs/`: the log of the agent's run, with that whole note in it. | Add the line `logs/` at the end of `.gitignore`. Stage `.gitignore`. |

<details><summary>Why each answer</summary>

| Change | Why, in section 4.1 |
|---|---|
| `extractor.py`, `tests/test_extractor.py`, `README.md`: a log line for each failed reply, its test and a `README.md` row, which you asked for. | `../agent-session.txt` asks for all three: a log line for each failed reply, a test and a `README.md` line. The table under "Skipping staging lets an agent's stray edit in.", row Who chooses: "You choose which changes go in". |
| `model.py`: a debugging print that you did not ask for. It wrote the whole note to `logs/extractor.log`. | Line 1 of `logs/extractor.log` holds the whole note, but you asked for "the note's number only". The change to `model.py`, a debugging print, wrote it. The same table, row The debugging print: with git add, then git commit, it "Can stay out". |
| `logs/`: the log of the agent's run, with that whole note in it. | A commit of `logs/` keeps a whole note in the history. Your line stops Git listing and adding `logs/`. Committed, it does so in each clone. The heading "Keep the logs out: a pushed commit is very hard to take back." Below it: "A .gitignore file lists patterns of files Git will not offer to add." |

</details>

Save `.gitignore`, then stage the four files by path:

```sh
git add extractor.py tests/test_extractor.py README.md .gitignore
git status --short
```

Expect `M` in the first column, staged, for these four files, and ` M model.py`, not staged. To unstage a file, run `git restore --staged` with its path. Then commit and check:

```sh
git commit -m "Log each failed reply by note number"
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. The check reads what Git holds; it does not run the tests.

## Reflect

When is `git commit -a` safe, and why? Would staging by path keep out a stray edit inside `extractor.py`, and why? Which files of your own work belong in `.gitignore`, and why?

[Worked answer](../answers/commit-three-of-four/) · [Start over](../../../README.md#start-an-exercise-again)
