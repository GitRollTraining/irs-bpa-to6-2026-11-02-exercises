# Exercise 1: the kept run

The author ran it on 2026-11-13, on a laptop, not in Databricks. The machine that wrote it has no Databricks access. The run used Python 3.12.6 in the course's `.venv`. `nbclient` ran the notebook, with the notebook's folder as the working folder. The run called no model and started no agent.

## The starting notebook, cells 1 to 3 as given

Cell 1:

```text
wages_amt          returns          the wages the taxpayer reported on the return
total_income_amt   returns          the total income the taxpayer reported on the return
w2_wages_amt       wage_statements  the wages the employer reported on the W-2 for the same year
exam_changed_tax   exam_outcomes    for a return examined in the past: did the examination change the tax, yes or no
exam_picked_by     exam_outcomes    for a return examined in the past: how it was picked, random sample or score
taxpayer_name      returns          the taxpayer's name
tin                returns          the taxpayer identification number, which joins the three tables
street_address     returns          the taxpayer's street address
```

Cell 2: `Saved record.json. Now run cell 3.`

Cell 3, the check, printed `Not yet:` and ten lines. One line is for the empty question. Eight lines are for the fields, one each. One line is for the empty target line.

## The solved copy, cells 1 to 3

Cell 3: `Done: your question names its unit, target and time; each field has its kind, verdict and reason; your target line names what you considered.`

## Wrong records the check refuses

Each record was the kept answer with one change. The check printed `Not yet:` for each of these six:

1. The identifying number left out.
2. The name kept.
3. `exam_picked_by` as `compare`.
4. A question about being "selected for review".
5. A target line with no amount.
6. A reason of two words.
