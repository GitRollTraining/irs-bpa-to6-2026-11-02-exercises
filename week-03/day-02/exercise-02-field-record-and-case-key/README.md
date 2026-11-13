# Exercise 2: The field record and the case key

**Goal:** After this exercise, you can record each field's need, class and action, and prepare the batch so no field that names a person survives.

**Scenario:** On Wednesday this batch becomes features. Before that, each field gets a row in a record: does the use need it, what is its class, and what happens to it. A given cell then prepares the batch from your record.

**AI tool:** none.

**Where you work:** the notebook `week-03/day-02/exercise-02-field-record-and-case-key/exercise.ipynb` in your Git folder of the course, in Databricks. Attach the notebook to the compute the trainer names.

**Done when:** cell 4 prints `Done:`: every field of the batch has its row, and the prepared data holds no removed field.

**Optional part:** none.

**What you have:**

- Your notebook of Monday's exercise 2: your list, each item with its verdict.
- The dirty batch `course.returns.batch_dirty`: 14 fields. The course made up every row.
- In cell 2, a record with one row per field. The course filled the rows for `tin` and `filing_status`.
- `check.py`, beside this notebook. Cell 4 runs it.

**Start from:** this notebook as the course gives it. The trainer just filled the rows for `tin` and `filing_status` and ran cell 3. To start again, set the values you typed back to `""`.

### Step 1. See the batch's fields

Why: "You cannot decide what to remove until each field has a class." First read what each field holds.

Run cell 1. `DESCRIBE TABLE` lists a table's columns. You should see a table of 14 rows: each field's name, its type and its comment. The comment says what the field holds. Step 2 uses it for each field. The dirty batch has the same fields as the clean one.

Notebook cell 1:

```python
# 1. The batch's fields: name, type and comment.
display(spark.sql("DESCRIBE TABLE course.returns.batch_dirty"))
```

### Step 2. Fill the record: need, class and action for every field

Why: "The record you keep for each field: removed or transformed, how, before which of features, prompts and outputs, and why."

Cell 2 holds one row per field. The course filled the rows for `tin` and `filing_status`, as the trainer did. Fill the other 12 rows, one value at a time:

1. `monday`: find the item of your list in your notebook of Monday's exercise 2 that names the field, by this table. Copy its verdict: `needed`, `not needed` or `transformed`. A field with no item in your list: `not listed`.

| An item that names | is the field |
|---|---|
| wages | `wages_amt` |
| adjusted gross income | `agi_amt` |
| total income | `total_income` |
| total tax | `total_tax_amt` |
| tax year | `tax_year` |
| filing status | `filing_status` |
| the taxpayer's name | `taxpayer_name` |
| the identifying number | `tin` |
| the address | `street_address` |

2. `needed`: `yes` or `no`. The use: "the model must decide which returns to examine." "It needs the income figures, the filing status and the tax year. It does not need the taxpayer's name or street address to learn what makes a return worth examining."

3. `class`: the policy uses three short names. FTI is federal tax information, PII is personally identifiable information, and SBU is sensitive but unclassified data. Ask the policy's questions in this order:
   - "If related to a tax account, categorize it as FTI (even if it is also PII or SBU data)."
   - "If it identifies an individual, but not FTI, categorize it as PII (mostly personnel information)."
   - "If it is sensitive, but not FTI or PII, categorize it as SBU data."

   Write FTI as `sensitive but unclassified`: "Federal tax information is a kind of sensitive but unclassified data". Write PII as `personally identifiable`. A field that is none of these: `neither`.
4. `action`: `keep` a field the use needs. `remove` a field the use does not need. `transform` only `tin`: the use does not need the number, but Wednesday matches a filer's returns by it.
5. `reason`: why, in 4 words or more.

This table gives each answer and its reason:

| Field | needed | class | action | Why |
|---|---|---|---|---|
| `wages_amt`, `agi_amt`, `total_income`, `total_tax_amt`, `tax_year` | `yes` | `sensitive but unclassified` | `keep` | the figures and the year the use needs. They are lines of one return of a tax account, so they are FTI |
| `return_id` | `yes` | `sensitive but unclassified` | `keep` | it names one return of a tax account, so it is FTI. It tells returns apart without naming the filer |
| `taxpayer_name`, `street_address` | `no` | `sensitive but unclassified` | `remove` | "The name and street address are FTI too, because they sit on a return, and they also identify a person; the use does not need them." |
| `zip_code` | `no` | `sensitive but unclassified` | `remove` | it is part of the filer's address on the return, so it is FTI. "A ZIP code alone names nobody; joined to a birth date and a filing status it may name one person." No Wednesday feature uses a region |
| `received_date` | `no` | `sensitive but unclassified` | `remove` | the date the IRS received one return of a tax account, so it is FTI. The day it arrived says nothing about the return's lines |
| `loaded_by` | `no` | `personally identifiable` | `remove` | the clerk's user name: "A field that is personally identifiable but not FTI is one that names a person with no tax account behind it" |
| `batch_id` | `no` | `neither` | `remove` | it names no person and no tax account |

Run cell 2. It prints each field with its action and class. A row that prints `(no action yet)` is still empty.

Notebook cell 2:

```python
# 2. Your record: one row per field of the batch. The rows for tin and filing_status are filled.
# monday: Monday's verdict (needed, not needed, transformed) or not listed
# needed: yes or no.  class: sensitive but unclassified, personally identifiable, or neither
# action: keep, remove or transform.  reason: why, 4 words or more
record = [
    {"field": "return_id", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "tin", "monday": "transformed", "needed": "no", "class": "sensitive but unclassified", "action": "transform", "reason": "FTI. The model needs no number, but Wednesday matches a filer's returns, so a case key replaces it."},
    {"field": "taxpayer_name", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "street_address", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "zip_code", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "filing_status", "monday": "not listed", "needed": "yes", "class": "sensitive but unclassified", "action": "keep", "reason": "FTI from the return. The use needs it to compare like returns."},
    {"field": "wages_amt", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "agi_amt", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "total_income", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "total_tax_amt", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "tax_year", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "received_date", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "loaded_by", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
    {"field": "batch_id", "monday": "", "needed": "", "class": "", "action": "", "reason": ""},
]
for r in record:
    print(f"{r['field']:15} {r['action'] or '(no action yet)':10} {r['class'] or '(no class yet)'}")
```

### Step 3. Prepare the batch, and explain the case key

Why: "A field that never enters the training data cannot reach a score, a prompt or an output."

The case key replaces the identification number "with a stand-in that still lets you match rows". Cell 3 makes it as `filer_key`. It hashes the number together with a secret: `sha2` is the hash, and the secret is a random value that the cell makes and never saves. The same number gets the same key, so a filer's returns still match.

Hashing alone is not safe: "it is possible for an attacker to perform a brute force search". A brute force search hashes every possible number until one gives the same key. A nine-digit number has only a billion values. The secret is the "information for the transformation", and it "must be highly protected": here nobody keeps it.

In cell 3, between the quotes of `explain = ""`, write why the case key can stay when the identification number goes.

Then run cell 3. It reads your record and builds the prepared data:

- It drops each field whose action is `remove` or `transform`, and adds `filer_key` for `tin`.
- A `transform` of `zip_code` would keep its first three digits as `zip3`. Your record removes `zip_code`.
- The assertion fails if a field that names a person (`tin`, `taxpayer_name`, `street_address` or `loaded_by`) is still a column. An `AssertionError` names each one. Then change its action in cell 2, and run cells 2 and 3 again.

You should see a line with the count of columns and their names, then 5 rows of the prepared data. The first three rows are one filer's returns of 2021, 2022 and 2023. Their `filer_key` is the same: that is the match Wednesday needs.

Wednesday's files carry case keys that the trainer made by the same rule. The trainer used the trainer's own secret, so those key values differ from the keys this cell makes.

Notebook cell 3:

```python
# 3. Prepare the batch from your record, then show that no field that names a person survives.
explain = ""  # before you run this cell: why can the case key stay when the number goes?

import secrets
from pyspark.sql import functions as F

NAMES_A_PERSON = {"tin", "taxpayer_name", "street_address", "loaded_by"}  # fields that name or identify a person
removed = [r["field"] for r in record if r["action"] == "remove"]
transformed = [r["field"] for r in record if r["action"] == "transform"]
prepared = spark.table("course.returns.batch_dirty")
if "tin" in transformed:  # the case key: the number hashed with a secret that is never saved
    secret = secrets.token_hex(16)
    prepared = prepared.withColumn("filer_key", F.substring(F.sha2(F.concat(F.lit(secret), F.col("tin")), 256), 1, 16))
if "zip_code" in transformed:  # the first three digits of the ZIP code only
    prepared = prepared.withColumn("zip3", F.substring("zip_code", 1, 3))
prepared = prepared.drop(*removed, *transformed)

survived = NAMES_A_PERSON & set(prepared.columns)
assert not survived, f"These fields name a person and are still in the prepared data: {sorted(survived)}"
print(f"{len(prepared.columns)} columns: {', '.join(prepared.columns)}")
display(prepared.orderBy("return_id").limit(5))
```

### Step 4. Check

Run cell 4. It builds the prepared columns again from your record. It prints `Done:` when these things are true:

- The record has a row for each field of the batch.
- Each row has Monday's verdict or `not listed`, `yes` or `no`, a class, an action and a reason of 4 words or more.
- No field that names a person has the class `neither` or the action `keep`. No field the use does not need has the action `keep`.
- A transform is only on `tin` or `zip_code`.
- No removed field is in the prepared data, and it has `filer_key`.
- `explain` holds 8 words or more.

Otherwise it prints `Not yet:` and each thing still to do. It does not judge your reasons: the debrief does. You do not need to read its code.

Notebook cell 4:

```python
# 4. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Which field did you keep without a reason you could say aloud?
2. You removed `received_date`. What could Wednesday's features lose with it, and what would keeping it risk?
3. Cell 3's assertion reads the prepared data's columns. Where else could a removed field come back: in a prompt, or in an output?

The answer, after you try: [`answers/exercise-02-field-record-and-case-key`](../answers/exercise-02-field-record-and-case-key/).
