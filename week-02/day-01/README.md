# Week 2, day 1: coding agents

Three exercises, in order. Each one starts from the app as the one before it ends. Each exercise has its own `reference-app` folder; work in that exercise's copy.

From the course folder (containing `pyproject.toml`), run `uv sync`. Select the course folder's `.venv/bin/python` as the notebook kernel, and run `source .venv/bin/activate` in each new terminal before starting Codex. Both weeks share this environment. Full instructions: [Set up for week 2](../../README.md#set-up-for-week-2).

1. [Fix a wrong value with Codex](exercise-01-fix-a-wrong-value/exercise.ipynb). What you do: ask Codex to fix a wrong value on a page, and check the fix in the running app. Where you work: `exercise-01-fix-a-wrong-value/reference-app`, in the notebook and a terminal. Done when: cell 3 prints `Done:`, and the page of case CS-2026-0001 shows Balance due $12,250. [Start](exercise-01-fix-a-wrong-value/) · [Answer](answers/exercise-01-fix-a-wrong-value/)
2. [Tell Codex how to run the tests](exercise-02-write-agents-md/exercise.ipynb). What you do: write an `AGENTS.md` file that makes a new Codex session run the app's tests without being told. Where you work: `exercise-02-write-agents-md/reference-app`, in the notebook and a terminal. Done when: cell 4 prints `Done:`. [Start](exercise-02-write-agents-md/) · [Answer](answers/exercise-02-write-agents-md/)
3. [Install a skill and use it on the app](exercise-03-use-a-skill/exercise.ipynb). What you do: install a skill into a project and have Codex use it for one change to the app. Where you work: `exercise-03-use-a-skill/reference-app`, in the notebook and a terminal. Done when: cell 4 prints `Done:`. [Start](exercise-03-use-a-skill/) · [Answer](answers/exercise-03-use-a-skill/)
