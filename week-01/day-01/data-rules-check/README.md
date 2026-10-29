# Exercise: Classify four uses of AI tools with the data-rules check

After this exercise, you can classify a use of an AI tool with the data-rules check.

**Scenario:** Your team wants to send four files to AI tools. Decide for each file if it may go.

**Success criterion:** from `lab`, `python3 ../check.py` prints `Done:`.

**Where you work:** the folder `~/practice/week-01/day-01/data-rules-check/lab`, in VS Code and in a terminal. Each path in this exercise starts there. Do not use AI tools.

**Start from:** the folder `data-rules-check`. Run `python3 ~/practice/reset.py data-rules-check`. Then run `cd ~/practice/week-01/day-01/data-rules-check/lab`. To start again, run the same reset. The reset removes your commits.

**What you have:** your table `docs/data-rules-check.md`, which is not committed, and the files of the four uses: `notes/0147.txt`, `exports/case-2231.txt` and `model.py`. `../check.py` is the check.

## Steps

1. Open your table and the files of the four uses.
2. Fill in the table by hand. For each use, look for this in its file:

| Use | Look for this |
|---|---|
| 1. `notes/0147.txt` to the course's approved tool | Read its first line. Is the note from the lab? Then find its row in the six-row table of section 1.2. |
| 2. `exports/case-2231.txt` to a public chat tool | Read its first line. Where does the note come from? The name is gone. What does the note still give? Section 1.1: "Nameless, it still gives year, form, amount, date". |
| 3. `exports/case-2231.txt` to the course's approved tool | Does the approval cover a real note? Section 1.2, move 5: "Use approval: the accountable official". |
| 4. `model.py` to a public chat tool | It holds no taxpayer data. Is it safe? Section 1.1: the policy covers "any information, including seemingly innocuous work-related matters", in "public or non-Treasury AI tools". |

3. Commit, and run `python3 ../check.py`. You should see `Done:`. If you see `Not yet:`, fix what it names, and run the check again.

**Answer:** `~/practice/week-01/day-01/answers/data-rules-check/` holds the filled-in table, and `commands.sh`, which ends with `Done:`.

## Afterwards, together

Uses 1 and 3 go to the same tool. Why are their answers different? Uses 2 and 3 send the same file. Why are their answers different? Use 4 holds no taxpayer data. Why is it still a No?
