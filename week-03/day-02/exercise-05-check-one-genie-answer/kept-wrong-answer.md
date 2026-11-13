# A wrong answer, kept for this exercise

The course wrote this answer in the form Genie shows, to give every learner a wrong answer to check. Genie did not write it. Use it when Genie gives you no answer or no **Show code**, or when the trainer asks you to.

**Question:** For each tax year in the clean batch, how many returns are there and what is their total wages_amt?

**Answer:** The batch holds 2 returns for tax year 2019, 8 for 2021, 12 for 2022 and 10 for 2023. Their total wages are 91,470, 552,830, 821,860 and 666,679.

**Show code:**

```sql
SELECT tax_year, COUNT(*) AS returns, SUM(wages_amt) AS total_wages
FROM course.returns.batch_dirty
GROUP BY tax_year
ORDER BY tax_year
```
