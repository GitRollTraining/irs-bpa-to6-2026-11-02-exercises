# Exercise 3: Predict, then query the governed batch as yourself

**Goal:** After this exercise, you can predict what a mask and a filter show you, and check it with a query as yourself.

**Scenario:** A copy of the dirty batch has a mask on the identification number and a filter by tax year. You predict what your group sees, query it as yourself, and read who may read it.

**AI tool:** none. Nothing in this exercise changes a grant, a mask or a filter.

**Where you work:** the notebook `week-03/day-02/exercise-03-query-the-governed-batch-as-yourself/exercise.ipynb` in your Git folder of the course, in Databricks. Attach the notebook to the compute the trainer names.

**Done when:** cell 5 prints `Done:`: your prediction, what you see, the grants, and why it differs from the trainer's demo.

**Optional part:** none.

**What you have:**

- The governed batch `course.returns.batch_governed`: the 32 rows of the dirty batch, of tax years 2019, 2021, 2022 and 2023. The trainer set a mask and a filter on it for the learners' group. The course made up every row.
- `check.py`, beside this notebook. Cell 5 runs it.

**Start from:** this notebook as the course gives it. The trainer just ran the same query as a reviewer. To start again, set the values you typed back to `""` and `{}`.

### Step 1. Predict what you will see

Why: "So a filter is tested like any other code: query the table as a user who should see less, and count what comes back." A prediction makes the count a test.

`course.returns.batch_governed` holds the same 32 rows as the dirty batch. The trainer set two controls on it:

- a row filter: the learners' group, the account group that holds every learner, sees the rows of tax year 2023 only.
- a column mask: the learners' group sees each `tin` as a pattern of stars.

The reviewer group, the trainer's account group, sees every row and every number. The trainer just queried the table as a reviewer, and saw these rows per tax year: 2019: 2, 2021: 8, 2022: 12, 2023: 10.

You are a member of the learners' group. In cell 1, between the quotes of `predict = ""`, write which tax years you will see, how many rows, and what `tin` will look like.

Then run cell 1.

Notebook cell 1:

```python
# 1. Your prediction: write it before you run cell 2.
predict = ""  # which tax years, how many rows, and what tin will look like to you
print(predict or "Write your prediction between the quotes.")
```

### Step 2. Query the table as yourself

Why: "Row filters and column masks are Unity Catalog access controls that restrict the rows and column values a user can see at query time."

Run cell 2. You should see two tables:

- the first: one row per tax year you may see, with its count of rows. "Rows where the function returns `FALSE` are excluded from query results."
- the second: three returns and their `tin`, as you see it. A column mask "takes the column value as input and returns the original value or a masked version."

Compare the two tables with your prediction. Then fill two values in cell 4:

1. In `rows_per_year`, write each tax year of the first table and its count, as `{year: rows}`.
2. In `identifier_seen`, copy one `tin` of the second table, as it is.

Notebook cell 2:

```python
# 2. The governed batch as you see it: rows per tax year, then three identification numbers.
display(spark.sql("""
SELECT tax_year, count(*) AS rows
FROM course.returns.batch_governed
GROUP BY tax_year
ORDER BY tax_year
"""))
display(spark.sql("SELECT return_id, tin FROM course.returns.batch_governed ORDER BY return_id LIMIT 3"))
```

### Step 3. Read the grants

Why: "to run a SELECT query on a table, a user must have the SELECT privilege on the table, the USE SCHEMA privilege on its parent schema and the USE CATALOG privilege on its catalog". USE SCHEMA and USE CATALOG are the privileges to open the schema and the catalog that hold the table. And "Privileges granted on a catalog automatically apply to all current and future schemas, tables, views, volumes, and functions within it."

Run cell 3. You should see a table of grants, one row per privilege:

- `SHOW GRANTS` shows each principal (a person or a group) and its privilege (its action type, such as `SELECT`). It also shows the object that holds the grant: the table, or the schema or catalog above it.
- If Databricks refuses `SHOW GRANTS`, the cell prints one line. Then it reads `information_schema.table_privileges`, a view that lists the grants you hold on tables. `grantee` is who holds the privilege. `inherited_from` is the object above the table that holds the grant.

Find the rows whose privilege is `SELECT`. In cell 4, in `grants`, write who holds `SELECT`, and the object that holds the grant.

Notebook cell 3:

```python
# 3. Who holds which privilege on the table.
try:
    display(spark.sql("SHOW GRANTS ON TABLE course.returns.batch_governed"))
except Exception as refused:  # SHOW GRANTS needs more than SELECT: show the grants you hold instead
    print("SHOW GRANTS refused:", str(refused).splitlines()[0][:200])
    display(spark.sql("""
    SELECT grantee, privilege_type, inherited_from
    FROM course.information_schema.table_privileges
    WHERE table_schema = 'returns' AND table_name = 'batch_governed'
    """))
```

### Step 4. Write why you see less than the trainer

Why: "Restrict access to SBU data (including PII and FTI) to those IRS personnel who have a need for the information in the performance of their duties." SBU is sensitive but unclassified data, and FTI and PII are kinds of it.

Run cell 4. It prints which of the last two values to fill:

| Cell 4 prints | Fill | What to write |
|---|---|---|
| `You see less than the trainer` | `why_differs` | which control hid what, and which group it applies to |
| `You see every tax year and the full number` | `fallback` | this workspace has no mask or filter on the table: tell the trainer. From cell 3's grants: which group could read the number, and why that is more than need to know |

Notebook cell 4:

```python
# 4. What you saw, and why it differs from the trainer's demo.
rows_per_year = {}  # from cell 2: each tax year and its rows, as {year: rows, year: rows}
identifier_seen = ""  # from cell 2: one value of tin, as it is
grants = ""  # from cell 3: who holds SELECT, and where it was granted
why_differs = ""  # step 4: why you see less than the trainer did
fallback = ""  # step 4: which group could read the number, and why
all_years = {2019, 2021, 2022, 2023}  # the tax years the trainer saw
if not rows_per_year or not identifier_seen:
    print("Copy rows_per_year and identifier_seen from cell 2 first.")
elif set(rows_per_year) != all_years or not any(c.isdigit() for c in identifier_seen):
    print("You see less than the trainer: fill why_differs.")
else:
    print("You see every tax year and the full number: fill fallback.")
```

### Step 5. Check

Run cell 5. It queries the table again as you. It prints `Done:` when these things are true:

- `predict` holds 5 words or more.
- `rows_per_year` holds each tax year you see, and its count.
- `identifier_seen` is a value of `tin` that you see.
- `grants` names who holds `SELECT`.
- `why_differs` holds 8 words or more. Where you see every year and every number, `fallback` holds 10 words or more instead.

Otherwise it prints `Not yet:` and each thing still to do. It does not judge your sentence: the debrief does. You do not need to read its code.

Notebook cell 5:

```python
# 5. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Your prediction and cell 2 agreed, or not. Which part was hardest to predict, and why?
2. The mask hides `tin` from you, but the batch still holds a name and a street address. Would you mask them, or remove them, and why?
3. A filter written with a wrong parameter type can return all rows. How would your count in cell 2 show that, and who would see it?

The answer, after you try: [`answers/exercise-03-query-the-governed-batch-as-yourself`](../answers/exercise-03-query-the-governed-batch-as-yourself/).
