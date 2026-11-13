# Set up Monday in Databricks (week 3, day 1)

For the trainer. Monday's four exercises run in the class's Databricks workspace. Do these steps before class, in order. The course made up the tables: no row is a real taxpayer. Monday's setup makes two tables in the catalog `course`, schema `returns`: `return_header`, Monday's return table, and `return_summary`, built from it.

## Before Monday

1. **Get the files.** Sign in to the class workspace. Open your Git folder of the course (in the left bar, **Workspace**). Pull, so that the folder `week-03` is there: select the branch name at the top of the Git folder, then **Pull**.
2. **Start the compute.** Start the compute the class uses for notebooks, and the SQL warehouse for the SQL editor. Write both names on the board: exercises 1 and 3 tell learners to select the compute and the SQL warehouse by the names on the board.
3. **Run the setup notebook once.** Open `week-03/setup/day-01-setup.ipynb` and attach it to the compute. In cell 1, set `CLASS_GROUP` to the group that holds the learners (`account users` holds every user of the account). The catalog `course` must exist, and you need `USE CATALOG` and `CREATE SCHEMA` on it. Run cells 1 to 5. Cell 4 should print these things:
   - `return_header`: 40 rows, no comment on `total_tax_amt` and `total_income`
   - `return_summary`: 40 rows
   - the tags `data_class = case_key` on `filer_key` and `role = label` on `exam_changed_tax`
4. **Give the learners read access.** Cell 5 does it: `USE CATALOG` on `course`, and `USE SCHEMA` and `SELECT` on `course.returns`, to `CLASS_GROUP`. Lineage in Catalog Explorer needs only `BROWSE` on the catalog, which these grants cover.
5. **Decide how learners get AI generate drafts (exercise 3).** AI generate needs the `MODIFY` privilege on a table. `MODIFY` also lets a learner save a comment, or change rows. Choose one:
   - Run cell 6. It grants `MODIFY` on `return_header`. Learners press **AI generate** themselves. Tell them again: never select the check mark.
   - Or do not run cell 6. Learners take their drafts from `week-03/day-01/exercise-03-find-and-check-two-drafts/drafts.md`, and you show **AI generate** once in the demo.
6. **Check AI generate.** As yourself, open `return_header` in Catalog Explorer, select the **Columns** tab, and check that **AI generate** shows above the column headings. Reload the browser tab, as exercise 3 tells learners, and check that no comment changed. Databricks says AI generate has no workspace toggle. Its models are Databricks' partner-powered AI features, which an account admin can turn off.
7. **Optional, for exercise 4's extra cell.** The lineage system table `system.access.column_lineage` needs grants from an account or metastore admin: `USE CATALOG` on `system`, `USE SCHEMA` on `system.access`, and `SELECT` on the table. Without them, the extra cell fails with a permission error and you show its result on your screen.

## In class

- Demo of exercise 1: count `course.returns.return_summary`. Exercise 1 uses `return_header`. Run one notebook cell before you attach compute, and read the message aloud.
- Demo of exercise 3: search the word `tax`. Then press **AI generate** on `return_header`, and read the draft for `total_tax_amt`, which has no comment. Close it unsaved. Run the column summary on it. The learners' first column is `total_income`.
- Demo of exercise 4: trace the column `adjustments_amt` of `return_summary`. Exercise 4 traces `non_wage_income`, and asks learners to predict `income_band`.

## After class, or after anyone saves a draft

Run cells 2 to 4 of the setup notebook again. They make each table again from the same rows, and put back the comments the course gave.

## Not yet checked in Databricks

The course team ran the exercises on a computer without Databricks, against a stand-in that holds the same rows. Each exercise's `decisions.md` says how, under "Where it ran". Check each item at your run-through, and tell the course team what differs:

1. The setup notebook runs on the class compute, cell 1 finds `day-01-course-data.py` beside it, and cell 3 registers the Python function `income_band` that the query calls.
2. Each exercise's check cell finds its `check.py` beside the notebook.
3. Catalog Explorer shows a copy icon beside a table's full name.
4. **AI generate** shows above the column headings for a learner with `MODIFY`, and gives a draft per column.
5. Reloading the browser tab closes AI generate's drafts without saving them.
6. In the lineage graph, clicking a table's box shows its columns.
7. The lineage graph of `return_summary` highlights `return_header.total_income` and `return_header.wages_amt` for `non_wage_income`. Write down what it shows for `income_band`.
