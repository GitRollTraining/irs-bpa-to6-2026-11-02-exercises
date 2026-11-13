# Exercise 4: Mark what the selection day knows, then split by year

**Goal:** After this exercise, you can mark each feature known on the selection day or not, and split the features by tax year without leakage.

**Scenario:** The selection day is the day the IRS picks a return for examination. A feature not known on that day leaks the answer to next week's model. You mark every feature, drop the no's from `features`, and split the rest by tax year.

**AI tool:** none.

**Where you work:** the Databricks workspace. This notebook is `week-03/day-03/exercise-04-selection-day-and-split/exercise.ipynb` in your Git folder of the course.

**Done when:** cell 7 prints `Done:`.

**Optional part:** none.

**What you have:**

- `features` and `feature_record` in your schema, from exercises 2 and 3. The tax years are 2020 to 2023.
- The label `exam_changed_tax`: yes when an examination changed the tax.
- `check.py`, beside this notebook. Cell 7 runs it.

**Start from:** this notebook as the course gives it. The trainer ran the same five tests just before. New here: your own mark on each feature.

### Step 1. Name your schema, and list every feature

Why: every column a model could read needs your mark, so it gets a record row first.

1. In cell 1, type your number in place of `NN`.
2. Attach the compute the trainer names.
3. Run cell 1.
4. Run cell 2. It adds a record row for each column copied from the return table. You should see 10 features, or 9 after cell 4.

Notebook cell 1:

```python
# 1. Your schema, where your tables go. Type your number in place of NN.
schema = "course.learner_NN"

import os
course_folder = os.getcwd().split("/week-03/")[0]  # your Git folder of the course
print("Your tables go in", schema)
```

Notebook cell 2:

```python
# 2. A record row for each feature. Columns copied from the return file get a row too.
from pyspark.sql import functions as F
features = spark.table(f"{schema}.features")
not_features = ["return_id", "filer_key", "tax_year", "file_name", "exam_changed_tax"]  # keys, the file, the label
rows = [tuple(r) for r in spark.table(f"{schema}.feature_record")
        .select("feature", "table_read", "columns_read", "code").collect()]
for column in features.columns:
    if column not in not_features and column not in [r[0] for r in rows]:
        rows.append((column, "return_table", column, "copied from the return file"))
print(len(rows), "features:", ", ".join(r[0] for r in rows))
```

### Step 2. Mark each feature: known on the selection day?

Why: a value written after the selection day carries the answer.

1. In cell 3, type `"yes"` or `"no"` for each feature.
2. Beside each mark, type the reason in three words or more.
3. Run cell 3. You should see each feature's mark.

Mark yes when the value is on the return as filed, or reads earlier years only. Mark no when someone writes the value after the selection day. The amounts in `features` are the amounts as filed, before any examination.

The label `exam_changed_tax` stays in each set, and nothing computed from it becomes a feature.

Notebook cell 3:

```python
# 3. For each feature: known on the selection day, "yes" or "no", and why.
known = {
    "tax_to_agi": ("", ""),
    "w2_wage_share": ("", ""),
    "mean_prior_wages": ("", ""),
    "wages_change_pct": ("", ""),
    "filing_status": ("", ""),
    "wages_amt": ("", ""),
    "total_income": ("", ""),
    "agi_amt": ("", ""),
    "total_tax_amt": ("", ""),
    "tax_added_by_exam": ("", ""),
}
for feature, (mark, why) in known.items():
    print(f"{feature}: {mark or '?'}, {why}")
```

### Step 3. Drop the no's, split by tax year, and write

Why: the model learns from earlier years and scores later ones.

1. Run cell 4. It drops each feature you marked no, and writes the record, `train` (2020 and 2021), `valid` (2022) and `test` (2023). Then it writes `features` again without them. You should see `Dropped:` and four `Wrote` lines. The record gains two columns, `known_on_selection_day` and `why`: your marks.

Notebook cell 4:

```python
# 4. Drop the no's, split by tax year, and write.
dropped = [feature for feature, (mark, _) in known.items() if mark == "no"]
kept = features.drop(*dropped)
sets = {"train": kept.filter(F.col("tax_year") <= 2021),
        "valid": kept.filter(F.col("tax_year") == 2022),
        "test": kept.filter(F.col("tax_year") == 2023)}
record = [r + known.get(r[0], ("", "")) for r in rows]
spark.createDataFrame(record, "feature string, table_read string, columns_read string, code string, "
                              "known_on_selection_day string, why string") \
    .write.mode("overwrite").saveAsTable(f"{schema}.feature_record")
print("Dropped:", ", ".join(dropped) or "nothing")
for name, df in sets.items():
    df.write.mode("overwrite").saveAsTable(f"{schema}.{name}")
    print("Wrote", f"{schema}.{name}")
written = [spark.table(f"{schema}.{name}") for name in sets]
written[0].unionByName(written[1]).unionByName(written[2]) \
    .write.mode("overwrite").saveAsTable(f"{schema}.features")
print("Wrote", f"{schema}.features")
```

### Step 4. Run the five leakage tests

Why: each test fails a bad split. Read each test's comment before you run it.

Tests 3 and 4 compute `mean_prior_wages` again with `mean_mismatches`, which joins each row to the filer's earlier rows. Test 3 reads all three sets: the selection day knows a filer's own history, so a 2023 mean may read 2022 rows in `valid`. Test 4 reads `train` alone: a value fitted across many returns, such as a mean over all filers, must come from training rows only.

1. Run cell 5. You should see `The five leakage tests pass`. If an `assert` stops the cell, its message names the test.
2. Run cell 6. You should see three lines, such as `train: 21 returns, 3 tax-change cases`. Every learner sees the same counts.

Notebook cell 5:

```python
# 5. The five leakage tests. Each assert stops the cell when its test fails.
tr, va, te = (spark.table(f"{schema}.{n}") for n in ("train", "valid", "test"))
rec = spark.table(f"{schema}.feature_record")
leak_tests_passed = False

def mean_mismatches(df: "DataFrame") -> int:
    """Count the rows of df whose mean_prior_wages is not the mean of the filer's earlier rows."""
    a, b = df.alias("a"), df.alias("b")  # each row of a, joined to the same filer's earlier rows in b
    again = (a.join(b, (F.col("a.filer_key") == F.col("b.filer_key")) & (F.col("b.tax_year") < F.col("a.tax_year")), "left")
              .groupBy("a.return_id", "a.mean_prior_wages").agg(F.avg("b.wages_amt").alias("again")))
    # count the rows whose two means differ. Two nulls count as the same
    return again.filter(~(F.col("mean_prior_wages").isNull() & F.col("again").isNull())
                        & (F.col("again").isNull() | (F.abs(F.col("mean_prior_wages") - F.col("again")) > 0.01))).count()

# Test 1: no return_id in two sets.
ids = tr.select("return_id").union(va.select("return_id")).union(te.select("return_id"))
assert ids.count() == ids.distinct().count(), "test 1: a return_id is in two sets"
# Test 2: every training year before every validation year, before every test year.
years = [sorted(r[0] for r in df.select("tax_year").distinct().collect()) for df in (tr, va, te)]
assert years[0][-1] < years[1][0] and years[1][-1] < years[2][0], f"test 2: the years overlap: {years}"
# Test 3: over all three sets (unionByName stacks them by column name), every history mean reads earlier years only.
assert mean_mismatches(tr.unionByName(va).unionByName(te)) == 0, "test 3: a history mean reads its own or a later year"
# Test 4: computed again from train alone, the training means do not change: none needs a row outside train.
assert mean_mismatches(tr) == 0, "test 4: a training value needs rows outside the training set"
# Test 5: no feature marked no is in a set, and every record row has its mark.
no = [r["feature"] for r in rec.filter("known_on_selection_day = 'no'").collect()]
ft = spark.table(f"{schema}.features")
assert not [c for df in (tr, va, te, ft) for c in df.columns if c in no], "test 5: a feature marked no is still there"
assert rec.filter("known_on_selection_day IS NULL OR known_on_selection_day NOT IN ('yes', 'no')").count() == 0, \
    "test 5: a record row has no yes or no"
leak_tests_passed = True
print("The five leakage tests pass.")
```

Notebook cell 6:

```python
# 6. Rows and tax-change cases in each set.
for name, df in (("train", tr), ("valid", va), ("test", te)):
    cases = df.filter(F.col("exam_changed_tax") == "yes").count()
    print(f"{name}: {df.count()} returns, {cases} tax-change cases")
```

### Step 5. Check

Run cell 7. It prints `Done:` when your marks follow step 2's rule and the tests passed. Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 7:

```python
# 7. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{course_folder}/week-03/day-03/exercise-04-selection-day-and-split/check.py").read(), _check)
print(_check["in_notebook"](spark, schema, {"tests_ran": leak_tests_passed}, course_folder))
```

### Afterwards, together

1. `tax_added_by_exam` would raise next week's test score. Why would that score fail on next year's returns?
2. `valid` holds only 3 tax-change cases. What could a score on 3 cases tell you, and what could it not?
3. Next week you scale every feature to one range. Which rows should the scale come from, and why?

The answer, after you try: [`answers/exercise-04-selection-day-and-split`](../answers/exercise-04-selection-day-and-split/).
