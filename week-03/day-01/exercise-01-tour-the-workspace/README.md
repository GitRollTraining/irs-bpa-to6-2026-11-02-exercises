# Exercise 1: Tour the workspace: one table, two counts

**Goal:** After this exercise, you can find a table in Catalog Explorer by its full name and count its rows in a notebook and the SQL editor.

**Scenario:** The course's synthetic returns sit in one table of the course catalog. Before you decide what a model needs from it, you find it, copy its full name and count its rows twice, in two tools.

**AI tool:** none.

**Where you work:** the Databricks workspace. This notebook is `week-03/day-01/exercise-01-tour-the-workspace/exercise.ipynb` in your Git folder of the course. You also use Catalog Explorer and the SQL editor, from the left bar.

**Done when:** cell 4 prints `Done:`, the full name you pasted, and the row count. The notebook's count and the count you typed from the SQL editor must be the same.

**Optional part:** open the table's **Sample Data** tab in Catalog Explorer. Which column would you read first, and why?

**What you have:**

- The course catalog. Its name is the value of `CATALOG` in cell 1. The trainer tells you if it is different.
- In it, the schema `case_selection`, and in that, the table `returns`: one row for each return of the course. The course made up every row. No row is a real taxpayer.
- `check.py`, beside this notebook. Cell 4 runs it.

**Start from:** this notebook as the course gives it. The trainer showed the same steps on another table just before this exercise. To start again, set the values you typed back to `""` and `None`.

### Step 1. Find the table, and copy its full name

Why: every query this week names a table by its full name. "A full name joins the three with dots": catalog, schema, table.

1. In the left bar, select **Catalog**. Catalog Explorer opens.
2. Open the course catalog, then the schema `case_selection`, then the table `returns`.
3. At the top of the table's page, find the table's full name. Select the copy icon beside it. If you see no copy icon, type the name: catalog, a dot, schema, a dot, table.
4. In cell 1, paste the full name between the quotes of `full_name = ""`.
5. Run cell 1. You should see the three parts of the name, one on each line: the table, the schema, the catalog.

Notebook cell 1:

```python
# 1. The table's full name.
CATALOG = "workspace"  # the course catalog: the trainer tells you if it is different
full_name = ""  # paste the full name from Catalog Explorer here

parts = full_name.replace("`", "").split(".")
if len(parts) != 3:
    print("Paste the full name: three parts with a dot between them, catalog.schema.table.")
else:
    print("Table:  ", parts[2])
    print("Schema: ", parts[1])
    print("Catalog:", parts[0])
```

### Step 2. Count the rows in the notebook

Why: a notebook runs code on a table. "A notebook runs on a cluster, so a notebook with none attached runs nothing."

1. At the top right of the notebook, open the compute menu (**Connect**). Select the compute the trainer names.
2. Run cell 2. It counts the rows of the table that you named in cell 1.

You should see one line: `Rows in`, the full name, and a number.

Notebook cell 2:

```python
# 2. Count the rows in the notebook.
notebook_count = None
if full_name.count(".") != 2:
    print("Paste the full name in cell 1 and run it first. Then run this cell again.")
else:
    notebook_count = spark.sql(f"SELECT COUNT(*) AS row_count FROM {full_name}").first()["row_count"]
    print("Rows in", full_name, ":", notebook_count)
```

### Step 3. Count the rows in the SQL editor

Why: the SQL editor runs one query, with no notebook. "A SQL warehouse is the compute behind the SQL editor."

First, predict. The notebook ran on the compute you attached. The SQL editor runs on a SQL warehouse, which is different compute. In cell 3, between the quotes of `explain = ""`, write one or two sentences: will the two counts be the same, and why?

Then count:

1. In the left bar, select **SQL Editor**. A new query opens.
2. At the top of the editor, select the SQL warehouse that the trainer names.
3. Type this query. Put your full name from cell 1 in place of `<full name>`.

   SQL editor:

   ```sql
   SELECT COUNT(*) FROM <full name>
   ```

4. Select **Run**. You should see one row with one number.
5. In cell 3, type that number after `sql_editor_count = `, in place of `None`.
6. Run cell 3. It prints the two counts side by side.

Notebook cell 3:

```python
# 3. The SQL editor's count, and your prediction.
sql_editor_count = None  # the number the SQL editor showed, such as 12
explain = ""  # will the two counts be the same, and why? Write it before you count.

print("SQL editor:", sql_editor_count, "| notebook:", notebook_count)
```

### Step 4. Check

Run cell 4. It counts the table's rows again. It prints `Done:` when these things are true:

- `full_name` names the table `returns` in the schema `case_selection` of the course catalog.
- The notebook's count and the SQL editor's count are both the table's count.
- `explain` holds 8 words or more.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. The notebook and the SQL editor ran on different compute. When would you open the SQL editor instead of a notebook in your own work?
2. Two tables can share a short name, and "only the full name tells them apart." A schema `staging` could also hold a table `returns`. How would you know which of the two you counted?
3. Catalog Explorer showed the table before you ran a query. What did it tell you that the count did not?

The answer, after you try: [`answers/exercise-01-tour-the-workspace`](../answers/exercise-01-tour-the-workspace/).
