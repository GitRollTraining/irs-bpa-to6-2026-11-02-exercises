# Exercise 4: Trace one column to its source

**Goal:** After this exercise, you can trace one column of a derived table to its source columns in the Lineage tab and say where the trace stops.

**Scenario:** On Wednesday each feature is traced to the table it came from. Today you trace one column of a table the course built from the returns.

**AI tool:** none.

**Where you work:** Catalog Explorer's **Lineage** tab, and the notebook `week-03/day-01/exercise-04-trace-one-column/exercise.ipynb` in your Git folder of the course, where you record the trace.

**Done when:** cell 3 prints `Done:`.

**Optional part:** cell 4, after cell 3 prints `Done:`. It reads the same trace from a lineage system table, by query.

**What you have:**

- The table `course.returns.return_summary`. The trainer's setup notebook built it from the return table, `course.returns.return_header`, with one SQL query on Databricks. Two of its columns are differences the query works out from columns of `return_header`. Its column `income_band` comes from a Python function: the query hands each return's `total_income` to the function, and the function gives back a band.
- `check.py`, beside this notebook. Cell 3 runs it.

**Start from:** this notebook as the course gives it. The trainer traced the column `adjustments_amt` just before this exercise. You trace `non_wage_income`. To start again, set the values you typed back to `[]` and `""`.

### Step 1. Trace `non_wage_income`

Why: "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level". `non_wage_income` came from one such query.

1. In Catalog Explorer, open the catalog `course`, the schema `returns`, then the table `return_summary`.
2. Select the **Lineage** tab, then **See Lineage Graph**. The graph shows `return_summary` and the table it came from.
3. In the graph, select the column `non_wage_income`. The graph highlights the columns it came from.
4. In cell 1, write each highlighted column in `non_wage_income_sources`, as table and column with a dot between, such as `"return_header.total_income"`.
5. In `non_wage_income_stops_at`, write where the trace stops: the table at the left end of the trace, and why it goes no further.

| What to write | The answer | Why |
|---|---|---|
| `non_wage_income_sources` | `"return_header.total_income"`, `"return_header.wages_amt"` | `non_wage_income` is total income minus wages. "A feature built from two return fields leaves the same two-row trace." |
| `non_wage_income_stops_at` | the table `return_header`, and why | the setup notebook filled `return_header` with values it wrote itself. No other table feeds it. |

Run cell 1. It prints what you recorded.

Notebook cell 1:

```python
# 1. The trace of return_summary.non_wage_income.
non_wage_income_sources = []  # each highlighted column, as "table.column", such as "return_header.total_income"
non_wage_income_stops_at = ""  # the table where the trace stops, and why it stops there

print("non_wage_income comes from:", non_wage_income_sources)
print("The trace stops at:", non_wage_income_stops_at)
```

### Step 2. Predict, then trace `income_band`

Why: "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns." "So an empty trace does not prove a column has no source."

First, predict. Read **What you have** again: how the setup notebook made `income_band`. In cell 2, between the quotes of `predict = ""`, write: will the trace of `income_band` reach `return_header.total_income`? Why?

Then look:

1. In the same graph, select the column `income_band`.
2. Look at what the graph highlights: a column of `return_header`, or nothing.
3. In `income_band_trace`, write what the graph shows, and whether it matches your prediction.

Run cell 2.

Notebook cell 2:

```python
# 2. Predict, then trace return_summary.income_band.
predict = ""  # before you look: will the trace reach return_header.total_income? Why?
income_band_trace = ""  # what the graph shows for income_band, and whether it matches your prediction

print("Prediction:", predict)
print("The graph shows:", income_band_trace)
```

### Step 3. Check

Run cell 3. It compares your record with how the setup notebook built `return_summary`. It prints `Done:` when these things are true:

- `non_wage_income_sources` holds the two columns `non_wage_income` came from, and no other.
- `non_wage_income_stops_at` names `return_header`, in 4 words or more.
- `predict` holds 5 words or more.
- `income_band_trace` holds 4 words or more. The check does not judge it: the debrief compares it with your prediction.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 3:

```python
# 3. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Compare your `income_band` trace with your prediction. What would you write beside the column so that on Wednesday nobody reads an empty trace as "no source"?
2. The band went through a Python function inside the query. How would you build it so that lineage records where it came from, every time?
3. On Wednesday you build features yourself. Which step of your own build would you look at first if a trace came back empty?

The answer, after you try: [`answers/exercise-04-trace-one-column`](../answers/exercise-04-trace-one-column/).

### Optional part: the same trace by query

Why: "The system tables are `system.access.table_lineage` and `system.access.column_lineage`." A query gives a trace you can save and repeat.

Run cell 4. You should see one row per source column of `non_wage_income`. If it fails with a permission error, your account cannot read the system tables. The trainer then shows the result on screen.

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
