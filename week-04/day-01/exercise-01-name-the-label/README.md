# Exercise 1: Name the label each question could learn from (we do)

**Goal:** After this exercise, you can name the label a case-selection question could learn from, or say that it has none.

**Scenario:** Two teams each bring a case-selection question and ask for a model. Before anyone builds a model, you say which past decision each model could learn from. One of the two questions has none.

**AI tool:** none. This is thinking work: you write text in this notebook. One cell lists the columns of the table.

**Where you work:** the notebook `week-04/day-01/exercise-01-name-the-label/exercise.ipynb` in your Git folder of the course, in Databricks. You type in the code cells marked `# 2.` and `# 3.`: cell 2 is the code cell whose first line starts with `# 2.`, and so on. Cell 4 checks what you typed.

**Done when:** cell 4 prints `Done:`.

**Optional part:** Finished early? In a new cell, write a third question of your own, its label or `no label`, and the kind of answer it needs: yes or no, or an amount.

**What you need to know first:** a label is the past decision recorded for a return. "A label exists only where someone decided."

**What you have:**

- `course.returns.model_returns`, the week's return table in Unity Catalog, where Databricks keeps the course's tables: 1,000 returns, made up by the course.
- The trainer's example, shown before this exercise.
- `check.py`, beside this notebook. Cell 4 runs it. It reads your text and the table's column names.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names (the computer in Databricks that runs your cells). To start again, set the cells you typed back to how the course gives them. In a Git folder, Databricks saves your edits as you type.

### Step 1. See which past decisions the table records

Why: a label is a past decision that the table records. So you look first at what the table records.

Run cell 1. You should see 18 column names, from `case_id` to `tax_added_by_exam`. Two of them come from past examinations: `exam_changed_tax` and `tax_added_by_exam`. One, whose name starts with `made_up`, is a code the course made up for a later day: nothing today uses it. The other 15 are keys (numbers that tell one return or filer from another), header fields and the amounts on the return. None of them records what happened after filing.

Notebook cell 1:

```python
# 1. The columns of the week's return table. You do not need to change this cell.
columns = spark.table("course.returns.model_returns").columns
print(len(columns), "columns:", ", ".join(columns))
```

### Step 2. Name each question's label

Why: "If no column records a past decision, it is not classification."

In cell 2, type the label and the reason for each question, between the quotes. Copy the reason from the table below, or write it in your own words: 6 words or more. Type no quotation marks inside an answer: they end it early.

| Question | `label` | `why` |
|---|---|---|
| `Q1`: Which of this year's returns would an examination most likely change the tax on? | `exam_changed_tax` | The column records a past decision, yes or no, and the question asks yes or no. |
| `Q2`: Which of this year's returns will the taxpayer later correct with an amended return? | `no label` | No column records whether a taxpayer amended a past return. |

Run cell 2. You should see your two answers printed.

Notebook cell 2:

```python
# 2. Each question's label: a column name, or "no label". Then why, 6 words or more.
answers = {
    "Q1": {"label": "", "why": ""},
    "Q2": {"label": "", "why": ""},
}
for question, answer in answers.items():
    print(question, "label:", answer["label"] or "(empty)", "| why:", answer["why"] or "(empty)")
```

### Step 3. Say what Q2 would need

Why: the reading gives two reasons a question can lack a label. Q2 has the first: "the decision could be recorded and nobody recorded it, so the question gets a label once someone does." So you say what the table would have to record.

In cell 3, between the quotes of `needs = ""`, write what the table would have to record for Q2 to have a label: 8 words or more. Run cell 3. You should see your sentence printed.

Stuck? Cell 3's comment gives an example for a different question, not Q2. Copy its shape, not its words: a column, for each past return, that records a decision, yes or no.

Notebook cell 3:

```python
# 3. What would the table have to record for Q2 to have a label?
# An example for a different question, not Q2: "A column that records, for each past return, whether the IRS sent the taxpayer a notice, yes or no."
needs = ""
print(needs or "Write your sentence between the quotes.")
```

### Step 4. Check

Run cell 4. It prints `Done:` when these things are true:

- Q1's label is a column of `course.returns.model_returns` that records a yes-or-no past decision.
- Q2's label is `no label`.
- Each `why` has 6 words or more, and `needs` has 8 words or more.

Otherwise it prints `Not yet:` and each thing still to do. It checks the labels, not your reasons. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# Do not change this cell. It runs check.py, beside this notebook.
```

### Afterwards, together

1. Q2 gets a label once someone records it. Which returns would still have no label?
2. When can a model learn from today's new decisions?
3. What would you ask about a label before you trust it?

The answer: after the talk together, open `week-04/day-01/answers/exercise-01-name-the-label/` in your Git folder of the course ([link](../answers/exercise-01-name-the-label/)).
