# Exercise 3: Find two of your items and check two drafts

**Goal:** After this exercise, you can find a column in the catalog by searching and check an AI-drafted column comment against the column's facts.

**Scenario:** Your list from exercise 2 names information the model needs. You find two of those items in the catalog, let AI generate draft their comments, and check each draft before anyone saves it.

**AI tool:** AI generate in Catalog Explorer, and no other. It drafts a column's comment. You never save a draft.

**Where you work:** the notebook `week-03/day-01/exercise-03-find-and-check-two-drafts/exercise.ipynb` in your Git folder of the course, and Catalog Explorer. Attach the notebook to the compute the trainer names.

**Done when:** cell 4 prints `Done:`: two entries, each with its check.

**Optional part:** in a new cell, run `display(spark.table(f"{CATALOG}.case_selection.returns"))`, then select **+** above the result, then **Data Profile**. Which column's profile surprises you?

**What you have:**

- Your list from exercise 2.
- The tables of the schema `case_selection` in the course catalog. The course made up every row.
- `drafts.md`, beside this notebook: drafts that the course prepared in the form AI generate gives. Use it when you do not see **AI generate**, or when AI generate gives you no draft.
- `check.py`, beside this notebook. Cell 4 runs it.

**Start from:** this notebook as the course gives it. The trainer showed one search, one draft and one check just before this exercise. To start again, set the values you typed back to `""` and `None`.

### Step 1. Search the catalog for an item of your list

Why: you know a word of the item, not its table. A search of the catalog's columns finds every column whose name or comment holds the word. "A table missing from your results may exist and be one you lack permission to see."

1. In cell 1, check `CATALOG`. Put a word of an item on your list between the quotes of `word = "income"`. The cell starts with `income`: "the first entry to check is the line item the question depends on most: the income the return reports."
2. Run cell 1. You should see a table: one row per column that matches, with its table's full name, the column's name, its type and its comment.
3. Change the word to a second item of your list, and run cell 1 again.

Choose two columns to check. Take `returns.total_income` as one of them. Write each as table and column with a dot between, such as `returns.total_income`.

Notebook cell 1:

```python
# 1. Search the catalog's columns for a word.
CATALOG = "workspace"  # the course catalog: the trainer tells you if it is different
word = "income"  # change this to a word of an item on your list

display(spark.sql(f"""
SELECT table_catalog || '.' || table_schema || '.' || table_name AS full_name,
       column_name, data_type, comment
FROM {CATALOG}.information_schema.columns
WHERE table_schema = 'case_selection'
  AND (column_name ILIKE '%{word}%' OR comment ILIKE '%{word}%')
ORDER BY full_name, column_name
"""))
```

### Step 2. Let AI generate draft the comments, and save nothing

Why: "Comments are powered by a large language model (LLM) that takes into account object metadata, such as the table schema and column names." It reads the names, not the values. "AI models are not always accurate and comments must be reviewed prior to saving."

1. In Catalog Explorer, open the table of your first column. Select the **Columns** tab.
2. Above the column headings, select **AI generate**. A draft comment appears beside each column.
3. Copy the draft of your column into cell 3: between the quotes of `"draft": ""`, in the first entry.
4. Close the draft. Do not select the check mark beside it: the check mark saves the draft as the column's comment, for everyone in the class.
5. Do the same for your second column, into the second entry.

If you do not see **AI generate**, or it gives you no draft, copy the column's draft from `drafts.md`.

### Step 3. Read each column's facts

Why: a check reads what the catalog and the values say, in this order. "Compare the entry's type with the column's type in the catalog." "Compare the entry's description with the column's comment, where one exists." "Query the column: its empty count, its smallest and largest values, a sample of distinct values."

First, predict. In cell 2, between the quotes of `predict = ""`, write: what smallest value do you expect for `total_income`, and why?

1. In cell 2, set `column` to your first column. Run cell 2. You should see four tables, in this order:
   - the type and the comment
   - the tags (an empty table when the column has none)
   - the empty count, the smallest value and the largest value
   - up to 20 distinct values
2. Copy the type, the comment and tags, and the three numbers into the first entry of cell 3.
3. Set `column` to your second column, run cell 2 again, and fill the second entry.

Notebook cell 2:

```python
# 2. One column's facts: type and comment, tags, then its values.
column = "returns.total_income"  # table.column, from cell 1
predict = ""  # before you run this cell: the smallest total_income you expect, and why

table, name = column.split(".")
where = f"table_schema = 'case_selection' AND table_name = '{table}' AND column_name = '{name}'"
display(spark.sql(f"SELECT data_type, comment FROM {CATALOG}.information_schema.columns WHERE {where}"))
display(spark.sql(f"SELECT tag_name, tag_value FROM {CATALOG}.information_schema.column_tags "
                  f"WHERE schema_name = 'case_selection' AND table_name = '{table}' AND column_name = '{name}'"))
display(spark.sql(f"SELECT count_if({name} IS NULL) AS empty, min({name}) AS smallest, max({name}) AS largest "
                  f"FROM {CATALOG}.case_selection.{table}"))
display(spark.sql(f"SELECT DISTINCT {name} FROM {CATALOG}.case_selection.{table} LIMIT 20"))
```

### Step 4. Record each check, and its verdict

Why: "Write what you checked and what you found beside the entry, so a reader can see the check, not only the verdict."

In cell 3, finish each entry. Its verdict is `keep` or `change`. This table gives the verdict:

| What cell 2 shows | Verdict | Why |
|---|---|---|
| A value the draft rules out. For example, the draft says always positive, and the smallest value is below 0. Or it says always present, and the empty count is above 0. | `change` | "A description that says always present fails on one empty row." For income: "either the entry is wrong or losses are recorded in the same column." |
| A type that is not the one the draft names | `change` | "Compare the entry's type with the column's type in the catalog." |
| Nothing in the type, the comment, the tags or the values goes against the draft | `keep` | the check found nothing that contradicts the draft |

In `reason`, write what in the facts decides the verdict, in 4 words or more. Run cell 3. It prints each entry's column and verdict.

Notebook cell 3:

```python
# 3. Your two entries: one per column, each with its check.
entries = [
    {
        "column": "",  # table.column, such as returns.total_income
        "draft": "",  # the draft, word for word
        "type": "",  # the type cell 2 shows
        "comment_and_tags": "",  # the comment and tags cell 2 shows, or "none"
        "empty": None, "smallest": None, "largest": None,  # the three numbers cell 2 shows
        "verdict": "",  # keep, or change
        "reason": "",  # what in the facts decides the verdict
    },
    {
        "column": "",
        "draft": "",
        "type": "",
        "comment_and_tags": "",
        "empty": None, "smallest": None, "largest": None,
        "verdict": "",
        "reason": "",
    },
]
for entry in entries:
    print(entry["column"] or "(no column yet)", "->", entry["verdict"] or "(no verdict yet)")
```

### Step 5. Check

Run cell 4. It reads each column's type and values again. It prints `Done:` when these things are true:

- `predict` holds 5 words or more.
- Each entry names a different column of `case_selection`, with its draft.
- Each entry's type, empty count, smallest and largest value are the ones the column has, and it records the comment and tags.
- Each entry has the verdict `keep` or `change` and a reason of 4 words or more. A draft that a value contradicts has `change`.

Otherwise it prints `Not yet:` and each thing still to do. It never judges the draft's wording. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. AI generate reads names, not values. Which words of your two drafts come only from the column's name?
2. Your two entries got the same verdict, or two different ones. What in the values decided each?
3. "The model should not be relied on for data classification tasks such as detecting columns with PII." Which column of `returns` would you not trust a draft to classify, and what would you read instead?

The answer, after you try: [`answers/exercise-03-find-and-check-two-drafts`](../answers/exercise-03-find-and-check-two-drafts/).
