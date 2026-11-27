# Exercise 3: decisions

The answer is `exercise.ipynb` beside this file. It reads the course's shared tables and scores all 250 returns of `model_valid` with Tuesday's two candidates, fitted again in cell 2 as in exercise 1.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 1, 2 | run as given | As exercise 1. |
| 3 | either way round, with a reason of five words or more after `because` | The answer: a false negative costs more, because a missed return stays as filed and nobody sees it, while a wasted examination shows in the no-change rate. The check reads only the form and the reason's length; the debrief questions the reason. |
| 4 | a guess from 0 to 40 for a list of 30 (the answer types 22); `k = 25` | The guess: how many of the 40 labelled change a list of 30, threshold 0.709, picks out; the reading does not give it. The cell shows nothing until both are typed. Then places 1 to 26 by the logistic regression's score: case #123 is at place 11, on the list. Cell 5 then counts the list of 30: 26 examined, 25 right, 1 wrong, so 25 picked out. Four returns show 1.000, which is a score rounded to three places. |
| 5 | `threshold = 0.844` | The score at place 25 (case 890, 0.8443); place 26, 0.818, stays off. The cell counts with the exact 25th score, not the typed one, so rounding never moves a return. On the list: 25 returns, 4 never examined (no label, in no cell), 20 of 21 right, 1 wrong; 20 of 40 labelled change picked out, 20 missed. At 0.5, beside it: 42 returns, 5 never examined, 34 of 37 right, 3 wrong, 6 missed. |
| 6 | `logistic-regression`; `more capacity` if cell 3 says a false negative costs more, `accept` if a false positive does; one sentence of eight words or more with a count | The rule follows the reading: if a missed return costs more, the list of 25 is a known weakness, so ask for more capacity; if an examiner's wasted hours cost more, accept the list of 25 and report the 20 missed (an `accept` must name 20). The answer's cell 3 says a false negative costs more, so it asks for more capacity: 20 of 40 picked out, 20 missed, against 6 at 0.5. `decision-tree` gets `Not yet` with the reading's two reasons: at 0.5 the logistic regression is ahead on both measures, and the tree's 25 ties at 1.0 cannot choose a list of 20 or 10. |
| 8, optional | `tree_threshold = 1.0`; why not 10: 25 returns tie at 1.0 | The tree gives seven scores. At 1.0 exactly 25 returns fill the list (19 right of the examined, against the logistic regression's 20); any higher threshold puts none on it, so a list of 10 or 20 cannot be filled without breaking a tie. |

For the trainer: the cost sentence decides the choice the reading poses, 0.5 (34 right, 3 wrong, 6 missed) against a capacity of 25 (20 right, 1 wrong, 20 missed). Thursday starts from the chosen candidate at 0.844.

## What version 2.0 cut, and why

Learners of this cohort could not finish some exercises. 25 minutes became 15.

- The made-up files (`ten-returns.csv`, `case-123.csv`, `candidate-counts.csv`, `validation-scores.csv`) are gone. The capacity is the reading's own question: 25 cases from the 250 returns of `model_valid`. Case #123 has a label in the course's tables, so version 1's step on an unlabelled case #123 is gone.
- Version 1's two thresholds (the ten, then with case #123) are one: the reading's threshold, 0.844. The trade against 0.5 is printed by cell 5, not typed.
- Typed values, 10 to 7; steps, 8 to 5. A guess of what a list of 30 picks out comes before the sort is shown.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "No model or formula makes that judgment. The people who run the examinations make it, and you must be able to state it in a sentence and defend it." | `days/day-03/curated.md` § Say which error costs more, Why this matters to you |
| the two errors' costs (step 2, our words) | the same section, the table under In general |
| "A *threshold from capacity* is the score of the k-th return when the returns are sorted by score, highest first." | § Set the threshold from the examiners' capacity, In general |
| "a logistic regression never gives exactly 0 or 1" | § opening, Case #123, and ten returns with labels |
| "The list never holds more returns than the examiners can take" | § Set the threshold from the examiners' capacity, Then the whole set |
| "You cannot say whether they are right: they have no label" | the same, Then the whole set |
| "If a missed return costs more, the list at 0.5 is better, ..." | the same section, Which error the threshold trades |

The exercise is deck slide 47; its debrief is slide 48; the demo is slide 46.

## Simulated data added

None beyond the course's tables.

## Where it ran

- Not run in Databricks: a trainer gap. What only a run there confirms: the scores on the course compute giving 0.844 at place 25 (Tuesday's fit; scikit-learn's logistic regression is deterministic on the same rows).
- Run on a laptop, 2026-11-21, Python 3.11, on a stand-in for Spark over the course's week 4 tables made by `week-04/setup/day-01-course-data.py`, and with no table readable: start `Not yet: 7 left.`, answer `Done:`. `commands.sh` prints `Not yet: 7 left.`, then `Done:`.

## Pages behind the steps (opened 2026-11-20)

| Step | Page |
|---|---|
| the threshold | scikit-learn example, Post-tuning the decision threshold for cost-sensitive learning, https://scikit-learn.org/stable/auto_examples/model_selection/plot_cost_sensitive_learning.html (the outline's reference; it prices each error, which this exercise does not) |

## Modelled on

None found that is proven. Closest: the outline's reference above, an example with no learner task. Shape taken: state the cost, apply a rule given in the reading, choose and give the reason.
