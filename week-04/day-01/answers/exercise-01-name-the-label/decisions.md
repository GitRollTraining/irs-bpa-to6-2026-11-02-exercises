# Exercise 1: decisions

The answer is `exercise.ipynb` beside this file.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 2 | Q1: `exam_changed_tax` | The column records a past decision for each examined return, yes or no. Q1 asks yes or no. `tax_added_by_exam` also comes from an examination, but it is an amount, and the check says so. |
| 2 | Q2: `no label` | No column of `course.returns.model_returns` records whether a taxpayer amended a past return. So no past decision answers Q2 in this table. |
| 3 | `needs`: a column that records, for each past return, whether the taxpayer later amended it | A label exists only where someone recorded the decision. |

What else the check accepts: any `why` of 6 words or more and any `needs` of 8 words or more. It checks the two labels, not the reasons. The debrief takes the reasons.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "A label is the past decision recorded for a case." | `days/day-01/curated.md` line 105, § Find the label a question can learn from, What a label is |
| "If you cannot name that decision for a question, no model of this week's kind can answer it." | line 102, same section, Why this matters to you |
| "It reads `yes` when an examination changed the tax and `no` when it did not." | lines 114 and 115, same section, What a label is |
| "A model can learn only from a decision someone recorded in the past." | line 101, same section, Why this matters to you |
| "knows only what the past cases it was shown had in common" (debrief 2) | line 71, § Know what a model is, What a model is |
| "An examination that changed the tax is itself a stand-in for 'this return was wrong'." (debrief 3) | lines 130 and 131, § Find the label a question can learn from (the file's double quotes become single quotes inside the quote) |

The deck is not built yet. The deck's owner adds the slide numbers.

## Where it ran

- Not run in Databricks: a trainer gap (`week-04/setup/day-01-setup.md` § Checked in Databricks, and not yet checked).
- Run on a laptop, 2026-11-19 UTC, by `commands.sh`: the stand-in loads the week's tables into DuckDB under their Databricks names and runs every code cell. The start prints `Not yet: 5 left.` The answer prints `Done:`. Q1 typed as `tax_added_by_exam` prints `Not yet: 1 left.` with the line on amounts.

## Pages behind the steps

`spark.table(...).columns` is the only call. Week 3 used it (week 3, Wednesday, exercise 4). We cite no other page.

## Modelled on

Google for Developers, Introduction to Machine Learning Problem Framing, "Framing an ML problem", https://developers.google.com/machine-learning/problem-framing/ml-framing. Its two "Check Your Understanding" tasks ask if a health app needs a proxy label, and which of two framings fits a fashion firm. The page shows each answer with its reason. Shape taken: a judgment on given questions, each answer with its reason. Also week 3 Monday's exercise 2 in this repository, the course's framing exercise in a notebook text cell.
