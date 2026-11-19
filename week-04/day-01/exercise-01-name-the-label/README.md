# Exercise 1: Name the label each question learns from (we do)

**Goal:** After this exercise, you can name the past decision that a case-selection question learns from, or say that it has none.

**Scenario:** Two colleagues each bring a question for a model. The week's return table records one kind of past decision. You decide which question that decision can teach, and which question it cannot.

**AI tool:** none. This is thinking work: you write text in this notebook. One cell lists the columns of the table.

**Where you work:** the notebook `week-04/day-01/exercise-01-name-the-label/exercise.ipynb` in your Git folder of the course, in Databricks. You type in the code cells marked `# 2.` and `# 3.`: cell 2 is the code cell whose first line starts with `# 2.`, and so on. Cell 4 checks what you typed.

**Done when:** cell 4 prints `Done:`.

**Optional part:** Finished early? Write a third question in a new cell, and say what kind of answer it needs: yes or no, an amount, or no label.

**What you need to know first:** a label is the past decision recorded for a case. A model learns only from cases that have one.

**What you have:**

- `course.returns.model_returns`, the week's return table in Unity Catalog: 1,000 returns, made up by the course.
- The trainer's example, shown before this exercise.
- `check.py`, beside this notebook. Cell 4 runs it. It reads your text and the table's column names.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. To start again, set the cells you typed back to how the course gives them. In a Git folder, Databricks saves your edits as you type.

### Step 1. See which past decisions the table records

Why: "A label is the past decision recorded for a case." So you look first at what the table records.

Run cell 1. You should see 18 column names, from `case_id` to `tax_added_by_exam`. Two of them come from past examinations: `exam_changed_tax` and `tax_added_by_exam`. The other 16 are keys, header fields, a made-up filing channel and the amounts of the return as filed. None of them records what happened after filing.

Notebook cell 1:

```python
# 1. The columns of the week's return table. You do not need to change this cell.
columns = spark.table("course.returns.model_returns").columns
print(len(columns), "columns:", ", ".join(columns))
```

### Step 2. Name each question's label

Why: "If you cannot name that decision for a question, no model of this week's kind can answer it."

In cell 2, type the label and the reason for each question. Write each answer between the quotes. The table gives each answer and its reason. Copy the table's reason, or write it in your own words: 6 words or more. Type no quotation marks inside an answer: they end it early.

| Question | `label` | `why` |
|---|---|---|
| `Q1`: Which of this year's returns would an examination most likely change the tax on? | `exam_changed_tax` | The column records the past decision: yes when an examination changed the tax, no when it did not. The question asks yes or no, so this is its label. |
| `Q2`: Which of this year's returns will the taxpayer later correct with an amended return? | `no label` | No column records whether a taxpayer amended a past return. A model can learn only from a decision someone recorded in the past. |

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

Why: a question with no label today can get one, if someone records the decision.

In cell 3, between the quotes of `needs = ""`, write one or two sentences: what would the table have to record for Q2 to have a label? Write 8 words or more. Your sentence names the decision, and says that the table records it for each past return. Run cell 3. You should see your sentence printed.

<details><summary>Stuck? One way to say it</summary>

A column that records, for each past return, whether the taxpayer later filed an amended return, yes or no.

</details>

Notebook cell 3:

```python
# 3. What would the table have to record for Q2 to have a label?
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

1. No exam ever: what could Q1 learn from?
2. Examiners chose the returns: what could a model miss?
3. When could a wrong return still read no?

The answer: after the talk together, open `week-04/day-01/answers/exercise-01-name-the-label/` in your Git folder of the course ([link](../answers/exercise-01-name-the-label/)).
