# Exercise 1: Name the top three features, then explain case #123 in two sentences (we do)

**Goal:** After this exercise, you can name the three features your model leans on most and explain case #123's score in two sentences an examiner could read.

**Scenario:** A made-up examiner opens case #123 on the list of the 25 highest scores, sees one number, 0.964, and asks why it is there. You read the model's ranked chart and name its top three features. Then you read case #123's chart and write the two sentences the examiner reads.

**AI tool:** none.

**Time:** 15 minutes: 11 to do it, 4 for setup problems.

**Where you work:** this notebook, `week-04/day-04/exercise-01-explain-case-123/exercise.ipynb`, in your Git folder of the course in Databricks.

**Done when:** cell 7 prints `Done:`.

**Cells:** a cell's number is the `# N.` comment on its first line, such as `# 1.`; text cells have no number.

**Optional part:** Finished early? Cell 8 draws the chart of a return the model left off the list.

**What you have:**

- `course.returns.model_train` and `course.returns.model_valid`, as on Wednesday. If they cannot be read, cell 1 makes the same rows from the course's setup file and says so.
- `load.py` and `check.py`, given code that cells 1 and 7 run. `load.py` draws the charts: with the SHAP library where it is on the compute, and by the same exact formula where it is not.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. No cell changes your tables. New here: the ranked chart, and one return's chart.

### Step 1. Fit the model again

Run cells 1 and 2. You do not need to change them. You should see:

1. Which tables cell 1 uses, then 500 returns in `model_train` and 250 in `model_valid`.
2. Cell 2 fits Tuesday's logistic regression again, with Tuesday's lines, on the 400 examined returns of `model_train`, and scores every return of `model_valid`. You should see case #123's score, 0.964, at place 11 of 250: on the list of the 25 highest scores.

The model is the logistic regression, the candidate ahead at 0.5 on both precision and recall. A score is one return's number from 0 to 1: a relative risk indicator that a person acts on, never a finding about the taxpayer.

Notebook cell 1:

```python
# 1. Read the course's tables. You do not need to change this cell.
import os
course_folder = os.getcwd().split("/week-04/")[0]  # your Git folder of the course
folder = f"{course_folder}/week-04/day-04/exercise-01-explain-case-123"
try:
    train_table = spark.table("course.returns.model_train")  # the training set: tax years 2020 and 2021
    valid_table = spark.table("course.returns.model_valid")  # the validation set: tax year 2022
except Exception:
    train_table, valid_table = None, None  # not there: load.py makes the same rows
exec(open(f"{folder}/load.py", encoding="utf-8").read())  # you do not need to read load.py
train, valid = load_sets(train_table, valid_table)
```

Notebook cell 2:

```python
# 2. Tuesday's logistic regression, fitted again as Tuesday fitted it; it scores every return of model_valid.
assert "valid" in globals(), "Run cell 1 first."
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

features = ["filing_status", "wages_amt", "taxable_interest_amt", "other_income_amt",
            "total_income", "agi_amt", "deduction_amt", "deduction_missing",
            "total_tax_amt", "withholding_amt", "tax_to_agi", "deduction_to_agi"]  # Tuesday's twelve
examined = train[train["exam_changed_tax"].notna()]  # the 400 examined returns of model_train
X_train, y_train = examined[features].fillna(0), examined["exam_changed_tax"]
logistic = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)

scores = valid[["case_id"]].copy()  # all 250 returns of model_valid
scores["logistic_score"] = logistic.predict_proba(valid[features].fillna(0))[:, 1]  # column 1 is "yes"
place_123 = int((scores["logistic_score"] > scores.loc[scores["case_id"] == 123, "logistic_score"].iloc[0]).sum()) + 1
print(len(scores), "returns of model_valid scored. Case #123:",
      f"{scores.loc[scores['case_id'] == 123, 'logistic_score'].iloc[0]:.3f}, place {place_123} of {len(scores)}.")
```

### Step 2. Name the top three features

"The chart is a *ranked list*: the features in order, with the one the model leans on most at the top." (the day's reading)

1. Run cell 3. You should see twelve bars, the longest at the top, then the same list as text. Each bar is the average size of a feature's push, up or down, over the 250 returns of `model_valid`.
2. In cell 3, between the quotes, type the names of the three longest bars, the longest first. Two may be level: type them in the chart's order.
3. Run cell 3 again. You should see your top three.

Set the list beside your feature record: the feature at the top has no row in it yet. The list describes the model. It does not say what made a tax wrong.

Notebook cell 3:

```python
# 3. The ranked list: the features the model leans on most. Then type the top three, the longest bar first.
assert "logistic" in globals(), "Run cells 1 and 2 first."
ranked = draw_ranking()
top_three = ["", "", ""]
print("Your top three:", top_three)
```

### Step 3. Draw case #123's chart, and check the sum

"So read the axis label before you write a number: here, log-odds." (the day's reading)

1. In cell 4, type `123` in place of `None`. Until you do, the cell stops with `Type the case id in place of None.`
2. Run cell 4. You should see the chart, then the same chart as a table: a return with average values first, then the twelve features, largest push first, each with case #123's value and the training average, then case #123's output and its score.
3. Read the axis label: the unit every push is in.
4. Read the sum under the table. "The exact pushes take -4.55 to 3.28; the pushes shown are rounded to one place, and their roundings add up to the difference." (the day's reading) So the pushes shown add up to 3.15, not 3.28.

"The exact pushes in your notebook can differ in the second decimal place with the version of the library that fits the model; the score 0.964, the order of the pushes and every count in this reading stay the same." (the day's reading)

"The list describes the whole model; one return's pushes may come in another order." (the day's reading) Find `wages_amt` in the table: high on the ranked list, it hardly moves case #123.

Notebook cell 4:

```python
# 4. One return's chart: a return with average values, each feature's push, the return's output. Change only the case id.
case_id = None  # the return to explain: 123
assert case_id is not None, "Type the case id in place of None."
chart = explain(case_id)
```

### Step 4. Guess, then see

1. Case #123's other income pushes +3.8 on the log-odds axis. In cell 5, in place of `None`, type your guess: if case #123's other income were the training average, 7,584, and everything else stayed as filed, what would its score be? Any number from 0 to 1 counts.
2. Run cell 5. You should see your guess beside the score it would have, and beside 0.964.

This is not the reading's 0.904: that score comes from the model fitted again without other income. Here the same model scores the same return, with one value changed.

Then read why: "A step of the same size in log-odds moves the score a great deal near the middle and very little near the ends, so a push has no fixed size in score." (the day's reading)

Notebook cell 5:

```python
# 5. Your guess, then the score. Type it, then run this cell.
guess = None  # case #123's score with its other income at the training average: a number from 0 to 1

if guess is None:
    print("Type your guess, then run this cell again.")
else:
    print(what_if(123, "other_income_amt", guess))
```

### Step 5. Write the two sentences, and check

"The pushes are in log-odds, so you give their order and direction, and the values that made them, not an amount of score" (the day's reading).

1. In cell 6, between the quotes, write the two sentences. The table says what each holds.

| Sentence | It says | Read it from |
|---|---|---|
| 1 | case #123's score, against what a return with average values scores | cell 2, and the first line of cell 4's table as a score: about 0.01 |
| 2 | the two largest pushes, the largest first: what each feature says about the return, its value against the training average, and the direction it pushed the score | cell 4's table |
| neither | an amount of push or of score, such as "by 3.8"; anything the taxpayer did | the axis; the examiner decides |

2. Run cell 6. You should see your sentences.
3. Run cell 7. It prints `Done:`, or `Not yet:` and what is left.

"A push says that the model moved the score because of this value, not that the value is wrong." (the day's reading)

Keep this notebook. Friday's challenge asks for the same two sentences.

Notebook cell 6:

```python
# 6. The two sentences an examiner reads.
sentences = ""
print(sentences or "Write your two sentences between the quotes.")
```

Notebook cell 7:

```python
# 7. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{folder}/check.py", encoding="utf-8").read(), _check)
check_now = _check["in_notebook"]
print(check_now(globals()))
```

### Finished early?

Optional: cell 7 does not check it.

1. In cell 8, type in place of `None` the id of a return the model left off the list, such as `471`: labelled change, with a score of about 0.18. Its pushes point both ways.
2. Run cell 8. You should see its chart and table.
3. Between the quotes, write two sentences of the same form. Where a push lowers the score, say so.

Notebook cell 8:

```python
# 8. Optional: explain a return that the model left off the list.
other_id = None  # a return off the list, such as 471
if other_id is not None:
    other = explain(other_id)
other_sentences = ""
print(other_sentences or "Write your two sentences between the quotes.")
```

### Afterwards, together

1. Why does the top feature say nothing about what the taxpayer did?
2. How do you check that case #123's pushes are read right?
3. Why give a push's direction and order, not an amount of score?

The answer, after you try: [`answers/exercise-01-explain-case-123`](../answers/exercise-01-explain-case-123/).
