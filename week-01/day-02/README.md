# Day 2: How a model writes, and how to direct it

See the model sample its replies, write the extractor's system prompt, and choose a model and reasoning levels with a reason for each.

Complete the [course setup](../../README.md#set-up-once), then open [the Day 2 notebook](week-01-day-02.ipynb). Use the **.venv** kernel. For terminal work, open a new terminal, which starts in the course folder, and activate the environment first:

```sh
source .venv/bin/activate
```

Exercises 2.1 and 2.2 send notes to the model through `model.py`; before them, check model access as the [course README](../../README.md#when-an-exercise-needs-ai-access) says. Use no other AI tool, and start no coding agent today. All notes and scenarios are fictional.

| Exercise | What you will do | Terminal instructions |
|---|---|---|
| 2.1 Send each note five times | Send two notes five times each, and record which replies give a value the note does not state. | [same-note-five-times](same-note-five-times/README.md) |
| 2.2 Write the system prompt | Fix the draft system prompt, and record three replies that pass the lab's tests. | [system-prompt](system-prompt/README.md) |
| 2.3 Choose the model and levels | Choose the extractor's model and two reasoning levels, with a reason for each. | [model-and-reasoning-level](model-and-reasoning-level/README.md) |

Use either the notebook cells or the terminal instructions. Startup keeps existing work. Each exercise ends when its check prints `Done:`; an initial `Not yet:` identifies work still to do. The reasons for each table's answers are in its **Why** toggle.

Answers are in [answers/](answers/). To start over, follow the [reset instructions](../../README.md#start-an-exercise-again); reset discards that exercise's edits and commits. For 2.1 and 2.2, reset also removes the saved replies, so the next send calls the model again: 10 times for 2.1, 3 times for 2.2.
