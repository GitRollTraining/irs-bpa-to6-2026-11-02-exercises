# Exercise 1: Tour the workspace: one table, two counts

**Goal:** After this exercise, you can find a table by its full name and count its rows in a notebook and the SQL editor.

**Scenario:** The course's synthetic returns sit in one table of the course catalog. Before you decide what a machine-learning model needs from it, you find it, copy its full name and count its rows twice, in two tools.

**AI tool:** none.

**Where you work:** the Databricks workspace. This notebook is `week-03/day-01/exercise-01-tour-the-workspace/exercise.ipynb` in your Git folder of the course. You also use Catalog Explorer and the SQL editor, from the left bar. Cell 1 is the code cell whose first line starts with `# 1.`, and so on for each cell.

**Done when:** cell 4 prints `Done:`.

**Optional part:** in Catalog Explorer, open the table's **Sample Data** tab. If it asks for compute, select the SQL warehouse of step 3. Which column would you read first, and why? Write your answer as a comment in a new cell at the end of this notebook.

**What you have:**

- The catalog `course`, its schema `returns`, and in that, the table `return_header`: one row for each return of the course. The course made up every row. No row is a real taxpayer.
- `check.py`, beside this notebook. Cell 4 runs it.

**Start from:** this notebook as the course gives it. The trainer showed the same steps on another table just before this exercise. To start again, set the values you typed back to `""` and `None`.

### Step 1. Find the table, and copy its full name

Why: every query this week names a table by its full name. A full name joins catalog, schema and table with dots, in that order.

1. In the left bar, select **Catalog**. Catalog Explorer opens.
2. Open the catalog `course`, then the schema `returns`, then the table `return_header`.
3. Look at the table's **Overview** tab: its columns, their types, and its owner. You need them for the talk after the exercise.
4. At the top of the table's page, find the table's full name. Select the copy icon beside it. If you see no copy icon, type the name: catalog, a dot, schema, a dot, table.
5. In cell 1, paste the table's full name between the quotes of `full_name = ""`.

You run cell 1 in step 2, after you attach compute.

Notebook cell 1:

```python
# 1. The table's full name.
full_name = ""  # paste the full name from Catalog Explorer here

parts = full_name.replace("`", "").split(".")
if len(parts) != 3:
    print("Paste the full name: three parts with a dot between them, catalog.schema.table.")
else:
    print("Catalog:", parts[0])
    print("Schema: ", parts[1])
    print("Table:  ", parts[2])
```

### Step 2. Count the rows in the notebook

Why: a notebook runs code on a table, on compute (a cluster). "A notebook runs on a cluster, so a notebook with none attached runs nothing." (the day's reading)

1. At the top right of the notebook, open the compute menu (**Connect**). Select the compute whose name the trainer wrote on the board. If it shows that it is starting, wait: it can take a few minutes.
2. Run cell 1. You should see the three parts of the name, one on each line: the catalog, the schema, the table.
3. Run cell 2. It counts the rows of the table that you named in cell 1. You should see one line: `Rows in`, the full name, and a number.

Notebook cell 2:

```python
# 2. Count the rows in the notebook.
notebook_count = None
if full_name.count(".") != 2:
    print("Cell 1 has no full name yet. Run cell 1 first, with the full name in it.")
else:
    notebook_count = spark.sql(f"SELECT COUNT(*) AS row_count FROM {full_name}").first()["row_count"]
    print("Rows in", full_name, ":", notebook_count)
```

### Step 3. Count the rows in the SQL editor

Why: the SQL editor runs one query, with no notebook, on a different kind of compute. "A SQL warehouse is the compute behind the SQL editor." (the day's reading)

First, predict. The notebook ran on the compute you attached. The SQL editor runs on a SQL warehouse, which is different compute. In cell 3, between the quotes of `explain = ""`, write one or two sentences: will the two counts be the same, and why?

Then count:

1. Open the SQL editor in a new browser tab: in the left bar, right-click **SQL Editor**, then open the link in a new tab. The notebook keeps its values in its own tab.
2. At the top of the editor, select the SQL warehouse whose name the trainer wrote on the board. If its status is Stopped, it starts when you run the query. Wait: it can take a few minutes.
3. Type this query. Put the table's full name from cell 1 in place of `<full name>`.

   SQL editor:

   ```sql
   SELECT COUNT(*) FROM <full name>
   ```

4. Select **Run**. You should see one row with one number.
5. Go back to the notebook's tab. In cell 3, type that number after `sql_editor_count = `, in place of `None`. Type the digits only, with no quotes.
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

- `full_name` names the table `return_header` in the schema `returns` of the catalog `course`.
- The notebook's count is the count that cell 4 finds.
- The SQL editor's count is the count that cell 4 finds.
- `explain` holds 8 words or more.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

If a cell shows an error, such as a missing table, no permission or no `check.py`, show the error to the trainer.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# Do not change this cell. The code is in the notebook.
```

### Afterwards, together

1. The notebook and the SQL editor ran on different compute. When would you open the SQL editor instead of a notebook in your own work?
2. Two tables can share a short name, and "only the full name tells them apart" (the day's reading). A schema `staging` could also hold a table `return_header`. How would you know which of the two you counted?
3. The table's **Overview** tab showed its columns, their types and its owner. What did it tell you that the count did not?

The answer: after the talk together, open `week-03/day-01/answers/exercise-01-tour-the-workspace/` in your Git folder of the course ([link](../answers/exercise-01-tour-the-workspace/)).
