# Exercise 2: decisions

For the trainer. Exercise 2, "The field record and the case key", follows the worked example, where the trainer fills the rows for `tin` and `filing_status` and runs cell 3. Modelled on DataCamp's "Data Privacy and Anonymization in Python" (https://www.datacamp.com/courses/data-privacy-and-anonymization-in-python; 3,907 enrolments on the page, opened 2026-11-13), its chapter 1 exercise "Is it sensitive or non-sensitive?" before suppression and masking: here each field is classed by the IRS order of questions, then removed or replaced. Shape: "Decide, record, then run". No tag is set by learners (the program owner's ruling of 2026-11-13: "No tag in the exercise"). The check is `check.py` in the exercise folder.

## 1. Need, class and action, per field

| Field | needed | class | action | Reason, and the notebook line |
|---|---|---|---|---|
| `return_id` | yes | sensitive but unclassified | keep | it names one return of a tax account (FTI by "If related to a tax account, categorize it as FTI"), and tells returns apart without naming the filer |
| `tin` | no | sensitive but unclassified | transform | filled as the worked example: FTI; the model needs no number (needed: no), but Wednesday matches a filer's returns, so a case key replaces it (transform, the one field step 2 allows it on) |
| `taxpayer_name`, `street_address` | no | sensitive but unclassified | remove | "The name and street address are FTI too, because they sit on a return, and they also identify a person; the use does not need them." |
| `zip_code` | no | sensitive but unclassified | remove | "A ZIP code alone names nobody; joined to a birth date and a filing status it may name one person." No feature on Wednesday uses a region |
| `filing_status` | yes | sensitive but unclassified | keep | filled as the worked example: "It needs the income figures, the filing status and the tax year." |
| `wages_amt`, `agi_amt`, `total_income`, `total_tax_amt` | yes | sensitive but unclassified | keep | the income figures the use needs; FTI from the return |
| `tax_year` | yes | sensitive but unclassified | keep | the use ranks this year's returns and learns from earlier years |
| `received_date` | no | sensitive but unclassified | remove | the date the IRS received one return of a tax account, so FTI; the day it arrived says nothing about the return's lines. Step 2's table now gives remove; the debrief asks what keeping it would risk |
| `loaded_by` | no | personally identifiable | remove | a clerk's user name: "A field that is personally identifiable but not FTI is one that names a person with no tax account behind it" |
| `batch_id` | no | neither | remove | it names no person and no tax account |

Monday's verdicts in the kept answer come from Monday's kept list (its exercise 2 answer): wages needed, total income needed, the name not needed, the identifying number transformed (the filled `tin` row copies that verdict); the other fields `not listed`. Step 2 gives the course's mapping from a Monday item to a field.

**What else the check accepts.** Any of Monday's three verdicts or `not listed`; `yes` or `no`; any class except `neither` on a field that names a person (`tin`, `taxpayer_name`, `street_address`, `loaded_by`); any action except `keep` on a field the use does not need or one that names a person, and `transform` only on `tin` or `zip_code`; a reason of 4 words or more. It does not judge whether `received_date` is needed, or whether `zip_code` is removed or transformed.

## 2. The prepared data, and the case key

- **The answer.** 8 columns: `return_id, filing_status, wages_amt, agi_amt, total_income, total_tax_amt, tax_year, filer_key`. The assertion passes. It checks the four fields that name a person (`tin`, `taxpayer_name`, `street_address`, `loaded_by`) against the prepared columns, so it fails when a learner keeps one of them; before 2026-11-13 it checked the record's removed fields, which the cell had just dropped, so it could never fail. The first three rows shown are F-30037's returns of 2021, 2022 and 2023, with one `filer_key`. Wednesday's files carry the trainer's case keys (such as F-30037), made by the same rule with the trainer's own secret, so the values differ from the cell's.
- **How the case key is made.** `filer_key` is the first 16 characters of SHA-256 of a secret and the number. The secret is `secrets.token_hex(16)`, made new on each run and never saved, so the same number gets the same key within a run, and nobody can work back from a key. This stands in for the trainer's protected lookup table, which no learner reads; Wednesday's files already carry the trainer's keys. Curated: "replace the taxpayer identification number with a random case key, kept in a protected lookup table"; and of hashing, "if a hashing key is not used or is discovered, 'it is possible for an attacker to perform a brute force search'".
- **Explain (kept).** "The key lets Wednesday match a filer's returns across tax years, and without the secret nobody can work back from it to the number." The check asks for 8 words or more.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks: `check.py` built the prepared columns from the record and the setup's column list. Start: `Not yet: 13 left.` Answer: `Done: 14 fields recorded; the prepared data has 8 columns: return_id, filing_status, wages_amt, agi_amt, total_income, total_tax_amt, tax_year, filer_key.` Cell 3 did not run in a kernel: no Spark on that computer.
- Trainer gap, at the run-through (`week-03/setup/day-02-setup.md`, Not yet checked, item 3): cell 3 runs on the class compute.

## Where each quote comes from

`days/day-02/curated.md` in the Program repository:

| Quote | Heading, line |
|---|---|
| "You cannot decide what to remove until each field has a class." | Mark each field as sensitive but unclassified, personally identifiable, or neither, line 191 |
| the three questions of the IRS order; "Federal tax information is a kind of sensitive but unclassified data" | same section, lines 210 to 217 |
| "The name and street address are FTI too, ..."; "A field that is personally identifiable but not FTI ..." | same section, lines 234 to 236 |
| "A ZIP code alone names nobody; ..." | same section, line 205 |
| "the model must decide which returns to examine."; "It needs the income figures, ..." | Keep only the data the use needs, lines 182 to 183 |
| "A field that never enters the training data cannot reach a score, a prompt or an output." | same section, line 166 |
| "The record you keep for each field: ..." | Remove or transform a field before it reaches a feature, a prompt or an output, line 287 |
| "with a stand-in that still lets you match rows"; "it is possible for an attacker to perform a brute force search"; "information for the transformation", "must be highly protected" | same section, lines 255 to 264 |

The exercise is deck slide 47, "Exercise 2: Record, mark and prepare the fields".
