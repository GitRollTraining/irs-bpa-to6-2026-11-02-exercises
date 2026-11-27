# Exercise 2: Compare selection rates by channel, then state the gap (we do)

**Goal:** After this exercise, you can compute each group's selection rate at your threshold and state the gap with its counts.

**Scenario:** Before a made-up examination group puts the model in use, its manager asks whether the list of 25 falls more on one group of returns than on another. Each return carries the course's column `made_up_channel`: channel A or B, a code the course made up. You compute each channel's selection rate at Wednesday's threshold and write the result with its counts.

**The channel:** "It describes no real way of filing, no real person and no real group, and it stands for no protected class such as race, sex or age; the arithmetic is the same for any grouping." (the day's reading) It is not a feature: Tuesday's twelve leave it out, and the model never reads it.

**AI tool:** none.

**Time:** 15 minutes: 11 to do it, 4 for setup problems.

**Where you work:** this notebook, `week-04/day-04/exercise-02-selection-rates-by-group/exercise.ipynb`, in your Git folder of the course in Databricks.

**Done when:** cell 5 prints `Done:`.

**Cells:** a cell's number is the `# N.` comment on its first line, such as `# 1.`; text cells have no number.

**Optional last step:** Finished early? Step 5 and cell 6 ask whether one feature could stand in for the channel.

**What you have:**

- `course.returns.model_train` and `course.returns.model_valid`, as on Wednesday, and `course.returns.model_features`, all 1,000 returns of the four tax years. If they cannot be read, cell 1 makes the same rows from the course's setup file and says so.
- `load.py` and `check.py`, given code that cells 1 and 5 run.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. No cell changes your tables. New here: the list of 25 split by channel.

### Step 1. Put the validation returns on the list, and count each channel

"Split the held-out returns by group." (the day's reading) The 250 returns of `model_valid` are the held-out returns.

Run cells 1 and 2. You do not need to change them. You should see:

1. Which tables cell 1 uses, then 500 returns in `model_train`, 250 in `model_valid` and 1,000 in `model_features`.
2. Cell 2 fits Tuesday's logistic regression again, with Tuesday's lines, and scores every return of `model_valid`. Wednesday's threshold is the 25th score: you should see `Threshold 0.844: 25 of 250 returns on the list`, then one row for each channel: its returns, and how many of them are on the list.

Channel A has 15 on the list and channel B 10. Counts alone do not answer the manager: the two channels are not the same size.

A score is one return's number from 0 to 1: a relative risk indicator that a person acts on, never a finding about the taxpayer. The model puts a return on the list or leaves it off; a person selects.

Notebook cell 1:

```python
# 1. Read the course's tables. You do not need to change this cell.
import os
course_folder = os.getcwd().split("/week-04/")[0]  # your Git folder of the course
folder = f"{course_folder}/week-04/day-04/exercise-02-selection-rates-by-group"
try:
    train_table = spark.table("course.returns.model_train")  # the training set: tax years 2020 and 2021
    valid_table = spark.table("course.returns.model_valid")  # the validation set: tax year 2022
    all_table = spark.table("course.returns.model_features")  # all 1,000 returns, the four tax years
except Exception:
    train_table, valid_table, all_table = None, None, None  # not there: load.py makes the same rows
exec(open(f"{folder}/load.py", encoding="utf-8").read())  # you do not need to read load.py
train, valid, all_returns = load_sets(train_table, valid_table, all_table)
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

scores = valid[["case_id", "made_up_channel", "exam_changed_tax"]].copy()  # all 250 returns of model_valid
scores["logistic_score"] = logistic.predict_proba(valid[features].fillna(0))[:, 1]  # column 1 is "yes"
threshold = scores["logistic_score"].sort_values(ascending=False).iloc[24]  # Wednesday's: the 25th score
scores["on_list"] = (scores["logistic_score"] >= threshold).astype(int)  # 1 on the list, 0 off it
print(f"Threshold {threshold:.3f}: {scores['on_list'].sum()} of {len(scores)} returns on the list.")
counts = scores.groupby("made_up_channel").agg(returns_in_channel=("case_id", "size"), on_the_list=("on_list", "sum"))
print(counts.to_string())
```

### Step 2. Guess

"So a gap belongs to a threshold, as precision and recall did on Wednesday: write the threshold beside it." (the day's reading)

1. In cell 3, in place of `None`, type your guess: if the examiners could take 50 returns, not 25, what share of channel B's 88 returns would be on the list? A number from 0 to 1. Any number counts.
2. Run cell 3. You should see your guess. Cell 4 shows the answer.

Notebook cell 3:

```python
# 3. Your guess: on a list of 50, what share of channel B's 88 returns is on the list?
guess_50 = None  # a number from 0 to 1
print("Your guess:", "(not yet)" if guess_50 is None else guess_50)
```

### Step 3. Compute each rate, and state the result

"The *selection rate* of a group is the share of its returns that the model puts on the list." (the day's reading)

1. In cell 4, type in place of each `None` the channel's rate as a division, with no quotes: its returns on the list, divided by its returns in `model_valid`, such as `3 / 50`.
2. Run cell 4. You should see each rate and the gap, then the same at two other thresholds (compare the list of 50 with your guess), then the past labels by channel. In the course's made-up data an examination's outcome follows the amounts on the return, never the channel, so a gap in the labels says the past decisions differ, not that either channel's filers comply less.
3. Between the quotes after `result`, write the result in one sentence. The table says what it holds.

| Part | Give | Read it from |
|---|---|---|
| each channel's rate | with its counts beside it: on the list, of its returns | cells 2 and 4 |
| the threshold | 0.844 | cell 2 |
| the gap | the difference between the two rates | cell 4 |
| the end | that the gap needs a reason | "A gap is a result that needs a reason." (the day's reading) |

4. Run cell 4 again. You should see your sentence.

The labels' line is why a gap needs a reason: "So a gap in the list can come from the labels as well as from the model." (the day's reading) Do not call the model fair or unfair from one number.

<details><summary>Stuck? One way to start</summary>

At a threshold of 0.844, the model puts ... of channel A's ... returns on the list, ..., and ...

</details>

Notebook cell 4:

```python
# 4. Each channel's rate as a division, then the result in one sentence.
rate_a = None  # channel A: its returns on the list, divided by its returns in model_valid
rate_b = None  # channel B: the same
result = ""    # one sentence: each rate with its counts, the threshold, the gap, and that it needs a reason

if rate_a is None or rate_b is None:
    print("Type each rate as a division, then run this cell again.")
elif isinstance(rate_a, str) or isinstance(rate_b, str):
    print("Type each rate as a division with no quotes around it, such as 3 / 50, then run this cell again.")
else:
    print(f"Channel A: {rate_a:.3f}. Channel B: {rate_b:.3f}. The gap: {abs(rate_a - rate_b):.3f}, "
          f"at a threshold of {threshold:.3f}.")
    if guess_50 is not None:
        compare()
    else:
        print("Type your guess in cell 3 and run it, then run this cell again to see the comparison.")
print(result or "Write your sentence between the quotes.")
```

### Step 4. Check

Run cell 5. It prints `Done:`, or `Not yet:` and what is left.

Keep this notebook. Friday's challenge asks for the result sentence of cell 4.

Notebook cell 5:

```python
# 5. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{folder}/check.py", encoding="utf-8").read(), _check)
check_now = _check["in_notebook"]
print(check_now(globals()))
```

### Step 5. Optional last step: could one feature stand in for the channel?

<!-- For the trainer: this step and cell 6 go with the proxy segment (the reading's section "Spot a feature that stands in for a group"). Cut both with it; nothing renumbers. -->

"A *proxy* is a feature that names no group and still tracks one. You see it when the feature's typical value differs between the groups." (the day's reading) A group's *typical value* is its median: half its returns lie below it, half above.

1. Run cell 6. You should see two features' medians in each channel, over all 1,000 returns: `other_income_amt`, the top of exercise 1's ranked list, and `wages_amt`, its third.
2. Between the quotes, write one sentence: `other_income_amt could stand in for the channel, because ...`, or `could not stand in`. After `because`, give its median in each channel. Compare `wages_amt`'s two medians before you write.
3. Run cell 6.
4. Run cell 5 again. It now checks your sentence too.

"So your sentence says that the feature *could* stand in for the group, and the ranked list tells you how much the model leans on it." (the day's reading)

Notebook cell 6:

```python
# 6. Optional last step: two features' typical values in each channel. Then one sentence on other_income_amt.
# For the trainer: goes with the proxy segment; cut this cell with step 5.
print(medians("other_income_amt", "wages_amt"))
proxy_sentence = ""  # other_income_amt could stand in, or could not stand in, for the channel, because ...
print(proxy_sentence or "Write your sentence between the quotes.")
```

### Afterwards, together

1. Why compare rates and not the counts on the list?
2. What does a gap need before anyone calls it unfair?
3. How can a list lean toward one channel without its column?

<!-- For the trainer: question 3 goes with the proxy segment. -->

The answer, after you try: [`answers/exercise-02-selection-rates-by-group`](../answers/exercise-02-selection-rates-by-group/).
