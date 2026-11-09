# Test plan: late_payment_penalty

The rule, from `payment_job/rules.py`: the penalty is 1 percent of the unpaid tax for each whole month late. It stops growing after 10 months, which is 10 percent. Nothing owed means no penalty. A negative number of months is an error. The rule is made up for the course.

Work out each expected value by hand, from the rule.

| Partition or boundary | months_late | unpaid_tax | Expected |
|---|---|---|---|
| first month late | 1 | 1000 | 10 |
