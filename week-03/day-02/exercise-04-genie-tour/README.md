# Exercise 4: Genie tour

**Goal:** After this exercise, you can ask a Genie Agent a question and find the query behind its answer.

**Scenario:** Genie answers questions about tables in plain words. A Genie Agent is a set of tables that an author prepared for those questions. Before you check one of Genie's answers, you find what it gives you: a short answer, a result table, and the query it ran.

**AI tool:** Genie, in the trainer's Genie Agent "Week 3 returns", and no other.

**Where you work:** Genie, then the notebook `week-03/day-02/exercise-04-genie-tour/exercise.ipynb` in your Git folder of the course, in Databricks. Attach the notebook to the compute the trainer names.

**Done when:** cell 2 prints `Done:`: Genie's answer, its result table and its query, and what a second ask gave.

**Optional part:** none.

**What you have:**

- The Genie Agent "Week 3 returns": the clean batch `course.returns.batch_clean` and the dirty batch `course.returns.batch_dirty`.
- `genie-reply.md`, beside this notebook: a reply the course wrote in the form Genie shows. Use it when Genie gives you no answer or no **Show code**.
- `check.py`, beside this notebook. Cell 2 runs it.

**Start from:** a new chat in the Genie Agent, and this notebook as the course gives it. The trainer just asked Genie a question and opened its query. To start again, set the values you typed back to `""`.

### Step 1. Open the Genie Agent and start a chat

Why: Genie is new today. The trainer shows each move on screen first. Wait until you see it.

1. In the left bar of Databricks, select **Genie Agents**. If you do not see it, open the link to the Genie Agent that the trainer posted.
2. Select **Week 3 returns**. It holds the clean batch and the dirty batch.
3. "Click the New chat button to start a new conversation." You should see an empty chat with a box to type in.

### Step 2. Ask the given question

Why: Genie answers "natural-language questions" by writing a query and running it. Start with a question whose answer you can count.

1. Type this question in the chat box:

Genie:

```text
How many returns are in the clean batch for each filing status?
```

2. Press Enter. You should see a short answer, then a result table.
3. In cell 1, put the cursor between the quote marks of `answer`, and paste the short answer.
4. In `result_table`, type each row of the result table as `status: count`, with a comma between rows.

### Step 3. Find the query behind the answer

Why: "Click Show code to inspect the query Genie generated." The query says what Genie read and counted. The answer does not.

**Show code** is the button that opens the query behind the answer: the trainer called it the query.

1. Under the answer, select **Show code**. You should see a SQL query.
2. Copy the whole query into `query` in cell 1, from its first word to its last.
3. In `table_read`, write the table the query reads: the name after `FROM`.

If Genie gives you no answer, or no **Show code**, use `genie-reply.md` beside this notebook, and tell the trainer.

### Step 4. Ask again, and compare

Why: "This means that you might receive different outputs when submitting the same prompt multiple times." Genie uses a language model to write its query, and the model can write a different query for the same words.

1. Start a new chat.
2. Ask the same question, word for word.
3. Compare the new result table and query with what cell 1 holds.
4. In `second`, write `same` if the table read and every number are the same. Other words in the short answer still count as `same`. Write `changed` if a number or the table after `FROM` differs.
5. If you wrote `changed`, write in `what_changed` what changed.
6. Run cell 1. It prints your `table_read` and your `second`. A value that prints `(none yet)` or `(not asked again yet)` is still empty.

Notebook cell 1:

```python
# 1. What Genie gave you. Paste between the three opening and the three closing quote marks.
answer = """"""  # Genie's short answer
result_table = """"""  # each row of its result table, as status: count, status: count
query = """"""  # the whole query, from Show code
table_read = ""  # the table the query reads: the name after FROM, as the query writes it
second = ""  # after you ask again in a new chat: same, or changed
what_changed = ""  # only if changed: the answer, the table or the query, and how
print("table read:", table_read or "(none yet)", "| second ask:", second or "(not asked again yet)")
```

### Step 5. Check

Run cell 2. It runs the query you copied, to see that it is the whole query. It prints `Done:` when these things are true:

- `answer` and `result_table` hold what Genie gave you.
- `query` starts with `SELECT` or `WITH`, runs, and names a table of `course.returns`.
- `table_read` is a table the query names.
- `second` is `same` or `changed`. If changed, `what_changed` says what.

Otherwise it prints `Not yet:` and each thing still to do. It does not judge Genie's answer: exercise 5 does. You do not need to read its code.

Notebook cell 2:

```python
# 2. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Genie read one of two batches. What in your question decided which one?
2. Your second ask came back the same, or changed. If it can change, what does that mean for a number you report?
3. Genie reads the column comments you checked on Monday. Where in this query could a wrong comment show up?

The answer, after you try: [`answers/exercise-04-genie-tour`](../answers/exercise-04-genie-tour/).
