# Exercise 1: The question, the list, each verdict

**Goal:** After this exercise, you can write a case-selection question and decide, with a reason, which information it needs.

**Scenario:** Your team will build a model that ranks this year's returns for examination. Before anyone opens a table, you write the question. Then you give each of eight fields a kind, a verdict and a reason. The course made up the fields. Tuesday starts from your verdicts.

**Coding agent:** no.

**Where you work:** the notebook `exercise.ipynb` in `week-03/day-01/exercise-01-the-question-the-list-each-verdict`, in your copy of the course. In Databricks, it is in the course's Git folder. On the Workstation, it is in VS Code's Explorer under `week-03 > day-01`.

**Start from:** the notebook as the course gives it. In Databricks, get the course once: in the sidebar, select **Workspace**, then **Create > Git folder**, and paste the course's address in **Git repository URL**. Open `exercise.ipynb` in this folder. Attach the notebook to compute, as this morning's tour showed. On the Workstation, open the same notebook in VS Code. Each code cell has a number on its first line: `# 1.`, `# 2.` or `# 3.` The steps use that number. To start again, set the values in cell 2 back to `""`. Then run cell 2.

**What you have:** `fields.csv`, eight fields the course made up, in three tables: `returns`, `wage_statements` and `exam_outcomes`. The course made up every file in this folder.

**Done when:** cell 3 prints `Done:`.

**Optional part:** none.

## Step 1. Write the question

Run cell 1. It prints the eight fields of `fields.csv`: each field, its table and what it holds. The course made up every field and table.

In cell 2, type your question between the quotes of `question = ""`. Write one sentence. The question names three things:

| Part | What to write | Why |
|---|---|---|
| Unit | one return | the model ranks returns, one row for each return |
| Target | whether an examination changes the tax | "a measurable stand-in is whether an examination of the return ended with a change to the tax" |
| Time | this year's returns | the returns you rank are the ones filed this year |

For example: *for each return filed this year, how likely is an examination to change the tax?*

## Step 2. Give each field a kind, a verdict and a reason

In cell 2, each field has three values to fill in. Type each value between its quotes.

- `kind`: `line item` (the return's own line items), `compare` (information to compare with the return), `outcome` (the outcome of a past examination) or `none` (none of the three). Case does not matter.
- `verdict`: `needed`, `not needed` or `transform`. `transform` means the field does a job, such as joining tables, but the model never sees its value: Tuesday replaces the value.
- `reason`: why, in three words or more.

The rule for a verdict: "Keep a field only if the prediction needs it."

| Field | kind | verdict | Why |
|---|---|---|---|
| `wages_amt`, `total_income_amt` | `line item` | `needed` | "A line item the ranking compares with similar returns" |
| `w2_wages_amt` | `compare` | `needed` | information matching compares "third-party reports, such as wage and interest statements" with the return |
| `exam_changed_tax` | `outcome` | `needed` | it is the target, the answer the model learns from |
| `exam_picked_by` | `outcome` | `needed` | the list keeps "a record of which outcomes came from a random sample and which from returns an earlier score chose" |
| `taxpayer_name`, `street_address` | `none` | `not needed` | a name or an address "says nothing the ranking needs" |
| `tin` | `none` | `transform` | the ranking needs no identifying number, but the three tables join on it. So you keep it for the join, and Tuesday replaces its value |

Write the reasons in your own words.

## Step 3. Write the target line, and check

In cell 2, type your target line between the quotes of `target = ""`. It says the target you chose, why, and what you considered. For example: *We predict a change to the tax, yes or no, because examiner time is the scarce resource. We considered predicting the amount, which moves audits toward higher incomes, and we note that cost.*

Run cell 2. It saves your values to `record.json`, a file beside the notebook that the check reads. Then run cell 3. It runs `check.py`, the course's check. It prints `Done:` when these things are true:

- The question names its unit, its target and its time.
- Each field has the kind and the verdict of the table in step 2, and a reason of three words or more.
- The target line names the change to the tax and the amount you considered.

Otherwise it prints `Not yet:` and each thing still to do. Fix each one in cell 2. Then run cell 2 and cell 3 again.

## Afterwards, together

1. Which field was hardest to tie to the question, and why?
2. Why would a random sample change which outcomes you trust?
3. Which verdict would a reviewer challenge first, and why?

The answer: [answers/exercise-01-the-question-the-list-each-verdict](../answers/exercise-01-the-question-the-list-each-verdict/).
