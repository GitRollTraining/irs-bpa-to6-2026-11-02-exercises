# Exercise 4: decisions

For the trainer. Exercise 4, "Trace one column to its source", follows the demo on `case_features.interest_gap`. Modelled on Microsoft Learning's DP-750T00 lab 5, "Govern Unity Catalog Objects" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/05-govern-unity-catalog-objects.html), its column-lineage step; the steps follow Databricks, "View data lineage using Unity Catalog" (https://docs.databricks.com/aws/en/data-governance/unity-catalog/data-lineage). Shape "Follow and confirm", with one "Predict, then run" question. The check is `check.py` in the exercise folder.

## How the setup notebook built `case_features`

- `income_gap` and `interest_gap`: one `CREATE TABLE ... AS SELECT` query on `returns` and `third_party_reports` (`course_data.py`, `features_statements`). Unity Catalog records column lineage for it.
- `income_band`: joined from `income_bands`. The setup notebook's cell 3 read `returns.total_income` into Python (pandas), put each value in a band, and appended the bands to `income_bands`. The read and the write are two steps, and the write comes from Python's own values, so no query links `total_income` to `income_band`.
- `returns` and `third_party_reports` were filled by `INSERT ... VALUES` with values the notebook wrote, so no table feeds them.

## 1. The trace of `income_gap`

- **The answer.** `returns.wages` and `third_party_reports.wages_reported`. The trace stops at those two tables.
- **Reason.** `income_gap` is `r.wages - t.wages_reported`, two source columns in one query.
- **The notebook lines.** "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level" "A feature built from two return fields leaves the same two-row trace."
- **What else the check accepts.** Full names (`workspace.case_selection.returns.wages`) or short ones, any case. It ignores `return_id`, in case the graph also highlights the join column. `income_gap_stops_at` must name both tables, in 4 words or more.

## 2. The prediction, and the trace of `income_band`

- **The answer.** Prediction: no, the trace will not reach `returns.total_income`, because the band was computed in Python, outside any query. The trace stops at `income_bands`.
- **The notebook lines.** "So an empty trace does not prove a column has no source." "Records are only emitted when lineage can be inferred."
- **What else the check accepts.** A `predict` of 5 words or more, either way: the debrief compares it with what the graph showed. `income_band_stops_at` must name `income_bands`.

## The demo's column

The demo traces `interest_gap` (`returns.taxable_interest` and `third_party_reports.interest_reported`). The exercise traces `income_gap`, and predicts `income_band`, which the demo does not open.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks: the notebook's cells in order, with a stand-in for `spark` on DuckDB; the optional cell 4 read a stand-in `column_lineage` table holding the two rows the query should return. The start printed `Not yet: 4 left.`. The answer printed `Done: income_gap traces to returns.wages and third_party_reports.wages_reported, and stops at those two tables; income_band stops at income_bands.` `commands.sh` printed the same on Python 3.10 and 3.14.
- Trainer gaps, at the run-through: (1) the lineage graph highlights exactly `returns.wages` and `third_party_reports.wages_reported` for `income_gap`; (2) it stops `income_band` at `income_bands` with no column of `returns` before it (the setup notebook may show as an entity beside the table); (3) the optional cell 4 needs `SELECT` on `system.access.column_lineage`, which an account or metastore admin grants.

## Where each quote comes from

The curated file is `days/day-01/curated.md` in the Program repository, all under "Trace a column back to its source table". The day's deck is being rebuilt, so no slide number is given.

| Quote in the notebook | Line |
|---|---|
| "Unity Catalog captures lineage automatically for queries run on Databricks, down to the column level" | 487 |
| "A feature built from two return fields leaves the same two-row trace." | 504 |
| "So an empty trace does not prove a column has no source." | 520 |
| "Records are only emitted when lineage can be inferred." | 509 |
| "Use of user-defined functions (UDFs) can obscure the mapping between source and target columns." | 514 |
| "The system tables are `system.access.table_lineage` and `system.access.column_lineage`." | 499 |

## Findings of the linter inside quotes

None. Outside quotes: the Goal has 27 words (cap 25) and the Scenario has one passive verb ("is traced"). Both are the exercise block's lines in the day's activities, kept word for word; a rewording is proposed to the block's owner.
