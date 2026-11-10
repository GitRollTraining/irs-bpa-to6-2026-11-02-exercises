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
