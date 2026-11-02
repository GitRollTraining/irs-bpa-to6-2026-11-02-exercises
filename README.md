# Practice exercises: the case-notes extractor

Work through the notebooks in order. Each day combines reading with exercises. Exercise READMEs provide terminal instructions; worked solutions are in each day's `answers/` folder.

All names, notes, and scenarios are fictional. Use only the supplied course data.

## Set up once

Use Python 3.10 or later, Git 2.28 or later, and VS Code with the Python and Jupyter extensions. The exercises use Unix shell commands; on Windows, use WSL.

1. In the hosted workspace, open a terminal in `~/practice`. On your own computer, clone the course there:

   ```sh
   git clone https://github.com/GitRollTraining/irs-bpa-to6-2026-11-02-exercises.git ~/practice
   cd ~/practice
   ```

2. From `~/practice`, run:

   ```sh
   python3 setup.py
   ```

   Setup installs the Python packages, registers the notebook kernel, and asks for a Git name and email if needed. Initial installation needs internet access. You can rerun setup without losing exercise work.

3. In each new terminal, activate the environment and check readiness:

   ```sh
   cd ~/practice
   source .venv/bin/activate
   python3 check_setup.py
   ```

   Continue when it prints `Setup OK (offline)`. If it prints `Missing`, follow the messages and rerun the check. Day 1 needs no model access or coding agent.

4. Open `~/practice` in VS Code and open the day's notebook. Select **Python (practice .venv)** as its kernel. Restart the kernel if it was running during setup.

### If setup needs attention

- **Git name or email missing:** rerun `python3 setup.py` and enter your own details. They are saved for this course and its exercises; existing global Git settings are left alone.
- **Python environments differ:** activate `.venv` in the terminal, select **Python (practice .venv)** in the notebook, and restart its kernel. In a notebook cell, `import sys; print(sys.executable)` should show a path inside `~/practice/.venv`.
- **Other missing requirements:** follow the readiness message, then rerun setup.

## Week 1

| Day | Notebook | Exercises |
|---|---|---|
| 1 | [What may go into an AI tool](week-01/day-01/week-01-day-01.ipynb) | [Data boundaries and approvals](week-01/day-01/README.md) |
| 2 | [Day 2](week-01/day-02/week-01-day-02.ipynb) | [Prompts and model choices](week-01/day-02/README.md) |
| 3 | [Day 3](week-01/day-03/week-01-day-03.ipynb) | [Validation, functions, and evaluation](week-01/day-03/README.md) |
| 4 | [Day 4](week-01/day-04/week-01-day-04.ipynb) | [Git and tool permissions](week-01/day-04/README.md) |
| 5 | [Day 5](week-01/day-05/week-01-day-05.ipynb) | [Directing and verifying agent work](week-01/day-05/README.md) |

## When an exercise needs AI access

Four exercises call a model through `model.py`: `same-note-five-times` and `system-prompt` on Day 2, and `define-a-function` and `score-the-prompt` on Day 3. Before those exercises, check access from the activated environment:

```sh
python3 ~/practice/check_setup.py --check-model
```

This sends a short live request. Follow any provider sign-in instructions it reports. Ordinary readiness and exercise checks do not call a live model.

Only `tool-modes` on Day 4 and `direct-run-one` on Day 5 ask you to start a coding agent. Follow their instructions for choosing and launching it.

## Start an exercise again

To discard your work in one exercise, run its reset command, for example:

```sh
python3 ~/practice/reset.py find-note-leaks
```

Reset removes your edits and commits in that exercise and rebuilds its starting files. Save anything you want to keep first. Other exercises and the supplied answers are preserved. Notebook startup cells keep an existing exercise workspace; use reset only when you want to start over.

For model exercises, reset also removes saved replies. The next run makes 10 model calls for `same-note-five-times`, 3 for `system-prompt`, 2 for `define-a-function`, or 20 for `score-the-prompt`.

## Check your work

Each exercise explains how to run its check and what `Done:` means. If you need help, its day's `answers/<exercise>/` folder contains a worked solution. Try the exercise before opening the answer.
