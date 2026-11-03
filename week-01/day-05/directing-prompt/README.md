# 5.1 Write run 2's directing prompt

Complete the directing prompt for run 2 with a done-when that anyone can check from a command.

Run 1 added the output schema and its tests. Run 2 asks a coding agent for the extractor. The prompt for run 2 gives the Goal; you write the other three parts.

## Start

Follow the [Day 5 setup](../README.md). Work by hand, without AI tools. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-05/directing-prompt/lab/.git || python3 reset.py directing-prompt
cd week-01/day-05/directing-prompt/lab
```

All paths below are relative to `lab/`. Git does not track your prompt, `run2-prompt.txt`, so you save it and commit nothing.

## Write and check

```sh
git log --oneline --name-only -3
```

Expect three commits: run 2's system prompt and recorded replies, Claude Code's settings, and run 1's schema and tests. Your Context names `model.py` and files from these commits, and your Constraints keep them as they are.

Open `run2-prompt.txt` and write each part's line after its empty label. Keep the Goal as it is. Use the Opening and section 5.1 of the notebook to explain each line.

| Part | What to write |
|---|---|
| Context | read model.py, prompts/system.txt and schema/output.schema.json. The tests use the replies in tests/recorded/. |
| Constraints | The tests call no model. Do not edit anything outside extractor.py and tests/test_extractor.py. Do not log note text. |
| Done-when | pytest tests/test_extractor.py passes. It includes one reply that must fail (amount_in_question missing) and note 0102, for which the function must return amount_in_question null. |

<details><summary>Why each answer</summary>

| Part | Why |
|---|---|
| Context | The function sends prompts/system.txt through model.py to the model. It checks each reply against schema/output.schema.json. The tests use the recorded replies. Without these paths, the agent guesses. Section 5.1, under "A one-line task is a wish": "Reference specific files". |
| Constraints | The Goal's function calls the model, whose reply can change. So its tests use the recorded replies. If the agent changes run 1's files or the recorded replies, wrong code can pass. So it edits only the Goal's two files. A log line with note text copies taxpayer data. Section 5.1, run 1's table, Constraints: "Do not call any model. Do not edit anything outside schema/ and tests/. Do not log note text." The Opening, under "Today's runs build the extractor": "tested on model replies recorded earlier". |
| Done-when | Anyone can run the command. A reply that must fail catches an extractor that accepts any reply. Note 0102 has a recorded reply and names no amount. So its test catches an extractor that supplies an amount. Section 5.1, under "Only the done-when": "the part someone who did not watch can check from a command". Run 1's table, Done-when: "it includes one output that must fail (amount_in_question missing)". The Opening, under "Today's runs build the extractor": "A note with no amount: amount_in_question is null". |

</details>

Save the file, then check:

```sh
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings and check again. The check runs your done-when on the course's run 2 and on two wrong runs; it starts no agent.

## Reflect

What if a run had to change run 1's schema: what would its Constraints say? Which wrong run 2 would still pass your done-when, and why?

[Worked answer](../answers/directing-prompt/) · [Start over](../../../README.md#start-an-exercise-again)
