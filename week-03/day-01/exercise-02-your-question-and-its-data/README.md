# Exercise 2: Your question, its data, each verdict

**Goal:** After this exercise, you can write a case-selection question and give each piece of information it needs a verdict and a reason.

**Scenario:** Next week's model ranks this year's synthetic returns for examination. You write the question it answers, then the information it needs, and decide for each piece whether the model may have it.

**AI tool:** none. This is thinking work: you write text in this notebook, and no cell reads a table.

**Where you work:** the notebook `week-03/day-01/exercise-02-your-question-and-its-data/exercise.ipynb` in your Git folder of the course, in Databricks. You type in cells 1 to 3. Cell 4 checks what you typed.

**Done when:** cell 4 prints `Done:`.

**Optional part:** none.

**What you have:**

- The trainer's worked example, just before this exercise: the same table, filled for another question.
- In cell 2, a table with one row filled for you.
- `check.py`, beside this notebook. Cell 4 runs it. It reads only your text.

**Start from:** this notebook as the course gives it, attached to any compute. To start again, set the cells you typed back to how the course gives them. Exercise 3 searches for items of your list, and Tuesday reads it, so keep it.

### Step 1. Write the question

Why: the question decides which data the model needs and which data it must not see. So you write it before you open a table.

In cell 1, write after each label. The day's question is one example: "for each return filed this year, how likely is an examination to change the tax?" "That sentence names the unit (one return), the target (a change, yes or no) and the time (this year's returns)." You can use it, or write your own with the same three parts.

| Line | What to write | Why |
|---|---|---|
| `Unit:` | what the model ranks, one row each, such as one return | the model gives each unit one score |
| `Target:` | the outcome the model predicts, such as whether an examination changes the tax | "A measurable stand-in is whether an examination of the return ended with a change to the tax." |
| `Time:` | which returns, as of when, such as returns filed this year | the model ranks this year's returns, and learns from earlier ones |

Run cell 1. It prints your three lines.

Notebook cell 1:

```python
# 1. Your question: write after each label, two words or more.
question = """
Unit:
Target:
Time:
"""
print(question)
```

### Step 2. List the information, and give each item a verdict

Why: each item you keep is information about a taxpayer. Each one needs a reason that comes from your question.

In cell 2, each row of the table is one item. Write 6 rows or more: two or more of each kind. Keep the `|` between the columns. Each row has five columns:

- **Item:** the piece of information, in your words.
- **Kind:** one of three, word for word. `the return's lines`: "The return's reported line items, one row per return." `data to match against`: "Information that can be compared with the return, such as third-party statements." `past outcomes`: "The outcome of past examinations, the target the model learns from, with a record of which outcomes came from a random sample and which from returns an earlier score chose."
- **Question it serves:** the part of your question it helps answer, or `none`.
- **Verdict:** one of three: "needed, with the reason; not needed, so left out; or needed but to be transformed, which Tuesday handles." Write `needed`, `not needed` or `transformed`.
- **Reason:** why, in 4 words or more. The test: "Applied to a model, the test for each field is whether the prediction needs it."

Cell 2 holds the first row for you. The table below gives more rows and their reasons. Write them in your own words, and add your own:

| Item | Kind | Verdict | Why |
|---|---|---|---|
| Wages on the return (filled for you) | `the return's lines` | `needed` | "Start with directly observed and reported features as opposed to learned features." |
| Total income on the return | `the return's lines` | `needed` | the income the return reports is the line item the question depends on most |
| The taxpayer's name, or identifying number | `the return's lines` | `not needed` | "A field that names the taxpayer, such as a name or an identifying number, tells the model nothing about the return's line items that it needs to rank the return" |
| Wages that employers reported | `data to match against` | `needed` | a gap between the return and the payers' reports is what information matching looks for |
| Interest that banks reported | `data to match against` | `needed` | the same, for interest |
| Whether a past examination changed the tax | `past outcomes` | `needed` | it is the target the model learns from |
| How the IRS selected each examined return: random sample or score | `past outcomes` | `needed` | "A model trained only on returns chosen because they scored high never learns what the unchosen returns look like." |

Run cell 2. It prints how many rows you filled.

Notebook cell 2:

```python
# 2. Your list: one row per item. Keep the two header lines. One row is filled for you.
items = """
| Item | Kind | Question it serves | Verdict | Reason |
|---|---|---|---|---|
| Wages on the return | the return's lines | Did the return report all its wages? | needed | A first model starts with what the taxpayer reported directly. |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |
"""
filled = [line for line in items.splitlines() if line.startswith("|") and line.strip("| ") and "---" not in line][1:]
print(len(filled), "rows filled")
```

### Step 3. Explain one item

Why: the outcomes of past examinations are not all alike, and the model learns from them.

In cell 3, between the quotes of `explain = ""`, write one or two sentences: why does your list record how the IRS selected each examined return? Run cell 3.

Notebook cell 3:

```python
# 3. Explain: why does your list record how the IRS selected each examined return?
explain = ""
print(explain or "Write your explanation between the quotes.")
```

### Step 4. Check

Run cell 4. It prints `Done:` when these things are true:

- The question has a `Unit:`, a `Target:` and a `Time:` line, each with two words or more.
- The list has 6 rows or more, and two or more of each kind.
- Each row has a kind, the question it serves, a verdict and a reason of 4 words or more.
- At least one item is `not needed`, and no item that names or identifies a person is `needed`.
- A `past outcomes` item records how the IRS selected each examined return.
- `explain` holds 8 words or more.

Otherwise it prints `Not yet:` and each thing still to do. It checks the form of your record, not whether your reasons are good: the debrief does that. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. The trainer's question was about refunds, and yours is about examinations. Which item would change its verdict between the two questions, and why?
2. You build a feature from fields, and "derived data keeps the class of its source." Which item on your list would you turn into a feature on Wednesday, and what class does the feature keep?
3. A study of audit models found that "the target decides who carries the burden." What would change on your list if the target were the amount of the change, not yes or no?

The answer, after you try: [`answers/exercise-02-your-question-and-its-data`](../answers/exercise-02-your-question-and-its-data/).
