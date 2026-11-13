# Set up Tuesday in Databricks (week 3, day 2)

For the trainer. Tuesday's five exercises run in the class's Databricks workspace. Do these steps before class, in order, after Monday's setup. The course made up the batches: no row is a real taxpayer, and each identification number starts with 000, which is never issued. Tuesday's setup makes three tables in `course.returns`, and you make one Genie Agent by hand.

| Table | Rows | Used by |
|---|---|---|
| `course.returns.batch_clean` | 30 returns, tax years 2021, 2022 and 2023, no fault: the same returns as Wednesday's files (same `return_id`, tax year and amounts) | exercises 1, 4, 5 |
| `course.returns.batch_dirty` | the same returns, with a fault of each of the five kinds put in, and one fault no column summary shows (32 rows) | exercises 1, 2, 5 |
| `course.returns.batch_governed` | a copy of `batch_dirty`, with a column mask on `tin` and a row filter by tax year | exercise 3 |

The faults of `batch_dirty`, by `return_id`: completeness, `agi_amt` empty on F-30148-2022 and F-30296-2021; validity, `wages_amt` of -1 on F-30185-2023; uniqueness, F-30259-2022 there twice; consistency, `wages_amt` larger than `total_income` on F-30333-2021; freshness, tax year 2019 on F-30444-2021 and F-30518-2021; and the fault no column summary shows: F-30111-2022's return again under F-30629-2022, same `tin`, same tax year.

## Before Tuesday

1. **Get the files.** In your Git folder of the course, pull, so that `week-03/setup/day-02-setup.ipynb` is there.
2. **Make the reviewer group.** In the account console, make an account group that holds you and no learner, such as `week3_reviewers`. It sees every row and every identification number of `batch_governed`. The learners' group sees tax year 2023 only, and `tin` as `***-**-****`.
3. **Run the setup notebook once.** Open `week-03/setup/day-02-setup.ipynb` and attach it to the compute. In cell 1, set `CLASS_GROUP` as on Monday, and `REVIEWER_GROUP` to the group of step 2. You need `CREATE TABLE` and `CREATE FUNCTION` on `course.returns`, and you own the tables you make. Run cells 1 to 5. Cell 4 should print:
   - `batch_clean 30 rows` and `batch_dirty 32 rows`
   - `batch_governed, as you: 2019: 2, 2021: 8, 2022: 12, 2023: 10`
   - a first `tin` in full, such as `000-11-4037`
4. **If cell 3 prints `FALLBACK`.** The workspace or the compute refused the row filter or the column mask. `batch_governed` is then a plain copy, and every learner sees every row. Tell the class at exercise 3 that they take its written fallback: the step 4 table's second row. Databricks: "Databricks Runtime versions below 12.2 LTS do not support row filters or column masks."; on a dedicated (single user) compute, "You cannot access a table with row filters or column masks from a dedicated access compute resource" on Databricks Runtime 15.3 or below. Use standard access mode compute for the class.
5. **Make the Genie Agent "Week 3 returns".** Genie needs a pro or serverless SQL warehouse, and partner-powered AI features turned on for the account.
   1. Select **Genie Agents** in the left bar, then **New** in the upper-right corner.
   2. Choose `course.returns.batch_clean` and `course.returns.batch_dirty`, then **Create**. Do not add `batch_governed`.
   3. Genie Code may suggest descriptions and example queries. Accept none: exercise 5 asks learners to find a query that reads the wrong batch.
   4. Select **Configure**, then **Settings**. Set the **Title** to `Week 3 returns`, and the **Default warehouse** to the class's SQL warehouse.
   5. Select **Share**, add the learners' group with **CAN RUN**, then **Add**. Each learner already holds `SELECT` on both batches (step 3, cell 5, and Monday's grant on the schema).
6. **Keep the wrong answer for exercise 5.** In the Genie Agent, as yourself, ask: `For each tax year in the clean batch, how many returns are there and what is their total wages_amt?` Select **Show code**. If the query reads `batch_dirty`, or counts rows of a batch with a row twice, keep that chat to show in class. If it does not, the course's kept wrong answer stands: `week-03/day-02/exercise-05-check-one-genie-answer/kept-wrong-answer.md`. Show it on screen when you send learners to it.
7. **Ask exercise 4's question once.** Ask `How many returns are in the clean batch for each filing status?` The answer should be 8 returns of filing status 1, 7 of 2, 5 of 3 and 10 of 4. Select **Show code** and see the query.

## In class

- Demo before exercise 1: one test, `wages_amt >= 0`, action fail, in a copy of exercise 1's cell 2, on `batch_clean` (passes), then `batch_dirty` (fails: 1 row, F-30185-2023). Read the failing row aloud.
- Worked example before exercise 2: fill the rows for `tin` and `filing_status` (the notebook has them filled), and run cell 3 with only `tin` set to transform.
- Demo before exercise 3: as a reviewer, run exercise 3's cell 2. You see 2019: 2, 2021: 8, 2022: 12, 2023: 10, and every `tin`. Say that the learners' group gets a different result, and do not show it.
- Demo before exercise 4: ask Genie a count question that is not exercise 4's, such as the number of returns per tax year in the clean batch; select **Show code**. Then ask about a column the batches do not hold, such as the filer's age, and read the reply aloud.
- Demo before exercise 5: check one answer with the four checks: the table, the filters, returns or rows, your own query beside it.
- Exercise 5 is the on-your-own work when the day runs over: nothing on Wednesday starts from it.

## After class

Run cells 2 to 5 of the setup notebook again only if a table changed. Nothing in the exercises writes to a table.

## Not yet checked in Databricks

The course team ran the exercises' checks on a computer without Databricks, on the same made-up rows in SQLite, and parsed every SQL statement with a Databricks SQL parser. Each answer's `decisions.md` says how, under "Where it ran". Check each item at your run-through, and tell the course team what differs. Each item gives our proposed answer and the page it comes from.

1. Exercise 1: `run_test` in cell 1 runs a rule with a window, `count(*) OVER (PARTITION BY return_id) = 1`, inside `withColumn(..., F.expr(...))`, and filters `NOT _ok`. Proposed: it runs; Spark allows a window expression in a select. Page: https://docs.databricks.com/aws/en/ldp/expectations ("Expectations use standard SQL Boolean statements to specify constraints.").
2. Exercise 1: each check cell finds its `check.py` beside the notebook, as Monday's do.
3. Exercise 2: cell 3 runs on the class compute: `secrets.token_hex`, `F.sha2`, `F.concat`, `F.substring`. Proposed: it runs; these are standard Spark functions.
4. Exercise 3: a learner's query of `batch_governed` returns 2023: 10 and `tin` as `***-**-****` on the class compute. Proposed: yes on standard access mode, Databricks Runtime 12.2 LTS or above. Page: https://docs.databricks.com/aws/en/data-governance/unity-catalog/filters-and-masks/ ("Rows where the function returns `FALSE` are excluded from query results.").
5. Exercise 3: `SHOW GRANTS ON TABLE` runs for a learner, or is refused and cell 3 shows the learner's own grants. Proposed: refused, since it needs "the owner of the object" or "the `READ METADATA` or `MANAGE` permission on the object"; the fallback query shows the learner's grants. Pages: https://docs.databricks.com/aws/en/sql/language-manual/security-show-grant and https://docs.databricks.com/aws/en/sql/language-manual/information-schema/table_privileges ("the `INFORMATION_SCHEMA` only shows users their own grants on the object.").
6. Exercise 4: a learner with **CAN RUN** opens "Week 3 returns", starts a new chat, and sees **Show code** under an answer. Page: https://docs.databricks.com/aws/en/genie/talk-to-genie ("Click Show code to inspect the query Genie generated.").
7. Exercise 4: the check cell runs the pasted query on the class compute; Genie's query may name tables with backticks.
8. Exercise 5: what Genie answers to step 6's question: does its query read `batch_clean`, and count rows or returns? Proposed: it reads `batch_clean`, so most learners' answers hold, and the kept wrong answer gives every learner one that does not.
