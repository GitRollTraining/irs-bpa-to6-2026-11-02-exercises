# Exercise 1: Write the keyed tables and test their counts

**Goal:** After this exercise, you can write the return files into three keyed tables, and test that their counts match the files.

**Scenario:** The course's synthetic returns are XML files in a volume. You turn the files into three tables, and prove with tests that no return is lost.

**AI tool:** none.

**Where you work:** the Databricks workspace. This notebook is `week-03/day-03/exercise-01-keyed-tables/exercise.ipynb` in your Git folder of the course.

**Done when:** cell 7 prints `Done:`.

**Optional part:** none.

**What you have:**

- The volume `/Volumes/course/returns/raw/`: one XML file for each return, made up by the course. Before class, the trainer wrote the case key into each file in place of the taxpayer identification number, by Tuesday's rule. You need no join.
- Your schema, `course.learner_NN`. The trainer gives you your number.
- Week 2's tested reader, `form1040.py`, in `week-02/day-03/answers/exercise-04-a-repeated-element/files/` of your Git folder. Its function `dependent_relationships` gives the dependents of one return.
- `check.py`, beside this notebook. Cell 7 runs it.

**Start from:** this notebook as the course gives it. The trainer showed the read, the dependents and the counts just before. New here: the W-2 table and the count tests.

### Step 1. Name your schema

Why: every table today goes in your own schema.

1. In cell 1, type the number the trainer gave you in place of `NN`, such as `course.learner_07`.
2. At the top right, select the compute the trainer names from the compute menu (**Connect**).
3. Run cell 1. You should see `Your tables go in` and your schema.

Notebook cell 1:

```python
# 1. Your schema, where your tables go. Type your number in place of NN.
schema = "course.learner_NN"

import os
course_folder = os.getcwd().split("/week-03/")[0]  # your Git folder of the course
print("Your tables go in", schema)
```

### Step 2. Read the files, and keep each row's file name

Why: the return table needs one row for each file, and the file's name.

1. Run cell 2. You should see `52 returns read`, then the column names, `CourseLabel` and `ReturnData` among them.
2. Read cell 3. Its last line selects `file_name`. In cell 3, type `"yes"` or `"no"` between the quotes of `predict_file_name = ""`: will cell 3 run as it is?
3. Run cell 3. Compare what happens with your prediction.
4. If cell 3 stopped on `file_name`, add the line of the table to cell 2.
5. Run cell 2 and cell 3 again. Cell 3 should print `52 rows in return_table`.

| What | Write this | Why |
|---|---|---|
| A new line in cell 2, right after the line `.load("/Volumes/course/returns/raw/")` | `.select("*", "_metadata.file_name")` | `_metadata` is a hidden column: a read gets it only when it names it. `file_name` in it names each row's file. `"*"` keeps the other columns. |

Cell 3 keeps Tuesday's kept fields only: no name, no address. `CourseLabel` holds the course's label, on examined returns only. Exercise 4 uses it.

Notebook cell 2:

```python
# 2. Read the return files: one row for each Return element.
from pyspark.sql import functions as F

returns = (spark.read.format("xml")
           .option("rowTag", "Return")
           .load("/Volumes/course/returns/raw/")
           .withColumn("return_id", F.concat_ws("-", F.col("ReturnHeader.Filer.CaseKey"),
                                                     F.col("ReturnHeader.TaxYr"))))
print(returns.count(), "returns read. Columns:", ", ".join(returns.columns))
```

Notebook cell 3:

```python
# 3. The return table: one row for each return, with Tuesday's kept fields only.
# Each line: an XML element, then .alias(Tuesday's name).
predict_file_name = ""  # will this cell run as it is? Type "yes" or "no" before you run it.

h, d = "ReturnHeader.", "ReturnData.IRS1040."
return_table = returns.select(
    "return_id",
    F.col(h + "Filer.CaseKey").alias("filer_key"),
    F.col(h + "TaxYr").alias("tax_year"),
    F.col(d + "IndividualReturnFilingStatusCd").cast("string").alias("filing_status"),
    F.col(d + "WagesAmt").alias("wages_amt"),
    F.col(d + "TotalIncomeAmt").alias("total_income"),
    F.col(d + "AdjustedGrossIncomeAmt").alias("agi_amt"),
    F.col(d + "TotalTaxAmt").alias("total_tax_amt"),
    F.col("CourseLabel.ExamChangedTax").alias("exam_changed_tax"),
    F.col("CourseLabel.TaxAddedByExam").alias("tax_added_by_exam"),
    "file_name")
print(return_table.count(), "rows in return_table")
```

### Step 3. Make the two child tables

Why: a return holds lists of dependents and of W-2s. `F.explode` makes one row for each item of a list. Each new row keeps `return_id`, so it joins back to its return.

1. Cell 4 makes `dependents` as the trainer showed.
2. In cell 4, type the W-2 element's name between the quotes of `w2_element = ""`, as the table says.
3. Run cell 4. You should see `77 dependent rows, 62 W-2 rows`.

| What | Write this | Why |
|---|---|---|
| `w2_element`, in cell 4 | `"IRSW2"` | Each W-2 is an `<IRSW2>` element in `ReturnData`, its wages in `<WagesAmt>`. A return can hold two, so the column is a list. |

Notebook cell 4:

```python
# 4. The child tables: explode turns each list into one row for each item.
dependents = (returns
    .select("return_id", F.explode(d + "DependentDetail").alias("dep"))
    .select("return_id", F.col("dep.DependentRelationshipCd").alias("relationship")))

w2_element = ""  # the name of the W-2 element in the files
w2s = (returns
    .select("return_id", F.explode("ReturnData." + w2_element).alias("w2"))
    .select("return_id", F.col("w2.WagesAmt").alias("wages_amt")))
print(dependents.count(), "dependent rows,", w2s.count(), "W-2 rows")
```

### Step 4. Write the tables, then test their counts

Why: the day's reading says: "A table is not finished until its counts reconcile with the files." Each test is an `assert`, as on Tuesday: a wrong count stops the cell with a message.

1. Run cell 5. `saveAsTable` writes each table to your schema. You should see three `Wrote` lines.
2. In cell 6, type the lines of tests 2 and 3 where the comments say, as the table says. Test 1 is already there.
3. Run cell 6. You should see `All three tests pass`. If an `assert` stops the cell, its message names the count that is wrong.

| Test | Write this | Why |
|---|---|---|
| 2 | `assert rt.select("return_id").distinct().count() == rt.count(), "a return_id shows twice"` | No `return_id` may appear twice. If the distinct count is smaller, one return is in the table twice. |
| 3, first line | `assert dep.count() == reader_count, f"{dep.count()} dependent rows, the reader counts {reader_count}"` | The dependent rows must equal the `DependentDetail` elements that week 2's reader counts. It reads each file with plain Python, not Spark, and passed its tests in week 2. |
| 3, second line | `assert dep.join(rt, "return_id", "left_anti").count() == 0, "a dependent has no return"` | Every dependent's `return_id` must be in the return table. A `left_anti` join keeps the rows of `dep` with no match in `rt`. There must be none. |

Notebook cell 5:

```python
# 5. Write the three tables. overwrite replaces a table that is there.
for name, df in [("return_table", return_table), ("dependents", dependents), ("w2s", w2s)]:
    df.write.mode("overwrite").saveAsTable(f"{schema}.{name}")
    print("Wrote", f"{schema}.{name}")
```

Notebook cell 6:

```python
# 6. Three count tests. Each assert stops the cell when its count is wrong.
import sys
volume = "/Volumes/course/returns/raw/"
files = [n for n in os.listdir(volume) if n.endswith(".xml")]  # the names of the XML files
rt = spark.table(f"{schema}.return_table")
dep = spark.table(f"{schema}.dependents")
tests_passed = False

# Test 1: one row for each file.
assert rt.count() == len(files), f"{rt.count()} rows, {len(files)} files"
assert rt.select("file_name").distinct().count() == len(files), "a file is missing or read twice"

# Test 2: no return_id twice. Type its assert line below.


# Test 3: week 2's reader counts the dependents.
sys.path.append(course_folder + "/week-02/day-03/answers/exercise-04-a-repeated-element/files")  # where Python finds the reader
from form1040 import dependent_relationships
reader_count = sum(len(dependent_relationships(volume + n)) for n in files)
# Type the two assert lines of test 3 below.


tests_passed = True
print("All three tests pass:", rt.count(), "returns,", dep.count(), "dependents.")
```

### Step 5. Check

Run cell 7. It prints `Done:` when your tables and tests are right. Otherwise it prints `Not yet:` and each thing still to do: if cell 6 stopped, it says the tests have not passed. You do not need to read its code.

Notebook cell 7:

```python
# 7. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{course_folder}/week-03/day-03/exercise-01-keyed-tables/check.py").read(), _check)
print(_check["in_notebook"](spark, schema, {"predict_file_name": predict_file_name, "tests_ran": tests_passed}, course_folder))
```

### Afterwards, together

1. A return with no dependents has a row in `return_table` and none in `dependents`. When would two different counts be a fault?
2. Test 3 counts with week 2's reader, not with Spark. What would a second count with Spark miss?
3. The files already hold the case key. What would change in your cells if they still held the taxpayer identification number?

The answer, after you try: [`answers/exercise-01-keyed-tables`](../answers/exercise-01-keyed-tables/).
