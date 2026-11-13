# Exercise 1: decisions

For the trainer. Exercise 1, "Tests that fail the dirty batch", follows the demo of one test, wages never below 0, on the clean batch and then the dirty batch. Modelled on Microsoft Learning's DP-750T00 lab 9, "Implement and Manage Data Quality Constraints in Unity Catalog" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/09-implement-manage-data-quality-constraints-unity-catalog.html): its null, allowed-value and range checks, each with a warn, drop or fail action, written here as assertion cells (week 2's test form) rather than pipeline expectations. The actions follow Databricks, "Manage data quality with pipeline expectations" (https://docs.databricks.com/aws/en/ldp/expectations), opened 2026-11-13: "Expectations use standard SQL Boolean statements to specify constraints." Shape: "Write, run, read the result". The check is `check.py` in the exercise folder.

## 1. Tests 1 and 2, from Monday's columns

- **The answer.** Monday's kept columns are `total_income` and `wages_amt` (Monday's exercise 3 answer). Test 1: completeness, fail, `total_income IS NOT NULL`. Test 2: validity, fail, `wages_amt >= 0`.
- **Reason.** Step 2's rule table: `wages_amt` is an amount never below 0, so validity, `>= 0`; `total_income` is any other column, so completeness, `IS NOT NULL` (it can be below 0 with losses). Step 2's action table: both columns had an empty count of 0 on Monday, so fail: one bad row means the feed is broken.
- **The notebook lines.** "The intuitions you hold about returns, from years of Compliance work, are the expectations. Write them down first, then compare them to the data." The two kind definitions. "either the entry is wrong or losses are recorded in the same column." (Monday).
- **What else the check accepts.** Any rule that runs on both batches and passes the clean one, any of the five kinds, any action. A learner with no Monday columns takes the course's pair, `agi_amt IS NOT NULL` (fails the dirty batch, 2 rows) and `wages_amt >= 0`.

## 2. The given test, and the predictions

- **The answer.** Test 3, uniqueness, fail, `count(*) OVER (PARTITION BY return_id) = 1`: fails the dirty batch, 2 rows (F-30259-2022 twice). The kept predictions: test 1 fails (wrong: it passes), tests 2 to 4 fail (right). A wrong prediction is kept on purpose: the step asks to compare.
- **What else the check accepts.** `fails` or `passes` for each test; it does not judge whether the prediction was right.

## 3. The run on each batch

- **The answer.** Clean batch: four `PASS` lines. Dirty batch: `PASS` for test 1; `FAIL` for test 2 (1 row, F-30185-2023, wages -1) and test 3 (2 rows); `WARN` for test 4 (1 row, F-30333-2021).
- **Why test 1 passed.** No fault of this kind is in `total_income`; the empty values of the dirty batch are in `agi_amt`. The check asks for `passed_why` of 5 words or more on each test that passes the dirty batch.
- **The notebook lines.** "a check that is too strict stops good batches too." "Either way the result you keep is the same: the test, and the run where it failed the dirty batch." "Invalid records are written to the target." "Invalid records prevent the update from succeeding."

## 4. Test 4, a kind not yet used

- **The answer.** Consistency, warn, `wages_amt <= total_income`: fails 1 row. Warn, as step 5's table gives it: a person should read that return, as a business loss can make total income smaller than wages, so the row may be right.
- **The notebook lines.** "Checks only for completeness. Every field is filled and every value is wrong. Caught by listing your checks against the five kinds and seeing which kinds have none." The consistency definition and its example, "wages on the return do not exceed the total income on the same return".
- **What else the check accepts.** Any kind tests 1 to 3 do not use. Freshness, `tax_year BETWEEN 2021 AND 2023`, fail, fails 2 rows (tax year 2019). Validity, `filing_status IN ('1', '2', '3', '4', '5')`, passes the dirty batch: no fault was put in filing status.

## 5. The optional part

`count(*) OVER (PARTITION BY tin, tax_year) = 1` fails 4 rows: F-30111-2022 and F-30629-2022 (one return filed again under a new `return_id`, every value in range), and the copied F-30259-2022. The optional part names the fault and the rule, so the answer only confirms it. The check reads the first four tests only.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks: `check.py` ran each rule on the setup's rows in SQLite (`week-03/setup/day-02-course-data.py`, `local_db`). Start: `Not yet: 4 left.` Answer: `Done: 4 tests pass the clean batch; on the dirty batch: completeness passes, validity fails, uniqueness fails, consistency fails.` Every rule and query was parsed by sqlglot 30.31.0, dialect `databricks`. The notebook's cells did not run in a kernel: no Spark on that computer.
- Trainer gaps, at the run-through (`week-03/setup/day-02-setup.md`, Not yet checked, items 1 and 2): `run_test` with a window rule inside `F.expr`, on the class compute; the check cell finds `check.py`.

## Where each quote comes from

The curated file is `days/day-02/curated.md` in the Program repository, except where Monday's is named.

| Quote in the notebook | Heading, line |
|---|---|
| "The intuitions you hold about returns, ..." | Name the kind of check each field needs, line 139 |
| "Completeness describes ...", "Validity describes ...", "Uniqueness describes ...", "Consistency describes ..." | same section, lines 122 to 125 |
| "every return has a tax year and an adjusted gross income"; "the filing status is one of the allowed codes"; "wages on the return do not exceed the total income on the same return"; "the batch holds the tax years it says it holds" | same table, lines 122 to 126 |
| "either the entry is wrong or losses are recorded in the same column." | `days/day-01/curated.md`, Check a dictionary entry against the column's metadata, line 471 |
| "For the checks that decide whether a batch is usable, ..."; "keep warnings for what a person should look at later." | Write a data expectation as a test that fails a bad batch, line 83 |
| "the data looks perfectly fine for the training code, since -1 is an acceptable value for the int feature." | same section, lines 63 to 64 |
| "Invalid records are written to the target."; "Invalid records prevent the update from succeeding." | same section, lines 77 to 78; deck slide 7 |
| "Either way the result you keep is the same: ..." | same section, line 106 |
| "a check that is too strict stops good batches too." | The trade-off, line 448 |
| "Checks only for completeness. Every field is filled ..." | Where today's work goes wrong, line 433 (bold in the curated file) |

The exercise is deck slide 19, "Exercise 1: Expectations that fail, each one's kind".
