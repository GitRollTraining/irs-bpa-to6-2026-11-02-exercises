# Exercise 1: decisions

For the trainer. The exercise is deck slide 30, "Exercise 1: The question, the list, each verdict". Each section gives one thing the learner does, the answer and its reason. It also gives where the rule is taught and what else the check accepts. The check is `check.py` in the exercise folder. It reads `record.json`, which cell 2 writes. `files/record.json` holds the kept answer. The check calls no model.

## 0. The tables in the catalog

- **What the learner does.** In Catalog Explorer, the learner opens the course catalog, the schema `case_selection` and its three tables. The learner reads each table's comment and each column's comment, and looks at the **Sample Data** tab. Then cell 1 lists the eight fields from the catalog with `DESCRIBE TABLE`.
- **Why.** Monday is the day learners meet the workspace. The fields come from the catalog. So the learner decides from the catalog's own descriptions, as the afternoon's exercises do.
- **Where it is taught.** Deck slide 8, "Today's order: sign in, find, attach, run": "Catalog Explorer: find the return tables". Deck slide 9, "Catalog Explorer shows a table's columns before you query it": "Catalog, then schema (a folder of tables), then table" and "Comment: text someone wrote about a column". The Opening's live build opens Catalog Explorer. Talk segment 1's demo opens "the course catalog, a schema, a return table" and points at Columns.
- **What the day teaches after the slot.** Deck slide 35 teaches the three-part name, after the exercise. So step 1 gives the name the learner types in full, with an example. `DESCRIBE TABLE` sits in the code under "You do not need to read the code below this line".
- **The fallback.** Sometimes cell 1 cannot read the tables: no schema typed, a wrong name, no permission, or no Databricks. Then it reads `fields.csv` and prints why on its second line. `fields.csv` holds the same comments as the catalog. So every later step works with either source.
- **Who makes the tables.** The trainer, once per workspace, with `setup-tables.ipynb` beside this file. Its first cell gives the steps and the privileges.

## 1. The question

- **The answer.** "For each return filed this year, how likely is an examination to change the tax?"
- **Reason.** It names the unit (one return) and the target (a change to the tax, yes or no). It also names the time (this year's returns).
- **Where it is taught.** Monday's curated file, § Let the question decide the data: "That sentence names the unit (one return), the target (a change, yes or no) and the time (this year's returns)." The target, from the same section: "A measurable stand-in is whether an examination of the return ended with a change to the tax."
- **What else the check accepts.** Any sentence with three things in it: "return", a form of "change" with "tax", and "year" or a year in digits. A question about being "selected for review" fails. The target of this week is whether an examination changed the tax.

## 2. The kinds

- **The answer.** `wages_amt` and `total_income_amt`: line item. `w2_wages_amt`: compare. `exam_changed_tax` and `exam_picked_by`: outcome. `taxpayer_name`, `tin` and `street_address`: none.
- **Reason.** The three kinds are the three parts of the reading's list. They are the return's own line items, information to compare with the return, and the outcome of past examinations. Each column's comment says which part it holds. The identifying fields are none of the three.
- **Where it is taught.** Curated file, § Pick the information that helps select a case. Step 3 quotes each item of its numbered list. The table's row for information matching: "Third-party reports, such as wage and interest statements, to compare with the return". Item 3 of the list names "a record of which outcomes came from a random sample and which from returns an earlier score chose". So `exam_picked_by` is an outcome.
- **What else the check accepts.** Only these kinds. The kind is what the field holds, so it has one answer.

## 3. The verdicts

- **The answer.** Needed: the five line item, compare and outcome fields. Not needed: `taxpayer_name` and `street_address`. Transform: `tin`.
- **Reason.** "Keep a field only if the prediction needs it." A name or an address identifies a person and tells the ranking nothing. The identifying number is in all three tables, so the learner keeps it for the join. Tuesday replaces its value with a substitute value.
- **Where it is taught.** Deck slide 26, right column: "Keep a field only if the prediction needs it". The same column: "A name or identifying number tells the ranking nothing it needs". Deck slide 28, the verdict record's row for the name: "Not needed: left out". Its row for the identifying number: "Needed, to be transformed". The curated file, last paragraph of § Leave out what the use does not need, gives the three verdicts.
- **What else the check accepts.** `tin` takes only `transform`. Slide 26 and the curated file say the ranking has no need for an identifying number. Both read as "not needed". Slide 28 rules the same field "Needed, to be transformed" because it joins tables. The column's comment says it "joins the three tables". Step 1 asks which column is in all three tables. So the check keeps slide 28's verdict. Take it to the debrief. Both sources are right about different uses: the model's input, and the join.

## 4. The two fields in the guide table

- **What changed on 2026-11-13.** Step 3's guide table gave the kind and the verdict of all eight fields. A cold reader said the table makes the exercise "closer to copying than deciding". Now each column's comment says what the field holds, and the learner reads it in Catalog Explorer. So the table gives two fields, already filled in cell 2: `wages_amt` (line item, needed) and `taxpayer_name` (none, not needed). The learner decides the other six. The check names each wrong field and what to read again, but never the right value. This change waits for the program owner's ruling.
- **The question and the target line.** A cold reader on 2026-11-13 found that it could paste step 2's example question and step 4's example target line, and pass. Now step 2's example has the same form for a different case, a refund claim. Step 4 gives the target line's three parts in a table, each with its source, and no whole sentence. The reading still holds both sentences, so the trainer reads the learners' own wording in the debrief.
- **The verdict definitions.** The same reader could not choose between `needed` and `transform` for `exam_picked_by`, and asked whether the target is `needed`, since the model does not read it as an input. Step 3 now defines each verdict. `needed`: the model or the training reads the value. `transform`: the model never reads the value, but the field does a job, such as a join. A second reader found the rule, "Keep a field only if the prediction needs it", at odds with that definition. So step 3 now says the prediction needs a field when the model reads its value, or when the training reads it.
- **Why these two.** One shows a kept field and one a field left out. The learner decides the three hardest: `w2_wages_amt` (the only compare), `exam_picked_by` (an outcome that is not the target) and `tin` (the only transform).
- **Where the two reasons come from.** `wages_amt`: the curated file, § Let the question decide the data, quoting Google's rules: "Start with directly observed and reported features as opposed to learned features." `taxpayer_name`: deck slide 26, "A name or identifying number tells the ranking nothing it needs".

## 5. The explain sentence

- **The answer.** `exam_picked_by` tells outcomes from a random sample apart from outcomes of returns a score chose. A model trained only on the score's picks "never learns what the unchosen returns look like".
- **Where it is taught.** Curated file, § Pick the information that helps select a case: "The rule is to know which outcomes came from a random sample and which from a score". Deck slide 18, "Outcomes of score-chosen returns hide the unchosen ones".
- **What else the check accepts.** Any sentence with the word "random". This is the exercise's explain question. The curriculum's method file `docs/methods/teaching-from-the-baseline.md` § 5 asks for one in each exercise.

## 6. The reasons

- **The answer.** Any reason of three words or more. The kept answer's reasons are in `files/record.json`.
- **Reason.** A reason is a judgment in the learner's words. So the check reads its length only. The trainer reads the reasons in the debrief.

## 7. The target line

- **The answer.** "We predict a change to the tax, yes or no, because examiner time is scarce. We considered predicting the amount, which moves audits toward higher incomes, and we note that cost."
- **Where it is taught.** Curated file, § Leave out what the use does not need: "So the anchor question needs one more line before you search: a recorded choice of target." Deck slide 27: "Predicting the amount: higher incomes".
- **What else the check accepts.** Any line with a form of "change" and the word "amount".

## 8. The statements the setup notebook runs

Each row gives a page of Databricks' public documentation. The author opened each page on 2026-11-13.

| Statement | What the setup uses it for | The page, and its words |
|---|---|---|
| `CREATE SCHEMA IF NOT EXISTS ... COMMENT '...'` | the schema `case_selection` | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-schema: "CREATE SCHEMA [ IF NOT EXISTS ] schema_name [ COMMENT schema_comment" |
| `CREATE OR REPLACE TABLE ... (column type COMMENT '...', ...) COMMENT '...'` | each table, its column comments and its table comment | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-ddl-create-table-using: a column's properties include "COMMENT column_comment". The table clauses include "COMMENT table_comment". OR REPLACE: "If specified, replaces the table and its content if it already exists." |
| `INSERT INTO ... VALUES (...), (...)` | the made-up rows | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-dml-insert-into: "INSERT INTO students VALUES" with several rows |
| A string literal | each comment | https://docs.databricks.com/aws/en/sql/language-manual/data-types/string-type: a backslash escapes an apostrophe, as in `'O\'Connell'`. From Databricks Runtime 18.0, SQL joins two literals side by side. So no comment holds an apostrophe |
| `GRANT ... ON ... TO` | cell 4, only if learners cannot see the schema | https://docs.databricks.com/aws/en/sql/language-manual/security-grant: "GRANT privilege_types ON securable_object TO principal". https://docs.databricks.com/aws/en/admin/users-groups/groups: "Each account includes an `account users` group containing all users and service principals." |
| `DESCRIBE TABLE` | the learner's cell 1, and the setup's cell 3 | https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-aux-describe-table: "The metadata information includes column name, column type and column comment." The page names no privilege for it |

**The learners' privileges.** The privileges page says: "to read from a table, a user needs `SELECT` on the table, `USE CATALOG` on the parent catalog, and `USE SCHEMA` on the parent schema." (https://docs.databricks.com/aws/en/data-governance/unity-catalog/manage-privileges/privileges). On the same page, `BROWSE` lets a user "Discover objects, view their metadata, and request access to them without needing `USE CATALOG` or `USE SCHEMA`". `BROWSE` gives no rows. The **Sample Data** tab and cell 1 read the tables. So the learners need `USE CATALOG`, `USE SCHEMA` and `SELECT`. Cell 4 of the setup grants them.

**Catalog Explorer.** It opens from "**Catalog** in the sidebar" (https://docs.databricks.com/aws/en/catalog-explorer/). "Select the **Columns** tab to view table columns." "Select the **Sample Data** tab to view sample data. You must have access to active compute to sample data." (https://docs.databricks.com/aws/en/discover/database-objects). An existing comment "appears in the right pane on the Overview tab or below the object name". A user adds a column's comment from its "column row" (https://docs.databricks.com/aws/en/comments/). No page that the author read says in words that the Columns tab shows each column's comment. Deck slide 9 says it does. The reviewer checks it (`run-in-databricks.md`, step 7).

## 9. Where it runs

- The author ran it on 2026-11-13 on a laptop, not in Databricks. The machine that wrote it has no Databricks access. The runs are in `kept-run.md`.
- **Trainer gap.** A trainer or reviewer with access to the course's Databricks workspace runs `setup-tables.ipynb` once. Then they run the exercise as a learner, by the steps in `run-in-databricks.md`. The run checks four answers we propose. First, the setup's SQL runs as written. Second, the **Columns** tab shows each column's comment. Third, cell 1 reads the catalog with `spark.sql` on the course's compute. Fourth, cell 2 can write `record.json` beside the notebook in a Git folder. If one fails, the fix goes in the cells, not in the learner's steps.

## Findings of the readability linter inside quotes

- Step 3 of the README quotes item 3 of the curated file's list, 30 words. The quote keeps the curated file's words.
- Sections 0, 1, 5 and 7: four "Where it is taught" lines hold a sentence over 25 words. Each runs long inside a quote.
