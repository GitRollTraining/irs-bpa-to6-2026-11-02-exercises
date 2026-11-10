# AGENTS.md

## The project

`payment_job` is a nightly batch job: it reads the day's accounts, works out a late-payment penalty
for each, and writes a report. The course made up the job, its rules and its data.

## How to run it and its tests

From this folder, with the course environment active:

```sh
python -m payment_job data/accounts.csv report.txt
python -m pytest -q
```

## Code Review Rules

Review each pull request against these rules. Cite a rule by its number in every comment.

1. Design: the change belongs in this code, and its parts fit how the job is built.
2. Functionality: the change does what its description says, for every account, including the edge cases.
3. Complexity: a reader understands the change quickly, and it builds nothing the change does not use now.
4. Tests: each new rule or branch of the code has a test, and the tests pass with `python -m pytest -q`.
