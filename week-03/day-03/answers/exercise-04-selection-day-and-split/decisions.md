# Exercise 4: decisions

The answer is `exercise.ipynb` beside this file, with the schema `course.learner_00`.

## Each answer, and why

| Feature | Known on the selection day | Why |
|---|---|---|
| `tax_to_agi` | yes | both amounts are on the filed return |
| `w2_wage_share` | yes | the W-2s and the wages are filed with the return |
| `mean_prior_wages` | yes | it reads earlier years only, the frame ends at -1 |
| `wages_change_pct` | yes | it reads last year's return, which is on file |
| `filing_status`, `wages_amt`, `total_income`, `agi_amt`, `total_tax_amt` | yes | each is on the filed return |
| `tax_added_by_exam` | no | the examination writes it after selection |

Cell 4 then drops `tax_added_by_exam`, and writes `train` (2020 and 2021: 21 returns, 3 tax-change cases), `valid` (2022: 15, 3) and `test` (2023: 16, 5). The label `exam_changed_tax` stays in each set. Last, it writes `features` again from the three sets, so `features` loses `tax_added_by_exam` too (the lead's instruction of 2026-11-13: Thursday's exercise 3 asks whether the column is gone from `features`, `train`, `valid` and `test`). It reads the three written sets, not `features`, so no cell overwrites a table it is reading. Test 5 also reads `features`.

What else the check accepts: any reason of three words or more. The marks are fixed: only `tax_added_by_exam` is no. The debrief starts from `valid`'s 3 tax-change cases.

The five tests are given (cell 5): the new thing is the learner's mark on each feature. Test 4 ("any mean or scale ... computed on the training set only") is checked by computing the history means again from the training rows alone: a split by year leaves every training row's earlier years inside the training set, so the values must not change. No required feature uses a group mean. The anomaly score of exercise 3 is an extra and writes no table.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "every column a model could read needs your mark" (our words) | `days/day-03/curated.md` § Remove features the selection day cannot know, Who decides: "No script can tell you which columns are legitimate." |
| "For each feature in the documented table, add one line: known on the selection day, yes or no, and why. Drop every no." | the same paragraph; deck slide 59 |
| `tax_added_by_exam`: "the examination writes it after selection" (our words) | the same section, the table's first row: "anything else written after selection, such as the tax amount an examination added"; deck slides 58 and 59 |
| "The examination label itself is the answer column: it stays as the label, and nothing computed from it becomes a feature." | the same section, Who decides |
| "the model learns from earlier years and scores later ones" (our words) | § Split the data so the test cannot see the answer, Why split by time: "The model will be used on next year's returns after being trained on this year's and earlier ones."; deck slide 60 |
| "each test fails a bad split" (our words) | the same section, The leakage check: "each is a test that fails a bad split"; deck slide 62 |
| cell 6, the tax-change cases in each set (no quote in the cell) | § Expect few selected cases among many returns, What it means for today: "count the tax-change cases in each of the three sets and record the counts"; deck slide 65 |

The exercise is deck slide 70 (as built, "Exercise 3").
## Where it ran

- Not run in Databricks: a trainer gap (`week-03/setup/day-03-setup.md` § Not yet checked in Databricks, items 4 and 5).
- Run on a laptop, 2026-11-13: the plain-Python stand-in built the record, dropped the no, split by year, ran the five tests (each passed) and counted the cases per set. `commands.sh` prints `Not yet: 7 left.` on the start and `Done:` on the answer, on Python 3.10 and 3. A wrong record (`tax_added_by_exam` marked yes and left in the sets and in `features`) prints `Not yet: 5 left.`
- The filters of cell 5 parsed with sqlglot 30.31, dialect `databricks`.

## Pages behind the steps (opened 2026-11-13)

| Step | Page | Sentence |
|---|---|---|
| leakage | https://scikit-learn.org/stable/common_pitfalls.html | "Data leakage occurs when information that would not be available at prediction time is used when building the model." Also: "it is important that these transformations are only learnt from the training data." (test 4) |
| `saveAsTable`, `overwrite` | https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframewriter/saveAsTable | "Saves the content of the `DataFrame` as the specified table." |

## Modelled on

Microsoft Learn, "Train a machine learning model in Azure Databricks", its lab https://microsoftlearning.github.io/mslearn-databricks/Instructions/Exercises/DS-03-Train-machine-learning-model.html: "We'll use 70% of the data for training, and hold back 30% for testing." It states "This exercise should take approximately 45 minutes to complete." Shape taken: split, then print the rows in each set. Ours splits by tax year, adds the record and the five tests, and stops before training. Leakage rule from scikit-learn's common pitfalls (above).
