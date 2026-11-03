# Practice exercises: the case-notes extractor

Work through the notebooks in order. Each day combines reading with exercises. Exercise READMEs provide terminal instructions; worked solutions are in each day's `answers/` folder.

All names, notes, and scenarios are fictional. Use only the supplied course data.

## Set up once

Use VS Code, or Code OSS in the hosted workspace, with the Python and Jupyter extensions. Run each command below in its terminal (Terminal > New Terminal). The exercises use Unix shell commands; on Windows, use WSL.

1. Install the Codex CLI:

   ```sh
   curl -fsSL https://chatgpt.com/codex/install.sh | sh
   ```

   Then open a new terminal and sign in with `codex login`. In the hosted workspace, run `codex login --device-auth` instead: it gives a code to enter in your browser.

2. Install uv, which sets up the course's Python and its packages, then open a new terminal:

   ```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Give Git your name and email, for your commits:

   ```sh
   git config --global user.name "Your Name"
   git config --global user.email "you@example.com"
   ```

4. Clone the course, for example into `~/practice`, and open that folder (File > Open Folder):

   ```sh
   git clone https://github.com/GitRollTraining/irs-bpa-to6-2026-11-02-exercises.git ~/practice
   ```

   Any folder works: every path in the exercises is relative to the course folder or to the exercise. In the hosted workspace, keep the course in your home folder, which is kept when the workspace stops.

5. In a new terminal, which opens in the course folder, set up the environment and check it:

   ```sh
   uv sync
   uv run check_setup.py
   ```

   `uv sync` makes `.venv` with the course's Python packages; the first run needs internet access. `check_setup.py` checks Python, Git and the Codex CLI, then runs every cell of every notebook in a temporary copy of the course, with nothing sent to a model. It takes a minute or two. Continue when it prints `Setup OK`. If it prints `Missing`, follow each message and run the check again.

6. Open the day's notebook, select **.venv** as its kernel (Select Kernel > Python Environments), and run its first cell.

For an exercise's terminal commands, run `source .venv/bin/activate` first in each new terminal.

### If setup needs attention

- **Git name or email missing:** run the two `git config --global` commands in step 3, with your own details.
- **Codex CLI not signed in:** run `codex login`, or in the hosted workspace `codex login --device-auth`.
- **Python environments differ:** run `source .venv/bin/activate` in the terminal, select **.venv** as the notebook's kernel, and restart the kernel. In a notebook cell, `import sys; print(sys.executable)` should show a path inside the course folder's `.venv`.
- **A notebook cell fails in the check:** send the course team the lines under `Missing`.

## Week 1

| Day | Notebook | Exercises |
|---|---|---|
| 1 | [What may go into an AI tool](week-01/day-01/week-01-day-01.ipynb) | [Data boundaries and approvals](week-01/day-01/README.md) |
| 2 | [Day 2](week-01/day-02/week-01-day-02.ipynb) | [Prompts and model choices](week-01/day-02/README.md) |
| 3 | [Day 3](week-01/day-03/week-01-day-03.ipynb) | [Validation, functions, and evaluation](week-01/day-03/README.md) |
| 4 | [Day 4](week-01/day-04/week-01-day-04.ipynb) | [Git and tool permissions](week-01/day-04/README.md) |
| 5 | [Day 5](week-01/day-05/week-01-day-05.ipynb) | [Directing and verifying agent work](week-01/day-05/README.md) |

## When an exercise needs AI access

Four exercises call a model through `model.py`: `same-note-five-times` and `system-prompt` on Day 2, and `define-a-function` and `score-the-prompt` on Day 3. Before those exercises, check access from the course folder:

```sh
uv run check_setup.py --check-model
```

This checks only the route to the model, with one short live request. Follow any provider sign-in instructions it reports. The setup check and the exercise checks do not call a live model.

Only `tool-modes` on Day 4 and `direct-run-one` on Day 5 ask you to start a coding agent. Follow their instructions for choosing and launching it.

## Start an exercise again

To discard your work in one exercise, run its reset command from the course folder, for example:

```sh
python3 reset.py find-note-leaks
```

From the exercise's `lab` or `extractor` folder, the same reset is `python3 ../../../../reset.py find-note-leaks`. In a notebook, run `!python3 "{_dh[0]}/../../reset.py" find-note-leaks` in a new cell: `{_dh[0]}` is the folder of the notebook, where its kernel starts.

Reset removes your edits and commits in that exercise and rebuilds its starting files. Save anything you want to keep first. Other exercises and the supplied answers are preserved. Notebook startup cells keep an existing exercise workspace; use reset only when you want to start over.

For model exercises, reset also removes saved replies. The next run makes 10 model calls for `same-note-five-times`, 3 for `system-prompt`, 2 for `define-a-function`, or 20 for `score-the-prompt`.

## Check your work

Each exercise explains how to run its check and what `Done:` means. If you need help, its day's `answers/<exercise>/` folder contains a worked solution. Try the exercise before opening the answer.
