# Exercise 4: Trace one column to its source

**Goal:** After this exercise, you can trace a derived table's column to its source columns in the Lineage tab and say where the trace stops.

**Scenario:** On Wednesday each feature is traced to the table it came from. Today you trace one column of a table the course built from the returns.

**AI tool:** none.

**Where you work:** Catalog Explorer's **Lineage** tab, and the notebook `week-03/day-01/exercise-04-trace-one-column/exercise.ipynb` in your Git folder of the course, where you record the trace. Cell 1 is the code cell whose first line starts with `# 1.`, and so on for each cell.

**Done when:** cell 3 prints `Done:`.

**Optional part:** cell 4, after cell 3 prints `Done:`. It reads the same trace from a lineage system table, by query.

**What you have:**

- The table `course.returns.return_summary`. The trainer's setup notebook built it from the return table, `course.returns.return_header`, with one SQL query on Databricks. Two of its columns, `non_wage_income` and `adjustments_amt`, are differences the query works out from columns of `return_header`, with plain SQL. Its column `income_band` comes from a Python function: the query hands each return's `total_income` to the function, and the function gives back a band.
- Lineage records the columns a query reads. From the Databricks documentation: "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level".
- `check.py`, beside this notebook. Cell 3 runs it.

**Start from:** this notebook as the course gives it. The trainer traced the column `adjustments_amt` just before this exercise. You trace `non_wage_income`. To start again, set the values you typed back to `[]` and `""`.

### Step 1. Trace `non_wage_income`

Why: `non_wage_income` came from one SQL query on Databricks, so lineage recorded the columns it reads.

1. In Catalog Explorer, open the catalog `course`, the schema `returns`, then the table `return_summary`.
2. Select the **Lineage** tab, then **See Lineage Graph**. The graph shows `return_summary` and the table it came from.
3. Click the `return_summary` box. Its columns show. Click the `return_header` box too, to show its columns.
4. In the `return_summary` box, select the column `non_wage_income`. The graph highlights the columns it came from.
5. In cell 1, write each highlighted column in `non_wage_income_sources`, as table and column with a dot between, such as `"return_header.total_income"`. With or without `course.returns.` in front: the check accepts both.
6. If the graph highlights `return_id` too, leave it out. If it highlights any other column, write what you see. Then tell the trainer.
7. Find the table at the left end of the trace. In `non_wage_income_stops_at`, write its name.
8. In the same line, write what the graph shows to the left of that table.

Run cell 1. It prints what you recorded.

Notebook cell 1:

```python
# 1. The trace of return_summary.non_wage_income.
non_wage_income_sources = []  # each highlighted column, as "table.column", such as "return_header.total_income"
non_wage_income_stops_at = ""  # the table at the left end of the trace, and what the graph shows to its left

print("non_wage_income comes from:", non_wage_income_sources)
print("The trace stops at:", non_wage_income_stops_at)
```

### Step 2. Predict, then trace `income_band`

First, predict. Read **What you have** again: how the setup notebook made `income_band`. Will the trace of `income_band` reach `return_header.total_income`? In cell 2, between the quotes of `predict = ""`, write yes or no, and the reason.

Then look:

1. In the same graph, select the column `income_band`.
2. Look at what the graph highlights: a column of `return_header`, or nothing.
3. In `income_band_trace`, write what the graph shows. If it shows anything else, or no lineage yet, write exactly what you see.
4. In the same line, write whether it matches your prediction.

Run cell 2.

Why: "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns" (Databricks documentation). A user-defined function is a function you write and call inside a query, such as the Python function behind `income_band`. So an empty trace does not prove a column has no source.

Notebook cell 2:

```python
# 2. Predict, then trace return_summary.income_band.
predict = ""  # before you look: will the trace reach return_header.total_income? Yes or no, and the reason
income_band_trace = ""  # what the graph shows for income_band, and whether it matches your prediction

print("Prediction:", predict)
print("The graph shows:", income_band_trace)
```

### Step 3. Check

Run cells 1 and 2 first, in this session, so cell 3 has their values. Then run cell 3. It compares your record with how the setup notebook built `return_summary`. It prints `Done:` when these things are true:

- `non_wage_income_sources` holds the two columns `non_wage_income` came from, and no other.
- `non_wage_income_stops_at` names the table where the trace stops, in 4 words or more.
- `predict` holds 5 words or more.
- `income_band_trace` holds 4 words or more. The check does not judge it: you compare it with your prediction in **Afterwards, together**.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 3:

```python
# 3. Check. You do not need to read this code.
# Do not change this cell. The code is in the notebook.
```

### Afterwards, together

1. Compare your `income_band` trace with your prediction. What would you write beside the column so that on Wednesday nobody reads an empty trace as "no source"?
2. The band went through a Python function inside the query. Lineage records plain SQL, such as the subtraction behind `non_wage_income`. How would you build the band so that lineage records where it came from, every time?
3. On Wednesday you build features yourself. Which step of your own build would you look at first if a trace came back empty?

The answer: after the talk together, open `week-03/day-01/answers/exercise-04-trace-one-column/` in your Git folder of the course ([link](../answers/exercise-04-trace-one-column/)).

### Optional part: the same trace by query

Why: the lineage system tables are `system.access.table_lineage` and `system.access.column_lineage` (Databricks documentation). A query gives a trace you can save and repeat.

Run cell 4. You should see one row per source column of `non_wage_income`. A permission error means your account cannot read the system tables. In that case, the trainer shows the result on screen.

Notebook cell 4:

```python
# 4. Optional: the trace of non_wage_income, from the column lineage system table.
display(spark.sql("""
SELECT DISTINCT source_table_full_name, source_column_name, target_column_name
FROM system.access.column_lineage
WHERE target_table_full_name = 'course.returns.return_summary'
  AND target_column_name = 'non_wage_income'
"""))
```
