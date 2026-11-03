# Day 3: Forms, tools and a score

Check replies against a schema and your own check, offer the model one function, and score a prompt on a labelled set.

Complete the [course setup](../../README.md#set-up-once), then open [the Day 3 notebook](week-01-day-03.ipynb). Use the **.venv** kernel. For terminal work, open a new terminal, which starts in the course folder, and activate the environment first:

```sh
source .venv/bin/activate
```

Exercises 3.2 and 3.3 send notes to the model through `model.py`; before them, check model access as the [course README](../../README.md#when-an-exercise-needs-ai-access) says. Use no other AI tool, and start no coding agent today. All notes and scenarios are fictional.

| Exercise | What you will do | Terminal instructions |
|---|---|---|
| 3.1 Check every reply | Make `check_reply` count bad replies as failures, while good replies and the lab's tests still pass. | [validate-replies](validate-replies/README.md) |
| 3.2 Define one function | Offer the model one harmless function, and test it where a call is right and where none is. | [define-a-function](define-a-function/README.md) |
| 3.3 Score the prompt | Name one failure of a teammate's prompt and its cause, revise the prompt once, and score it again. | [score-the-prompt](score-the-prompt/README.md) |

Use either the notebook cells or the terminal instructions. Startup keeps existing work. Each exercise ends when its check prints `Done:`; an initial `Not yet:` identifies work still to do. The reasons for each table's answers are in its **Why** toggle.

Answers are in [answers/](answers/). To start over, follow the [reset instructions](../../README.md#start-an-exercise-again); reset discards that exercise's edits and commits. For 3.2 and 3.3, reset also removes the saved replies, so the next send calls the model again: 2 times for 3.2, 20 times for 3.3.
