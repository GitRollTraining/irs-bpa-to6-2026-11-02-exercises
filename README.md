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

6. Open the day's notebook, select the course folder's **.venv** as its kernel (Select Kernel > Python Environments), and run its first cell. Both weeks use this same environment.

For an exercise's terminal commands, run `source .venv/bin/activate` first in each new terminal.

### If setup needs attention

- **Git name or email missing:** run the two `git config --global` commands in step 3, with your own details.
- **Codex CLI not signed in:** run `codex login`, or in the hosted workspace `codex login --device-auth`.
- **Python environments differ:** run `source .venv/bin/activate` in the terminal, select **.venv** as the notebook's kernel, and restart the kernel. In a notebook cell, `import sys; print(sys.executable)` should show a path inside the course folder's `.venv`.
- **A notebook cell fails in the check:** send the course team the lines under `Missing`.

## Get today's files

The course team adds and fixes days during the week. At the start of each day, run these in a terminal in the course folder:

```sh
git pull
uv sync
```

`git pull` downloads the new and changed files into your course folder. Your work inside an exercise's folders stays as it is. `uv sync` updates the course's Python packages if they changed.

If `git pull` stops and names a notebook you changed, save your copy under a new name, undo your change, and pull again. For example, for the Day 2 notebook:

```sh
cp week-01/day-02/week-01-day-02.ipynb ~/my-week-01-day-02.ipynb
git restore week-01/day-02/week-01-day-02.ipynb
git pull
```

Use the path that `git pull` names.

## Set up for week 2

Week 2 uses the same uv environment as week 1: `.venv` in the course folder. Flask, pytest, coverage.py, pydeps, lxml and the notebook kernel are installed together by `uv sync`. No separate environment or system package installation is needed.

1. Open a terminal in the course folder (the folder containing `pyproject.toml`) and run:

   ```sh
   git pull
   uv sync
   uv run check_setup.py
   ```

   If `git pull` stops and names a notebook you changed, follow [Get today's files](#get-todays-files). The first sync needs internet access. Continue when the check prints `Setup OK`; follow any `Missing` messages before continuing.

2. In the notebook, click **Select Kernel > Python Environments** and select the course folder's `.venv/bin/python`. If you previously selected another environment, restart the kernel and run from cell 1.

3. Before starting Codex, activate the same environment in each new terminal, from the course folder:

   ```sh
   source .venv/bin/activate
   ```

The app you change is inside each exercise, for example [`week-02/day-01/exercise-01-fix-a-wrong-value/reference-app`](week-02/day-01/exercise-01-fix-a-wrong-value/reference-app/README.md). Each exercise supplies its own starting state; worked solutions are in `answers/`. There is no root `reference-app` folder.

### If week 2 setup needs attention

- **The kernel is missing:** run `uv sync`, then refresh the Python environment picker. If needed, run **Python: Select Interpreter** from the Command Palette, choose **Enter interpreter path**, and browse to the course folder's `.venv/bin/python`. Reopen the notebook's kernel picker and select it.
- **You followed older instructions for a separate week 2 environment or saw `ensurepip is not available`:** use `uv sync` in the course folder and select `.venv/bin/python`. In each new terminal, activate it with `source .venv/bin/activate`.
- **The app's link does not open from the hosted workspace:** run `echo "https://5000-$WEB_HOST"` in its terminal and open the address it prints. `WEB_HOST` is the workstation's own address ([Google Cloud Workstations: access HTTP servers running on a workstation](https://docs.cloud.google.com/workstations/docs/access-http-servers-running-on-workstations)).

## Week 1

| Day | Notebook | Exercises |
|---|---|---|
| 1 | [What may go into an AI tool](week-01/day-01/week-01-day-01.ipynb) | [Data boundaries and approvals](week-01/day-01/README.md) |
| 2 | [Day 2](week-01/day-02/week-01-day-02.ipynb) | [Prompts and model choices](week-01/day-02/README.md) |
| 3 | [Three exercise notebooks](week-01/day-03/README.md) | [Validation, functions, and evaluation](week-01/day-03/README.md) |
| 4 | [Three exercise notebooks](week-01/day-04/README.md) | [Git: commit, push and diff](week-01/day-04/README.md) |
| 5 | [Two exercise notebooks](week-01/day-05/README.md) | [Directing and verifying agent work](week-01/day-05/README.md), optional practice |
| Codex | [Three exercise notebooks](week-01/day-special/README.md) | [Codex CLI: a hands-on start](week-01/day-special/README.md) |
| Git | [Four exercise notebooks](week-01/day-git/README.md) | [Git basics](week-01/day-git/README.md) |

## Week 2

| Day | Notebook | Exercises |
|---|---|---|
| 1 | [Three exercise notebooks](week-02/day-01/README.md) | [Coding agents: Codex, AGENTS.md and a skill](week-02/day-01/README.md) |
| 2 | [Three exercise notebooks](week-02/day-02/README.md) | [Mapping a codebase, and testing it](week-02/day-02/README.md) |
| 3 | [Four exercise notebooks](week-02/day-03/README.md) | [Code review, and a return's XML](week-02/day-03/README.md) |
| 4 | No notebook: Friday is worked in the Challenge repository | [Challenge 1: IT Access Requests](https://github.com/GitRollTraining/ai-full-stack-it-access-requests), starting with its `docs/00-prerequisites.md` |

Friday (day 4) has no folder here. You work Challenge 1 in your own clone of [its repository](https://github.com/GitRollTraining/ai-full-stack-it-access-requests), with Codex, following the files in its `docs/` folder in order.

## Week 3

Monday to Wednesday run in the class's Databricks workspace, from your Git folder of this repository. Pull it at the start of each day.

| Day | Notebook | Exercises |
|---|---|---|
| 1 | [Four exercise notebooks](week-03/day-01/README.md) | [Find the data a case-selection model needs, in Databricks](week-03/day-01/README.md) |

## When an exercise needs AI access

Two exercises call a model through `model.py`, which sends each request through the Codex CLI that you signed in to in step 1: `same-note-five-times` and `system-prompt` on Day 2. Before those exercises, check access from the course folder:

```sh
uv run check_setup.py --check-model
```

This checks only the route to the model, with one short live request. If it reports a sign-in problem, run `codex login` again. The setup check and the exercise checks do not call a live model.

Only the Codex exercises in [week-01/day-special](week-01/day-special/README.md), [week-01/codex](week-01/codex/README.md), [week-02/day-01](week-02/day-01/README.md), [week-02/day-02](week-02/day-02/README.md) and [week-02/day-03](week-02/day-03/README.md) ask you to start a coding agent. Follow their instructions for launching it.

## Start an exercise again

To discard your work in one exercise, run its reset command from the course folder, for example:

```sh
python3 reset.py find-note-leaks
```

From the exercise's `lab` or `extractor` folder, the same reset is `python3 ../../../../reset.py find-note-leaks`. In a notebook, run `!python3 "{_dh[0]}/../../reset.py" find-note-leaks` in a new cell: `{_dh[0]}` is the folder of the notebook, where its kernel starts.

Reset removes your edits and commits in that exercise and rebuilds its starting files. Save anything you want to keep first. Other exercises and the supplied answers are preserved. Notebook startup cells keep an existing exercise workspace; use reset only when you want to start over.

For model exercises, reset also removes saved replies. The next run makes 10 model calls for `same-note-five-times`, or 3 for `system-prompt`.

The one-notebook exercises (Days 3, 4 and 5, the Codex exercises in `week-01/day-special` and the Git exercises in `week-01/day-git`) need no reset: run the notebook again from the top. A Codex exercise's **Start over** cell writes its practice files again.

## Check your work

Each exercise explains how to run its check and what `Done:` means. If you need help, its day's `answers/<exercise>/` folder contains a worked solution. Try the exercise before opening the answer.

## Repository validation

From the repository root, run the structural check and the offline Day 1 check:

```sh
python3 .github/check_repository.py
.venv/bin/python .github/check_day_one.py
```

The Day 1 check needs Git, `sh`, pytest, and jsonschema in the selected Python environment. CI installs with `uv sync --locked` and runs both checks on Python 3.12. The runner copies tracked course inputs with their current working-tree contents into a temporary checkout; commit or stage new fixture files before expecting them to be included. Ignored learner repositories are excluded.

For all three Day 1 exercises, it checks the expected unfinished state, runs the supplied answer, resets from inside the exercise repository, and repeats the answer. It also checks preservation of other exercise work, an edited notebook, unrelated files, and temporary home settings. Child Python processes block socket access and live model calls. The temporary checkout and home are removed afterward; no setup script or live agent is run. These regression guards are not a sandbox for untrusted code.

This verifies the exercise scripts and answers. Notebook cells, Markdown commands, editor integration, fresh dependency installation, and live agent behavior still need separate validation.
