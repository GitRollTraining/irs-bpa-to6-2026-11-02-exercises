# Exercise 3: Find two of your items and check two drafts

**Goal:** After this exercise, you can find a column in the catalog by searching and check an AI-drafted column comment against the column's facts.

**Scenario:** Your list from exercise 2 names information your question needs. You find two of those items in the catalog, let AI generate draft their comments, and check each draft before anyone saves it.

**AI tool:** AI generate in Catalog Explorer, and no other. It drafts a column's comment. You never save a draft.

**Where you work:** the notebook `week-03/day-01/exercise-03-find-and-check-two-drafts/exercise.ipynb` in your Git folder of the course, and Catalog Explorer. Attach the notebook to the compute whose name the trainer wrote on the board. Cell 1 is the code cell whose first line starts with `# 1.`, and so on for each cell.

**Done when:** cell 4 prints `Done:`.

**Optional part:**

1. In a new cell, run `display(spark.table("course.returns.return_header"))`.
2. Above the result, select **+**.
3. Select **Data Profile**. Which column's profile surprises you?

**What you have:**

- Your list from exercise 2.
- The return table `course.returns.return_header`: one made-up row per return, with a comment on most columns.
- `drafts.md`, beside this notebook: drafts that the course prepared in the form AI generate gives.
- `check.py`, beside this notebook. Cell 4 runs it.

**Start from:** this notebook as the course gives it. The trainer showed one search in Catalog Explorer, one draft and one check just before this exercise. To start again, set the values you typed back to `""` and `None`.

### Step 1. Search the catalog for an item of your list

Why: you know a word of the item, not its column. You search with SQL here: cell 1 finds each column of `return_header` whose name or comment holds the word.

1. In cell 1, put a word of an item on your list between the quotes of `word = "income"`. The cell starts with `income`, because total income is the line item the day's question depends on most.
2. Run cell 1. You should see a table: one row per matching column, with the table's full name, the column's name, its type and its comment.
3. No row means no column matches. Then try another word.
4. Change the word to a second item of your list.
5. Run cell 1 again.

Choose two columns to check. Take `return_header.total_income` as one of them. If no other item on your list is in `return_header`, choose a column from `drafts.md`.

Notebook cell 1:

```python
# 1. Search the catalog's columns for a word.
word = "income"  # change this to a word of an item on your list

display(spark.sql(f"""
SELECT table_catalog || '.' || table_schema || '.' || table_name AS full_name,
       column_name, data_type, comment
FROM course.information_schema.columns
WHERE table_schema = 'returns' AND table_name = 'return_header'
  AND (column_name ILIKE '%{word}%' OR comment ILIKE '%{word}%')
ORDER BY full_name, column_name
"""))
```

### Step 2. Let AI generate draft the comments, and save nothing

Why: "Comments are powered by a large language model (LLM) that takes into account object metadata, such as the table schema and column names" (Databricks documentation). It reads the names, not the values. "AI models are not always accurate and comments must be reviewed prior to saving" (Databricks documentation).

1. In Catalog Explorer, open the catalog `course`, the schema `returns`, then the table `return_header`. Select the **Columns** tab.
2. Above the column headings, select **AI generate**. A draft comment appears beside each column.
3. In cell 3's first entry, write your first column between the quotes of `"column": ""`.
4. Copy its draft, word for word, between the quotes of `"draft": ""`.
5. Do not select the check mark beside the draft: the check mark saves the draft as the column's comment, for everyone in the class. To close the drafts, reload the browser tab.
6. Do the same for your second column, in the second entry.

Use the column's draft from `drafts.md` in these cases:

- You do not see **AI generate**, or it gives you no draft.
- The draft says nothing the values could contradict, such as no sign and no "always".
- The column's comment is already the same as its draft: a classmate saved it. Do not change it. Tell the trainer.

### Step 3. Read each column's facts

Why: a check reads, in this order, the type, then the comment, then the values. "Compare the entry's type with the column's type in the catalog." "Compare the entry's description with the column's comment, where one exists." "Query the column: its empty count, its smallest and largest values, a sample of distinct values." (All three from the day's reading.)

First, predict. In cell 2, between the quotes of `predict = ""`, write: what smallest value do you expect for `total_income`, and why?

1. In cell 2, set `column` to your first column. Run cell 2. You should see four tables, in this order:
   - the type and the comment
   - the tags (an empty table when the column has none)
   - the empty count, the smallest value and the largest value
   - up to 20 distinct values: they show what kind of value the column holds
2. Copy the type, the comment and tags, and the three numbers into the first entry of cell 3. Write the comment and tags as `comment: <the comment>; tags: none`.
3. Set `column` to your second column.
4. Run cell 2 again.
5. Fill the second entry.

Notebook cell 2:

```python
# 2. One column's facts: type and comment, tags, then its values.
column = "return_header.total_income"  # table.column, from cell 1
predict = ""  # before you run this cell: the smallest total_income you expect, and why

table, name = column.split(".")
where = f"table_schema = 'returns' AND table_name = '{table}' AND column_name = '{name}'"
display(spark.sql(f"SELECT data_type, comment FROM course.information_schema.columns WHERE {where}"))
display(spark.sql(f"SELECT tag_name, tag_value FROM course.information_schema.column_tags "
                  f"WHERE schema_name = 'returns' AND table_name = '{table}' AND column_name = '{name}'"))
display(spark.sql(f"SELECT count_if({name} IS NULL) AS empty, min({name}) AS smallest, max({name}) AS largest "
                  f"FROM course.returns.{table}"))
display(spark.sql(f"SELECT DISTINCT {name} FROM course.returns.{table} LIMIT 20"))
```

### Step 4. Record each check, and its verdict

Why: "Write what you checked and what you found beside the entry, so a reader can see the check, not only the verdict" (the day's reading).

In cell 3, finish each entry. Its verdict is `keep` or `change`. This verdict table gives it:

| What cell 2 shows | Verdict | Why |
|---|---|---|
| A value the draft rules out. For example, the draft says always present, and the empty count is above 0. | `change` | "A description that says always present fails on one empty row" (the day's reading). |
| A comment that says something the draft contradicts | `change` | the comment is the catalog's record of the column |
| A type that is not the one the draft names. Most drafts name no type: then this row does not apply. | `change` | the catalog records the column's type |
| Nothing in the type, the comment, the tags or the values goes against the draft | `keep` | the check found nothing that contradicts the draft |

In `reason`, write what in the facts decides the verdict, in 4 words or more. Run cell 3. It prints each entry's column and verdict.

Notebook cell 3:

```python
# 3. Your two entries: one per column, each with its check.
entries = [
    {
        "column": "",  # table.column, such as return_header.total_income
        "draft": "",  # the draft, word for word
        "type": "",  # the type cell 2 shows
        "comment_and_tags": "",  # such as "comment: none; tags: none"
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

If you changed cell 2 or cell 3, run it again first. Then run cell 4. It prints `Done:` when these things are true:

- `predict` holds 5 words or more.
- Each entry names a different column of `return_header`, with its draft.
- Each entry's type, empty count, smallest and largest value are the ones the column has, and it records the comment and tags.
- Each entry has the verdict `keep` or `change` and a reason of 4 words or more. A draft that a value contradicts has `change`.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# Do not change this cell. The code is in the notebook.
```

### Afterwards, together

1. AI generate reads names, not values. Which words of your two drafts come only from the column's name?
2. Your two entries got the same verdict, or two different ones. What in the values decided each?
3. "The model should not be relied on for data classification tasks such as detecting columns with PII" (Databricks documentation). Which column of `return_header` would you not trust a draft to classify, and what would you read instead?

The answer: after the talk together, open `week-03/day-01/answers/exercise-03-find-and-check-two-drafts/` in your Git folder of the course ([link](../answers/exercise-03-find-and-check-two-drafts/)).
