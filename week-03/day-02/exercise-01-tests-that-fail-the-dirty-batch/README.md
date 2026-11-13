# Exercise 1: Tests that fail the dirty batch

**Goal:** After this exercise, you can write data tests that fail a dirty batch, and name each test's kind and action.

**Scenario:** A new batch of synthetic returns came in two copies: a clean one, and a dirty one with faults put in on purpose. You turn Monday's column checks into tests, and see which faults they catch.

**AI tool:** none.

**Where you work:** the notebook `week-03/day-02/exercise-01-tests-that-fail-the-dirty-batch/exercise.ipynb` in your Git folder of the course, in Databricks. Attach the notebook to the compute the trainer names.

**Done when:** cell 5 prints `Done:`: four tests pass the clean batch, and each has its kind, its action and its result on the dirty batch.

**Optional part:** one return is in the dirty batch twice, under two different `return_id` values, with the same `tin` and `tax_year`. No rule in this exercise's tables sees it. Copy test 3's block in cell 2, and paste it after test 4 as a fifth test. Change its rule to `count(*) OVER (PARTITION BY tin, tax_year) = 1`. Run cell 4 again.

**What you have:**

- Your notebook of Monday's exercise 3: two columns, each with its empty count, smallest value and largest value.
- The clean batch `course.returns.batch_clean`: 30 returns of tax years 2021, 2022 and 2023, with no fault. The dirty batch `course.returns.batch_dirty`: the same returns with faults put in. The course made up every row.
- `check.py`, beside this notebook. Cell 5 runs it.

**Start from:** this notebook as the course gives it. The course gives test 3. Tests 1, 2 and 4 are empty. The trainer just ran one test, wages never below 0, on both batches. To start again, set the values you typed back to `""`.

### Step 1. See the two batches

Why: a test compares a batch with what you expect of it. First see what each batch holds.

1. Run cell 1. You should see three lines: `batch_clean: 30 rows`, `batch_dirty: 32 rows`, and the batch's columns.
2. In the columns line, find the two columns of your notebook of Monday's exercise 3.

Cell 1 also makes `run_test`, which cells 3 and 4 use. `run_test` reads a rule's text as a SQL condition (`F.expr` does that). It counts the rows for which the condition is false, then applies the test's action. The action fail is the assertion of week 2's tests: `assert bad == 0`.

Notebook cell 1:

```python
# 1. The two batches, and the function that runs one test. You do not need to read the function.
from pyspark.sql import functions as F

for name in ("batch_clean", "batch_dirty"):
    print(f"{name}: {spark.table('course.returns.' + name).count()} rows")
print("columns:", ", ".join(spark.table("course.returns.batch_clean").columns))


def run_test(test: dict, table: str) -> str:
    """Run one test on one batch and apply its action.

    Args:
        test: its name, kind, action and rule, as cell 2 holds them.
        table: the batch's full name.

    Returns:
        One line: PASS, WARN or DROP, with the count of rows that break the rule.

    Raises:
        AssertionError: the action is fail and a row breaks the rule.
    """
    label = f"{test['kind']}, {test['action']}: {test['name']}"
    checked = spark.table(table).withColumn("_ok", F.expr(test["rule"]))
    bad = checked.filter("NOT _ok").count()
    if bad == 0:
        return f"PASS  {label}"
    if test["action"] == "fail":
        assert bad == 0, f"FAIL  {label}: {bad} rows break the rule"
    if test["action"] == "drop":
        return f"DROP  {label}: {bad} rows left out"
    return f"WARN  {label}: {bad} rows stay in"
```

### Step 2. Write tests 1 and 2 from Monday's columns, and predict

Why: "The intuitions you hold about returns, from years of Compliance work, are the expectations. Write them down first, then compare them to the data."

Each test in cell 2 has a kind: which of the five kinds of check it is. The kinds are completeness, validity, uniqueness, consistency and freshness.

The course gives test 3. Its rule is `count(*) OVER (PARTITION BY return_id) = 1`. For each row, `count(*) OVER (PARTITION BY return_id)` counts the rows of the batch with the same `return_id`. A count of 1 means the return is there once. "Uniqueness describes the degree to which there is no duplication in records."

Your first column is the first entry of cell 3 in Monday's notebook. Your second column is its second entry. Use the part of each name after the dot, such as `total_income`.

Write test 1 from your first column. Use the first row of this table that fits:

| Your column | Rule to write | Kind | Why |
|---|---|---|---|
| no notebook from Monday, or a column that cell 1 does not list | test 1: `agi_amt IS NOT NULL`. Test 2: `wages_amt >= 0` | `completeness`, then `validity` | the course's pair: "every return has a tax year and an adjusted gross income" |
| `wages_amt` or `total_tax_amt`: an amount that is never below 0 | `<column> >= 0` | `validity` | "Validity describes the degree to which the data is in the range and format expected." |
| any other column | `<column> IS NOT NULL` | `completeness` | "Completeness describes the degree to which records are present." A column such as `total_income` can be below 0: "either the entry is wrong or losses are recorded in the same column." |

Write test 2 from your second column, with the same table.

A rule that meets an empty value is neither true nor false, and that row does not count as breaking it. So a test for empty values uses `IS NOT NULL`, not `>= 0`.

Then choose each test's action. Use the first row of this table that fits:

| Your test | Action | Why |
|---|---|---|
| a completeness test on a column that Monday's summary showed with an empty count above 0 | `warn` | a good return can have the column empty, so a person reads the rows: "keep warnings for what a person should look at later." The rows stay in: "Invalid records are written to the target." |
| any other completeness or validity test | `fail` | one bad row means the feed that made the batch is broken. In Google's example a bug set a field to -1 for part of the data: "the data looks perfectly fine for the training code, since -1 is an acceptable value for the int feature." "For the checks that decide whether a batch is usable, choose the action that stops the batch." |

Drop leaves the row out with nobody reading it. No test of this exercise uses it.

Last, predict. In each test's `predict`, write `fails` if you expect the dirty batch to break the rule. Otherwise, write `passes`.

Run cell 2. It prints each test's kind and rule. A test that prints `(no rule yet)` is still empty.

Notebook cell 2:

```python
# 2. Your tests. Tests 1 and 2: from Monday's two columns. Test 3: given. Test 4: step 5.
tests = [
    {
        "name": "",  # what the test expects, in words, such as "wages never below 0"
        "kind": "",  # completeness, validity, uniqueness, consistency or freshness
        "action": "",  # warn, drop or fail
        "rule": "",  # a SQL condition that is true for a good row, such as "wages_amt >= 0"
        "predict": "",  # before you run cell 4: fails or passes, on the dirty batch
        "passed_why": "",  # after cell 4, only if it passed the dirty batch: why
    },
    {
        "name": "",
        "kind": "",
        "action": "",
        "rule": "",
        "predict": "",
        "passed_why": "",
    },
    {
        "name": "each return_id once",
        "kind": "uniqueness",
        "action": "fail",
        "rule": "count(*) OVER (PARTITION BY return_id) = 1",  # how many rows share this row's return_id
        "predict": "",
        "passed_why": "",
    },
    {
        "name": "",
        "kind": "",
        "action": "",
        "rule": "",
        "predict": "",
        "passed_why": "",
    },
]
for n, test in enumerate(tests, 1):
    print(n, test["kind"] or "(no kind yet)", "|", test["rule"] or "(no rule yet)")
```

### Step 3. Run the tests on the clean batch

Why: "a check that is too strict stops good batches too." A test must pass a good batch before its failures mean anything.

1. Run cell 3. You should see one `PASS` line for each test that has a rule.
2. A test that does not print `PASS` here is too strict, or the wrong way round: the rule must be true for a good row. Change its rule in cell 2.
3. Run cell 2 again.
4. Run cell 3 again.

Notebook cell 3:

```python
# 3. Run each test on the clean batch.
for test in tests:
    if test["rule"]:
        try:
            print(run_test(test, "course.returns.batch_clean"))
        except AssertionError as failed:
            print(failed)
```

### Step 4. Run the tests on the dirty batch, and read each line

Why: "Either way the result you keep is the same: the test, and the run where it failed the dirty batch."

Run cell 4. You should see one line for each test. Read each line by its first word, and read its count of rows:

| First word | What it means for the batch |
|---|---|
| `PASS` | no row breaks the rule |
| `FAIL` | the batch does not load: "Invalid records prevent the update from succeeding." The cell prints the error and goes on |
| `WARN` | the rows stay in the table, and a person reads them later |
| `DROP` | the test leaves the rows out, and the rest loads |

Compare each line with your `predict`. For each test that printed `PASS`, write why in its `passed_why`. A rule on one column sees every fault of its kind in that column. So write: no fault of this kind is in this column. Then run cell 2 again.

Notebook cell 4:

```python
# 4. Run each test on the dirty batch. A fail raises an error: this cell prints it and goes on.
for test in tests:
    if test["rule"]:
        try:
            print(run_test(test, "course.returns.batch_dirty"))
        except AssertionError as failed:
            print(failed)
```

### Step 5. Add a test of a kind that tests 1 to 3 do not use

Why: "Checks only for completeness. Every field is filled and every value is wrong. Caught by listing your checks against the five kinds and seeing which kinds have none."

Fill test 4 in cell 2 with a kind that tests 1 to 3 do not use. Take its rule and its action from this table:

| Kind | Rule | Action | Why |
|---|---|---|---|
| `consistency` | `wages_amt <= total_income` | `warn` | "Consistency describes the degree to which values in a data set do not contradict other values representing the same entity." The example: "wages on the return do not exceed the total income on the same return". A real return can break it, as losses can make total income smaller than wages, so a person reads it |
| `freshness` | `tax_year BETWEEN 2021 AND 2023` | `fail` | the batch says it holds tax years 2021, 2022 and 2023: "the batch holds the tax years it says it holds". Another year means the feed sent the wrong returns |
| `validity` | `filing_status IN ('1', '2', '3', '4', '5')` | `fail` | "the filing status is one of the allowed codes" |

1. Write a name: what the test expects, in words.
2. Write your prediction.
3. Run cells 2, 3 and 4 again.
4. If test 4 passed the dirty batch, write its `passed_why`.

### Step 6. Check

Run cell 5. It runs each rule again on both batches. It prints `Done:` when these things are true:

- Cell 2 holds four tests, each with a name, a kind, an action, a rule and a prediction.
- Each test passes the clean batch. A test that passes the dirty batch has a `passed_why`.
- Test 4's kind is not the kind of test 1, 2 or 3.

Otherwise it prints `Not yet:` and each thing still to do. It does not judge the action you chose: the debrief does. You do not need to read its code.

Notebook cell 5:

```python
# 5. Check. You do not need to read this code.
# It runs check.py, beside the notebook.
```

### Afterwards, together

1. Which of your tests passed the dirty batch? Was the batch right there, or was the test blind to the fault?
2. You chose fail or warn for each test. Which fault in your own feeds would you let through with a warning, and why?
3. A column summary looks at one column at a time. Which kinds of fault can it never show, and why?

The answer, after you try: [`answers/exercise-01-tests-that-fail-the-dirty-batch`](../answers/exercise-01-tests-that-fail-the-dirty-batch/).
