# Exercise 3: decisions

The answer is `exercise.ipynb` beside this file, with the schema `course.learner_00`.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 2 | `amount = "deduction_amt"` | It prints 1000 returns, 937 filled, 63 empty. The trainer's `withholding_amt` prints 0 empty. |
| 3 | `empty_means = "unknown"` | The learner decides it: the step gives no answer, and its Stuck? hint and cell 3's comment give an example for a different line (line 2b on a paper Form 1040, where a blank line means zero), so the learner sees the shape of a reason, not this one. The reason, which the notebook does not show (its folded hint showed open in Databricks): every return takes the standard deduction or itemized deductions, and line 12e holds the one it took, so an empty line 12e cannot mean that the taxpayer had none. No return in the course tables has a deduction of 0. `zero` prints a Not yet line that sends the learner back to what line 12e holds, without the answer. |
| 3 | `why_empty = "every return takes the standard deduction or itemized deductions, so an empty line 12e cannot mean none"` | The reason above, in the learner's words; the check asks 6 words or more and does not read its meaning. |
| 3 | `flag = "deduction_missing"`, given | The name the reading gives it (curated line 272); given so the new reason costs no extra typed value. Cell 3 reads `deduction_amt` itself, not cell 2's `amount`, so a learner who skips or restarts cell 2 still flags the right column. Cell 3 writes `course.learner_NN.features_flagged`: every column of `course.returns.model_features` and the flag, 1 on the 63 empty rows. |
| 4 | `deduction_amt`: line 12e, a reason, `yes` | Line 12e is on the return as filed. |
| 4 | the flag's row, all given | Its source field, reason, `yes` and timing are given: typing them teaches nothing the `deduction_amt` row does not. |

What else the check accepts: any flag name, any `why_empty` and any reason of 6 words or more, and `yes` or `no` (the debrief takes the timing). It checks that the flag matches the empty cells and that both source fields name 12e. The optional part (more rows, `name_length` struck) is not checked.

The feature record starts in the exercise's own cell 4 with the reading's two rows, `tax_to_agi` and `tax_added_by_exam` (struck), copied from its table. Cells 3 and 4 write two tables in the learner's schema: `features_flagged` and `model_feature_record`, the feature record. Tuesday reads `model_feature_record`.

The reason for `deduction_amt` is general on purpose: it says nothing about any one return's score, a later day's topic.

The learner types 7 values: the end of the schema's name, the amount's name, `empty_means`, `why_empty`, and three slots of the `deduction_amt` row. Step 1 says where the schema is (Catalog, `course`); its name may end in two digits or not (`learner_07`, `learner_ctv`).

## Where each rule comes from (for the trainer, never in a learner cell)

Lines are those of `days/day-01/curated.md` in the Program repository, version 2.0 (2026-11-21).

| Quote or rule in the exercise | From |
|---|---|
| "its source field, its reason, and whether it is known when the case is selected." | line 26, Today's words, A feature's defence |
| "an amount that is not on the return, which can mean zero or unknown." | line 27, Today's words, Missing amount |
| "a column that records which amounts were missing." (Step 3) | line 28, Today's words, Flag column |
| Tuesday's cells fill the empty amounts (Step 3, in plain words) | line 270, § Keep zero apart from unknown: "Tuesday's cells then fill the missing amounts." |
| "Standard deduction or itemized deductions (from Schedule A)" | line 245, § Build features from the body of Form 1040, the table's Deductions row |
| `deduction_missing`, 1 where line 12e is empty | line 272, § Keep zero apart from unknown, One return first |
| "A feature you cannot defend is a feature you cannot keep." (Step 4) | line 205, § Defend a feature before the model reads it |
| the rows of `tax_to_agi` and `tax_added_by_exam` in cell 4 | lines 219 and 220, same section, the feature record's table |
| Debrief 1, struck when the tax withheld stays | line 213, same section (fails on timing); line 260, `withholding_amt` is line 25 |
| Debrief 2, zero or unknown | line 272, § Keep zero apart from unknown |
| Debrief 3, the flag before the fill | lines 274 to 282, same section, the three made-up returns |

The debrief questions are `days/day-01/activities.md`'s, word for word, and deck slide 45's. The worked example is deck slide 43; the exercise is slide 44.

## Where it ran

- Not run in Databricks: a trainer gap (`week-04/setup/day-01-setup.md` § Checked in Databricks, and not yet checked).
- Run on a laptop, 2026-11-21 UTC, by `answers/stand_in.py` (as `commands.sh` runs it): the start prints `Not yet: 1 left.` (the schema). The answer prints `Done:`. `withholding_amt` left in cell 2 with `zero` prints `Not yet: 2 left.`

## Pages behind the steps

| Step | Page | Sentence |
|---|---|---|
| `saveAsTable`, `overwrite` | https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframewriter/saveAsTable | "Saves the content of the `DataFrame` as the specified table." (as week 3 cited it) |

`CREATE OR REPLACE TABLE ... AS SELECT` and `CASE WHEN ... IS NULL` are standard Databricks SQL, as week 3 used them.

## Modelled on

Databricks Academy, Data Preparation for Machine Learning, its "Lab: Build a Feature Engineering Pipeline", https://www.databricks.com/training/catalog/data-preparation-for-machine-learning-2381 (already found for week 3, and only the outline is public). Its feature lab is the shape: a demo on one column, then the learner adds a feature in a lab. The record's three facts follow Google's Rules of Machine Learning, Rule #11 (https://developers.google.com/machine-learning/guides/rules-of-ml): a reference, not an exercise.
