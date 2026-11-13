# Set up Monday in Databricks (week 3, day 1)

For the trainer. Monday's four exercises run in the class's Databricks workspace. Do these steps before class, in order. The course made up the tables: no row is a real taxpayer.

## Before Monday

1. **Get the files.** Sign in to the class workspace. Open your Git folder of the course (in the left bar, **Workspace**). Pull, so that the folder `week-03` is there: select the branch name at the top of the Git folder, then **Pull**.
2. **Start the compute.** Start the compute the class uses for notebooks, and the SQL warehouse for the SQL editor. Write down both names: the learners select them in exercise 1.
3. **Run the setup notebook once.** Open `week-03/day-01/setup/setup.ipynb` and attach it to the compute. In cell 1, set `CATALOG` to the course catalog and `CLASS_GROUP` to the group that holds the learners (`account users` holds every user of the account). You need `USE CATALOG` and `CREATE SCHEMA` on the catalog. Run cells 1 to 6. Cell 5 should print these three things:
   - 40, 40, 24, 40 and 40 rows
   - no comment on `total_income`, `interest_reported` and `payer_count`
   - the tag `data_class = pii` on `taxpayer_name` and `taxpayer_tin`
4. **Give the learners read access.** Cell 6 does it: `USE CATALOG`, `USE SCHEMA` and `SELECT` on the schema `case_selection`, to `CLASS_GROUP`. Lineage in Catalog Explorer needs only `BROWSE` on the catalog, which these grants cover.
5. **Decide how learners get AI generate drafts (exercise 3).** AI generate needs the `MODIFY` privilege on a table. `MODIFY` also lets a learner save a comment, or change rows. Choose one:
   - Run cell 7. It grants `MODIFY` on `returns`, `third_party_reports` and `exam_outcomes`. Learners press **AI generate** themselves. Tell them again: never select the check mark.
   - Or do not run cell 7. Learners take their drafts from `exercise-03-find-and-check-two-drafts/drafts.md`, and you show **AI generate** once in the demo.
6. **Check AI generate.** As yourself, open `returns` in Catalog Explorer, select the **Columns** tab, and check that **AI generate** shows above the column headings. Close the drafts without saving. Databricks says AI generate has no workspace toggle. Its models are Databricks' partner-powered AI features, which an account admin can turn off.
7. **Optional, for exercise 4's extra cell.** The lineage system table `system.access.column_lineage` needs grants from an account or metastore admin: `USE CATALOG` on `system`, `USE SCHEMA` on `system.access`, and `SELECT` on the table. Without them, the extra cell fails with a permission error and you show its result on your screen.
8. **Tell the learners the names.** Each learner notebook starts with `CATALOG = "workspace"`. If the course catalog has another name, write it on the board: learners change that one line.

## In class

- Demo of exercise 1: use `third_party_reports`. Exercise 1 uses `returns`. Run one notebook cell before you attach compute, and read the message aloud.
- Demo of exercise 3: search the word `wage`. Then press **AI generate** on `third_party_reports`, and read the draft for `interest_reported`, which has no comment. Close it unsaved. Run the column summary on it.
- Demo of exercise 4: trace the column `interest_gap` of `case_features`. Exercise 4 traces `income_gap`, and asks learners to predict `income_band`.

## After class, or after anyone saves a draft

Run cells 2 to 5 of the setup notebook again. They make each table again from the same rows, and put back the comments the course gave.

## Not yet checked in Databricks

The course team wrote and ran the exercises on a computer without Databricks, against a stand-in that holds the same rows (`../answers/exercise-01-tour-the-workspace/decisions.md`, section "Where it ran"). Check each item at your run-through, and tell the course team what differs:

1. The setup notebook runs on the class compute, and cell 1 finds `course_data.py` beside it.
2. Each exercise's check cell finds its `check.py` beside the notebook.
3. Catalog Explorer shows a copy icon beside a table's full name.
4. **AI generate** shows above the column headings for a learner with `MODIFY`, and gives a draft per column.
5. The lineage graph of `case_features` highlights `returns.wages` and `third_party_reports.wages_reported` for `income_gap`, and stops `income_band` at `income_bands`.
