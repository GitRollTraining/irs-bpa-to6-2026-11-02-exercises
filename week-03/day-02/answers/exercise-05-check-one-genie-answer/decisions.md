# Exercise 5: decisions

For the trainer. Exercise 5, "Check one Genie answer", follows the demo where the trainer checks one answer by its query and an own query. Modelled on DataCamp's "Introduction to Databricks Genie" (https://www.datacamp.com/courses/introduction-to-databricks-genie; 1,869 enrolments in the page's data, opened 2026-11-13), its chapter 1 exercise "Reading the generated SQL". Shape: "Check an AI tool's output". The check is `check.py` in the exercise folder.

## 1. The question

- **The answer (kept).** "For each tax year in the clean batch, how many returns are there and what is their total wages_amt?" Monday's kept question depends most on income; `wages_amt` is the first `needed` item of Monday's kept list that names an amount, the rule step 1 gives.
- **What else the check accepts.** Any question of 6 words or more that names the column set in cell 2.

## 2. Genie's reply (the kept wrong answer)

- **The answer.** From `kept-wrong-answer.md`: the query reads `course.returns.batch_dirty`, has no filter, and counts rows with `COUNT(*)`. Its numbers: 2019: 2 rows, 91,470; 2021: 8, 552,830; 2022: 12, 821,860; 2023: 10, 666,679.
- **Reason it is wrong.** The dirty batch holds F-30259-2022 twice, F-30111-2022 again as F-30629-2022, two returns moved to 2019, and wages of -1 and of more than total income on two rows (`week-03/setup/day-02-course-data.py`, `FAULTS`).
- **Fallback.** Genie's reply varies, so `kept-wrong-answer.md` gives every learner one wrong answer to check; its first lines say Genie did not write it. Whether the trainer's own Genie gives such an answer is item 8 of `week-03/setup/day-02-setup.md`, Not yet checked.

## 3. The own query, and the checks

- **The answer.** Cell 2 with `wages_amt`: 2021: 10 returns, 633,480; 2022: 10, 681,970; 2023: 10, 700,490. `reads`: `course.returns.batch_dirty`; `filters`: none; `counts`: rows.
- **The notebook lines.** "Open the query behind the answer, and read it before the number." The four checks, word for word, lines 416 to 419. "Run your own query for the same question and compare the two results."
- **What else the check accepts.** `reads` must be a name in Genie's query; `filters` any word; `counts` `returns` or `rows` (it does not judge which).

## 4. The verdict and the deciding line

- **The answer.** `does not hold`; deciding line `FROM course.returns.batch_dirty`.
- **Reason.** The question asks about the clean batch; the query reads the dirty one, so every count and total differs. `COUNT(*)` is a second fault, as the dirty batch holds a row twice.
- **What else the check accepts.** The check runs both queries and compares every number in the two results: equal sets mean `holds`, else `does not hold`. The deciding line must be a line of Genie's query of 2 words or more; it accepts the `COUNT(*)` line too. Step 4's table is ranked: the first row that fits is the `FROM` line.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks or Genie: `check.py` ran both queries on the setup's rows in SQLite. Start: `Not yet: 8 left.` Answer: `Done: Genie's answer does not hold; the deciding line: FROM course.returns.batch_dirty`. Both queries were parsed by sqlglot 30.31.0, dialect `databricks`.
- Trainer gap, at the run-through (`week-03/setup/day-02-setup.md`, Not yet checked, item 8): what Genie answers to the kept question in the class's agent.

## Where each quote comes from

`days/day-02/curated.md` in the Program repository:

| Quote | Heading, line |
|---|---|
| "Open the query behind the answer, and read it before the number." | Check a Genie answer against its query, line 414 |
| "Tables: ...", "Filters: ...", "Joins and counts: ...", "Run your own query ..." | same section, lines 416 to 419; the last also deck slide 69 |
| "A Genie number reported without its query." | Where today's work goes wrong, line 442 (bold in the curated file); deck slide 74 |

The deck's Genie exercise is slide 73, which still names one exercise of two questions.
