# payment_job

A nightly batch job. It reads the day's accounts, works out a late-payment penalty for each, and writes a report. It was ported to Python. The course made up the job, its rule and its data.

Run it from this folder:

```sh
python -m payment_job data/accounts.csv report.txt
```
