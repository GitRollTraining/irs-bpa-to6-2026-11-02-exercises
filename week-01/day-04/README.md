# Day 4: Git and the coding agent

Three exercises, one notebook each. Each notebook runs real Git commands on a small practice project that it builds beside itself: a grocery list you share with your housemate. You write no code: you run cells and change one part of one command at a time.

The notebook's first cell, `%run steps.py`, builds that project and adds the `%step` and `%done` helpers. `steps.py` sits beside the notebook; you do not need to open it.

Open an exercise's `exercise.ipynb`, choose the **.venv** kernel, and run the cells from the top: click a cell and press Shift+Enter. Each step ends with a line that says OK when the result is right and PROBLEM when it is not. An exercise is done when its last cell prints `Done:`.

| Exercise | What you will do | Slides | Time |
|---|---|---|---|
| [1 · Commit what you mean](exercise-01-commit-what-you-mean/exercise.ipynb) | Keep a log out with `.gitignore`, stage only the changes you mean, and commit without `-a`, so your private note stays out. | 6, 8, 9 | 10 min |
| [2 · Push after a rejection](exercise-02-push-after-rejection/exercise.ipynb) | Check where your push goes, then fetch, read and merge your housemate's commit before you push again, so both commits are kept. | 15, 16, 19 | 12 min |
| [3 · Read each diff view](exercise-03-read-each-diff-view/exercise.ipynb) | Use the form of `git diff` that shows your next commit, put milk's new price from its `+` line in your commit message, then use the form that shows what the commit changed. | 24, 25, 29 | 12 min |

Section 4.4, the kinds of AI coding tool, has no exercise here: the [Codex exercises](../day-special/README.md) practise an agent's sandbox and approval modes hands-on.

Solved copies are in [answers/](answers/): each is the same notebook with the answers filled in, beside the same `steps.py`.
