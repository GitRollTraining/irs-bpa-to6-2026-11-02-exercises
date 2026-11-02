# Practice exercises: the case-notes extractor

This repository holds the practice exercises of the course, by week and by day. Each day has one notebook, with the reading of the day and its exercises in the order of the slides. Each exercise has a folder with its starting files. Its answer is in the folder `answers` of its day.

The course made up every note and name in this repository. Some replies are the model's, and some runs are a coding agent's. A file beside each one says so. The course made up the other replies and runs. None is about a real person, business or tax return.

## Set up once

Use the same setup in the hosted workspace and on your own computer. Python 3.10 or later and Git 2.28 or later are required. The current notebook shell commands assume a Unix-like environment; Windows users should use WSL for the notebook exercises.

1. In the hosted workspace, open the existing course folder (`~/practice`). On your own computer, clone the repository into that folder:

   ```sh
   git clone https://github.com/GitRollTraining/irs-bpa-to6-2026-11-02-exercises.git ~/practice
   cd ~/practice
   ```

2. From the course root, run:

   ```sh
   python3 setup.py
   ```

   Setup creates or reuses `.venv`, installs `requirements.txt`, registers the notebook kernel "Python (practice .venv)", and creates the `start` reset tag if absent. The first package installation needs package-index access. Its final readiness check is offline and sends nothing to a model. Rerunning setup preserves exercise files and history.

   If Git has no effective name or email, setup asks for them and saves them in this course checkout's local configuration. Existing global settings are accepted and are never edited. You can configure the course identity yourself from its root:

   ```sh
   git config --local user.name "Your Name"
   git config --local user.email "your-email@example.com"
   ```

   Rerun setup after adding a missing identity. It copies missing local identity settings into existing exercise repositories without resetting work; newly built exercises copy the course identity automatically. Explicit local overrides in existing exercises are preserved. No instructor identity is supplied.

3. In each new terminal, change to the course root and activate the environment before running shell commands:

   ```sh
   source .venv/bin/activate
   python3 check_setup.py
   ```

   `Setup OK (offline)` means the selected Python has pytest, jsonschema and ipykernel, Git and identity are available, and `python3` on PATH uses the same Python environment. A `Missing` list names what to repair. Day 1 needs no model or coding agent.

4. Open the course folder in VS Code, trust the course files, and install the Python and Jupyter extensions when prompted. Open the day's notebook and select "Python (practice .venv)" on both hosted and local machines. Restart an already running kernel after setup. In a notebook cell, `import sys; print(sys.executable)` should point into this course's `.venv`; terminal activation alone does not change an existing kernel.

   For a readiness check using the actual notebook kernel, run this diagnostic cell from anywhere inside the course checkout:

   ```python
   import pathlib
   import subprocess
   import sys

   root = next(p for p in (pathlib.Path.cwd(), *pathlib.Path.cwd().parents)
               if (p / "check_setup.py").is_file())
   result = subprocess.run([sys.executable, str(root / "check_setup.py")])
   assert result.returncode == 0, "Resolve the readiness messages before continuing."
   ```

Before the four model exercises on Days 2–3, explicitly run `python3 check_setup.py --check-model` in the activated environment. This sends a short live request through `model.py`; provider access and sign-in are required. `python3 setup.py --check-model` requests the same optional probe after setup. Default setup/readiness never imports or calls the model. Neither readiness mode starts a coding agent.

## The days

| Day | The notebook | The exercises |
|---|---|---|
| Week 1, day 1 | [`week-01-day-01.ipynb`](week-01/day-01/week-01-day-01.ipynb) | [Three exercises](week-01/day-01/README.md) |
| Week 1, day 2 | [`week-01-day-02.ipynb`](week-01/day-02/week-01-day-02.ipynb) | [Three exercises](week-01/day-02/README.md) |
| Week 1, day 3 | [`week-01-day-03.ipynb`](week-01/day-03/week-01-day-03.ipynb) | [Three exercises](week-01/day-03/README.md) |
| Week 1, day 4 | [`week-01-day-04.ipynb`](week-01/day-04/week-01-day-04.ipynb) | [Four exercises](week-01/day-04/README.md) |
| Week 1, day 5 | [`week-01-day-05.ipynb`](week-01/day-05/week-01-day-05.ipynb) | [Two exercises](week-01/day-05/README.md) |

## The model and your coding agent

**The model.** Four exercises send text to the model that the extractor calls: `same-note-five-times` and `system-prompt` on day 2, and `define-a-function` and `score-the-prompt` on day 3. They send it through `model.py`. The table under "Start an exercise again" says how many calls each one makes after a reset. When you send the same text again, nothing goes to the model. Exercise checks do not call the model. The optional setup probe `check_setup.py --check-model` does. If a call fails, the script that sends tells you what to do.

**Your coding agent.** Two exercises start a coding agent in a terminal: `tool-modes` on day 4, with Codex, and `direct-run-one` on day 5, with Codex or Claude Code. The other exercises use no coding agent.

1. Open a terminal. In VS Code, select Terminal > New Terminal.
2. Go to the folder that the exercise names.
3. Start the agent: type `codex` for Codex, or `claude` for Claude Code.
4. The first time in a folder, the agent asks if you trust the folder. Answer yes for a folder that the course gave you. Then the agent uses the settings in that folder. Without the yes, Claude Code ignores the list of actions that the folder allows, and Codex can start in Read Only.
5. Before the agent does an action that its settings do not allow, it asks you. Read each question before you answer it.
6. In Codex, type `/status`. Its line `Permissions:` shows the sandbox, then the approvals. In a folder that you trust, it should show `Workspace (Ask for approval)`. `/permissions` lists the modes.
7. Type `/exit` to close the agent.

In the folder, Codex reads `.codex/config.toml`, and Claude Code reads `.claude/settings.json`. In your home folder, Codex keeps `~/.codex/`, and Claude Code keeps `~/.claude/` and `~/.claude.json`. Codex writes your answer to the trust question in `~/.codex/config.toml`. Claude Code writes it in `~/.claude.json`. A reset does not change your home folder.

## Start an exercise again

Run `python3 ~/practice/reset.py <folder>`, such as `python3 ~/practice/reset.py find-note-leaks`. The reset puts the folder of that exercise back as the course supplied it, and builds its Git repository again. It removes your changes and your commits in that folder. It does not change other folders or the answers. In a notebook, the first cell of each exercise runs the reset only when the exercise has no Git repository yet.

| Day | Folder | What its reset builds |
|---|---|---|
| Week 1, day 1 | `find-note-leaks` | `extractor/`: the extractor that the course team committed, and the change of a teammate's coding agent on its own branch. |
| Week 1, day 1 | `data-rules-check` | `lab/`: the lab at its first saved state, the four uses to classify in `docs/data-rules-check.md`, and an exported note that Git ignores. |
| Week 1, day 1 | `agent-boundary` | `lab/`: the lab after its run 2, the facts of the pilot, and a teammate's commit of the settings of the coding agents. |
| Week 1, day 2 | `same-note-five-times` | `lab/`, with `prompt.txt`, `send_five.py` and `record.md`, your record with its rows empty. The saved replies go, so your next send calls the model 10 times. |
| Week 1, day 2 | `system-prompt` | `lab/`: the lab after the data-rules check, with a draft system prompt. The saved replies in `runs/` go, so your next record of a changed prompt calls the model 3 times. |
| Week 1, day 2 | `model-and-reasoning-level` | `lab/`: the lab after its run 2, with `docs/model-scores.md`, `docs/next-tasks.md` and `docs/pull-request.md`. |
| Week 1, day 3 | `validate-replies` | `lab/`: the lab after its run 2, eight saved replies, `count_failures.py`, and a teammate's commit on the branch `fewer-failures`. |
| Week 1, day 3 | `define-a-function` | `lab/`: the lab after the data-rules check, with a teammate's `functions.json`, `tools.py`, `ask.py` and `system-prompt.txt`. The saved replies go, so your next send of a changed list calls the model 2 times. |
| Week 1, day 3 | `score-the-prompt` | `extractor/`: the lab after its run 2, a set of 20 labelled notes, a teammate's change to the prompt, and the first score of the set. Your runs go, so your next score of a changed prompt calls the model 20 times. |
| Week 1, day 4 | `commit-three-of-four` | `extractor/`: the lab after its run 2, a coding agent's changes to four files, not committed, and the log of its run. |
| Week 1, day 4 | `push-after-rejection` | `extractor/`, your clone of the lab with one commit of yours, and two repositories next to it. Then the reset makes a teammate's push. |
| Week 1, day 4 | `diff-views` | `lab/`: the lab after its run 2, and one more run of the coding agent, not committed. |
| Week 1, day 4 | `tool-modes` | `extractor/`, and `modes.md`, your table. Codex's changes go. The settings of Codex in your home folder stay. |
| Week 1, day 5 | `directing-prompt` | `lab/`: the lab after run 1, and `run2-prompt.txt` with the Goal and three empty parts. |
| Week 1, day 5 | `direct-run-one` | `lab/`: the lab before run 1, `run1-prompt.txt`, and `run-1-record.md`, your report with empty parts. The files of your agent's run go. |

## Answers

The answer to each exercise is in `answers/<folder>/`, in the folder of its day. The exercises are not graded, so you can open the answers. Do the exercise first.

## The other files

- `reset.py` puts an exercise back as the course supplied it.
- `notes/` holds the simulated case notes that the exercises share.
- `lab-states/` holds the files of the lab of the week at each of its saved states. The exercises build their starting repositories from it.
- `model.py` and `model-route.json` send a request to the model that the extractor calls. Four exercises of days 2 and 3 use them (see "The model and your coding agent"). Exercise checks do not call the model. The optional setup probe `check_setup.py --check-model` does.
- `setup.py` sets up this repository in hosted and local workspaces (see "Set up once"). `requirements.txt` lists what it installs.
- `check_setup.py` checks offline readiness: Python, pytest, jsonschema, ipykernel, shell interpreter consistency, Git, and commit identity. `--check-model` explicitly adds a live model probe.

## Setup validation

Run `.venv/bin/python .github/test_setup.py` to exercise readiness and setup in disposable repositories with synthetic identities and a fake model. The dedicated setup workflow installs requirements and runs these tests independently of the Day 1 exercise runner. Tests cover missing packages/Git/identity, shell interpreter mismatch, opt-in model success/failure, nested identity propagation, and repeat setup preserving work and global configuration. Package installation and kernel registration are stubbed in the orchestration test.

S2 was also checked with real kernel registration in a disposable home, a checkout path containing spaces, a real Day 1 build and learner commit without global identity, and repeated setup. That check reused installed dependencies without downloads. Fresh dependency downloads, interactive VS Code kernel selection, full notebook execution, and native Windows behavior remain unverified. The notebook command portability work is separate from setup readiness.
