# Git basics

Four exercises, one notebook each, that practise the Git commands you use most: `git init`, `git status`, `git add`, `git commit`, `git log`, `git branch`, `git checkout`, `git remote`, `git push`, `git pull` and `git clone`. Exercises 1 to 3 run real Git commands on a small practice project, a meal plan you share with your housemate, which each notebook builds beside itself. Exercise 4 runs them on a repository of your own on GitHub. You write no code: you run a cell, change one part of one command, and run it again to see what the change does.

Open an exercise's `exercise.ipynb`, choose the **.venv** kernel, and run the cells from the top: click a cell and press Shift+Enter. The first code cell, `%run steps.py`, builds the practice project and adds the `%step` and `%done` helpers; `steps.py` sits beside the notebook, and you do not need to open it. Each step ends with a line that says OK when the result is right and PROBLEM when it is not. An exercise is done when its last cell prints `Done:`.

| Exercise | Commands | What you will do | Time |
|---|---|---|---|
| [1 · Start a repository](exercise-01-start-a-repository/exercise.ipynb) | `init`, `status`, `add`, `commit`, `log` | Turn a folder into a Git repository, stage its two files, and save them in a first commit. | 10 min |
| [2 · Try an idea on a branch](exercise-02-try-an-idea-on-a-branch/exercise.ipynb) | `branch`, `checkout`, `log` | Make a branch and move to it, commit a new dinner on it, then switch back to `main`, which stays as it was. | 10 min |
| [3 · Share through a remote](exercise-03-share-through-a-remote/exercise.ipynb) | `remote`, `push`, `pull` | Connect your project to a shared repository, push your commits to it, then pull the commit your housemate pushed. | 10 min |
| [4 · Push to your own GitHub repository](exercise-04-push-to-your-github/exercise.ipynb) | `clone`, `add`, `commit`, `push` | Clone a repository of your own from GitHub, commit a file in it and push it, push your Exercise 2 branch too, then see both on GitHub. | 15 min |

Exercises 1 to 3 each build their own project, so you can do them in any order; in Exercise 3 a folder stands in for GitHub, so you need no account and no network. Exercise 4 needs a GitHub account with a repository of your own, Git signed in to GitHub in a terminal, and your meal plan from Exercise 2. Solved copies are in [answers/](answers/): each is the same notebook with the answers filled in, beside the same `steps.py`.
