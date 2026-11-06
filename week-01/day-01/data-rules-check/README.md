# 1.2 Check data rules

Classify four proposed uses of AI tools and identify decisions that require approval.

Your team wants to send files to AI tools. Use sections 1.1–1.2 of the notebook to decide which uses are permitted in the scenario. All files are fictional; treat the exported case note as protected data for this exercise.

## Start

Follow the [Day 1 setup](../README.md). Work by hand, without AI tools. In a new terminal in the course folder, create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-01/data-rules-check/lab/.git || python3 reset.py data-rules-check
cd week-01/day-01/data-rules-check/lab
```

All paths below are relative to `lab/`.

## Classify and explain

Open `docs/data-rules-check.md` and the files it names. Fill in each row with a decision, the role that decides when needed, and a reason tied to the notebook's rules.

| Proposed use | Question to resolve |
|---|---|
| `notes/0147.txt` → course-approved tool | Does the note's origin fall within the approval? |
| `exports/case-2231.txt` → public chat tool | Does removing a name remove all protected information? |
| `exports/case-2231.txt` → course-approved tool | Does tool approval cover this data and use? |
| `model.py` → public chat tool | Does the rule cover work-related code without taxpayer data? |

<details><summary>Why each answer</summary>

| Proposed use | Look for this |
|---|---|
| `notes/0147.txt` → course-approved tool | Read its first line. Is the note from the lab? Then find its row in the six-row table of section 1.2. |
| `exports/case-2231.txt` → public chat tool | Read its first line. Where does the note come from? The name is gone. What does the note still give? Section 1.1: "Nameless, it still gives year, form, amount, date". |
| `exports/case-2231.txt` → course-approved tool | Does the approval cover a real note? Section 1.2, move 5: "Use approval: the accountable official". |
| `model.py` → public chat tool | It holds no taxpayer data. Is it safe? Section 1.1: the policy covers "any information, including seemingly innocuous work-related matters", in "public or non-Treasury AI tools". |

</details>

Save the table, then commit and check:

```sh
git add docs/data-rules-check.md
git commit -m "Answer the data-rules check"
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. Be ready to explain your reasoning as well as complete the table.

## Reflect

Why can the same tool be acceptable for one file and require approval for another? Why can code without taxpayer data still be restricted?

[Worked answer](../answers/data-rules-check/) · [Start over](../../../README.md#start-an-exercise-again)
