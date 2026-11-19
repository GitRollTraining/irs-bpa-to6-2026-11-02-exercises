# Exercise 2: decisions

The answer is `exercise.ipynb` beside this file.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 2 | `column = "exam_changed_tax"` | The baseline predicts the most common label, so the label is the column to count. It prints `no` 320, `NULL` 100, `yes` 80. |
| 3 | `prediction = 0.64` (any share from 0 to 1) | The prediction is the learner's own guess. 0.64 is 320 of 500, the guess of a learner who keeps the empty rows: the debrief starts from that gap. |
| 4 | `most_common = "no"`, `right = 320`, `labelled = 400` | Always predicting `no` is right on the 320 `no` returns. The 100 empty rows have no label, so the count leaves them out: 320 + 80 = 400. Accuracy 320 / 400 = 0.8. |

What else the check accepts: a prediction typed as `0.8`, `"0.8"`, `"80%"` or `80`. A `labelled` of 500 prints the line on the empty rows.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "Accuracy is the share of predictions that are right." | `days/day-01/curated.md` line 182, § Set the baseline every model must beat, What accuracy is |
| "the simplest prediction you can make, used as the score to beat" | line 168, same section, What a baseline is |
| "A return that was never examined has no label." | line 115, § Find the label a question can learn from, What a label is |
| "On our data, the baseline is computed on the labelled returns of the training set only, the ones with `yes` or `no`." | lines 207 and 208, § Set the baseline every model must beat, Why accuracy flatters a model on rare cases |

Debrief 1 rests on line 211: "The metrics that count what a model finds are Wednesday's". The question says it as "might find few changed returns". The deck is not built yet. The deck's owner adds the slide numbers.

## Where it ran

- Not run in Databricks: a trainer gap (`week-04/setup/day-01-setup.md` § Checked in Databricks, and not yet checked).
- Run on a laptop, 2026-11-19 UTC, by `commands.sh`: the start prints `Not yet: 5 left.` The answer prints `Done:`. `labelled = 500` prints `Not yet: 1 left.` with the line on the 100 empty rows. `prediction = "80%"` passes.

## Pages behind the steps

`spark.sql(...).show()` with `GROUP BY` and `COUNT(*)`, as in week 3. We cite no other page.

## Modelled on

Google Machine Learning Crash Course, "Classification: Accuracy, recall, precision, and related metrics", https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall, which the day plan names. Its accuracy section says "a model that predicts negative 100% of the time would score 99% on accuracy, despite being useless", and its "Check your understanding" tasks show each answer with its reason. The course page says "Since 2018, millions of people worldwide have relied on Machine Learning Crash Course" (https://developers.google.com/machine-learning/crash-course). Shape taken: count, predict, then compute by hand.
