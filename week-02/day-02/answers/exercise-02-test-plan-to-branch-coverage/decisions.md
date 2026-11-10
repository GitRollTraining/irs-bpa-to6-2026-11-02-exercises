# Exercise 2: the answer and its reasons

## The test plan, `files/TEST_PLAN.md`

| Row | Expected | Why | The line it rests on |
|---|---|---|---|
| -1 months | error | A negative number of months is an invalid partition, and it needs a test too. | "test cases must exercise all identified partitions (including invalid partitions) by covering each partition at least once." |
| 0 months | 0 | On time: no penalty. The first boundary of the months. | "Two-value analysis tests each boundary and its neighbour across the edge." |
| 1 month | 10 | 1 percent of 1,000 dollars. The neighbour of 0 across the edge. | the same |
| 5 months | 50 | One value inside 1 to 10. | "Therefore, one test for each partition is sufficient." |
| 10 months | 100 | The last month before the cap. | "Typical defects found by BVA are located where implemented boundaries are misplaced ..." |
| 11 months | 100 | The first capped month: the same as 10. | the same |
| 0 unpaid tax | 0 | Nothing owed is the second partition of `unpaid_tax`. | "For `unpaid_tax`, the rule gives two partitions: nothing owed, and something owed." |
| one account through `penalty_for`, 4 months, 2,000 dollars | 80 | Coverage measures all of `rules.py`, and `__main__.py` calls `penalty_for` for each account. | "Use branch coverage to see what those tests missed." |

## The tests, `files/tests/test_rules.py`

The kept run's tests, `files/tests/test_rules.codex.py`, with one change: the plan's `penalty_for` row first said 40, and its test failed. 4 months at 1 percent of 2,000 dollars is 80. The plan and the test were corrected to 80. The code was right.

## What else the check accepts

- Rows in any order, with any names, and with other values inside each partition.
- Expected values written as `100`, `100.0` or `100.00`.
- Rows as tuples or as `pytest.param(...)` in the test file. The `penalty_for` row may be its own test, with any account.
- More rows, such as 9 and 12, the 3-value rows of the optional part.

## Where the notebook's quoted lines come from

All are in the Program repository's day file `days/day-02/curated.md`, section 2. Design tests from the rule. The exercise is deck slide 29 ("From a test plan to full branch coverage").

| Quoted line | Heading |
|---|---|
| "test cases must exercise all identified partitions (including invalid partitions)" | Partition the inputs |
| "Two-value analysis tests each boundary and its neighbour across the edge." | Test the boundaries |
| "pytest runs the test once for each tuple." | Turn the plan into parametrized tests |
| "The negative row gets its own test, which expects the error." | Turn the plan into parametrized tests |
| "An expected value taken from the code's output only proves the code agrees with itself." | Turn the plan into parametrized tests |
| "To measure branch coverage, run coverage.py with the `--branch` flag" | Measure statement and branch coverage |
| "The `min` line always goes to the same next line, so coverage.py sees no branch there." | Measure statement and branch coverage |
| "Use partitions to decide which tests to write. Use branch coverage to see what those tests missed." | Measure statement and branch coverage |
