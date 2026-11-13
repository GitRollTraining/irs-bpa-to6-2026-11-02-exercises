# Exercise 2: decisions

The answer is `exercise.ipynb` beside this file, with the schema `course.learner_00`.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 3 | `predict_rows = "more"` | Joining the W-2 rows before summing gives one row for each W-2. Eleven returns have two W-2s, so the join gives 63 rows against 52 returns. |
| 3 | `w2_per_return = w2s.groupBy("return_id").agg(F.sum("wages_amt").alias("w2_wages"))`, then `joined = features.join(w2_per_return, "return_id", "left")` | Sum first, then join: one row for each return. `left` keeps the returns with no W-2 (`F-30111-2021`), whose confirmed wages count as 0. |
| 5 | `("w2_wage_share", "w2s, return_table", "w2s.wages_amt, return_table.wages_amt", "sum of w2s.wages_amt for each return_id, joined on return_id, over wages_amt where wages_amt > 0, else null")` | The record names the table, the columns and the code of each feature. |

What else the check accepts: any record wording with no empty field whose table field names `w2s`; any code that gives the same values (the check computes the share again from `w2s` and `return_table`). The debrief starts from the share of 0 for a return with wages and no W-2, against null for a return with no wages.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "Write the rule down: a null, not an error and not an infinity." | `days/day-03/curated.md` § Build ratios within one return, How; deck slide 29 |
| "Joining the W-2 table to returns before summing gives one row per W-2, not per return." | `days/day-03/curated.md` § Where today goes wrong, third bullet; deck slide 30 |
| "The sum happens before the join, so the result stays one row per return." | § Build ratios within one return, last paragraph; deck slide 30 |
| "For every feature, record three things beside it: the table it reads, the columns it reads, and the code that computes it." | § Compute features, each traced to its source table, Trace each one; deck slide 26 |

The exercise has no slide of its own in the deck as built: the deck's exercise 2 (slide 52) merges ratios, history, change and the anomaly score. See the round's `deck-disagreements.md`.

## Where it ran

- Not run in Databricks: a trainer gap (`week-03/setup/day-03-setup.md` § Not yet checked in Databricks, item 4).
- Run on a laptop, 2026-11-13: the plain-Python stand-in computed both ratios from the stand-in tables (sum, then join), counted 63 rows for the join that comes first, and found `tax_to_agi` and `w2_wage_share` null on `F-30111-2021`. `commands.sh` prints `Not yet: 5 left.` on the start and `Done:` on the answer, on Python 3.10 and 3. A wrong record (63 rows, prediction "same") prints `Not yet: 2 left.`
- The check's SQL parsed with sqlglot 30.31, dialect `databricks`.

## Pages behind the steps (opened 2026-11-13)

| Step | Page | Sentence |
|---|---|---|
| `saveAsTable`, `overwrite` | https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframewriter/saveAsTable | "Saves the content of the `DataFrame` as the specified table." |

`groupBy`, `agg`, `F.sum`, `F.when` and `join` are shown in the day's deck and curated file; no other page is cited.

## Modelled on

Databricks Academy, Data Preparation for Machine Learning, its "Lab: Build a Feature Engineering Pipeline", https://www.databricks.com/training/catalog/data-preparation-for-machine-learning-2381: "Each module combines lectures with hands-on demos and a lab that run on serverless compute." Only the outline is public. Also DP-750 Lab 08's exercise "Join listings with agents and sales data", https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/08-cleanse-transform-load-data-into-unity-catalog.html (its step text is not on the page). Shape taken: a demo, then a lab that adds a feature by a join.
