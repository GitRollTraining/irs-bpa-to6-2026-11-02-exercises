# Practice exercises: the case-notes extractor

This repository holds the practice exercises of the course, by week and by day. Each day has one notebook, with the reading of the day and its exercises in the order of the slides. Each exercise has a folder with its starting files. Its answer is in the folder `answers` of its day.

The course made up every note, name and reply in this repository. None is about a real person, business or tax return.

## Set up once

In the hosted workspace of the course, the folder `~/practice` is this repository. Start at step 3.

On your own computer, do all the steps.

1. Clone the repository into `~/practice`. Then mark the state that a reset restores:

   ```
   git clone https://github.com/GitRollTraining/irs-bpa-to6-2026-11-02-exercises.git ~/practice
   cd ~/practice
   git tag start
   ```

2. Make a Python environment for the exercises, with Python 3.9 or later:

   ```
   python3 -m venv .venv
   .venv/bin/pip install pytest jsonschema ipykernel
   ```

3. Give Git your name and email. Git writes them into each commit that you make:

   ```
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

4. Open the folder `~/practice` in VS Code. If VS Code asks if you trust the authors of the files, select Trust. When VS Code asks for the Python and Jupyter extensions, install them.

5. Open the notebook of the day, such as `week-01/day-01/week-01-day-01.ipynb`. At the top right, select Select Kernel. On your own computer, select the environment `.venv`. In the hosted workspace, select its Python.

## The days

| Day | The notebook | The exercises |
|---|---|---|
| Week 1, day 1 | [`week-01-day-01.ipynb`](week-01/day-01/week-01-day-01.ipynb) | [Three exercises](week-01/day-01/README.md) |
| Week 1, day 2 | [`week-01-day-02.ipynb`](week-01/day-02/week-01-day-02.ipynb) | Not in this repository yet |
| Week 1, day 3 | [`week-01-day-03.ipynb`](week-01/day-03/week-01-day-03.ipynb) | Not in this repository yet |
| Week 1, day 4 | [`week-01-day-04.ipynb`](week-01/day-04/week-01-day-04.ipynb) | Not in this repository yet |
| Week 1, day 5 | [`week-01-day-05.ipynb`](week-01/day-05/week-01-day-05.ipynb) | Not in this repository yet |

## Start an exercise again

Run `python3 ~/practice/reset.py <folder>`, such as `python3 ~/practice/reset.py find-note-leaks`. The reset puts the folder of that exercise back as the course supplied it, and builds its Git repository again. It removes your changes and your commits in that folder. It does not change other folders or the answers.

## Answers

The answer to each exercise is in `answers/<folder>/`, in the folder of its day. The exercises are not graded, so you can open the answers. Do the exercise first.

## The other files

- `reset.py` puts an exercise back as the course supplied it.
- `notes/` holds the simulated case notes that the exercises share.
- `lab-states/` holds the files of the lab of the week at each of its saved states. The exercises build their starting repositories from it.
- `model.py` and `model-route.json` are the route to the model that the extractor calls. The exercises of day 1 do not call the model.
- `check_setup.py` checks a workspace: Python, pytest, jsonschema, Git, and the model. Outside the hosted workspace, it can show the model as missing.
