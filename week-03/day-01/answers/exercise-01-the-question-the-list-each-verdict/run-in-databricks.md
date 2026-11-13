# Exercise 1: run it in Databricks

For a reviewer or trainer with access to the course's Databricks workspace. The machine that wrote the exercise has no Databricks access, so nobody made these runs yet (a trainer gap, `decisions.md` § 9). Write down what each step showed, and anything that differs.

## Set up, once per workspace

1. Sign in to the workspace. In the sidebar, select **Workspace**, then **Create > Git folder**. Paste the course repository's address in **Git repository URL**, and select the branch to test.
2. In the Git folder, open `week-03/day-01/answers/exercise-01-the-question-the-list-each-verdict/setup-tables.ipynb`. Attach it to the compute the learners use.
3. In cell 1, set `SCHEMA` to the course catalog's name, a dot, and `case_selection`. Run cell 1. Expected: no output.
4. Run cell 2. Expected: `Made <catalog>.case_selection with returns, wage_statements and exam_outcomes. Run cell 3.`
5. Run cell 3. Expected: `returns: 30 rows`, `wage_statements: 30 rows`, `exam_outcomes: 12 rows`, and under each its columns with their types and comments, as in `kept-run.md` § The setup notebook and the catalog path.
6. If a learner account cannot see the schema in Catalog Explorer, run cell 4. Expected: `Granted USE CATALOG, USE SCHEMA and SELECT on <catalog>.case_selection to account users.`

## The learner's path, from a learner account if you have one

7. In the sidebar, select **Catalog**. Open the course catalog, then `case_selection`. Expected: three tables. Open `returns`. Expected: the table's comment below its name, "One row per return filed this year. Made up by the course ...". Select **Columns**. Expected: each column's row shows its comment. Write down whether it does.
8. Select **Sample Data**. Expected: rows such as `000-00-0001`, `Made-up Taxpayer 01`.
9. Open `week-03/day-01/exercise-01-the-question-the-list-each-verdict/exercise.ipynb` from the Git folder. Attach it to the same compute.
10. In cell 1, type `<catalog>.case_selection` between the quotes. Run cell 1. Expected: `Read from the catalog: <catalog>.case_selection`, then eight lines, `tin` with all three tables.
11. Run cell 2, then cell 3. Expected: `Saved record.json. Now run cell 3.`, then `Not yet: 9 left.` and nine lines.
12. Put the values of `files/record.json` (beside this file) in cell 2, run cell 2, then cell 3. Expected: `Done:`.
13. Type a wrong schema name in cell 1, such as `<catalog>.no_such_schema`, and run it. Expected: `Read from fields.csv, the copy beside this notebook.`, a line that starts `Why:`, and the same eight lines.
14. Open `week-03/day-01/answers/exercise-01-the-question-the-list-each-verdict/exercise.ipynb`, change `training` in cell 1 to the course catalog's name, and run cells 1 to 3. Expected: `Read from the catalog: ...` and `Done:`.

On serverless compute, step 11 or 12 can fail because the working folder is not the notebook's folder. Then the cells need an absolute path. Databricks says "On serverless compute, the working directory is not guaranteed, so use absolute paths to reference files." (https://docs.databricks.com/aws/en/files/workspace-modules).
