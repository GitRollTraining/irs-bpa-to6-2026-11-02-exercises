# Exercise 1: decisions

The answer is `exercise.ipynb` beside this file, with the schema `course.learner_00`, the trainer's own.

## Each answer, and why

| Cell | Answer | Why |
|---|---|---|
| 1 | `schema = "course.learner_00"` | Each learner types their own number. The check fails on `course.learner_NN`. |
| 2 | add `.select("*", "_metadata.file_name")` after `.load(...)` | `_metadata` is a hidden column: the read must name it. Without it, `file_name` does not exist and cell 3 fails. This is the exercise's planted miss. |
| 3 | `predict_file_name = "no"` | Cell 2 printed no `file_name` column. Cell 3 selects it, so it fails. |
| 4 | `w2_element = "IRSW2"` | Each W-2 is an `<IRSW2>` element in `ReturnData` (`week-03/setup/day-03-course-data.py`, `xml_text`). |
| 6, test 2 | `assert rt.select("return_id").distinct().count() == rt.count(), ...` | No `return_id` twice. |
| 6, test 3 | `assert dep.count() == reader_count, ...` and `assert dep.join(rt, "return_id", "left_anti").count() == 0, ...` | Dependent rows equal week 2's reader's count; every dependent's `return_id` is in the return table. |

What else the check accepts: any assert lines that pass, since the check reads the tables, not the wording. The check reads `tests_ran`, which cell 6 sets only after every assert passed. Test 2 may also be written with `groupBy("return_id").count()`.

The kept answer's facts: 52 files, 52 rows in `return_table`, 77 dependents (week 2's reader counts 77), 62 W-2s.

## Where each rule comes from (for the trainer, never in a learner cell)

| Quote in the exercise | From |
|---|---|
| "The row tag `Return` makes one row of each return." (our words) | `days/day-03/curated.md` § Write the parsed returns into keyed tables, How it works in Databricks, item 1 ("For your files the row tag is `Return`."); deck slide 10 |
| "Hidden means you must name it in the read to get it." | the same section, item 3; deck slide 15 ("Hidden: there only when the read names it") |
| "The key of each return is the case key, never the taxpayer identification number." (our words) | rests on the same section, What the tables are, first bullet: "if it replaced the filer's taxpayer identification number with a substitute value, the key is the substitute value, never the original number." |
| "Returns a new row for each element in the given array or map." | the same section, item 2; deck slide 11 |
| "A table is not finished until its counts reconcile with the files." | the same section, The row-count check; deck slide 16 |
| "No `return_id` appears twice in the return table." | the same, second bullet |
| "counted by week 2's tested reader, the code you already trust", "Every `return_id` in the dependents table exists in the return table." | the same, third bullet |
| The assert form | Tuesday's exercise 1 (assertion cells), `days/day-02/curated.md`; "Write each count as a test, the way Tuesday wrote quality checks" (day 3 curated, The row-count check) |

The exercise is deck slide 21 (counted from 1 in `deck.json` `slides`).

## Kept fields

`return_table` keeps `return_id`, `filer_key`, `tax_year`, `filing_status`, `wages_amt`, `total_income`, `agi_amt`, `total_tax_amt`, `exam_changed_tax`, `tax_added_by_exam` and `file_name`. The name and the address stay out: a model of case selection does not need them, and Tuesday's record removes direct identifiers. The column names are the week's (`week-tables.md` of the round's plan). `tax_added_by_exam` is kept here on purpose: exercise 4 finds it and drops it.

Against Tuesday's kept record (`week-03/day-02/answers/exercise-02-field-record-and-case-key/decisions.md`, 8 columns): the same 8 names, each mapped from its XML element by one `.alias` line in cell 3 (`Filer/CaseKey` to `filer_key`, `TaxYr` to `tax_year`, `IndividualReturnFilingStatusCd` to `filing_status`, `WagesAmt` to `wages_amt`, `TotalIncomeAmt` to `total_income`, `AdjustedGrossIncomeAmt` to `agi_amt`, `TotalTaxAmt` to `total_tax_amt`; `return_id` is built from the case key and the year). `filing_status` is cast to a string, as Tuesday's batch types it. Three columns Tuesday's batch does not have: `exam_changed_tax` (the label), `tax_added_by_exam` (planted for exercise 4) and `file_name` (the count test's file name). Two forms differ: Tuesday's `return_id` looks like `R-2026-0004`, Wednesday's like `F-30037-2023`; Tuesday's `filer_key` is a 16-character hash made in class, Wednesday's is the trainer's case key such as `F-30037`.

## Week 2's reader

Week 2's reader is `form1040.py`, function `dependent_relationships(path)`, from week 2's day 3 exercise 4 (`week-02/day-03/exercise-04-a-repeated-element`). The learner's own copy lives in `lab/`, a separate Git repository on the Workstation that `start.py` builds and the course's clone ignores, so it is not in the Databricks Git folder. The exercise imports the course's tested copy, `week-02/day-03/answers/exercise-04-a-repeated-element/files/form1040.py`: the same file and function names, the reader week 2's exercise 4 ends with. Its namespace (`http://www.irs.gov/efile`) matches Wednesday's files.

## Where it ran

- Not run in Databricks: this machine has no Databricks access. A trainer gap (`week-03/setup/day-03-setup.md` § Not yet checked in Databricks, items 2 and 3).
- Run on a laptop, 2026-11-13: a stand-in in plain Python wrote the 52 files from `day-03-course-data.py`, read them with ElementTree in place of Spark's XML reader, built the three tables as the answer's cells do, ran the three tests, and counted the dependents with week 2's reader, unchanged (77 = 77). `values.json` holds the facts the check read. `commands.sh` prints `Not yet: 6 left.` on the start and `Done:` on the answer, on Python 3.10 and on the laptop's Python 3.
- Every SQL statement of `check.py` parsed with sqlglot 30.31, dialect `databricks`.

## Pages behind the steps (opened 2026-11-13)

| Step | Page | Sentence |
|---|---|---|
| read with `rowTag` | https://docs.databricks.com/aws/en/query/formats/xml | "You must specify the `rowTag` option to indicate the XML element that maps to a `DataFrame` `Row`." Also: "XML file format support requires Databricks Runtime 14.3 and above." |
| `_metadata.file_name` | https://docs.databricks.com/aws/en/ingestion/file-metadata-column | "The `_metadata` column is a _hidden_ column, and is available for all input file formats." |
| `explode` | https://docs.databricks.com/aws/en/pyspark/reference/functions/explode | "Returns a new row for each element in the given array or map." |
| `saveAsTable`, `overwrite` | https://docs.databricks.com/aws/en/pyspark/reference/classes/dataframewriter/saveAsTable | "Saves the content of the `DataFrame` as the specified table." "When `mode` is `'overwrite'`, the schema of the `DataFrame` does not need to match the existing table schema." |
| listing the volume, reading files by path | https://docs.databricks.com/aws/en/volumes/volume-files | "This makes them ideal for machine learning frameworks and open source Python modules that require POSIX-style access." |
| importing `form1040` by `sys.path` | https://docs.databricks.com/aws/en/files/workspace-modules | "To import modules from another directory, you must add the directory containing the module to `sys.path`." |

## Modelled on

Microsoft course DP-750, Lab 07, "Ingest data into Unity Catalog", https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/07-ingest-data-into-unity-catalog.html: "Load CSV data from a managed volume into a Delta table using PySpark DataFrames" (found in the downloaded page). Shape taken: files in a volume, read with `spark.read`, written as catalog tables. Ours reads XML, explodes two child tables, and turns the counts into tests. The page states no time and no row-count step.
