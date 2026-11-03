# 2.3 Choose the model and levels

Choose the extractor's model and the coding agent's reasoning level for two tasks, and record the reason for each.

A teammate wants the extractor to call a more capable model. Your coding agent has two tasks next. The model scores and costs are fictional.

## Start

Follow the [Day 2 setup](../README.md). In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-02/model-and-reasoning-level/lab/.git || python3 reset.py model-and-reasoning-level
cd week-01/day-02/model-and-reasoning-level/lab
```

All paths below are relative to `lab/`. List the commits, then read `docs/model-scores.md` and `docs/next-tasks.md` for the facts:

```sh
git log --oneline --no-decorate
```

Expect six commits, the newest first.

## Choose and record

Fill in the table in `docs/pull-request.md` by hand. Use section 2.3 of the notebook to explain each answer.

| Choice | What to write |
|---|---|
| The extractor's model: haiku got note 0104 wrong, and sonnet did not. | Start with: `sonnet`. Reason: `capability`. |
| Task 1: its rule can change the reply for any note, so you score the whole set again. | Start with: `claude --effort medium`. Reason: `capability`. |
| Task 2: you read its three short tests line by line. | Start with: `claude --effort low`. Reason: `speed`. |

<details><summary>Why each answer</summary>

| Choice | Why |
|---|---|
| The extractor's model: haiku got note 0104 wrong, and sonnet did not. | In `docs/model-scores.md`, haiku got note 0104 wrong, and sonnet did not. So sonnet fixes a failure that the set shows: the one reason to move up. Section 2.3, under "The pull request names each model and level, and the reason.": "move up only for a failure the set shows it fixes". |
| Task 1: its rule can change the reply for any note, so you score the whole set again. | In `docs/next-tasks.md`, the rule of task 1 can change the reply for any note, so you score the whole set again. Work that you must check so well gets a higher level, but not high, the top one, which can overthink. Section 2.3, under the same heading: "work where verification matters or edge cases are likely". Under "Two dials": "the top level can overthink, so test it". |
| Task 2: you read its three short tests line by line. | In `docs/next-tasks.md`, you read the three tests line by line, so you check each result yourself. Such small work gets the lowest level, which is the fastest. Section 2.3, under the same heading: "quick exchanges where you review each result". |

</details>

With Codex, write `codex -c model_reasoning_effort=medium` and `codex -c model_reasoning_effort=low` in place of the two commands. Do not start either agent.

Save your changes, then commit and check:

```sh
git add docs/pull-request.md
git commit -m "Choose the model and levels"
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. The check compares your table with the course's answer; it does not test the choices on the evaluation set.

## Reflect

When would haiku be the better choice, and why? When would task 2, which also changes a file, need a higher level? Capability, speed or cost: which reason decides most often in your own work, and why?

[Worked answer](../answers/model-and-reasoning-level/) · [Start over](../../../README.md#start-an-exercise-again)
