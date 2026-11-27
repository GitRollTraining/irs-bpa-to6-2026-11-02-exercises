# Exercise 1: decisions

The answer is `exercise.ipynb` beside this file.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 2 | Q1: `exam_changed_tax` | The column records a past decision for each examined return, yes or no. Q1 asks yes or no. `tax_added_by_exam` also comes from an examination, but it is an amount, and the check says so. |
| 2 | Q2: `no label` | No column of `course.returns.model_returns` records whether a taxpayer amended a past return. So no past decision answers Q2 in this table. |
| 3 | `needs`: a column that records, for each past return, whether the taxpayer later filed an amended return | Q2 lacks a label because nobody recorded the decision, not because no decision could record it. So it gets a label once someone records it. |

One way to say it: "A column that records, for each past return, whether the taxpayer later filed an amended return, yes or no." The notebook does not show it: its Stuck? hint was folded, and Databricks shows a fold open. Step 3's hint and cell 3's comment give an example for a different question instead (whether the IRS sent the taxpayer a notice), so the learner sees the shape of an answer, not the answer.

What else the check accepts: any `why` of 6 words or more and any `needs` of 8 words or more. It checks the two labels, not the reasons. The debrief takes the reasons.

Step 1 says what the other columns hold in general words (keys, header, amounts). Of the one column the course made up for a later day, it says only that nothing today uses it.

What else the check says: a Q2 label that is not a column, such as `none`, prints a line that asks for `no label`, exactly.

## Where each rule comes from (for the trainer, never in a learner cell)

Lines are those of `days/day-01/curated.md` in the Program repository, version 2.0 (2026-11-21).

| Quote or rule in the exercise | From |
|---|---|
| "A label exists only where someone decided." (What you need to know first) | line 98, § Name the label a question can learn from |
| a label is the past decision recorded for a return (What you need to know first, Step 1's why, in plain words) | line 21, Today's words, Label; line 90, § Name the label, In general |
| "If no column records a past decision, it is not classification." (Step 2) | line 294, § Where today goes wrong |
| "the decision could be recorded and nobody recorded it, so the question gets a label once someone does." (Step 3, the first of the reading's two reasons a question can lack a label) | line 76, § See what a model does with one return, Named, not taught: anomaly detection |
| Debrief 1, which returns would still have no label | line 76 (a label once someone records it) and line 98 (a label exists only where someone decided) |
| Debrief 2, today's new decisions | line 307, § The trade-off: a decision arrives only after an examination ends |
| Debrief 3, what to ask about a label | line 100: the proxy-label caution |

Debrief 1 is new (2026-11-21), from Q2; questions 2 and 3 are `days/day-01/activities.md`'s and deck slide 20's, word for word. The worked example is deck slide 18; the exercise is slide 19.

## Where it ran

- Not run in Databricks: a trainer gap (`week-04/setup/day-01-setup.md` § Checked in Databricks, and not yet checked).
- Run on a laptop, 2026-11-21 UTC, by `answers/stand_in.py` (as `commands.sh` runs it): the stand-in loads the week's tables into DuckDB under their Databricks names and runs every code cell. The start prints `Not yet: 5 left.` The answer prints `Done:`.

## Pages behind the steps

`spark.table(...).columns` is the only call. Week 3 used it (week 3, Wednesday, exercise 4). We cite no other page.

## Modelled on

Google for Developers, Introduction to Machine Learning Problem Framing, "Framing an ML problem", https://developers.google.com/machine-learning/problem-framing/ml-framing. Its two "Check Your Understanding" tasks ask if a health app needs a proxy label, and which of two framings fits a fashion firm. The page shows each answer with its reason. Shape taken: a judgment on given questions, each answer with its reason. Also week 3 Monday's exercise 2 in this repository, the course's framing exercise in a notebook text cell.
