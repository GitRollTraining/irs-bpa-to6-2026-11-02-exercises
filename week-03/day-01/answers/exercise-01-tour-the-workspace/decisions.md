# Exercise 1: decisions

For the trainer. Exercise 1, "Tour the workspace: one table, two counts", follows the demo of the same steps on `course.returns.return_summary`. Modelled on Microsoft Learning's DP-750T00 lab 1, "Explore Azure Databricks" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/01-explore-azure-databricks.html): its Catalog Explorer and notebook steps only, shape "Follow and confirm". The check is `check.py` in the exercise folder.

## 1. The full name

- **The answer.** `course.returns.return_header`.
- **Reason.** Monday's return table sits in the schema `returns` of the catalog `course`. Its full name joins the three parts with dots.
- **The notebook line.** "A full name joins the three with dots".
- **What else the check accepts.** Backticks around the parts, and any case. A name with the wrong schema or two parts fails, with a message naming the problem.

## 2. The notebook's count

- **The answer.** 40. Cell 2 runs `SELECT COUNT(*)` on the full name.
- **Reason.** The setup notebook writes 40 returns (`week-03/setup/day-01-course-data.py`, `RETURNS = 40`).
- **The notebook line.** "A notebook runs on a cluster, so a notebook with none attached runs nothing."
- **What else the check accepts.** The check counts the table again with spark and compares. If the trainer's table holds another count, that count is the answer.

## 3. The SQL editor's count, and the prediction

- **The answer.** 40, typed into `sql_editor_count`. `explain`: the counts are the same, because both tools read the one table the full name names. The compute only runs the query.
- **Reason.** A notebook's cluster and the SQL editor's warehouse are two kinds of compute over one catalog.
- **The notebook line.** "A SQL warehouse is the compute behind the SQL editor."
- **What else the check accepts.** Any `explain` of 8 words or more: the check looks for the prediction, and the talk after the exercise judges it. A count typed in quotes, such as "40", is refused with a message to type the digits only.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks: the notebook's cells in order, with a stand-in for `spark` that runs the same SQL on DuckDB over the setup's rows. The start printed `Not yet: 4 left.`. The answer printed `Done: course.returns.return_header has 40 rows, in the notebook and in the SQL editor.` `commands.sh` printed the same on Python 3.10 and 3.14.
- Not run in Databricks: a trainer gap. Check at the run-through: the copy icon beside a table's full name in Catalog Explorer, the compute menu's name (**Connect**), and that cell 4 finds `check.py` beside the notebook (it builds the folder from the notebook's path, as serverless compute does not promise the notebook's folder as the working folder).

## Where each quote comes from

The curated file is the day's own file, `days/day-01/curated.md` in the Program repository. The day's deck is being rebuilt, so no slide number is given.

| Quote in the notebook | Curated file: heading, line |
|---|---|
| "A full name joins the three with dots" | Read a table's three-part name, line 399 |
| "A notebook runs on a cluster, so a notebook with none attached runs nothing." | Work inside a Databricks workspace, line 124 |
| "A SQL warehouse is the compute behind the SQL editor." | Work inside a Databricks workspace, line 111 |
| "only the full name tells them apart." | Read a table's three-part name, line 405 |

## Findings of the linter inside quotes

None. Outside quotes, one: the Goal has 27 words (cap 25). The Goal is the exercise block's line in the day's activities, kept word for word; a shorter Goal is proposed to the block's owner.
