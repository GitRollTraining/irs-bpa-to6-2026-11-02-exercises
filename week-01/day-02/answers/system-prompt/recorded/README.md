# The replies of the course's run

These three files are the replies of the model to the answer's prompt, `../system.txt`. The course team ran the commands of the exercise's README in a terminal on 2026-11-03, with the answer's prompt in `prompts/system.txt`. `../record.py 0147 0102 0104` sent the three notes through the lab's route to the model, `model.py`. Each file holds a reply as `model.py` gave it.

- Route: `codex`, as `model-route.json` names it. It runs the command `codex exec`, version 0.165.0-alpha.1.2.
- Model: `gpt-6-luna`, at the reasoning level `low`, as `model-route.json` names them.
- Date: 2026-11-03.
- Where: on a computer of the course team, not in the hosted workspace of the course.

The earlier run of 2026-10-30, on the route through Claude Code with `haiku`, gave the same values for `amount_in_question`: 18400, null and null.

`commands.sh` records these replies through `replay.py`, so the check can run with no call to the model.
