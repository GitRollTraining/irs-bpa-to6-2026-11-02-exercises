# A reply in the form Genie shows

The course wrote this reply. Genie did not. Use it when Genie gives you no answer, or no **Show code**, and tell the trainer.

**Question:** How many returns are in the clean batch for each filing status?

**Answer:** The clean batch holds 30 returns: 8 with filing status 1, 7 with 2, 5 with 3 and 10 with 4.

**Result table:**

| filing_status | returns |
|---|---|
| 1 | 8 |
| 2 | 7 |
| 3 | 5 |
| 4 | 10 |

**Show code:**

```sql
SELECT filing_status, COUNT(*) AS returns
FROM course.returns.batch_clean
GROUP BY filing_status
ORDER BY filing_status
```
