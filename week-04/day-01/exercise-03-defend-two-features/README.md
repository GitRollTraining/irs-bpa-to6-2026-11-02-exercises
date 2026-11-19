# Exercise 3: Defend two features and flag a missing amount (we do)

**Goal:** After this exercise, you can record a feature's source field, reason and timing, and add a flag column for a missing amount.

**Scenario:** A reviewer will ask why each input of Tuesday's model may be used. The feature record starts with two rows that the trainer wrote. You add the deduction, which some returns leave empty, and the flag that keeps those returns apart.

**AI tool:** none.

**Where you work:** the notebook `week-04/day-01/exercise-03-defend-two-features/exercise.ipynb` in your Git folder of the course, in Databricks. You type in the code cells marked `# 1.` to `# 4.`: cell 1 is the code cell whose first line starts with `# 1.`, and so on. Cell 5 checks what you made.

**Done when:** cell 5 prints `Done:`.

**Optional part:** Finished early? In cell 4, add a row for each other column of `course.returns.model_features` that you would keep. To list them, run `print(spark.table("course.returns.model_features").columns)` in a new cell. Add a row for `name_length` too: start its reason with `strike:`, and name the header field it comes from. Run cells 4 and 5 again: extra rows still give `Done:`.

**What you need to know first:** "A feature's defence is three facts written beside it": its source field, its reason and its timing. "An empty line can mean two different things": zero, or unknown.

**What you have:**

- `course.returns.model_features`, the week's feature table in Unity Catalog: 1,000 returns, made up by the course.
- Your own schema, `course.learner_NN`, from week 3. Your number is the same as in week 3.
- The trainer's example, shown before this exercise: the same cells on `withholding_amt`.
- `check.py`, beside this notebook. Cell 5 runs it. It reads the two tables you write.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names. To start again, set the cells you typed back to how the course gives them, and run them again: each one replaces its table. After a restart, run cells 1 to 5 in order: each cell uses a value from the one before it.

### Step 1. Name your schema

Why: cells 3 and 4 write two tables in your own schema.

In cell 1, type your two-digit number in place of `NN`, such as `07`: the number you used in week 3. Ask the trainer if you do not know it. Run cell 1. You should see `Your tables go in course.learner_07`, with your own number.

Notebook cell 1:

```python
# 1. Your schema, where your tables go. Type your number in place of NN.
schema = "course.learner_NN"
print("Your tables go in", schema)
```

### Step 2. Count the empty amounts

Why: a flag tells you something only where an amount is sometimes empty. So you count first.

Cell 2 counts the empty cells of one amount. The trainer ran it on `withholding_amt`. In cell 2, change `"withholding_amt"` to `"deduction_amt"`. Change nothing else. Run cell 2.

You should see `1000` returns, `937` filled and `63` empty. `COUNT` of a column counts only its filled cells.

Notebook cell 2:

```python
# 2. Count the filled and empty cells of one amount. Change only the name between the quotes.
amount = "withholding_amt"
spark.sql(f"SELECT COUNT(*) AS returns, COUNT({amount}) AS filled, COUNT(*) - COUNT({amount}) AS empty "
          f"FROM course.returns.model_features").show()
```

### Step 3. Decide what an empty deduction means, and add the flag

Why: "Once a cell is filled, nobody can tell a real 0 from a filled 0." The flag keeps the difference.

In cell 3, type the two values. The table gives each value and its reason.

| Value | Type this | Why |
|---|---|---|
| `empty_means` | `unknown` | `deduction_amt` is line 12e, "Standard deduction or itemized deductions (from Schedule A)". Each return takes one or the other, so an empty line 12e cannot mean that the taxpayer had none. |
| `flag` | `deduction_missing` | The flag "holds 1 where the amount was missing and 0 where it was present". Name it for its amount, as the trainer named `withholding_missing`. |

Run cell 3. It writes `features_flagged` in your schema: every column of `course.returns.model_features`, and your flag. You should see two rows: `0` with 937 returns, and `1` with 63.

Notebook cell 3:

```python
# 3. What an empty amount means, and the flag's name. Type both between the quotes.
empty_means = ""   # "zero" or "unknown"
flag = ""
if schema.endswith("_NN") or not flag:
    print("Type your number in cell 1 and the flag's name here, then run this cell again.")
else:
    spark.sql(f"CREATE OR REPLACE TABLE {schema}.features_flagged AS SELECT *, "
              f"CASE WHEN {amount} IS NULL THEN 1 ELSE 0 END AS {flag} FROM course.returns.model_features")
    spark.sql(f"SELECT {flag}, COUNT(*) AS returns FROM {schema}.features_flagged GROUP BY {flag} ORDER BY {flag}").show()
```

### Step 4. Write the defence of the two new features

Why: "If you cannot say where each input came from and why it was used, the score cannot be defended, however accurate it is."

In cell 4, fill the two empty rows: `deduction_amt`, and your flag. Keep the two filled rows. Copy each reason, or write it in your own words: 6 words or more. The table gives each answer and its reason. Type each of the four values between its own pair of quotes, in the order the row shows, and keep the commas between them.

| Row | Source field | Reason | Known at selection | Why |
|---|---|---|---|---|
| `deduction_amt` | Form 1040 line 12e, standard deduction or itemized deductions | A deduction that is large for the income may be claimed in error. A reason is a claim that a reviewer can disagree with. | `yes` | line 12e is on the return as filed |
| `deduction_missing` | Form 1040 line 12e, empty or not | an empty line may itself be a signal | `yes` | known when the return is filed |

Run cell 4. You should see `Wrote course.learner_07.model_feature_record: 4 rows`, with your own number.

Notebook cell 4:

```python
# 4. Your feature record: one row per feature. Two rows are filled for you. Fill the two empty rows.
#    Each row: feature, source field, reason, known at selection ("yes" or "no"), why it is known or not.
record = [
    ("tax_to_agi", "Form 1040 line 24, total tax, divided by line 11a, adjusted gross income",
     "a return whose tax is far from what its income suggests may hold an error", "yes",
     "both lines are on the return as filed"),
    ("wages_amt", "Form 1040 line 1a, total amount from Form(s) W-2, box 1",
     "wages are the income line that employers' W-2s can confirm", "yes",
     "line 1a is on the return as filed"),
    ("deduction_amt", "", "", "", ""),
    (flag, "", "", "", ""),
]
if schema.endswith("_NN"):
    print("Type your number in cell 1 first, then run this cell again.")
else:
    spark.createDataFrame(record, "feature string, source_field string, reason string, "
                                  "known_at_selection string, timing string") \
        .write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{schema}.model_feature_record")
    print(f"Wrote {schema}.model_feature_record:", len(record), "rows")
```

### Step 5. Check

Run cell 5. It prints `Done:` when these things are true:

- `empty_means` is `unknown`.
- `features_flagged` in your schema has your flag, 1 on each return whose `deduction_amt` is empty and 0 on the others.
- `model_feature_record` in your schema holds the two given rows, a row for `deduction_amt` and a row for your flag.
- Each of your two rows has a source field on line 12e, a reason of 6 words or more, `yes` or `no`, and why.

Otherwise it prints `Not yet:` and each thing still to do. It reads your two tables. You do not need to read its code.

Notebook cell 5:

```python
# 5. Check. You do not need to read this code.
# Do not change this cell. It runs check.py, beside this notebook.
```

### Afterwards, together

1. Blanks filled with 0, no flag: what does a model learn?
2. An all-0 flag: when would it earn its column?
3. Which column would say no for its timing?

The answer: after the talk together, open `week-04/day-01/answers/exercise-03-defend-two-features/` in your Git folder of the course ([link](../answers/exercise-03-defend-two-features/)).
