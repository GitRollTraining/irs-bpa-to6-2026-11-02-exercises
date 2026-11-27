# Exercise 2: decisions

The answer is `exercise.ipynb` beside this file. It reads the course's shared tables, `course.returns.model_train`, `model_valid` and `model_features`, fits Tuesday's logistic regression again in cell 2 with Tuesday's lines, and puts on the list the 25 returns of `model_valid` at or above Wednesday's threshold, the 25th score, 0.844. The column `made_up_channel` holds channel A or B, a code the course made up; it describes no real way of filing, no real person and no real group, and it is not one of the twelve features.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 1, 2 | run as given | 500, 250 and 1,000 returns; `Threshold 0.844: 25 of 250 returns on the list`; channel A 162 returns, 15 on the list; channel B 88, 10. The counts are given: typing the column's name was a copy. |
| 3 | a number from 0 to 1 (the answer types 0.2) | The guess: channel B's rate on a list of 50. The reading gives the rates at 0.844 and at 0.5, not on a list of 50. Cell 4 prints it beside the guess once the rates are typed: 23 of 88, 0.261 (channel A 27 of 162, 0.167; gap 0.095). A guess cannot be wrong. |
| 4 | `rate_a = 15 / 162`, `rate_b = 10 / 88`; one sentence | 0.093 and 0.114, a gap of 0.021 toward channel B. The cell then prints the list of 50 and 0.5 (22 of 162, 0.136; 20 of 88, 0.227; a gap of 0.091), and the past labels over the examined returns of all four tax years: 83 of 512 (0.162) and 77 of 288 (0.267). A rate typed in quotes gets a course message in the cell and in the check. The sentence must hold the four counts, the threshold 0.844, the gap (0.021, or 2.1 in 100) and the word reason; it may not call the model fair or unfair, and may not say the model selected. |
| 6, optional last step (proxy segment) | `could stand in`, with 0 and 16,140 | The medians over all 1,000 returns: `other_income_amt` 0 in channel A's 648, 16,140 in channel B's 352; `wages_amt` 52,695 and 53,140, printed beside it as the contrast. Checked only when the cell has run. |

Two things for the trainer to know:

- Counts first: 15 against 10 looks like a lean toward channel A; the rates point the other way. The debrief's first question.
- The labels' line answers the debrief's second question: the past decisions already differ by channel, so a gap can come from the labels as well as from the model.

## The optional last step: how to cut it with the proxy segment

Step 5 (cell 6), the "Optional last step" line of the task text and the debrief's third question go with the reading's section "Spot a feature that stands in for a group"; each is marked for the trainer in a comment. To cut them: delete step 5 and cell 6, that task line, and question 3, from the README and both notebooks. Nothing renumbers: the check is cell 5, before them. `check.py` checks the proxy sentence only when `proxy_sentence` exists in the notebook, so it needs no change; `values-without-proxy-step.json` is the answer's run with cell 6 removed, and `check.py` prints `Done:` on it. In the day's README, cut the two parentheses marked "Proxy segment". In this file, cut the row for cell 6, this section and the two proxy rows of the quote table, and the "(with the optional last step, 5)" in the typed values.

## What version 2.0 cut, and why

Learners of this cohort could not finish some exercises. 25 minutes became 15.

- The made-up files (`validation-returns.csv`, 1,000 made-up returns with `synthetic_group` and a built feature `amended_last_year`; `ten-returns.csv`) are gone. The groups are the course's column `made_up_channel` on the shared tables, and the feature that tracks it is `other_income_amt`, one of Tuesday's twelve, as the reading says.
- The tree is gone: Wednesday chose the logistic regression.
- The proxy part is an optional last step, marked for the trainer, and removable as one piece; the check does not need it.
- Typed values, 6 to 4 (with the optional last step, 5): guess, two rates, one sentence. The column's name, the comparison at two other thresholds and the labels by channel are given, not typed.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "It describes no real way of filing, no real person and no real group, and it stands for no protected class such as race, sex or age; the arithmetic is the same for any grouping." | `days/day-04/curated.md` § Check the model for bias before it is used, One return first |
| "Split the held-out returns by group." | § Check the model for bias before it is used, In general |
| "So a gap belongs to a threshold, as precision and recall did on Wednesday: write the threshold beside it." | § Compare selection rates across two groups, One return first |
| "The *selection rate* of a group is the share of its returns that the model puts on the list." | the same section, One return first |
| "A gap is a result that needs a reason." | the same section, The wrong belief |
| "So a gap in the list can come from the labels as well as from the model." | the same section, Where a gap can come from: the labels |
| (proxy segment) "A *proxy* is a feature that names no group and still tracks one. You see it when ..." | § Spot a feature that stands in for a group, In general |
| (proxy segment) "So your sentence says that the feature *could* stand in for the group, ..." | the same section, last paragraph |

The exercise is deck slide 40; its debrief is slide 41; the demo is slide 39. The deck must change: slide 40's Do line and notes (the guess is channel B's rate on a list of 50, not which channel at 0.844; no column to type; the check is cell 5; the proxy line is the optional last step, cell 6); its notes carry a literal `" + PX + "` left from a template; slide 39's demo sets 0.5 in cell 2's `threshold` line, not in a group-rate cell.

## Simulated data added

None beyond the course's tables.

## Where it ran

- Not run in Databricks: a trainer gap. What only a run there confirms: `course.returns.model_features` readable by every learner (the activities' "made_up_channel readable in every learner's notebook").
- Run on a laptop, 2026-11-21, Python 3.11.5, on a stand-in for Spark over the course's week 4 tables made by `week-04/setup/day-01-course-data.py`, with scikit-learn 1.3.0 and with scikit-learn 1.9.1 (every count the same): start `Not yet: 9 left.` (with the optional last step run empty), answer `Done:` (with the proxy sentence, when cell 5 is run again after cell 6), and the answer with cell 6 removed `Done:`. `check.py --start` prints `Not yet: 7 left.`; `check.py values.json` and `check.py values-without-proxy-step.json` print `Done:`. Wrong answers tried: a rate in quotes, the guess as a word, `could not stand in` for 0 and 16,140, a result that calls the model unfair, a result without the threshold, "selected": each `Not yet` with its line.

## Modelled on

None found that is proven (the day plan: no lab found in the Source library's captured pages; the web was not searched). Closest: the Program's common task, a bias check before use. Shape taken: split, divide, state the result; then compare one feature.
