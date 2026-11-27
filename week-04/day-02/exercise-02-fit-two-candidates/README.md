# Exercise 2: Fit two candidates and compare each with the baseline

**Goal:** After this exercise, you can fit two candidates from given cells and compare each one's validation accuracy with the baseline's.

**Scenario:** Your labels are counted and your features are marked. Now you train. You fit a logistic regression, change one line to fit a decision tree, and set both accuracies beside the baseline's, on the same validation rows.

**AI tool:** none.

**Time:** 15 minutes: 11 to do it, 4 for setup problems.

**Where you work:** this notebook, `week-04/day-02/exercise-02-fit-two-candidates/exercise.ipynb`, in your Git folder of the course in Databricks. Databricks may show tips under a cell, such as one about MLflow or Genie Code. Close them: they change nothing.

**Done when:** cell 8 prints `Done:`.

**Cells:** a cell's number is the `# N.` comment on its first line, such as `# 1.`; text cells have no number.

**Optional part:** Finished early? Cell 9 asks for one sentence.

**What you have:**

- `course.returns.model_train` and `course.returns.model_valid`, the course's training and validation sets, as on Monday. If they cannot be read, cell 2 makes the same rows from the course's setup file and says so. Cell 2 adds Monday's flag `deduction_missing`.
- `load.py` and `check.py`, given code that cells 2 and 8 run.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. No cell changes your tables. New here: you change the line that names the model.

### Step 1. Read the rows, keep the features, measure the baseline

"A comparison is fair only on the same rows." (the day's reading)

Cell 3 keeps twelve features of the course tables: Monday's three marked `before` in exercise 1, and nine more from the filed return (the filing status, amounts and a ratio), which the day's reading marks `before`. None comes from `fields.csv`.

Run cells 1 to 4. You do not need to change them. You should see:

1. Which tables cell 2 uses.
2. 400 training rows and 200 validation rows with a label.
   - Cell 3 keeps the twelve features known before selection.
   - It reads an empty amount as 0.
   - `deduction_missing` still says which deduction lines were empty.
3. The baseline always predicts `no`. Its accuracy is 0.8 on the training rows, counted as in Monday's exercise 2, and 0.8 on the validation rows. There are 200 validation returns, so each one more right moves an accuracy by 0.005: step 2's guess counts in returns.

Notebook cell 1:

```python
# 1. Where the course's files are. You do not need to change this cell.
import os
course_folder = os.getcwd().split("/week-04/")[0]  # your Git folder of the course
print("Your Git folder of the course:", course_folder)
```

Notebook cell 2:

```python
# 2. Read the course's training and validation sets, with Monday's flag deduction_missing.
try:
    train_table = spark.table("course.returns.model_train")  # the training set: tax years 2020 and 2021
    valid_table = spark.table("course.returns.model_valid")  # the validation set: tax year 2022
except Exception:
    train_table, valid_table = None, None  # not there: load.py makes the same rows

# You do not need to read the lines below. They run load.py, beside this notebook.
folder = f"{course_folder}/week-04/day-02/exercise-02-fit-two-candidates"
exec(open(f"{folder}/load.py", encoding="utf-8").read())
train, valid = load_sets(train_table, valid_table)
```

Notebook cell 3:

```python
# 3. The features known before selection, and the label. An empty amount is read as 0.
assert "train" in globals(), "Run cells 1 and 2 first."
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

features = ["filing_status", "wages_amt", "taxable_interest_amt", "other_income_amt",
            "total_income", "agi_amt", "deduction_amt", "deduction_missing",
            "total_tax_amt", "withholding_amt", "tax_to_agi", "deduction_to_agi"]  # each known before selection
train = train[train["exam_changed_tax"].notna()]  # leave out the returns with an empty label
valid = valid[valid["exam_changed_tax"].notna()]
X_train, y_train = train[features].fillna(0), train["exam_changed_tax"]  # an empty amount read as 0;
X_valid, y_valid = valid[features].fillna(0), valid["exam_changed_tax"]  # deduction_missing says which
print(len(X_train), "training rows and", len(X_valid), "validation rows have a label")
print("Deduction lines read as 0 because they were empty:", int(train["deduction_missing"].sum()), "in training,",
      int(valid["deduction_missing"].sum()), "in validation")
```

Notebook cell 4:

```python
# 4. The baseline, always "no", measured again on the validation rows.
assert "y_valid" in globals(), "Run cell 3 first."
n = len(y_valid)
print(n, "validation returns have a label. One more right moves the accuracy by", round(1 / n, 3))
print("Their labels:", y_valid.value_counts().to_dict())
baseline_accuracy = accuracy_score(y_valid, ["no"] * n)
results = {**globals().get("results", {}), "baseline": baseline_accuracy}  # keeps any fit of cell 6
fitted = globals().get("fitted", {})
print("The baseline on the training rows, Monday's way:", round((y_train == "no").mean(), 3))
print("The baseline on the validation rows:", round(baseline_accuracy, 3))
```

### Step 2. Write your guess, before you fit

In cell 5, type your guess for each candidate, the logistic regression and the decision tree you fit in step 3: will it beat the baseline? Then run cell 5.

- `a lot`: right on 20 or more of the 200 returns beyond the baseline.
- `a little`: right on 1 to 19 more.
- `not better`: the same or fewer.

Notebook cell 5:

```python
# 5. Your guess: will each candidate beat the baseline? Type "a lot", "a little" or "not better".
guess = {
    "logistic-regression": "",
    "decision-tree": "",
}
print("Your guess:", guess)
```

### Step 3. Fit two candidates

Fit trains the model on the training rows; predict asks it for an outcome on each validation return.

1. Run cell 6. It fits a logistic regression, with the amounts put on a common scale first. You should see its validation accuracy and how many returns it got right.
2. In cell 6, change the one line that names the model. Type this in place of `make_pipeline(StandardScaler(), LogisticRegression())`:

```python
DecisionTreeClassifier(max_depth=3, random_state=0)
```

`max_depth=3` is a setting: a tree at most three questions deep.

3. Run cell 6 again, by itself, not with Run all, so the logistic regression's result from your first run stays beside it. You should see the tree's accuracy.

Notebook cell 6:

```python
# 6. Fit a candidate on the training rows, then measure its accuracy on the validation rows.
assert "results" in globals(), "Run cells 3 and 4 first."
model = make_pipeline(StandardScaler(), LogisticRegression())  # the one line that names the model
model.fit(X_train, y_train)                      # fit: training, on the training rows
predictions = model.predict(X_valid)             # predict: one outcome for each validation return
accuracy = accuracy_score(y_valid, predictions)  # accuracy: the share of predictions that match the label
kind = type(model[-1] if hasattr(model, "steps") else model).__name__  # its type, inside the pipeline
name = {"LogisticRegression": "logistic-regression", "DecisionTreeClassifier": "decision-tree"}.get(kind, kind)  # as exercise 3 names its runs
results[name], fitted[name] = accuracy, model
print(name, "validation accuracy:", round(accuracy, 3))
print("Right:", int((predictions == y_valid).sum()), "of", len(y_valid), "validation returns")
```

### Step 4. Set the three numbers side by side, and check

1. Run cell 7. You should see three accuracies on the same validation rows. Compare each with your guess.
   - A large gain is the moment to ask whether a column gave the label away.
   - The course supplies those checks: exercise 1 checked the label's counts, the two columns of `fields.csv` and the four rows of Monday's record.
   - The day's reading marks the other features of cell 3 `before`, as each comes from the filed return.
   - An accuracy close to 1.000 → suspect a leak.
2. Run cell 8. It prints `Done:`, or `Not yet:` and what is left.

Notebook cell 7:

```python
# 7. Three numbers side by side, on the same validation rows.
assert "results" in globals(), "Run cells 3 and 4 first."
for name in ("baseline", "logistic-regression", "decision-tree"):
    if name in results:
        print(f"{name}: {results[name]:.3f}")
    else:
        print(f"{name}: not fitted yet. Step 3.")
```

Notebook cell 8:

```python
# 8. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{folder}/check.py", encoding="utf-8").read(), _check)
check_now = _check["in_notebook"]
print(check_now(globals()))
```

### Finished early?

Optional: cell 8 does not check it.

In cell 9, write one sentence: which candidate beat the baseline, and by how many returns? Run cell 9.

Notebook cell 9:

```python
# 9. Optional: one sentence.
by_how_much = ""
print(by_how_much or "Write your sentence between the quotes.")
```

### Afterwards, together

1. Why measure the baseline again on the validation rows?
2. What does the logistic regression's gain over the baseline not tell you about the 40 returns whose tax changed (`yes`)?
3. What would you check first if a candidate's accuracy were 0.999?

The answer, after you try: [`answers/exercise-02-fit-two-candidates`](../answers/exercise-02-fit-two-candidates/).
