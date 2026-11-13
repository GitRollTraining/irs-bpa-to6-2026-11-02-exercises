# Exercise 3: Add the history and the change since last year

**Goal:** After this exercise, you can add a filer's mean of earlier wages and the change since last year, from earlier years only.

**Scenario:** The filer F-30037 has four returns, 2020 to 2023. F-30074 has one. You predict F-30037's 2023 values by hand, then compute them for every return.

**AI tool:** none.

**Where you work:** the Databricks workspace. This notebook is `week-03/day-03/exercise-03-history-and-change/exercise.ipynb` in your Git folder of the course.

**Done when:** cell 8 prints `Done:`.

**Optional part:** cell 9, an anomaly score for early finishers. It is not part of done, and it writes no table.

**What you have:**

- `features` and `feature_record` in your schema, from exercise 2.
- `check.py`, beside this notebook. Cell 8 runs it.

**Start from:** this notebook as the course gives it. The trainer built the same window on another column just before. New here: the window on wages, and `LAG`.

### Step 1. Name your schema, and see one filer's rows

Why: you predict from rows you can see, before any code computes them.

1. In cell 1, type your number in place of `NN`.
2. Attach the compute the trainer names.
3. Run cell 1.
4. Run cell 2. `.show()` prints rows as a table. You should see four rows of F-30037, 2020 to 2023, with `return_id`, `tax_year` and `wages_amt`.

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
# 2. The rows of the filer F-30037, in tax-year order.
from pyspark.sql import functions as F
from pyspark.sql import Window
features = spark.table(f"{schema}.features")
features.filter(F.col("filer_key") == "F-30037") \
    .select("return_id", "tax_year", "wages_amt").orderBy("tax_year").show()
```

### Step 2. Predict the 2023 return's two values

Why: a value worked out by hand checks the code. Use only the rows of cell 2.

1. In cell 3, type the mean of the wages of the years before 2023, in place of `None` after `predict_mean = `.
2. Type the change since 2022 as a fraction, in place of `None` after `predict_change = `. For example, a rise from 40,000 to 44,000 is 0.1. The check accepts a change within 0.002 of the true one.
3. Run cell 3. You should see your two numbers.

Notebook cell 3:

```python
# 3. Your prediction for the return F-30037-2023, from the rows of cell 2.
predict_mean = None    # the mean of the wages of 2020, 2021 and 2022
predict_change = None  # the change from 2022 to 2023, as a fraction, such as 0.1
print("Mean of earlier wages:", predict_mean, "| change since last year:", predict_change)
```

### Step 3. Compute the two columns for every return

Why: a window function reads a filer's other rows. `F.lag` gives the value of the row before, in the window's order: the filer's return of the year before. Next week, you score the model on the latest year's returns.

1. In cell 4, type the column to average between the quotes of `history_column = ""`.
2. In cell 5, put the line of the table in place of the line `prior = F.lit(None)`.
3. Run cell 4. It prints nothing.
4. Run cell 5. It prints nothing.

| What | Write this | Why |
|---|---|---|
| `history_column`, in cell 4 | `"wages_amt"` | The history is the mean of earlier wages. The frame `rowsBetween(Window.unboundedPreceding, -1)` takes every earlier row of the filer and stops at the row before. |
| A new line in cell 5 | `prior = F.lag("wages_amt").over(by_year)` | A first return has no row before, so `prior` is null, and the change is null too. `wages_change_pct` is a fraction, such as 0.1. |

Notebook cell 4:

```python
# 4. History: the mean of the filer's earlier wages. The frame ends at -1, the year before.
history_column = ""  # the column to average
earlier = (Window.partitionBy("filer_key").orderBy("tax_year")
           .rowsBetween(Window.unboundedPreceding, -1))
features = features.withColumn("mean_prior_wages", F.avg(history_column).over(earlier))
```

Notebook cell 5:

```python
# 5. Change since last year: this year's wages against last year's, from LAG.
by_year = Window.partitionBy("filer_key").orderBy("tax_year")
prior = F.lit(None)  # put the LAG line here, in place of this line
features = features.withColumn(
    "wages_change_pct",
    F.when(prior > 0, (F.col("wages_amt") - prior) / prior))
```

### Step 4. Read the values beside your prediction

Why: one filer worked out by hand catches a frame that reaches the current year.

1. Run cell 6. It prints the two filers' rows, then your prediction.
2. Compare the two new values of the row F-30037-2023 with your prediction. If they differ, read cell 4's frame again.
3. Find the row F-30074-2023. Both new columns show `null`: the filer has no earlier return.

Notebook cell 6:

```python
# 6. The two filers' values, beside your prediction.
features.filter(F.col("filer_key").isin("F-30037", "F-30074")) \
    .select("return_id", "wages_amt", "mean_prior_wages", "wages_change_pct").orderBy("return_id").show()
print("Your prediction for F-30037-2023:", predict_mean, predict_change)
```

### Step 5. Record the two features, then write

Why: each feature keeps its record row: the table, the columns and the code.

1. Cell 7 already holds the row for `mean_prior_wages`. Type the row for `wages_change_pct` in place of the empty row, as the table says.
2. Run cell 7. You should see two `Wrote` lines.

| Field of the row | Write this | Why |
|---|---|---|
| feature | `"wages_change_pct"` | the column cell 5 added |
| `table_read`: the table it reads | `"return_table"` | its wages came from the return table, through `features` |
| `columns_read`: the columns it reads | `"filer_key, tax_year, wages_amt"` | the window groups by the filer, orders by the year, and reads the wages |
| code | `"(wages_amt - wages of the row before) / wages of the row before, LAG by filer_key in tax_year order, null for a first return"` | the rule for a first return is part of the code |

Notebook cell 7:

```python
# 7. Two record rows, then write features and feature_record again (overwrite).
new_rows = [
    ("mean_prior_wages", "return_table", "filer_key, tax_year, wages_amt",
     "mean of wages_amt over the filer's earlier years: frame unboundedPreceding to -1"),
    ("", "", "", ""),  # type the row for wages_change_pct here
]
names = [r[0] for r in new_rows]
old = [tuple(r) for r in spark.table(f"{schema}.feature_record")
       .select("feature", "table_read", "columns_read", "code").collect() if r[0] not in names]
spark.createDataFrame(old + new_rows, "feature string, table_read string, columns_read string, code string") \
    .write.mode("overwrite").saveAsTable(f"{schema}.feature_record")
features.write.mode("overwrite").saveAsTable(f"{schema}.features")
print("Wrote", f"{schema}.feature_record")
print("Wrote", f"{schema}.features")
```

### Step 6. Check

Run cell 8. It prints `Done:` when your prediction, both new columns and the record are right. Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 8:

```python
# 8. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{course_folder}/week-03/day-03/exercise-03-history-and-change/check.py").read(), _check)
print(_check["in_notebook"](spark, schema, {"predict_mean": predict_mean, "predict_change": predict_change}, course_folder))
```

### Optional: an anomaly score, for early finishers

Why: an anomaly is a return far from a norm, here the filer's own earlier years. The check does not read this cell.

1. Run cell 9. It divides each return's distance from `mean_prior_wages` by `F.stddev`, the spread (standard deviation) of the earlier wages.
2. Read the score of F-30037-2023. Here a score above 2 counts as far. The deck's score compares a return with a group of filers. This one compares it with the filer's own earlier years.

Notebook cell 9:

```python
# 9. Optional: distance from the filer's own history, in standard deviations. Writes no table.
spread = F.stddev("wages_amt").over(earlier)
features.withColumn("wages_anomaly", F.abs(F.col("wages_amt") - F.col("mean_prior_wages")) / spread) \
    .filter(F.col("filer_key") == "F-30037").select("return_id", "wages_anomaly").orderBy("return_id").show()
```

### Afterwards, together

1. F-30074 has one return, so both new columns are null. Why is null a better value there than 0?
2. A frame that ends at the current row gives F-30037-2023 a higher mean. Why would next week's test score then look too good?
3. A filer files for 2021 and 2023, with no 2022 return. What would `LAG` give for 2023, and would you keep that value?

The answer, after you try: [`answers/exercise-03-history-and-change`](../answers/exercise-03-history-and-change/).
