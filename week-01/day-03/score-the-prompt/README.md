# 3.3 Score the prompt

Name one failure of a teammate's prompt and its cause, revise the prompt once, and score it again on the same labelled set.

A teammate revised the extractor's prompt after reading five replies that looked right. Nobody has read the prompt's first score on the 20 labelled notes.

## Start

Follow the [Day 3 setup](../README.md). `evaluation/score.py` calls the model; use no other AI tool. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-03/score-the-prompt/extractor/.git || python3 reset.py score-the-prompt
cd week-01/day-03/score-the-prompt/extractor
```

All paths below are relative to `extractor/`. `evaluation/score.py` scores each reply against the labels in `evaluation/labels.jsonl`; the first run, on the teammate's prompt, is in `evaluation/runs/1/`.

## Revise and score

Open the teammate's prompt, its first score and your write-up:

```sh
code prompts/system.txt evaluation/runs/1/score.txt evaluation/failure.md
```

In the score, `form` is 0.00 for precision and recall. Use section 3.3 of the notebook and day 2's section 2.2 to explain each answer.

| Part | What to write |
|---|---|
| The failure: one wrong value of the first score, after `Note:` and `Field:` in `evaluation/failure.md`. | `Note: 0147` and `Field: form` |
| Its cause: the lines of `prompts/system.txt` that led to it, after `Cause:`. | `Cause: 11, 17` |
| The change: the model writes `form` as the examples do. | In both example replies of `prompts/system.txt`, write `"form": "1040"` in place of `"form": "Form 1040"`. |

<details><summary>Why each answer</summary>

| Part | Why |
|---|---|
| The failure: one wrong value of the first score, after `Note:` and `Field:` in `evaluation/failure.md`. | In `evaluation/runs/1/score.txt`, all 20 wrong values are in `form`. Each label gives the right value: the form number only, such as "1040". Each reply adds "Form". So any note shows the failure, such as 0147. Section 3.3, the list "Score the fields, not the note": "Per field, the score names the instruction to change" |
| Its cause: the lines of `prompts/system.txt` that led to it, after `Cause:`. | Lines 11 and 17 of `prompts/system.txt` are the replies of the two examples. Both write `"form": "Form 1040"`. No line says how to write a form, so the model copies the examples. Day 2 showed the same with amounts. Day 2, section 2.2, the list "Examples teach the shape": "Every example with an amount teaches that notes have amounts" |
| The change: the model writes `form` as the examples do. | The model copies the examples. With "1040" in them, it writes the form number only, as the labels do. Day 2, section 2.2, under "Revise by editing the prompt, then re-score the whole set.": "A loop: run the set, score it, edit the prompt" |

</details>

Save both files, then score your prompt:

```sh
python3 evaluation/score.py
```

For a new prompt, it sends the 20 notes to the model. Expect `form` above 0.00 in the line that ends with `(this prompt)`; if not, the check gives the next change. Then commit and check:

```sh
git add prompts/system.txt evaluation
git commit -m "Revise the prompt once"
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. The check scores your saved replies itself and calls no model.

## Reflect

Why can a labelled set find what the teammate's five replies did not? When would a new line about the form be a better change than the examples? Which differences in your second score come from your change, and which from the run?

[Worked answer](../answers/score-the-prompt/) · [Start over](../../../README.md#start-an-exercise-again)
