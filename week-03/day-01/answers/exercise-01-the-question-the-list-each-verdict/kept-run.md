# Exercise 1: the kept run

The author ran it on 2026-11-13, on a laptop, not in Databricks. The machine that wrote it has no Databricks access. The run called no model and started no agent.

## The notebooks in a Jupyter kernel

Python 3.12.6 in the course's `.venv`. `nbclient` ran each notebook in a scratch copy of the exercise folder, with that folder as the working folder. With no Databricks, cell 1 took its fallback.

The starting notebook, cell 1:

```text
Read from fields.csv, the copy beside this notebook.
Why: cell 1 has no schema name
tin               returns, wage_statements, exam_outcomes  the taxpayer identification number, which joins the three tables
taxpayer_name     returns                                  the name of the taxpayer
street_address    returns                                  the street address of the taxpayer
wages_amt         returns                                  the wages the taxpayer reported on the return
total_income_amt  returns                                  the total income the taxpayer reported on the return
w2_wages_amt      wage_statements                          the wages the employer reported on the W-2 for the same year
exam_changed_tax  exam_outcomes                            for a return examined in the past: did the examination change the tax, yes or no
exam_picked_by    exam_outcomes                            for a return examined in the past: how it was picked, random sample or score
```

Cell 2: `Saved record.json. Now run cell 3.` Cell 3: `Not yet: 9 left.` and nine lines: the question, the six fields not done for the learner, the explain sentence and the target line.

The solved notebook: cell 1 printed `Why: name 'spark' is not defined` and the same eight lines. Cell 3: `Done: the question names its unit, target and time. Each field has its kind, verdict and reason. The sentence on exam_picked_by names the random sample. The target line names what you considered.`

## The setup notebook and the catalog path, with a stand-in for Databricks

A stand-in `spark` kept the tables in memory. Each SQL statement went through `sqlglot` 30.31.0's Databricks dialect, which parsed all 18. It parsed the five `GRANT` statements only as an unchecked command, so their syntax rests on the cited page alone.

- Setup cell 1, with `SCHEMA` not set: stopped with "Set SCHEMA in cell 1 to the course catalog's name, a dot, and case_selection."
- Setup cell 3: `returns: 30 rows`, `wage_statements: 30 rows`, `exam_outcomes: 12 rows`, each column with its type and comment.
- The exercise's cell 1 with `training.case_selection`: `Read from the catalog: training.case_selection` and the eight lines above, `tin` listed once with its three tables.
- With `training.no_such_schema`: `Read from fields.csv, the copy beside this notebook.`, then `Why: [TABLE_OR_VIEW_NOT_FOUND] ...`, then the eight lines.

## The check

On Python 3.12 and on 3.10, the oldest the course allows. The kept answer: `Done:`. Each wrong record below is the kept answer with one change. The check printed `Not yet: 1 left.` (the question: `2 left.`) and named the field or part:

1. `tin` as not needed.
2. `taxpayer_name` as needed.
3. `exam_picked_by` as compare.
4. `w2_wages_amt` as line item.
5. A question about being "selected for review".
6. An explain sentence with no random sample.
7. A target line with no amount.
8. A reason of two words.
