# Exercise 3: Say which error costs more, then read the threshold from capacity (we do)

**Goal:** After this exercise, you can state which error costs more in a scenario and set a threshold from the examiners' capacity, with the error it trades.

**Scenario:** The examiners can take 25 cases from the 250 returns of `model_valid`. Their manager asks where the line goes, what it misses, whether case #123 makes the list, and whether to accept a list of 25 or ask for more capacity.

**AI tool:** none.

**Time:** 15 minutes: 11 to do it, 4 for setup problems.

**Where you work:** this notebook, `week-04/day-03/exercise-03-threshold-from-capacity/exercise.ipynb`, in your Git folder of the course in Databricks.

**Done when:** cell 7 prints `Done:`.

**Cells:** a cell's number is the `# N.` comment on its first line, such as `# 1.`; text cells have no number.

**Optional part:** Finished early? Cell 8 reads the tree's threshold from the same capacity.

**What you have:**

- `course.returns.model_train` and `course.returns.model_valid`, as in exercises 1 and 2. If they cannot be read, cell 1 makes the same rows from the course's setup file and says so.
- `load.py` and `check.py`, given code that cells 1 and 7 run.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. No cell changes your tables. New here: a threshold set from capacity, on all 250 returns.

### Step 1. Score the validation returns

Run cells 1 and 2. You do not need to change them. You should see:

1. Which tables cell 1 uses, then 500 returns in `model_train` and 250 in `model_valid`.
2. Cell 2 fits Tuesday's two candidates again, with Tuesday's lines, on the 400 examined returns of `model_train`. Then each one gives a score to every return of `model_valid`. `predict_proba` gives each return's score from 0 to 1; Tuesday's `predict` gave only `yes` or `no`. You should see 40 returns labelled `change`, 160 `no change` and 50 `never examined`.

A score is one return's number from 0 to 1: a relative risk indicator that a person acts on, never a finding about the taxpayer. A label records a past examination: `change` means it changed the tax (`exam_changed_tax` is `yes`).

Notebook cell 1:

```python
# 1. Read the course's training and validation sets. You do not need to change this cell.
import os
course_folder = os.getcwd().split("/week-04/")[0]  # your Git folder of the course
folder = f"{course_folder}/week-04/day-03/exercise-03-threshold-from-capacity"
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
# 2. Tuesday's two candidates, fitted again as Tuesday fitted them; each scores every return of model_valid.
assert "valid" in globals(), "Run cell 1 first."
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

features = ["filing_status", "wages_amt", "taxable_interest_amt", "other_income_amt",
            "total_income", "agi_amt", "deduction_amt", "deduction_missing",
            "total_tax_amt", "withholding_amt", "tax_to_agi", "deduction_to_agi"]  # Tuesday's twelve
examined = train[train["exam_changed_tax"].notna()]  # the 400 examined returns of model_train
X_train, y_train = examined[features].fillna(0), examined["exam_changed_tax"]
logistic = make_pipeline(StandardScaler(), LogisticRegression()).fit(X_train, y_train)
tree = DecisionTreeClassifier(max_depth=3, random_state=0).fit(X_train, y_train)

scores = valid[["case_id", "exam_changed_tax"]].copy()  # all 250 returns of model_valid
scores["label"] = scores["exam_changed_tax"].map({"yes": "change", "no": "no change"}).fillna("never examined")
scores["logistic_score"] = logistic.predict_proba(valid[features].fillna(0))[:, 1]  # column 1 is "yes"
scores["tree_score"] = tree.predict_proba(valid[features].fillna(0))[:, 1]
print(len(scores), "returns of model_valid scored by both candidates:", scores["label"].value_counts().to_dict())
```

### Step 2. Say which error costs more, and why

"No model or formula makes that judgment. The people who run the examinations make it, and you must be able to state it in a sentence and defend it." (the day's reading)

- **A false positive:** an examiner spends hours on a return whose examination changes nothing, and the taxpayer goes through an examination that changes nothing.
- **A false negative:** a return an examination would have changed stays as filed, and nobody looks at it.

1. In cell 3, between the quotes, write one sentence in this form: `In this scenario a false negative costs more than a false positive, because ...`, or the other way round. After `because`, give a reason of five words or more. Either way round can be right; the reason is what a reviewer questions.
2. Run cell 3. You should see your sentence.

Notebook cell 3:

```python
# 3. Which error costs more in this scenario, and why. One sentence.
cost_sentence = ""
print(cost_sentence or "Write your sentence between the quotes.")
```

### Step 3. Guess, then sort all 250 and keep the top k

"A *threshold from capacity* is the score of the k-th return when the returns are sorted by score, highest first." (the day's reading) *Capacity* is the number of cases the examiners can take, written k.

1. In cell 4, type your guess in place of the first `None`: a list of 30 of all 250, at a threshold of 0.709. How many of the 40 returns labelled change does it pick out? Any whole number from 0 to 40 counts.
2. In cell 4, type k in place of `None`: the cases the examiners can take.
3. Run cell 4. It sorts all 250 returns of `model_valid` by the logistic regression's score, highest first, and shows the top k and the next one down. You should see `place`, `case_id`, `logistic_score` and `label`, and where case #123 stands.

The 50 never-examined returns are sorted with the others: the list is drawn from every return the examiners could take.

Scores are shown to three places. A score shown as `1.000` is not a certainty: "a logistic regression never gives exactly 0 or 1" (the day's reading).

Notebook cell 4:

```python
# 4. Your guess, then the sort. Type both, then run this cell.
guess_30 = None  # a list of 30: how many of the 40 labelled change does it pick out?
k = None        # the cases the examiners can take

assert "scores" in globals(), "Run cells 1 and 2 first."
if guess_30 is None or not isinstance(k, int):
    print("Type your guess and k, then run this cell again.")
else:
    ranked = scores.sort_values("logistic_score", ascending=False).reset_index(drop=True)
    ranked.insert(0, "place", range(1, len(ranked) + 1))
    print(ranked.head(k + 1)[["place", "case_id", "logistic_score", "label"]].round(3).to_string(index=False))
    place_123 = int(ranked.loc[ranked["case_id"] == 123, "place"].iloc[0])
    print(f"Places 1 to {k} are on the list; place {k + 1}, the next score down, stays off.")
    print(f"Case #123 is at place {place_123}: {'on' if place_123 <= k else 'off'} the list.")
```

### Step 4. Read the threshold, and count what it trades

"The list never holds more returns than the examiners can take" (the day's reading).

1. In cell 5, type the threshold in place of `None`: the score at place k of cell 4, to three places.
2. Run cell 5. You should see the list counted against the labels, beside a list of 30 (compare it with your guess) and the list at 0.5. A never-examined return on the list is in no cell: "You cannot say whether they are right: they have no label" (the day's reading).

Notebook cell 5:

```python
# 5. The threshold you read from cell 4: the score at place k, to three places. Type it in place of None.
threshold = None

if not isinstance(threshold, (int, float)) or "ranked" not in globals():
    print("Run cell 4, then type the threshold as a number, with no quotes, and run this cell again.")
elif round(threshold, 3) != round(ranked["logistic_score"].iloc[k - 1], 3):
    print(f"That is not the score at place {k} of cell 4. Look at the last row on the list.")
else:
    examined_scores = scores[scores["label"] != "never examined"]
    for name, on in ((f"A list of {k}, threshold {threshold}", ranked.head(k)),
                     (f"A list of 30, threshold {ranked['logistic_score'].iloc[29]:.3f}", ranked.head(30)),
                     ("The list at 0.5", scores[scores["logistic_score"] >= 0.5])):
        labelled = on[on["label"] != "never examined"]
        right = int((labelled["label"] == "change").sum())
        print(f"{name}: {len(on)} returns, {len(on) - len(labelled)} never examined; right {right} of "
              f"{len(labelled)}, wrong {len(labelled) - right}. The list picks out {right} of the 40 labelled change "
              f"and misses {40 - right}.")
```

### Step 5. Decide, and check

"If a missed return costs more, the list at 0.5 is better, and a capacity of 25 is a known weakness: say how many returns labelled *change* it misses, and that more capacity would pick out more. If an examiner's wasted hours cost more, the list at 25 is better." (the day's reading)

So your cost sentence of cell 3 decides:

- A false negative costs more: ask for `more capacity`.
- A false positive costs more: `accept` the list of 25, and say how many returns labelled change it misses.

Then choose the candidate you put in front of the manager, and say why with counts. Two things decide it: the precision and recall of each candidate at 0.5, from exercise 2, and whether its scores can choose a list of any size the examiners' capacity asks for, such as 20 or 10 (cell 4 shows them).

1. In cell 6, type your decision for the examiners' manager. The table says what each value holds.

| Value | Type this | Why |
|---|---|---|
| `chosen` | `logistic-regression` or `decision-tree` | the candidate you put in front of the manager |
| `why_chosen` | one sentence of eight words or more, with counts | why this candidate and not the other |
| `decision` | `more capacity` or `accept` | the one your cost sentence of cell 3 decides |
| `why` | one sentence of eight words or more, with the counts of cell 5 | if you accept, it says how many returns labelled change the list misses |

2. Run cell 6. You should see your decision.
3. Run cell 7. It prints `Done:`, or `Not yet:` and what is left.

The list is a recommendation: the model recommends, and a person decides. Keep this notebook. Thursday starts from the candidate you chose and the threshold of cell 5.

Notebook cell 6:

```python
# 6. Your decision for the examiners' manager.
chosen = ""      # the candidate: logistic-regression or decision-tree
why_chosen = ""  # one sentence: why this candidate, with counts
decision = ""  # more capacity, or accept
why = ""       # one sentence, with the counts of cell 5
print("Chosen:", chosen or "(not yet)", "| decision:", decision or "(not yet)")
print("Why this candidate:", why_chosen or "(not yet)")
print("Why:", why or "(not yet)")
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

1. Run cell 8. You should see how many of the 250 returns share each of the tree's highest scores.
2. In cell 8, type the tree's threshold for a list of 25 in place of `None`.
3. Between the quotes, type why the tree's scores cannot choose a list of 10.
4. Run cell 8 again.

Notebook cell 8:

```python
# 8. Optional: the tree's highest scores, and how many returns share each.
tree_threshold = None  # the tree's threshold for a list of 25
why_not_10 = ""        # why the tree's scores cannot choose a list of 10

print(scores["tree_score"].round(3).value_counts().sort_index(ascending=False).head(3).to_string())
print("Your threshold for 25:", tree_threshold, "| why not 10:", why_not_10 or "(not yet)")
```

### Afterwards, together

1. What would change your sentence on which error costs more?
2. Why read the threshold from capacity, not keep 0.5?
3. Why can the tree's scores not choose a list of 10?

The answer, after you try: [`answers/exercise-03-threshold-from-capacity`](../answers/exercise-03-threshold-from-capacity/).
