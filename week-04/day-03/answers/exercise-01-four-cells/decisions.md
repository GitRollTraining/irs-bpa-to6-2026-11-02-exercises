# Exercise 1: decisions

The answer is `exercise.ipynb` beside this file. It reads the course's shared tables, `course.returns.model_train` and `model_valid`, and scores them with Tuesday's two candidates, fitted again in cell 2 with Tuesday's lines: `make_pipeline(StandardScaler(), LogisticRegression())` and `DecisionTreeClassifier(max_depth=3, random_state=0)`, on the 400 examined returns of `model_train` and Tuesday's twelve features.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 1, 2 | run as given | 500 and 250 returns; 250 scored, 40 `change`, 160 `no change`, 50 `never examined`. |
| 3 | run as given | The ten of the day's reading, highest score first, with the reading's scores to three places: 205 0.997, 224 0.983, 123 0.964, 905 0.942, 463 0.652, 37 0.474, 471 0.179, 50 0.071, 4 0.058, 11 0.000. |
| 4 | 905, 463 `FP`; 471 `FN`; 37 `TN` (given: 205, 224, 123 `TP`; 50 `FN`; 4, 11 `TN`) | The four left to the learner are the ones that teach: two high scores that are wrong, one just below the line, one change return left off. At 0.5 a score at or above the threshold goes on the list. The cell counts the sort: 3, 2, 2, 3; sum 1 is 10, sum 2 is 5. The check accepts `TP` or `true positive`, in any case. |
| 5 | FP: hours spent on a return whose examination changes nothing; FN: a return an examination would have changed, and nobody looks at it | The reading's table, "What it means for an examiner", in the learner's words. The check asks only for four words each; the words are read aloud in the debrief. |
| 6 | any whole number from 0 to 6 (the answer types 2) | The guess: how many of the 6 returns labelled change off the list at 0.5 score above 0.4; the reading does not give it. A guess cannot be wrong. The cell shows the table only once a guess is typed, then the six scores: 0.071, 0.179, 0.355, 0.416, 0.443, 0.498, so 3. Then `[[34 6] [3 157]]`: rows are the labels, change then no change; columns on the list, then off. |
| 7 | `{"TP": 34, "FN": 6, "FP": 3, "TN": 157}` | Row 1 is TP then FN; row 2 is FP then TN. A learner who reads the table as the day's layout types FP 6 and FN 3: sum 2 is then 37, not 40, and the check says the rows are the labels. Accuracy (34 + 157) / 200 is 0.955, Tuesday's number. |
| 9, optional | `463 TN` | At 0.7 only case 463 (0.652) moves, from FP to TN: 3, 1, 2, 4. The demo already sorted the ten at 0.1, so the optional part uses 0.7. |

Two things for the trainer to know:

- The debrief's second question: the false negatives are the cell nobody sees. True negatives are also off the list, but they were rightly left alone.
- Everyone reads the same course tables, so every learner's counts are the ones above.

## What version 2.0 cut, and why

Learners of this cohort could not finish some exercises. 25 minutes became 15.

- The made-up files (`ten-returns.csv`, ten other returns; `validation-scores.csv`, 1,000 made-up returns) are gone. The ten are the day's reading's own ten, from `model_valid`, and the 200 examined returns are the course's.
- Typed values, 32 to 11: cell 4 gives six of the ten sorted and asks only for the cell of the other four, not `on`/`off` too, and counts the sort itself; cell 5 asks for the two errors' meanings, not all four (the reading: "The two cells whose name starts with *false* are the model's two kinds of error."). A guess of the missed returns close to the line comes before the table is shown.
- Steps, 7 to 5.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "The first word of each cell's name, *true* or *false*, says whether the list agreed with the label." | `days/day-03/curated.md` § Sort ten returns into four cells, One return first |
| "in this course, it goes on the list" | § Judge a model on returns it never saw, In general |
| "The two cells whose name starts with *false* are the model's two kinds of error." | § Sort ten returns into four cells, In general |
| "Tools arrange the rows and columns differently"; the two sums, "The four counts add up to 200 ..." | § Sort ten returns into four cells, By hand, then by the counting code |

The exercise is deck slide 19; its debrief is slide 20; the demo is slide 18.

## Simulated data added

None beyond the course's tables. Cell 2 scores `model_valid` in the notebook; no table changes.

## Where it ran

- Not run in Databricks: a trainer gap. What only a run there confirms: `spark.table(...).toPandas()` on `course.returns.model_train` and `model_valid` for a learner, and scikit-learn on the course compute giving the same scores (Tuesday's exercises rest on the same fit).
- Run on a laptop, 2026-11-21, Python 3.11, on a stand-in for the Spark calls over the course's week 4 tables made by `week-04/setup/day-01-course-data.py`, and again with no table readable (load.py makes the same rows from that file): start `Not yet: 4 left.`, answer `Done:` on both (rerun 2026-11-21 after the learner read). `commands.sh` prints `Not yet: 4 left.`, then `Done:`.

## Pages behind the steps (opened 2026-11-20)

| Step | Page |
|---|---|
| the four cells | Google Machine Learning Crash Course, Thresholds and the confusion matrix, https://developers.google.com/machine-learning/crash-course/classification/thresholding (a Source of the day's reading) |
| the counting code | scikit-learn, `confusion_matrix`, in its Model evaluation guide (a Source of the day's reading) |

## Modelled on

None found that is proven. Closest: the outline's reference, Google Machine Learning Crash Course, Classification: Accuracy, recall, precision, and related metrics, https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall. Shape taken: classify each item, then count, then check with given code.
