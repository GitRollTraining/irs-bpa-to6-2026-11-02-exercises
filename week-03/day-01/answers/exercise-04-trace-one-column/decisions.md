# Exercise 4: decisions

For the trainer. Exercise 4, "Trace one column to its source", follows the demo on `return_summary.adjustments_amt`. Modelled on Microsoft Learning's DP-750T00 lab 5, "Govern Unity Catalog Objects" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/05-govern-unity-catalog-objects.html), its column-lineage step; the steps follow Databricks, "View data lineage using Unity Catalog" (https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage). Shape "Follow and confirm", with one "Predict, then run" question. The check is `check.py` in the exercise folder.

## How the setup notebook built `course.returns.return_summary`

One `CREATE TABLE ... AS SELECT` query on `course.returns.return_header` (`week-03/setup/day-01-course-data.py`, `summary_statements`):

- `non_wage_income` = `total_income - wages_amt`: two source columns, which Unity Catalog records.
- `adjustments_amt` = `total_income - agi_amt`: the demo's column, the same shape.
- `income_band` = `income_band(total_income)`, a Python function the setup notebook registers in cell 3 before the query. Databricks' lineage page: "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns." Whether the graph shows `total_income` for it is not known until the run-through.
- `return_header` was filled by `INSERT ... VALUES` with values the notebook wrote, so no table feeds it.

## 1. The trace of `non_wage_income`

- **The answer.** `return_header.total_income` and `return_header.wages_amt`. The trace stops at `return_header`.
- **Reason.** `non_wage_income` is `total_income - wages_amt`, two source columns in one query.
- **The notebook line.** "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level"
- **What else the check accepts.** Full names (`course.returns.return_header.wages_amt`) or short ones, any case. It ignores `return_id`. `non_wage_income_stops_at` must name `return_header`, in 4 words or more; the kept answer adds what the graph shows to its left: no table.

## 2. The prediction, and the trace of `income_band`

- **The answer.** Prediction: no, or not for sure, since a Python function can hide the link. The trace: what the graph shows, recorded beside the prediction.
- **The notebook line.** "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns." The step says the rest in its own words: an empty trace does not prove a column has no source.
- **What else the check accepts.** A `predict` of 5 words or more and an `income_band_trace` of 4 words or more, either way: the talk after the exercise compares them. The check cannot know what the graph shows, so it does not judge it.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks: the notebook's cells in order, with a stand-in for `spark` on DuckDB (the Python function registered as a DuckDB function); the optional cell 4 read a stand-in `column_lineage` table holding the two rows the query should return. The start printed `Not yet: 4 left.`. The answer printed `Done: non_wage_income traces to return_header.total_income and return_header.wages_amt, and stops at return_header; your income_band trace is recorded beside your prediction.` `commands.sh` printed the same on Python 3.10 and 3.14.
- Trainer gaps, at the run-through: (1) the lineage graph highlights exactly `total_income` and `wages_amt` for `non_wage_income`; (2) what it shows for `income_band`, written into this file and the answer notebook; (3) the optional cell 4 needs `SELECT` on `system.access.column_lineage`, which an account or metastore admin grants.

## Where each quote comes from

The curated file is `days/day-01/curated.md` in the Program repository, all under "Trace a column back to its source table". The day's deck is being rebuilt, so no slide number is given.

| Quote in the notebook | Line |
|---|---|
| "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level" | 487 |
| "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns." | 514 |

## Findings of the linter inside quotes

None. Outside quotes: the Scenario has one passive verb ("is traced"), the exercise block's line in the day's activities, kept word for word.
