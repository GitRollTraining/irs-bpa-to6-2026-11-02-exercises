# Exercise 2: decisions

The answer is `exercise.ipynb` beside this file. It reads the course's shared tables and scores `model_valid` with Tuesday's two candidates, fitted again in cell 2 as in exercise 1. Cell 6 records both candidates in two new runs in `week-04-candidates`; it needs no run made before.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 1, 2 | run as given | As exercise 1. |
| 3 | a whole number from 0 to 40 (the answer types 36) | The guess: at a threshold of 0.4, how many of the 40 labelled change the logistic regression puts on the list; the reading does not give it. A guess cannot be wrong. Cell 4 shows the counts only once it is typed: 37, the 34 at 0.5 and the 3 scoring from 0.4 to 0.5. |
| 4 | run as given | logistic-regression 34, 3, 6, 157; decision-tree 31, 12, 9, 148; both sums 200 and 40. |
| 5 | logistic-regression `34 / 37`, `34 / 40`; decision-tree `31 / 43`, `31 / 40` | 0.919, 0.85; 0.721, 0.775; beside the accuracies 0.955 and 0.895 on the same 200 returns. The check accepts any value within 0.0005; a rounded value such as `0.92` gets `Not yet` with the division to type, `34 / 37`. At 0.5 the logistic regression is ahead on both measures. |
| 6 | run as given | Starts a new run of each name and logs `threshold` 0.5 (a parameter), `validation_accuracy`, `precision` and `recall` (metrics), all on the same 200 examined returns: logistic-regression 0.955, decision-tree 0.895, as Tuesday measured them. Run again, it makes two more runs; cell 7 and **Compare** read the newest of each name. |
| 8, optional | `0 / 40` | The baseline puts no return on the list: recall 0 of 40, and precision cannot be computed, since there is nothing to divide by. |

## What version 2.0 cut, and why

Learners of this cohort could not finish some exercises. 25 minutes became 15.

- The made-up file `validation-scores.csv` (1,000 returns) is gone; the counts are the course's, and they are the reading's own table. Version 1 logged `accuracy_same_rows` because its rows were not Tuesday's; on the course's tables Tuesday's `validation_accuracy` is on the same rows, so that metric and the `rows` parameter are gone.
- Steps, 7 to 4. Typed values, 6 to 5: one guess and the four divisions. The Compare page is optional: cell 7 checks the runs themselves.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "*Precision* is the share of the returns on the list that are labelled *change*." "*Recall* is the share of the returns labelled *change* that are on the list." | `days/day-03/curated.md` § Count precision and recall from the matrix, In general |
| "write the threshold beside every precision and every recall" | the same section, In general |
| the guess before the counts | the same section, Why this matters to you |

The exercise is deck slide 32; its debrief is slide 33; the demo is slide 31.

## Simulated data added

None beyond the course's tables.

## Where it ran

- Not run in Databricks: a trainer gap. What only a run there confirms: `mlflow.start_run(run_name=...)` making the two runs in a learner's own experiment, and **Compare** showing the four measures.
- Run on a laptop, 2026-11-21, Python 3.11, on a stand-in for Spark and MLflow over the course's week 4 tables made by `week-04/setup/day-01-course-data.py`: with no table readable: start `Not yet: 7 left.`, answer `Done:`. `commands.sh` prints `Not yet: 7 left.`, then `Done:`.
- Run on a laptop, 2026-11-27, Python 3.12, MLflow 3.18 with a local store and no run made before, after cell 6 was changed to always make new runs (the self-contained rule): cells 1 to 7 of the answer print `Logged into a new run` twice, then `Done:`; run a second time, the experiment holds 4 runs and cell 7 still prints `Done:`. The start notebook prints `Not yet: 7 left.`

## Pages behind the steps (opened 2026-11-20)

| Step | Page |
|---|---|
| precision and recall | Google Machine Learning Crash Course, https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall (a Source of the day's reading) |
| logging into a run | MLflow Tracking documentation (a Source of Tuesday's reading) |

## Modelled on

None found that is proven. Closest: the outline's reference, the Google page above, whose "Check your understanding" items ask which measure to use for a stated cost. Shape taken: predict, count with given code, divide by hand, record.
