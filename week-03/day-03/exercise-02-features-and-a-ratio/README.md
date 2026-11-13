# Exercise 2: Build the features table with a ratio across two tables

**Goal:** After this exercise, you can add a ratio that reads two tables to the features table, and keep one row for each return.

**Scenario:** A model reads one row for each return. You start the features table from your return table. Then you add the share of wages that the W-2s show, which needs the W-2 table too.

**AI tool:** none.

**Where you work:** the Databricks workspace. This notebook is `week-03/day-03/exercise-02-features-and-a-ratio/exercise.ipynb` in your Git folder of the course.

**Done when:** cell 6 prints `Done:`.

**Optional part:** none.

**What you have:**

- `return_table` and `w2s` in your schema, from exercise 1. The adjusted gross income of one return is 0, and it has no W-2.
- `check.py`, beside this notebook. Cell 6 runs it.

**Start from:** this notebook as the course gives it. The trainer showed the `tax_to_agi` ratio and its record row just before this exercise. New here: a ratio that reads two tables.

### Step 1. Name your schema

Why: this notebook reads your tables from exercise 1.

1. In cell 1, type your number in place of `NN`.
2. Attach the compute the trainer names.
3. Run cell 1. You should see `Your tables go in` and your schema.

Notebook cell 1:

```python
# 1. Your schema, where your tables go. Type your number in place of NN.
schema = "course.learner_NN"

import os
course_folder = os.getcwd().split("/week-03/")[0]  # your Git folder of the course
print("Your tables go in", schema)
```

### Step 2. Start the features table with the ratio you saw

Why: a feature is one value for each return. A ratio with a bottom of 0 gets a null, not an error.

1. Run cell 2. It adds `tax_to_agi`, total tax over adjusted gross income, where adjusted gross income is above 0.
2. You should see `52 rows in features, 52 rows in return_table`.

Notebook cell 2:

```python
# 2. The features table starts from the return table, with the ratio the trainer showed.
from pyspark.sql import functions as F
return_table = spark.table(f"{schema}.return_table")
w2s = spark.table(f"{schema}.w2s")

features = return_table.withColumn(
    "tax_to_agi",
    F.when(F.col("agi_amt") > 0, F.col("total_tax_amt") / F.col("agi_amt")))
print(features.count(), "rows in features,", return_table.count(), "rows in return_table")
```

### Step 3. Add the share of wages the W-2s show

Why: the ratio is the W-2 wages of a return over the wages it reports. A return can have two W-2s, so the W-2 table can hold two rows for one return.

1. Read cell 3. It joins the W-2 rows to the features table, then divides.
2. Predict. In cell 3, type `"more"`, `"same"` or `"fewer"` between the quotes of `predict_rows = ""`: how many rows will the joined table have, against `return_table`?
3. Run cell 3. It prints the rows of the joined table, then the rows of `return_table`. Compare them with your prediction.
4. Run cell 4, a test of one row for each return. If it stops, its message gives the joined rows, then the returns.
5. If cell 4 stopped, put the two lines of the table in cell 3, in place of the line that starts `joined =` (it holds `withColumnRenamed`).
6. Run cell 3 and cell 4 again. Cell 4 should print `One row for each return: 52`.

| What | Write this | Why |
|---|---|---|
| First new line, in cell 3 | `w2_per_return = w2s.groupBy("return_id").agg(F.sum("wages_amt").alias("w2_wages"))` | `groupBy` with `F.sum` adds the W-2 wages of each return into one row, before the join. |
| Second new line, in cell 3 | `joined = features.join(w2_per_return, "return_id", "left")` | `left` keeps the returns with no W-2. Their `w2_wages` is empty, and `F.coalesce` in the next line turns it into 0. |

Where the wages are 0, the share is null, by the same rule as `tax_to_agi`: no bottom number, no ratio.

Notebook cell 3:

```python
# 3. The share of wages the W-2s show: W-2 wages over the wages the return reports.
predict_rows = ""  # "more", "same" or "fewer" rows than return_table? Type it before you run this cell.

joined = features.join(w2s.withColumnRenamed("wages_amt", "w2_wages"), "return_id", "left")
with_share = joined.withColumn(
    "w2_wage_share",
    F.when(F.col("wages_amt") > 0, F.coalesce(F.col("w2_wages"), F.lit(0)) / F.col("wages_amt"))
).drop("w2_wages")
print(with_share.count(), "rows in the joined table,", return_table.count(), "rows in return_table")
```

Notebook cell 4:

```python
# 4. Test: one row for each return. The assert stops the cell when the count is wrong.
assert with_share.count() == return_table.count(), f"{with_share.count()} rows, {return_table.count()} returns"
features = with_share
print("One row for each return:", features.count())
```

### Step 4. Record each feature, then write the two tables

Why: for every feature, the record holds the table it reads, the columns it reads, and its code. Thursday and next week read it.

1. Cell 5 already holds the row for `tax_to_agi`. Type the row for `w2_wage_share` in place of the empty row, as the table says.
2. Run cell 5. You should see two `Wrote` lines.

| Field of the row | Write this | Why |
|---|---|---|
| feature | `"w2_wage_share"` | the column cell 3 added |
| `table_read`: the table it reads | `"w2s, return_table"` | the W-2 wages come from `w2s`, the reported wages from `return_table` |
| `columns_read`: the columns it reads | `"w2s.wages_amt, return_table.wages_amt"` | the two amounts of the ratio, and `return_id` joins them |
| code | `"sum of w2s.wages_amt for each return_id, joined on return_id, over wages_amt where wages_amt > 0, else null"` | the order of the steps: sum, then join, then divide |

Notebook cell 5:

```python
# 5. The feature record: one row for each feature. Then write features and feature_record.
record = [
    ("tax_to_agi", "return_table", "total_tax_amt, agi_amt",
     "total_tax_amt / agi_amt where agi_amt > 0, else null"),
    ("", "", "", ""),  # type the row for w2_wage_share here
]
spark.createDataFrame(record, "feature string, table_read string, columns_read string, code string") \
    .write.mode("overwrite").saveAsTable(f"{schema}.feature_record")
features.write.mode("overwrite").saveAsTable(f"{schema}.features")
print("Wrote", f"{schema}.feature_record")
print("Wrote", f"{schema}.features")
```

### Step 5. Check

Run cell 6. It reads `features`, `feature_record`, `return_table` and `w2s` from your schema. It prints `Done:` when `features` has one row for each return, both ratios are right, and the record has both rows. Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 6:

```python
# 6. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{course_folder}/week-03/day-03/exercise-02-features-and-a-ratio/check.py").read(), _check)
print(_check["in_notebook"](spark, schema, {"predict_rows": predict_rows}, course_folder))
```

### Afterwards, together

1. A return with no W-2 gets a share of 0, and a return with no wages gets null. Why do the two cases get different values?
2. The row-count test caught the join that came first. Which other mistake in cell 3 would the same test not catch?
3. Your record says which tables and columns each feature reads. When would a reviewer of a selected return need that record?

The answer, after you try: [`answers/exercise-02-features-and-a-ratio`](../answers/exercise-02-features-and-a-ratio/).
