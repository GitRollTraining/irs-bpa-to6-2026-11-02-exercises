# Day 5: The AI-assisted loop

**Today's two exercises are optional practice.** Class time on Day 5 goes to the week's challenge. Do the exercises when you want more practice.

Two exercises, one notebook each. Each notebook runs real pytest and Git commands on a small practice project that it builds beside itself: a grocery list and `total.py`, a helper that adds up its prices. A coding agent was asked to fix the helper; its runs are made up and saved by the notebook, so you need no agent, key or sign-in. You write no code: you run cells and change one part of one command at a time.

The notebook's first cell, `%run steps.py`, builds that project and adds the `%step` and `%done` helpers. `steps.py` sits beside the notebook; you do not need to open it.

Open an exercise's `exercise.ipynb`, choose the **.venv** kernel, and run the cells from the top: click a cell and press Shift+Enter. Each step ends with a line that says OK when the result is right and PROBLEM when it is not. An exercise is done when its last cell prints `Done:`.

| Exercise | What you will do | Slides | Time |
|---|---|---|---|
| [1 · Check an agent's runs with your done-when](exercise-01-check-an-agents-runs/exercise.ipynb) | See that a total that looks right is not a check, run the whole done-when to reject run B, and switch to run A, which passes it. | 5, 7, 10 | 15 min |
| [2 · Check the done-when yourself](exercise-02-check-the-done-when/exercise.ipynb) | Run the done-when yourself, read the diff of the test file the agent changed, and undo its work with `git restore`. | 14, 16 | 10 min |

Solved copies are in [answers/](answers/): each is the same notebook with the answers filled in, beside the same `steps.py`.
