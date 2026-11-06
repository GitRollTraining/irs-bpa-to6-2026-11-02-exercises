# Git basics: ten commands

Three exercises, one notebook each, that practise the Git commands you use most: `git init`, `git status`, `git add`, `git commit`, `git log`, `git branch`, `git checkout`, `git remote`, `git push` and `git pull`. Each notebook runs real Git commands on a small practice project, a meal plan you share with your housemate, which it builds beside itself. You write no code: you run a cell, change one part of one command, and run it again to see what the change does.

Open an exercise's `exercise.ipynb`, choose the **.venv** kernel, and run the cells from the top: click a cell and press Shift+Enter. The first code cell, `%run steps.py`, builds the practice project and adds the `%step` and `%done` helpers; `steps.py` sits beside the notebook, and you do not need to open it. Each step ends with a line that says OK when the result is right and PROBLEM when it is not. An exercise is done when its last cell prints `Done:`.

| Exercise | Commands | What you will do | Time |
|---|---|---|---|
| [1 · Start a repository](exercise-01-start-a-repository/exercise.ipynb) | `init`, `status`, `add`, `commit`, `log` | Turn a folder into a Git repository, stage its two files, and save them in a first commit. | 10 min |
| [2 · Try an idea on a branch](exercise-02-try-an-idea-on-a-branch/exercise.ipynb) | `branch`, `checkout`, `log` | Make a branch and move to it, commit a new dinner on it, then switch back to `main`, which stays as it was. | 10 min |
| [3 · Share through a remote](exercise-03-share-through-a-remote/exercise.ipynb) | `remote`, `push`, `pull` | Connect your project to a shared repository, push your commits to it, then pull the commit your housemate pushed. | 10 min |

Each exercise builds its own project, so you can do them in any order. In Exercise 3 a folder stands in for GitHub, so you need no account and no network. Solved copies are in [answers/](answers/): each is the same notebook with the answers filled in, beside the same `steps.py`.
