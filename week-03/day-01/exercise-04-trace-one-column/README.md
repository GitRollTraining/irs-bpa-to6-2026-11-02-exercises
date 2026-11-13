# Exercise 4: Trace one column to its source

**Goal:** After this exercise, you can trace one column of a derived table to its source columns in the Lineage tab and say where the trace stops.

**Scenario:** On Wednesday each feature is traced to the table it came from. Today you trace one column of a table the course built from the returns.

**AI tool:** none.

**Where you work:** Catalog Explorer's **Lineage** tab, and the notebook `week-03/day-01/exercise-04-trace-one-column/exercise.ipynb` in your Git folder of the course, where you record the trace.

**Done when:** cell 3 prints `Done:`.

**Optional part:** cell 4, after cell 3 prints `Done:`. It reads the same trace from a lineage system table, by query.

**What you have:**

- The table `case_features` in the schema `case_selection`. The trainer's setup notebook built it from the other course tables. Its column `income_gap` came from one SQL query on Databricks. Its column `income_band` came from the table `income_bands`. The setup notebook wrote `income_bands` from Python. It read each return's `total_income` into Python, put it in a band, and wrote the bands as a new table.
- `check.py`, beside this notebook. Cell 3 runs it.

**Start from:** this notebook as the course gives it. The trainer traced the column `interest_gap` just before this exercise. You trace `income_gap`. To start again, set the values you typed back to `[]` and `""`.

### Step 1. Trace `income_gap`

Why: "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level". `income_gap` came from one such query.

1. In Catalog Explorer, open the course catalog, the schema `case_selection`, then the table `case_features`.
2. Select the **Lineage** tab, then **See Lineage Graph**. The graph shows `case_features` and the tables it came from.
3. In the graph, select the column `income_gap`. The graph highlights the columns it came from.
4. In cell 1, write each highlighted column in `income_gap_sources`, as table and column with a dot between, such as `"returns.wages"`.
5. In `income_gap_stops_at`, write where the trace stops: the tables at the left end of the trace, and why it goes no further.

| What to write | The answer | Why |
|---|---|---|
| `income_gap_sources` | `"returns.wages"`, `"third_party_reports.wages_reported"` | `income_gap` is wages on the return minus wages employers reported. "A feature built from two return fields leaves the same two-row trace." |
| `income_gap_stops_at` | the tables `returns` and `third_party_reports`, and why | the setup notebook filled these two tables with values it wrote itself. No other table feeds them. |

Run cell 1. It prints what you recorded.

Notebook cell 1:

```python
# 1. The trace of case_features.income_gap.
CATALOG = "workspace"  # the course catalog: the trainer tells you if it is different
income_gap_sources = []  # each highlighted column, as "table.column", such as "returns.wages"
income_gap_stops_at = ""  # the tables where the trace stops, and why it stops there

print("income_gap comes from:", income_gap_sources)
print("The trace stops at:", income_gap_stops_at)
```

### Step 2. Predict, then trace `income_band`

Why: "So an empty trace does not prove a column has no source." "Records are only emitted when lineage can be inferred."

First, predict. Read **What you have** again: how the setup notebook made `income_band`. In cell 2, between the quotes of `predict = ""`, write: will the trace of `income_band` reach `returns.total_income`? Why?

Then look:

1. In the same graph, select the column `income_band`.
2. Follow the highlighted columns to the left, as far as they go.
3. In `income_band_stops_at`, write the table where the trace stops.

Run cell 2.

Notebook cell 2:

```python
# 2. Predict, then trace case_features.income_band.
predict = ""  # before you look: will the trace reach returns.total_income? Why?
income_band_stops_at = ""  # the table where the trace stops, as the graph shows it

print("Prediction:", predict)
print("The income_band trace stops at:", income_band_stops_at)
```

### Step 3. Check

Run cell 3. It compares your record with how the setup notebook built `case_features`. It prints `Done:` when these things are true:

- `income_gap_sources` holds the two columns `income_gap` came from, and no other.
- `income_gap_stops_at` names `returns` and `third_party_reports`, in 4 words or more.
- `predict` holds 5 words or more.
- `income_band_stops_at` names the table where that trace stops.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 3:

```python
# 3. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Your `income_band` trace stopped before `returns`. What would you write beside it so that on Wednesday nobody reads `income_bands` as the band's real source?
2. "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns." The band went through Python, outside any query. How would you build it so that lineage records where it came from?
3. On Wednesday you build features yourself. Which step of your own build would you look at first if a trace came back empty?

The answer, after you try: [`answers/exercise-04-trace-one-column`](../answers/exercise-04-trace-one-column/).

### Optional part: the same trace by query

Why: "The system tables are `system.access.table_lineage` and `system.access.column_lineage`." A query gives a trace you can save and repeat.

Run cell 4. You should see one row per source column of `income_gap`. If it fails with a permission error, your account cannot read the system tables. The trainer then shows the result on screen.

Notebook cell 4:

```python
# 4. Optional: the trace of income_gap, from the column lineage system table.
display(spark.sql(f"""
SELECT DISTINCT source_table_full_name, source_column_name, target_column_name
FROM system.access.column_lineage
WHERE target_table_full_name = '{CATALOG}.case_selection.case_features'
  AND target_column_name = 'income_gap'
"""))
```
