# Exercise 2: decisions

The answer is `exercise.ipynb` beside this file. Its cell 6 holds the tree's line, as a learner leaves it after the second fit; the logistic regression is fitted first, with the line as the course gives it. So Run all on this answer ends at `Not yet`: the check needs both fits, and this copy holds only the second. To see `Done:`, run cell 6 with the course's line first, then with the tree's line, then the check. It uses the course's shared tables, the setup's twelve features, and its fill (an empty amount read as 0, with `deduction_missing`).

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 3 | run as given | 400 training rows and 200 validation rows have a label. The twelve features are the ones the week's setup measures: every amount of the filed return, two ratios and Monday's flag, each known before selection. An empty amount is read as 0: 20 deduction lines in training and 16 in validation. |
| 4 | run as given | It prints 200 validation returns with a label, so one return moves the accuracy by 0.005, and their labels, 160 `no` and 40 `yes`. Monday's baseline is 0.8 on the training rows and 0.8 on the validation rows, so on these tables the two agree; the cell still measures it on the rows the candidates are measured on. |
| 5 | any of `a lot` (right on 20 or more of the 200 returns beyond the baseline), `a little` (right on 1 to 19 more), `not better` (the same or fewer) | A guess cannot be wrong; the check asks only that it is written before the fit, in any case, with or without a full stop. The answer types `a lot` and `a little`. |
| 6, first run | `make_pipeline(StandardScaler(), LogisticRegression())` | Validation accuracy 0.955, 191 of 200 right. Unscaled, `LogisticRegression()` did not converge on these dollar amounts (The week's setup note). |
| 6, second run | `DecisionTreeClassifier(max_depth=3, random_state=0)` | Validation accuracy 0.895, 179 of 200 right. `random_state=0` makes every run grow the same tree, so exercise 3's record matches. The week's setup measured the full-depth tree at 0.910; Monday says Tuesday keeps the tree short. |
| 7 | run as given | baseline 0.800, logistic-regression 0.955, decision-tree 0.895. |
| 9, optional | one sentence | Both beat it: the logistic regression by 31 returns, the tree by 19. |

What else the check accepts: nothing else in cell 6; the tree must have `max_depth=3`; the check fits both candidates again on the notebook's rows and compares. A learner who adds `tax_added_by_exam` to the features list gets `Not yet` (cell 3's list), and an accuracy near 1.000 if they look (the course measured 0.990 for the logistic regression and 1.000 for the tree): the debrief's third question.

The trainer's demo (slide 31) fits the logistic regression on the same notebook and stops there; the tree is the learners'.

## What version 2.0 cut, and why

Learners of this cohort could not finish some exercises. Same cells, same goal, same check; 15 minutes instead of 25.

- Steps, 8 to 4: cells 1 to 4, which the learner only runs, are one step, and cells 7 and 8 are one step. No cell changed.
- Typed values stay three: the two guesses and the one model line, each part of the goal.
- Shorter text: the step that explained the twelve features and the fill is one sentence; the reading and the trainer's demo explain them.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "A comparison is fair only on the same rows." | `days/day-02/curated.md` § Fit two models from the given cells, Compare with the baseline; deck slide 29 |
| the cells' plain form: `features`, `notna()`, `X_train`, `model = LogisticRegression()`, `fit`, `predict`, `accuracy_score`, `DecisionTreeClassifier(max_depth=3)` | the same section, In general; deck slide 28 |
| a large gain is the moment to ask about a leak; an accuracy close to 1.000 is a warning (step 4, our words) | the same section, Compare with the baseline |

The exercise is deck slide 32; its debrief is slide 33; the demo is slide 31.

## Simulated data added

None beyond the course's tables. Cell 2 adds `deduction_missing` to `train` and `valid` in the notebook by Monday's rule; no table changes.

## Where it ran

- Not run in Databricks: a trainer gap. What only a run there confirms: `spark.table` on `course.returns.model_train` and `model_valid` for a learner in `training-students`, and `toPandas()` on them; scikit-learn on the course compute giving 0.955 and 0.895.
- Run on a laptop, 2026-11-21, Python 3.11.5, scikit-learn 1.3.0, pandas 2.0.3, on a stand-in for the Spark calls, over the course's week 4 tables made by `week-04/setup/day-01-course-data.py`, and again with no table readable (load.py makes the same rows from that file): start `Not yet: 2 left.` (the logistic regression is fitted when the cells run as given), answer `Done:` on both. The same numbers as the week's setup measurement, which used scikit-learn 1.5.2.

## Pages behind the steps (opened 2026-11-20)

| Step | Page |
|---|---|
| fit, predict | scikit-learn, Getting Started, https://scikit-learn.org/stable/getting_started.html (a Source of the day's reading) |
| the fill | scikit-learn, Common pitfalls and recommended practices, https://scikit-learn.org/stable/common_pitfalls.html (a Source of the day's reading) |

## Modelled on

None found that is proven. Closest: Microsoft Learn, "Train a machine learning model in Azure Databricks", its unit "Exercise - Train a machine learning model in Azure Databricks", https://learn.microsoft.com/en-us/training/modules/machine-learning-azure-databricks/7-exercise-machine-learning-databricks (opened 2026-11-20; 45 minutes; "you'll use a Databricks Spark cluster to train a classification model"). No count of learners on the page. Shape taken: run given cells, change one line, compare. Its case (Spark MLlib on its own data) is not used.
