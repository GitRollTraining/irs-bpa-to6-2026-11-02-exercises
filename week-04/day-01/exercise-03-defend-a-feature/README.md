# Exercise 3: Record a feature's defence, then flag a missing amount (we do)

**Goal:** After this exercise, you can record the defence of a feature and add a flag column for a missing amount.

**Scenario:** On Tuesday a model reads the course's features. Before it does, each feature needs its defence: its source field, its reason, and whether it is known when the case is selected. One amount, the deduction on line 12e, is empty on some returns.

**AI tool:** none.

**Where you work:** the notebook `week-04/day-01/exercise-03-defend-a-feature/exercise.ipynb` in your Git folder of the course, in Databricks. You type in the code cells marked `# 1.` to `# 4.`: cell 1 is the code cell whose first line starts with `# 1.`, and so on. Cell 5 checks what you made.

**Done when:** cell 5 prints `Done:`.

**Optional part:** Finished early?

1. In a new cell, run `print(spark.table("course.returns.model_features").columns)`. It lists the columns.
2. In cell 4, add a row for each column you would keep.
3. Add a row for `name_length` too. Its source field is `filer_name`, a header field. Type `yes` and `struck: names the taxpayer, on the filed return` in its last two slots: the name is on the return when it is filed, so it is known at selection, but `filer_name` says who the taxpayer is, so a feature built from it is never kept.
4. Run cells 4 and 5 again. Extra rows still give `Done:`.

**What you need to know first:** a feature's defence is "its source field, its reason, and whether it is known when the case is selected." A missing amount is "an amount that is not on the return, which can mean zero or unknown."

**What you have:**

- `course.returns.model_features`, the week's feature table in Unity Catalog, where Databricks keeps the course's tables: 1,000 returns, made up by the course.
- Your own schema, `course.learner_NN`, from week 3.
- The trainer's example, shown before this exercise: two features recorded, and the same count and flag cells on `withholding_amt`.
- `check.py`, beside this notebook. Cell 5 runs it. It reads the two tables you write.

**Start from:** this notebook as the course gives it, attached to the compute the trainer names (the computer in Databricks that runs your cells). To start again, set the cells you typed back to how the course gives them, and run them again: each one replaces its table. After a restart, run cells 1 to 5 in order: each cell uses a value that the cell above it sets.

### Step 1. Name your schema

Why: cells 3 and 4 write two tables in your own schema.

In cell 1, type the end of your schema's name in place of `NN`: the part after `learner_`, such as `07` or `ctv`. To find it: in the Databricks sidebar, select Catalog, then open `course`. Your schema is the `learner_` schema you made in week 3. If you cannot tell which one, ask the trainer. Run cell 1. You should see `Your tables go in course.learner_07`, with your own schema's name.

Notebook cell 1:

```python
# 1. Your schema, where your tables go. Type the part of its name after learner_ in place of NN.
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

Why: a flag column is "a column that records which amounts were missing." Tuesday's cells fill the empty amounts. After that, only the flag still shows which ones were empty.

You decide what an empty line 12e means. `deduction_amt` is line 12e of Form 1040, which the 2025 form calls “Standard deduction or itemized deductions (from Schedule A)”. Read what that line holds, then decide.

In cell 3, type two values between the quotes:

| Value | What you type |
|---|---|
| `empty_means` | `zero` or `unknown`: what an empty line 12e means |
| `why_empty` | your reason, 6 words or more: what line 12e holds, and so what its being empty tells you |

The flag's name is given: `deduction_missing`. It holds 1 where line 12e is empty and 0 where it is filled.

Stuck? Cell 3's comment gives an example reason for a different line, not 12e. Copy its shape, not its answer: what the line holds, so what its being empty tells you.

Run cell 3. It writes `features_flagged` in your schema: every column of `course.returns.model_features`, and the flag. You should see two rows: `0` with 937 returns, and `1` with 63.

Notebook cell 3:

```python
# 3. What an empty line 12e means, and why. Then the flag, named for you.
empty_means = ""   # "zero" or "unknown"
why_empty = ""   # example for a different line, not 12e: "On a paper Form 1040, a filer with no taxable interest may leave line 2b blank, so a blank line 2b there means zero."
flag = "deduction_missing"
if schema.endswith("_NN") or not flag:
    print("Type the part of your schema's name after learner_ in cell 1 first, then run this cell again.")
else:
    spark.sql(f"CREATE OR REPLACE TABLE {schema}.features_flagged AS SELECT *, "
              f"CASE WHEN deduction_amt IS NULL THEN 1 ELSE 0 END AS {flag} FROM course.returns.model_features")
    spark.sql(f"SELECT {flag}, COUNT(*) AS returns FROM {schema}.features_flagged GROUP BY {flag} ORDER BY {flag}").show()
```

### Step 4. Write the defence of the deduction and its flag

Why: "A feature you cannot defend is a feature you cannot keep."

Cell 4 holds the feature record, four rows. The first two are given, the reading's two examples: `tax_to_agi`, and `tax_added_by_exam`, which is struck. Your flag's row is given too. In the `deduction_amt` row, type three values: its source field, its reason, and `yes` or `no`. A comment beside each slot names it. Copy the reason from the table below, or write it in your own words: 6 words or more.

| Row | Source field | Reason | Known when the case is selected? |
|---|---|---|---|
| `deduction_amt` | Form 1040 line 12e, standard deduction or itemized deductions | a deduction lowers the taxable income, so it bears on the tax the return reports | `yes`, as line 12e is on the return as filed |

Run cell 4. You should see `Wrote course.learner_07.model_feature_record: 4 rows`, with your own number.

Notebook cell 4:

```python
# 4. Your feature record: one row per feature. Type between the empty quotes.
#    Each row: feature, source field, reason, known when the case is selected ("yes" or "no"), why.
record = [
    ("tax_to_agi", "Form 1040 line 24, total tax; line 11a, adjusted gross income",
     "a return whose tax is far from what its income suggests may hold an error", "yes",
     "both are on the filed return"),
    ("tax_added_by_exam", "the examination's result",
     "it moves with the examination's outcome", "no",
     "written after selection; struck"),
    ("deduction_amt",
     "",   # source field: the line of Form 1040
     "",   # reason: 6 words or more
     "",   # known when the case is selected: "yes" or "no"
     "line 12e is on the return as filed"),   # why: given
    (flag,
     "Form 1040 line 12e, empty or not",   # source field: given
     "the flag keeps the returns whose line 12e is empty apart from the others",   # reason: given
     "yes",   # known when the case is selected: given
     "whether line 12e is empty shows on the return as filed"),   # why: given
]
if schema.endswith("_NN"):
    print("Type the part of your schema's name after learner_ in cell 1 first, then run this cell again.")
else:
    spark.createDataFrame(record, "feature string, source_field string, reason string, "
                                  "known_at_selection string, timing string") \
        .write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"{schema}.model_feature_record")
    print(f"Wrote {schema}.model_feature_record:", len(record), "rows")
```

### Step 5. Check

Run cell 5. It prints `Done:` when these things are true:

- `empty_means` is the reading that line 12e supports, and `why_empty` has 6 words or more.
- `features_flagged` in your schema has the flag, 1 on each return whose `deduction_amt` is empty and 0 on the others.
- `model_feature_record`, the feature record in your schema, holds the two given rows, a row for `deduction_amt` and a row for your flag.
- The `deduction_amt` row and the flag's row each name line 12e, have a reason of 6 words or more, and say `yes` or `no`.

Otherwise it prints `Not yet:` and each thing still to do. It reads your two tables. You do not need to read its code.

Notebook cell 5:

```python
# 5. Check. You do not need to read this code.
# Do not change this cell. It runs check.py, beside this notebook.
```

### Afterwards, together

1. Why is the tax an examination added struck, when the tax withheld stays?
2. When is a missing amount zero, and when is it unknown?
3. Why add the flag before the fill, and not after it?

The answer: after the talk together, open `week-04/day-01/answers/exercise-03-defend-a-feature/` in your Git folder of the course ([link](../answers/exercise-03-defend-a-feature/)).
