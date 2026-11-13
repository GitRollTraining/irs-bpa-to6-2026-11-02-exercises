# Exercise 1: The question, the list, each verdict

**Goal:** After this exercise, you can write a case-selection question and decide, with a reason, which information it needs.

**Scenario:** Your team will build a model that ranks this year's returns for examination. Before anyone queries a table, you write the question. Then you find eight fields in the workspace's catalog, read what each holds, and give each a kind, a verdict and a reason. Tuesday starts from your verdicts.

**Coding agent:** no.

**Where you work:** Catalog Explorer, and the notebook `exercise.ipynb` in `week-03/day-01/exercise-01-the-question-the-list-each-verdict`, in the course's Git folder in Databricks.

**Start from:** the notebook as the course gives it, attached to compute as this morning's tour showed. The notebook is in the course's Git folder, a copy of the course's Git repository inside the workspace. If you do not have that folder yet: in the sidebar, select **Workspace**, then **Create > Git folder**. In **Git repository URL**, paste `https://github.com/GitRollTraining/irs-bpa-to6-2026-11-02-exercises`. Each code cell has a number on its first line: `# 1.`, `# 2.` or `# 3.` The steps use that number. To start again, set each value you typed in cell 2 back to `""`. Keep the two rows marked "done for you". Then run cell 2.

**What you have:** three tables in the schema `case_selection`: `returns`, `wage_statements` and `exam_outcomes`. Each column has a comment that says what it holds. Beside the notebook: `fields.csv`, which holds the same eight fields and comments, and `check.py`, the course's check, which cell 3 runs. Cell 1 reads `fields.csv` when it cannot read the tables. The course made up every table, row and file.

**Done when:** cell 3 prints `Done:`.

**Optional part:** none.

## Step 1. Find the fields in the catalog

Why: the fields a model may use sit in tables that other people built. The catalog tells you what each column holds before you decide on it.

In Catalog Explorer:

1. In the sidebar, select **Catalog**. Catalog Explorer opens. Why: it shows the tables and their descriptions, and you run no query.
2. Open the catalog that the trainer names in the chat. Why: a catalog is the top level, and it holds schemas.
3. Open the schema `case_selection`. You see three tables: `returns`, `wage_statements` and `exam_outcomes`. Why: a schema keeps the tables of one project together.
4. Open `returns`. Read the table's comment below its name. Why: it says what one row of the table is.
5. Select the **Columns** tab. Each row is one column: its name, its type and its comment. Find `tin`. Read its comment. Why: a comment is text that someone wrote about the column. In step 3 you decide from it.
6. Select the **Sample Data** tab. Why: a few rows show what the values look like. The tab uses compute. If it asks for compute, select the compute that the trainer named.
7. Open `wage_statements` and `exam_outcomes` in the same way. Which column is in all three tables?

In cell 1, type the schema's name between the quotes of `schema = ""`. The name is the catalog's name, a dot, and `case_selection`. For example, if the catalog is `training`, type `training.case_selection`. Then run cell 1.

How to read the output of cell 1: the first line says where cell 1 read the fields, the catalog or `fields.csv`. Then each field has one line: its name, its table or tables, and its comment. If the first line names `fields.csv`, the next line says why. Look at the name you typed, or ask the trainer. You can do the rest of the exercise with either source.

## Step 2. Write the question

Why: the question decides which fields a model needs. So you write it before you decide on a field.

In cell 2, type your question between the quotes of `question = ""`. Write one sentence. The question names three things:

| Part | What to write | Why |
|---|---|---|
| Unit | one return | the model ranks returns, one row for each return |
| Target | whether an examination changes the tax | "a measurable stand-in is whether an examination of the return ended with a change to the tax" |
| Time | this year's returns | the returns you rank are the ones filed this year |

An example of the form, for a different case: *for each refund claim filed this month, how likely is a review to reduce the refund?* Write yours for this week's case.

## Step 3. Give each field a kind, a verdict and a reason

Why: each field you keep is information about a person. So each field needs a reason that comes from the question.

In cell 2, each field has three values. Type each value between its quotes.

- `kind`: one of the three kinds on the list you take into the catalog, or `none`. `line item`: "the return's reported line items". `compare`: "information that can be compared with the return, such as third-party statements". A W-2 is the wage statement an employer sends. `outcome`: "the outcome of past examinations, the target the model learns from, with a record of which outcomes came from a random sample and which from returns an earlier score chose". `none`: none of the three, such as a field that only says who the taxpayer is.
- `verdict`: `needed`, `not needed` or `transform`. `needed`: the model, or the training that builds it, reads the field's value. `not needed`: nothing needs the field. `transform`: the model never reads the field's value, but the field still does a job, such as joining tables. Tuesday replaces its value with a made-up value that still joins the tables. Case does not matter in a kind or a verdict.
- `reason`: why, in three words or more, in your own words.

The rule for a verdict: "Keep a field only if the prediction needs it." The prediction needs a field when the model reads its value, or when the training reads it to learn the model.

Cell 2 already holds the values of two fields. This table gives them and their reasons:

| Field | kind | verdict | Why |
|---|---|---|---|
| `wages_amt` | `line item` | `needed` | its comment says the taxpayer reported it on the return, and a first model should "start with directly observed and reported features" |
| `taxpayer_name` | `none` | `not needed` | it is none of the three kinds, and a name "tells the ranking nothing it needs" |

The other six fields are yours. For each, read its comment in Catalog Explorer or in the output of cell 1. Then answer two questions. Which of the three kinds does it hold? Do the model or its training read its value, or does the field only do a job?

Explain one field. In cell 2, type one or two sentences between the quotes of `explain = ""`. Say what `exam_picked_by` lets the model tell apart. Then say why that matters for what the model learns.

## Step 4. Write the target line, and check

Why: the target is a choice, and the choice moves which taxpayers get examined. So you record what you chose and what you considered.

In cell 2, type your target line between the quotes of `target = ""`. Write it in your own words, in one or two sentences, with three parts:

| Part | What to write | Why |
|---|---|---|
| The target you chose | a change to the tax, yes or no | the question's target |
| Why | the scarce resource the ranking spends | the true objective is "to spend examiner time where it changes the most tax" |
| What you considered, and its cost | predicting the amount instead, and who it moves audits toward | "the expected amount of misreport (regression) shifts audit focus from lower income to higher income taxpayers" |

Run cell 2. It saves your values to `record.json`, a file beside the notebook. Then run cell 3. It runs `check.py`, the course's check. It prints `Done:` when these things are true:

- The question names its unit, its target and its time.
- Each field has the right kind and verdict, and a reason of three words or more.
- Your sentence on `exam_picked_by` says which two kinds of past examination it tells apart.
- The target line names the change to the tax and the amount you considered.

How to read the output of cell 3: `Not yet: 4 left.` means four things are not yet right. Each line under it names one field or one part, and the step to read again. The line names a wrong value, but not the right one. Fix each in cell 2. Then run cell 2 and cell 3 again.

## Afterwards, together

1. Which field was hardest to tie to the question, and why?
2. If the tables had no `exam_picked_by` column, which of your verdicts would change, and what would you ask the team that keeps the tables?
3. Which verdict would a reviewer challenge first, and why?

The answer: [answers/exercise-01-the-question-the-list-each-verdict](../answers/exercise-01-the-question-the-list-each-verdict/).
