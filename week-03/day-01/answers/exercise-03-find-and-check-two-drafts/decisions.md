# Exercise 3: decisions

For the trainer. Exercise 3, "Find two of your items and check two drafts", follows the demo of one search, one draft and one check on `return_header.total_tax_amt`, the other column with no comment. Modelled on Microsoft Learning's DP-750T00 lab 5, "Govern Unity Catalog Objects" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/05-govern-unity-catalog-objects.html), its comments step and its warning on assistant output; the draft step follows Databricks, "Add AI-generated comments to Unity Catalog objects" (https://docs.databricks.com/aws/en/comments/ai-comments). Shape "Direct an AI tool, check what it made". The check is `check.py` in the exercise folder.

## 1. The search

- **The answer.** `word = "income"` returns two columns of `course.returns.return_header`: `agi_amt` (its comment says adjusted gross income) and `total_income`. A second word from the learner's list, such as `wage`, finds `wages_amt`.
- **Reason.** The columns view of the information schema has one row per column the learner may see. The query keeps `return_header`'s columns and matches the word in the column's name or its comment.
- **The notebook line.** "A table missing from your results may exist and be one you lack permission to see."
- **What else the check accepts.** The check does not read the search. Any two columns of `return_header` count.

## 2. The drafts

- **The answer.** `total_income`: "Annual income in dollars, always positive." `wages_amt`: "Wages, salaries and tips reported on the return, in dollars." Both from `drafts.md`. A draft from AI generate can differ in its words.
- **Reason.** AI generate reads the column's name and the table's schema, not its values. `total_income` has no comment, so its draft comes from the name alone.
- **The notebook lines.** "Comments are powered by a large language model (LLM) that takes into account object metadata, such as the table schema and column names." "AI models are not always accurate and comments must be reviewed prior to saving."
- **What else the check accepts.** Any draft of 3 words or more. The check never judges the draft's wording. Step 2 sends a learner to `drafts.md` when the AI generate draft says nothing the values could contradict, so every learner meets a draft the values refute.

## 3. The facts and the prediction

- **The answer.** `total_income`: `INT`, no comment, no tags, 0 empty, smallest -10565, largest 97900. `wages_amt`: `INT`, comment "Wages, salaries and tips the filer reported, in whole dollars.", no tags, 0 empty, smallest 29750, largest 98000. The prediction: above zero, as the name says income, but losses could make it negative.
- **Reason.** Eight of the 40 made-up returns report a business loss larger than their wages and interest (`week-03/setup/day-01-course-data.py`, `header_rows`), so their total income is below 0.
- **The notebook lines.** "Compare the entry's type with the column's type in the catalog." "Compare the entry's description with the column's comment, where one exists." "Query the column: its empty count, its smallest and largest values, a sample of distinct values."
- **What else the check accepts.** Numbers typed as text, with or without commas; the type in any case. The check reads each column's type, empty count, smallest and largest value again, and compares. A `predict` of 5 words or more.

## 4. The verdicts

- **The answer.** `total_income`: change, because the smallest value is below 0, so losses sit in the same column. `wages_amt`: keep, because the type, the comment and the values agree with the draft.
- **The notebook lines.** "A description that says always present fails on one empty row." "Write what you checked and what you found beside the entry, so a reader can see the check, not only the verdict."
- **What else the check accepts.** `keep` or `change`, with a reason of 4 words or more. It refuses `keep` only where the draft says positive (or never negative) and the smallest value is below 0, or says always present (or never empty, not null) and the empty count is above 0. `exam_changed_tax` has 27 empty rows, for a learner who picks it.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks: the notebook's cells in order, with a stand-in for `spark` that runs the same SQL on DuckDB over the setup's rows, and an information schema built from the setup's column list. The start printed `Not yet: 3 left.`. The answer printed `Done: 2 entries, each with its check: return_header.total_income (change), return_header.wages_amt (keep).` `commands.sh` printed the same on Python 3.10 and 3.14.
- Trainer gaps, at the run-through: (1) **AI generate** shows above the column headings for a learner with `MODIFY` (Databricks' page: "you must be the object owner or have the `MODIFY` privilege"), and its draft per column; (2) reloading the browser tab closes the drafts without saving them, as step 2 tells learners; (3) the views `course.information_schema.columns` and `course.information_schema.column_tags` answer the cell's queries on the class compute.

## Where each quote comes from

The curated file is `days/day-01/curated.md` in the Program repository, all under "Check a dictionary entry against the column's metadata" except the first row. The day's deck is being rebuilt, so no slide number is given.

| Quote in the notebook | Heading, line |
|---|---|
| "A table missing from your results may exist and be one you lack permission to see." | Find governed data through Unity Catalog, line 370 |
| "Comments are powered by a large language model (LLM) ..." | line 451 |
| "AI models are not always accurate and comments must be reviewed prior to saving." | line 455 |
| "Compare the entry's type with the column's type in the catalog." | line 464 |
| "Compare the entry's description with the column's comment, where one exists." | line 465 |
| "Query the column: its empty count, ..." | line 466 |
| "A description that says always present fails on one empty row." The curated file puts *always present* in italics. | line 467 |
| "Write what you checked and what you found beside the entry, ..." | line 468 |
| "The model should not be relied on for data classification tasks such as detecting columns with PII." | line 457 |

## Findings of the linter inside quotes

- "Comments are powered by ...": passive voice (Databricks' sentence).
