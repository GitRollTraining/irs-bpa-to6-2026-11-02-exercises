# Test plan: late_payment_penalty

The rule, from `payment_job/rules.py`: the penalty is 1 percent of the unpaid tax for each whole month late. It stops growing after 10 months, which is 10 percent. Nothing owed means no penalty. A negative number of months is an error. The rule is made up for the course.

Work out each expected value by hand, from the rule.

| Partition or boundary | months_late | unpaid_tax | Expected |
|---|---|---|---|
| invalid: negative months | -1 | 1000 | error |
| on time | 0 | 1000 | 0 |
| first month late | 1 | 1000 | 10 |
| inside 1 to 10 | 5 | 1000 | 50 |
| last month before the cap | 10 | 1000 | 100 |
| first capped month | 11 | 1000 | 100 |
| nothing owed | 5 | 0 | 0 |
| one account, through penalty_for | 4 | 2000 | 80 |
