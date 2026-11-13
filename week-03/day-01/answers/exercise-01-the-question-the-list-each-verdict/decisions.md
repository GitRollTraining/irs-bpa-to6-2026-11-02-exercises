# Exercise 1: decisions

For the trainer. The exercise is deck slide 30, "Exercise 1: The question, the list, each verdict". Each section gives one thing the learner does, the answer and its reason. It also gives where the rule is taught and what else the check accepts. The check is `check.py` in the exercise folder. It reads `record.json`, which cell 2 writes. `files/record.json` holds the kept answer. The check calls no model.

## 1. The question

- **The answer.** "For each return filed this year, how likely is an examination to change the tax?"
- **Reason.** It names the unit (one return) and the target (a change to the tax, yes or no). It also names the time (this year's returns).
- **Where it is taught.** Monday's curated file, § Let the question decide the data: "That sentence names the unit (one return), the target (a change, yes or no) and the time (this year's returns)." The target, from the same section: "A measurable stand-in is whether an examination of the return ended with a change to the tax."
- **What else the check accepts.** Any sentence with three things in it: "return", a form of "change" with "tax", and "year" or a year in digits. A question about being "selected for review" fails. The target of this week is whether an examination changed the tax.

## 2. The kinds

- **The answer.** `wages_amt` and `total_income_amt`: line item. `w2_wages_amt`: compare. `exam_changed_tax` and `exam_picked_by`: outcome. `taxpayer_name`, `tin` and `street_address`: none.
- **Reason.** The three kinds are the three parts of the reading's list. They are the return's own line items, information to compare with the return, and the outcome of past examinations. The identifying fields are none of the three.
- **Where it is taught.** Curated file, § Pick the information that helps select a case. The numbered list holds the three parts. The table's row for information matching says: "Third-party reports, such as wage and interest statements, to compare with the return". Item 3 of the list names "a record of which outcomes came from a random sample and which from returns an earlier score chose". So `exam_picked_by` is an outcome.
- **What else the check accepts.** Only these kinds. The kind is what the field holds, so it has one answer.

## 3. The verdicts

- **The answer.** Needed: the five line item, compare and outcome fields. Not needed: `taxpayer_name` and `street_address`. Transform: `tin`.
- **Reason.** "Keep a field only if the prediction needs it." A name or an address identifies a person and tells the ranking nothing. The identifying number joins the three tables, so the learner keeps it for the join. Tuesday replaces its value with a substitute value.
- **Where it is taught.** Deck slide 26, right column: "Keep a field only if the prediction needs it". The same column: "A name or identifying number tells the ranking nothing it needs". Deck slide 28, the verdict record's row for the name: "Not needed: left out". Its row for the identifying number: "Needed, to be transformed". The curated file, last paragraph of § Leave out what the use does not need, gives the three verdicts.
- **What else the check accepts.** `tin` takes only `transform`. Slide 26 and the curated file say the ranking has no need for an identifying number. Both read as "not needed". Slide 28 rules the same field "Needed, to be transformed" because it joins tables. `fields.csv` says it "joins the three tables". So the check keeps slide 28's verdict. Step 2's table gives the reason for both readings: the ranking needs no identifying number, but the tables join on it. Take it to the debrief. Both sources are right about different uses: the model's input, and the join.

## 4. The reasons

- **The answer.** Any reason of three words or more. The kept answer's reasons are in `files/record.json`.
- **Reason.** A reason is a judgment in the learner's words. So the check reads its length only. The trainer reads the reasons in the debrief.

## 5. The target line

- **The answer.** "We predict a change to the tax, yes or no, because examiner time is scarce. We considered predicting the amount, which moves audits toward higher incomes, and we note that cost."
- **Where it is taught.** Curated file, § Leave out what the use does not need: "So the anchor question needs one more line before you search: a recorded choice of target." Deck slide 27: "Predicting the amount: higher incomes".
- **What else the check accepts.** Any line with a form of "change" and the word "amount".

## Findings of the readability linter inside quotes

- Section 5 quotes the curated file. The quote's colon and length are the curated file's.

## Where it runs

- The author ran it on 2026-11-13 in a scratch copy of the exercise folder on a laptop. The run used the course's `.venv` (Python 3.12.6) and a Jupyter kernel whose working folder is the notebook's folder. The author did not run it in Databricks: the machine that wrote the exercise has no Databricks access. The kept run is in `kept-run.md`.
- What Databricks must do, each step from Databricks' public documentation:
  1. Clone the course into the workspace as a Git folder. The page says: "Click Create > Git folder." The field is "Git repository URL" (https://docs.databricks.com/aws/en/repos/git-operations-with-repos). The page says the workspace "must have Git credentials configured". It does not say if a public repository needs them.
  2. Open `exercise.ipynb` as a notebook: "Databricks supports creating and editing notebooks in two formats: IPYNB (default) and source." (https://docs.databricks.com/aws/en/notebooks/notebook-format). The page does not say directly that an `.ipynb` file in a Git folder opens as a notebook.
  3. Read `fields.csv` and `check.py` from the notebook's folder: "In Databricks Runtime 14.0 and above, the CWD is the directory containing the notebook or script being run." (https://docs.databricks.com/aws/en/files/cwd-dbr-14). For that reason the cells use `Path.cwd()`. They use `runpy`, not `%run`. In Databricks, `%run` runs a notebook, not a Python file. Another page warns: "On serverless compute, the working directory is not guaranteed, so use absolute paths to reference files." (https://docs.databricks.com/aws/en/files/workspace-modules).
  4. Write `record.json` beside the notebook (cell 2). No page read for this exercise says if a notebook can write a file into a Git folder.
- **Trainer gap.** A trainer with access to the course's Databricks workspace runs the exercise once. The trainer starts from a fresh Git folder, on the compute the learners use. Cell 1 prints eight fields. Cell 2, with the values of `files/record.json`, prints "Saved record.json". Cell 3 prints `Done:`. If step 3 or step 4 fails on serverless compute, the fix goes in the cells, not in the learner's steps.
