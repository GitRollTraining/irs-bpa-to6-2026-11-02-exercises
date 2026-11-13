# Exercise 3: decisions

The answer is `exercise.ipynb` beside this file, with the schema `course.learner_00`.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 3 | `predict_mean = 48000` | F-30037's wages: 2020 46,000, 2021 48,000, 2022 50,000, 2023 57,500 (`day-03-course-data.py`). The mean of the years before 2023 is 144,000 / 3. |
| 3 | `predict_change = 0.15` | (57,500 - 50,000) / 50,000. |
| 4 | `history_column = "wages_amt"` | The history is the mean of earlier wages. |
| 5 | `prior = F.lag("wages_amt").over(by_year)` | The previous row's wages, in tax-year order. Null for a first return, so `F.when(prior > 0, ...)` gives null. |
| 7 | `("wages_change_pct", "return_table", "filer_key, tax_year, wages_amt", "(wages_amt - wages of the row before) / wages of the row before, LAG by filer_key in tax_year order, null for a first return")` | The record row. |

What else the check accepts: a prediction within 1 dollar of 48,000 and within 0.002 of 0.15; any record wording with no empty field. The check computes each filer's earlier mean and the change from the year before again by a self-join, not by a window, so a frame that reaches the current year fails it.

No filer has a gap year in the course's data: each filer files every year from their first to 2023. So `LAG` and "the year before" agree. The third debrief question asks about a gap; the curated file asks the learner to decide.

The optional anomaly score (cell 9) is the early finishers' extra (the program owner's ruling of 2026-11-13, "Extra for early finishers"). It writes no table and the check does not read it. It uses the filer's own earlier years, not a group mean, so it needs no training-years statistic.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "The frame must stop at the year before the current one, so the summary uses only earlier returns" | `days/day-03/curated.md` § Summarise earlier returns into history, How; deck slides 36 and 38 |
| `F.lag` "returns the value from the previous row in the window, here the previous tax year's return." | § Compute year-over-year changes, How; deck slides 40 and 41 |
| "A filer's first return has no prior year, so the change is null, not zero." | the same section; deck slide 40 ("A first return: null, not zero") |
| One filer recomputed by hand | § Where today goes wrong, fourth bullet; deck slide 39 ("Caught by one filer recomputed by hand") |

The deck as built has no exercise slide for history and change alone (slide 52 merges them with ratios and the anomaly score).

## Where it ran

- Not run in Databricks: a trainer gap (`week-03/setup/day-03-setup.md` § Not yet checked in Databricks, items 4 and 5).
- Run on a laptop, 2026-11-13: the plain-Python stand-in computed the earlier mean and the change for every filer and read 48,000 and 0.15 for `F-30037-2023`, null for `F-30074-2023`. `commands.sh` prints `Not yet: 6 left.` on the start and `Done:` on the answer, on Python 3.10 and 3. A wrong record (a frame that reaches the current year, 30 rows wrong, prediction 50,375) prints `Not yet: 2 left.`
- The check's SQL parsed with sqlglot 30.31, dialect `databricks`.

## Pages behind the steps (opened 2026-11-13)

| Step | Page | Sentence |
|---|---|---|
| window function | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-window-functions | "Functions that operate on a group of rows, referred to as a window, and calculate a return value for each row based on the group of rows." |
| `LAG` | https://docs.databricks.com/aws/en/sql/language-manual/functions/lag | "Returns the value of `expr` from a preceding row within the partition." "The `default` default is `NULL`." |

## Modelled on

None found. The round's search (`exercise-plan/wednesday/searched.md`) found no official lab or course exercise that builds history features with a window over earlier rows. The steps rest on the two pages above. Shape taken: predict a value by hand, then compute it and compare.
