# Exercise 3: decisions

The answer is `exercise.ipynb` beside this file, with the schema `course.learner_00`.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 2 | `amount = "deduction_amt"` | It prints 1000 returns, 937 filled, 63 empty. The trainer's `withholding_amt` prints 0 empty. |
| 3 | `empty_means = "unknown"` | Line 12e is the standard or the itemized deduction: each return takes one, so an empty line cannot mean none. |
| 3 | `flag = "deduction_missing"` | Named for its amount, as the day's worked example names `withholding_missing`. Cell 3 writes `course.learner_NN.features_flagged`: every column of `course.returns.model_features` and the flag, 1 on the 63 empty rows. |
| 4 | the rows for `deduction_amt` and `deduction_missing` | Each names line 12e as its source field, a reason, `yes` and why: the return as filed holds both. |

What else the check accepts: any flag name, any reason of 6 words or more, and `yes` or `no` (the debrief takes the timing). It checks that the flag matches the empty cells and that both source fields name 12e. The optional part (more rows, `name_length` struck) is not checked.

The feature record starts in the exercise's own cell 4, two rows filled (`tax_to_agi`, the day's worked example, and `wages_amt`), not in the week's setup. Cells 3 and 4 write two tables in the learner's schema: `features_flagged` and `model_feature_record`. Tuesday reads `model_feature_record`.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "A feature's defence is three facts written beside it" | `days/day-01/curated.md` line 283, § Defend each feature by its source, reason and timing |
| "An empty line can mean two different things" | line 374, § Keep a missing amount apart from a zero |
| "Once a cell is filled, nobody can tell a real 0 from a filled 0." | line 392, same section, A flag column keeps the difference |
| "holds 1 where the amount was missing and 0 where it was present" | lines 393 and 394, same paragraph |
| "Standard deduction or itemized deductions (from Schedule A)" | line 345, § Build features from the Form 1040 body, never the header, the table's row 12e |
| "If you cannot say where each input came from and why it was used, the score cannot be defended, however accurate it is." | lines 279 and 280, § Defend each feature by its source, reason and timing |
| "an empty line may itself be a signal", "known when the return is filed" | lines 410 and 411, § Keep a missing amount apart from a zero, Worked example |
| "Leave it out only for an amount that is never empty." (debrief 2) | line 435, § The trade-off |
| `tax_to_agi`'s row in cell 4 | lines 325 to 329, § Defend each feature, Worked example |

Line 303 names debrief 3's answer, `tax_added_by_exam`. The deck is not built yet. The deck's owner adds the slide numbers.

## Where it ran

- Not run in Databricks: a trainer gap (`week-04/setup/day-01-setup.md` § Checked in Databricks, and not yet checked).
- Run on a laptop, 2026-11-19 UTC, by `commands.sh`: the start prints `Not yet: 1 left.` (the schema). With a number typed and nothing else, it prints `Not yet: 7 left.` The answer prints `Done:`. `withholding_amt` left in cell 2 with `zero` prints `Not yet: 2 left.`

## Pages behind the steps

| Step | Page | Sentence |
|---|---|---|
| `saveAsTable`, `overwrite` | https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframewriter/saveAsTable | "Saves the content of the `DataFrame` as the specified table." (as week 3 cited it) |

`CREATE OR REPLACE TABLE ... AS SELECT` and `CASE WHEN ... IS NULL` are standard Databricks SQL, as week 3 used them.

## Modelled on

Databricks Academy, Data Preparation for Machine Learning, its "Lab: Build a Feature Engineering Pipeline", https://www.databricks.com/training/catalog/data-preparation-for-machine-learning-2381 (already found for week 3, and only the outline is public). Its feature lab is the shape: a demo on one column, then the learner adds a feature in a lab. The record's three facts follow Google's Rules of Machine Learning, Rule #11, which the day plan names (https://developers.google.com/machine-learning/guides/rules-of-ml): a reference, not an exercise.
