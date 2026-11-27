# Exercise 2: Compute the accuracy every model must beat (we do)

**Goal:** After this exercise, you can count the outcomes of a label and compute the accuracy of a baseline that always predicts the most common one.

**Scenario:** On Tuesday you train two models on the training set, `model_train`, and each one reports an accuracy. Today you work out the baseline's accuracy: the baseline always predicts the most common outcome. The models of Tuesday must beat that number.

**AI tool:** none.

**Where you work:** the notebook `week-04/day-01/exercise-02-baseline-accuracy/exercise.ipynb` in your Git folder of the course, in Databricks. You type in the code cells marked `# 1.` to `# 3.`: cell 1 is the code cell whose first line starts with `# 1.`, and so on. Cell 4 checks what you typed.

**Done when:** cell 4 prints `Done:`.

**Optional part:** Finished early? In a new cell, write one sentence: why does the baseline find no return whose tax changed, although its accuracy looks good?

**What you need to know first:** accuracy is "the share of predictions that are right." A baseline is "the simplest prediction; its accuracy is the one every model must beat." Here the baseline always predicts the most common outcome.

**What you have:**

- `course.returns.model_train`, the week's training set in Unity Catalog, where Databricks keeps the course's tables: the 500 returns of tax years 2020 and 2021, made up by the course.
- The trainer's example, shown before this exercise: the same cells, run on the validation set, `model_valid`.
- `check.py`, beside this notebook. Cell 4 runs it. It counts the table again and compares.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names (the computer in Databricks that runs your cells). To start again, set the cells you typed back to how the course gives them. In a Git folder, Databricks saves your edits as you type.

### Step 1. Count each outcome of the training set

Why: the baseline predicts the most common outcome of the training set. So you count each outcome there first.

In cell 1, type `exam_changed_tax`, the label, between the quotes of `column = ""`. Change nothing else. Run cell 1.

You should see `course.returns.model_train: 500 returns`, then three rows, the largest count first: `no` 320, `NULL` 100 and `yes` 80. `NULL` is an empty cell: the return was never examined, so it has no label.

Notebook cell 1:

```python
# 1. Count each value of the label in the training set. Type the label's column between the quotes.
table = "course.returns.model_train"
column = ""
print(f"{table}: {spark.table(table).count()} returns")
if column:
    spark.sql(f"SELECT {column}, COUNT(*) AS returns FROM {table} GROUP BY {column} ORDER BY returns DESC").show()
else:
    print("Type the label's column between the quotes, then run this cell again.")
```

### Step 2. Guess the baseline's accuracy

Why: writing a guess before cell 3 computes the accuracy shows what you expected, so the real number can surprise you.

The baseline always predicts `no`, the most common outcome. In cell 2, replace `None` with your guess of its accuracy, a share from 0 to 1, such as `0.6`. Any share counts. Run cell 2. You should see your guess printed.

Notebook cell 2:

```python
# 2. Your guess: the accuracy of always predicting "no", as a share from 0 to 1.
guess = None
print("Your guess:", guess)
```

### Step 3. Compute the baseline's accuracy

Why: "A prediction is right or wrong only against a recorded decision." So the returns never examined, which have no label, are left out of the count.

In cell 3, type the two numbers from cell 1's counts. The table below gives each number and its reason.

| Value | Type this | Why |
|---|---|---|
| `right` | `320` | Always predicting `no` is right on every return whose label is `no`. |
| `labelled` | `400` | 320 `no` plus 80 `yes`. The 100 `NULL` returns have no label, so the count leaves them out. |

Run cell 3. You should see `Baseline accuracy: 320 of 400 = 0.8`, and your guess beside it. Accuracy is the right predictions divided by the predictions that can be right or wrong.

Notebook cell 3:

```python
# 3. The baseline always predicts "no". Type how many returns it gets right, and how many have a label.
right = 0
labelled = 0
baseline_accuracy = right / labelled if labelled else None
print(f"Baseline accuracy: {right} of {labelled} = {baseline_accuracy}. Your guess: {guess}")
```

### Step 4. Check

Run cell 4. It prints `Done:` when these things are true:

- Cell 1 counts `exam_changed_tax`.
- Cell 2 holds a guess from 0 to 1.
- Cell 3's `right` and `labelled` match the table, without the empty labels.

Otherwise it prints `Not yet:` and each thing still to do. It counts the table again. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# Do not change this cell. It runs check.py, beside this notebook.
```

### Afterwards, together

1. What does a rarer yes do to the accuracy of the baseline?
2. What must a model show before you call it better than the baseline?
3. How could the returns nobody examined differ from the others?

The answer: after the talk together, open `week-04/day-01/answers/exercise-02-baseline-accuracy/` in your Git folder of the course ([link](../answers/exercise-02-baseline-accuracy/)).
