# Exercise 5: Check one Genie answer

**Goal:** After this exercise, you can check a Genie answer against its query and your own query, and say whether it holds.

**Scenario:** On Monday you wrote your own case-selection question. You ask Genie one question from it about the clean batch. Then you check the answer as the trainer did: the query first, then your own numbers.

**AI tool:** Genie, in the trainer's Genie Agent "Week 3 returns", and no other.

**Where you work:** Genie, then the notebook `week-03/day-02/exercise-05-check-one-genie-answer/exercise.ipynb` in your Git folder of the course, in Databricks. Attach the notebook to the compute the trainer names.

**Done when:** cell 4 prints `Done:`: your verdict on Genie's answer, and the line of its query that decides it.

**Optional part:** in a new chat, ask Genie the same question with `dirty batch` in place of `clean batch`. Read its query with the same checks. In cell 3, write in `optional` which lines changed.

**What you have:**

- Your notebook of Monday's exercise 2: your question, and the list of items it needs.
- The Genie Agent "Week 3 returns", on the clean batch `course.returns.batch_clean` and the dirty batch `course.returns.batch_dirty`.
- `kept-wrong-answer.md`, beside this notebook: a wrong answer the course kept, with its query. Use it when Genie gives you no answer or no **Show code**, or when the trainer asks you to.
- `check.py`, beside this notebook. Cell 4 runs it.

**Start from:** a new chat in the Genie Agent, and this notebook as the course gives it. The trainer just checked one Genie answer this way. To start again, set the values you typed back to `""`.

### Step 1. Ask Genie one question from your Monday question

Why: a check matters most on a question you would act on. Your Monday question names the information it depends on most.

1. Open your notebook of Monday's exercise 2. In its cell 2, find the first item with the verdict `needed` that names wages, adjusted gross income, total income or total tax. Its column is `wages_amt`, `agi_amt`, `total_income` or `total_tax_amt`, in that order. If no item names one, use `wages_amt`.
2. In the Genie Agent "Week 3 returns", start a new chat.
3. Ask this question, with your column in place of `wages_amt`:

Genie:

```text
For each tax year in the clean batch, how many returns are there and what is their total wages_amt?
```

4. Select **Show code**.
5. In cell 1, paste your question into `question`.
6. Paste the short answer into `genie_answer`.
7. Paste the whole query into `genie_query`.
8. Run cell 1. It prints your question.

Genie may give you no answer or no **Show code**, or the trainer may ask you to use the kept answer. Then copy the question, answer and query of `kept-wrong-answer.md` instead.

Notebook cell 1:

```python
# 1. Your question and Genie's reply. Paste between the quote marks.
question = ""  # the question you asked, word for word
genie_answer = """"""  # Genie's short answer
genie_query = """"""  # the whole query, from Show code
print(question or "(no question yet)")
```

### Step 2. Run your own query

Why: "Run your own query for the same question and compare the two results."

Cell 2 counts returns with `count(DISTINCT return_id)`: a return that is in the table twice counts once. `COUNT(*)` counts rows, so it counts that return twice.

1. In cell 2, set `column` to your column.
2. Run cell 2. You should see one row per tax year, 2021, 2022 and 2023, each with its count of returns and the column's total.
3. Put each row beside Genie's answer: the same tax years, the same counts, the same totals? Read a number such as 47,000 as 47000: the commas only group the digits.

Notebook cell 2:

```python
# 2. Your own query: per tax year of the clean batch, the returns and the column's total.
column = "wages_amt"  # the column your question names
display(spark.sql(f"""
SELECT tax_year, count(DISTINCT return_id) AS returns, sum({column}) AS total
FROM course.returns.batch_clean
GROUP BY tax_year
ORDER BY tax_year
"""))
```

### Step 3. Read Genie's query, one check at a time

Why: "Open the query behind the answer, and read it before the number."

Read `genie_query` line by line. Fill one value of cell 3 for each check:

| Check | What to read in the query | Write in |
|---|---|---|
| "Tables: is it reading the table you meant, the prepared one or the raw batch?" Here: the clean batch, or the dirty one | the table after `FROM` | `reads` |
| "Filters: does the tax year, filing status or date range match your question?" | the condition after `WHERE`, or `none` | `filters` |
| "Joins and counts: does it count returns or rows, and could a join have duplicated them?" A join puts the rows of two tables together, and can repeat a row | `COUNT(*)` counts rows. `count(DISTINCT return_id)` counts returns | `counts` |

The dirty batch holds one return twice, as exercise 1's uniqueness test showed. It also holds a return filed again: the same return under a new `return_id`. And it holds two returns moved to tax year 2019.

### Step 4. Give your verdict, and the line that decides it

Why: "A Genie number reported without its query." That is one of the day's mistakes. The deciding line is the one line of Genie's query that makes its numbers right or wrong. It is what you show a reviewer.

Use the first row of this table that fits:

| What you found | `verdict` | `deciding_line` |
|---|---|---|
| it reads `course.returns.batch_dirty` | `does not hold` | the `FROM` line |
| a filter your question did not ask for | `does not hold` | the `WHERE` line |
| it counts rows, and a number differs from cell 2's | `does not hold` | the line with `COUNT(*)` |
| a number differs from cell 2's for another reason | `does not hold` | the line that names the column it sums |
| the table you meant, no extra filter, and every number equal to cell 2's | `holds` | the `FROM` line: it reads the table you meant |

1. In cell 3, write `verdict`.
2. Copy the deciding line from `genie_query` into `deciding_line`, as it is.
3. Run cell 3. It prints your verdict and your line.

Notebook cell 3:

```python
# 3. The checks of Genie's query, and your verdict.
reads = ""  # the table after FROM
filters = ""  # the WHERE condition, or none
counts = ""  # returns or rows: what its count counts
verdict = ""  # holds, or does not hold
deciding_line = ""  # the one line of Genie's query that decides it, copied as it is
optional = ""  # only for the optional part: which lines of the query changed
print(verdict or "(no verdict yet)", "|", deciding_line or "(no line yet)")
```

### Step 5. Check

Run cell 4. It runs Genie's query and your own query again, and compares their numbers. It prints `Done:` when these things are true:

- `question` names the column you set in cell 2. `genie_answer` and `genie_query` hold Genie's reply, and the query runs.
- `reads` is the table the query names, `filters` holds a word, and `counts` is `returns` or `rows`.
- `verdict` is `holds` when the numbers of the two queries are the same, and `does not hold` when they differ.
- `deciding_line` is a line of `genie_query`.

Otherwise it prints `Not yet:` and each thing still to do. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Genie's query and yours may both name their count returns. When is a count of rows also a count of returns, and when is it not?
2. You named one deciding line. Which of the checks would you run first next time, and why?
3. Your own query can be wrong too. What would make you trust it more than Genie's?

The answer, after you try: [`answers/exercise-05-check-one-genie-answer`](../answers/exercise-05-check-one-genie-answer/).
