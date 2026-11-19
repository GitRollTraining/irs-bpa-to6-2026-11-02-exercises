# Exercise 2: Count the outcomes and compute the baseline's accuracy (we do)

**Goal:** After this exercise, you can compute the accuracy of a baseline that always predicts the most common outcome in the training set.

**Scenario:** On Tuesday you train two models, and each must beat a number. That number is the baseline's accuracy. You count the outcomes of the week's training set, predict the baseline's accuracy, then compute it.

**AI tool:** none.

**Where you work:** the notebook `week-04/day-01/exercise-02-baseline-accuracy/exercise.ipynb` in your Git folder of the course, in Databricks. You type in the code cells marked `# 2.` to `# 4.`: cell 2 is the code cell whose first line starts with `# 2.`, and so on. Cell 5 checks what you typed.

**Done when:** cell 5 prints `Done:`.

**Optional part:** Finished early? In a new cell, write one sentence: why does this accuracy look good, and still send no return to an examiner?

**What you need to know first:** "Accuracy is the share of predictions that are right." A baseline is "the simplest prediction you can make, used as the score to beat": here, always the most common outcome.

**What you have:**

- `course.returns.model_train`, the week's training set in Unity Catalog: the 500 returns of tax years 2020 and 2021, made up by the course.
- The trainer's example, shown before this exercise: the same counting cell, on another column.
- `check.py`, beside this notebook. Cell 5 runs it. It counts the table again and compares.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. To start again, set the cells you typed back to how the course gives them. In a Git folder, Databricks saves your edits as you type.

### Step 1. Open the training set

Why: a model learns from the training set, so the score it must beat comes from the same rows.

Run cell 1. You should see `course.returns.model_train: 500 returns`.

Notebook cell 1:

```python
# 1. The training set. You do not need to change this cell.
table = "course.returns.model_train"
print(f"{table}: {spark.table(table).count()} returns")
```

### Step 2. Count each outcome

Why: the baseline predicts the most common outcome, so you count each one first.

Cell 2 counts each value of one column. The trainer ran it on `filing_status`. In cell 2, change `"filing_status"` to `"exam_changed_tax"`, the label. Change nothing else. Run cell 2.

You should see three rows, the largest count first: `no` 320, `NULL` 100 and `yes` 80. `NULL` is an empty cell: "A return that was never examined has no label." 

Notebook cell 2:

```python
# 2. Count each value of one column. Change only the name between the quotes.
column = "filing_status"
spark.sql(f"SELECT {column}, COUNT(*) AS returns FROM {table} GROUP BY {column} ORDER BY returns DESC").show()
```

### Step 3. Predict the baseline's accuracy

Why: a prediction you write before you compute shows what you expected. Then the number can surprise you.

The baseline always predicts `no`, the most common outcome. Before cell 4 divides, guess its accuracy as a share from 0 to 1, such as `0.6`. In cell 3, replace `None` with your guess. Any share counts. Run cell 3. You should see your guess printed.

Notebook cell 3:

```python
# 3. Your guess: the accuracy of always predicting "no", as a share from 0 to 1.
prediction = None
print("Your prediction:", prediction)
```

### Step 4. Compute the baseline's accuracy

Why: "On our data, the baseline is computed on the labelled returns of the training set only, the ones with `yes` or `no`."

In cell 4, type the three values from cell 2's counts. The table gives each value and its reason.

| Value | Type this | Why |
|---|---|---|
| `most_common` | `"no"` | It has the most rows among the labels: 320 against 80. |
| `right` | `320` | Always predicting `no` is right on every return whose label is `no`. |
| `labelled` | `400` | 320 `no` plus 80 `yes`. The 100 `NULL` returns have no label, so a prediction on them is neither right nor wrong. |

Run cell 4. You should see `Baseline accuracy: 320 of 400 = 0.8`. Accuracy is the right predictions divided by all predictions.

Notebook cell 4:

```python
# 4. The baseline: its prediction, how many it gets right, and how many labelled returns it predicts.
most_common = ""
right = 0
labelled = 0
baseline_accuracy = right / labelled if labelled else None
print(f"Baseline accuracy: {right} of {labelled} = {baseline_accuracy}")
```

### Step 5. Check

Run cell 5. It prints `Done:` when these things are true:

- Cell 2 counts `exam_changed_tax`.
- Cell 3 holds a prediction from 0 to 1.
- Cell 4's `most_common`, `right` and `labelled` match the table, without the empty labels.

Otherwise it prints `Not yet:` and each thing still to do. It counts the table again. You do not need to read its code.

Notebook cell 5:

```python
# 5. Check. You do not need to read this code.
# Do not change this cell. It runs check.py, beside this notebook.
```

### Afterwards, together

1. A model scores 0.81: what else would you check?
2. Why would counting the 100 empty rows as no mislead?
3. If one change in four, how would the baseline move?

The answer: after the talk together, open `week-04/day-01/answers/exercise-02-baseline-accuracy/` in your Git folder of the course ([link](../answers/exercise-02-baseline-accuracy/)).
