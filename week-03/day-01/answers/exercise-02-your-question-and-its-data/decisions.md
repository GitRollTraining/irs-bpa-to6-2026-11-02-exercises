# Exercise 2: decisions

For the trainer. Exercise 2, "Your question, its data, each verdict", follows the worked example on a refund question. It is thinking work: no Databricks tool beyond the notebook, exempt from the day's-tool check by the program owner's ruling of 2026-11-13 ("Keep it, marked thinking work"). Modelled on Google for Developers, "Introduction to Machine Learning Problem Framing: framing an ML problem" (https://developers.google.com/machine-learning/problem-framing/ml-framing), its two Check Your Understanding items; shape "Complete the starter". The check is `check.py` in the exercise folder. It reads the text of cells 1 to 3 only.

**Why the record is text inside a Python cell.** A Databricks notebook cell's Markdown cannot be read by a check. The question (cell 1) and the list (cell 2) are plain text, a Markdown table, inside a Python string, so cell 4 can read them and Tuesday can open them. The learner types text, not code.

## 1. The question

- **The answer.** Unit: one return filed this year. Target: whether an examination changes the tax, yes or no. Time: returns filed this year, ranked now, with past examinations to learn from.
- **Reason.** A question names the unit, the target and the time. The day's own question is given as an example; a learner's own question with the three parts is as good.
- **The notebook line.** "That sentence names the unit (one return), the target (a change, yes or no) and the time (this year's returns)." For the target: "A measurable stand-in is whether an examination of the return ended with a change to the tax."
- **What else the check accepts.** Any `Unit:`, `Target:` and `Time:` line with two words or more after the label.

## 2. The list and its verdicts

- **The answer.** Seven rows (`values.json`, `items`): wages and total income on the return, needed; the name and identifying number, not needed; wages and interest that payers reported, needed; whether a past examination changed the tax, needed; how the IRS selected each examined return, needed.
- **Reason.** Each item is kept only when the prediction needs it. A field that names the taxpayer tells the ranking nothing. The selection record lets the model's builders correct for outcomes that a score chose.
- **The notebook lines.** "Applied to a model, the test for each field is whether the prediction needs it." "A field that names the taxpayer, such as a name or an identifying number, tells the model nothing about the return's line items that it needs to rank the return" "A model trained only on returns chosen because they scored high never learns what the unchosen returns look like."
- **What else the check accepts.** Any 6 rows or more, two or more of each kind, each with the question it serves, a verdict and a reason of 4 words or more. The check refuses `needed` on an item whose name says name, SSN, TIN, EIN, ID, identifying or address. It refuses a row with no item. It accepts kinds and verdicts in backticks, and indented rows. It asks for one `not needed` item, and for a past-outcomes item whose name says how the return was selected (selected, random, sample, score, chosen). It does not judge a reason: the talk after the exercise does.

## 3. The explanation

- **The answer.** Returns a score chose show outcomes only for the returns the score already favoured. A model trained on them never learns about the rest. The record of random sample or score lets the builders correct for that.
- **The notebook line.** The guide's last row, quoted above.
- **What else the check accepts.** Any text of 8 words or more.

## Where it ran

- On the author's computer, 2026-11-13: the notebook's cells in order (no table is read). The start printed `Not yet: 6 left.`. The answer printed `Done: your question names its unit, target and time, and each of its 7 items has a kind, the question it serves, a verdict and a reason.` `commands.sh` printed the same on Python 3.10 and 3.14.
- In Databricks: no trainer gap beyond the one every exercise shares, that cell 4 finds `check.py` beside the notebook.

## Where each quote comes from

The curated file is `days/day-01/curated.md` in the Program repository. The day's deck is being rebuilt, so no slide number is given.

| Quote in the notebook | Curated file: heading, line |
|---|---|
| "for each return filed this year, how likely is an examination to change the tax?" | Let the question decide the data, line 212 |
| "That sentence names the unit (one return), ..." | Let the question decide the data, line 213 |
| "A measurable stand-in is whether an examination ..." | Let the question decide the data, line 206 |
| "Start with directly observed and reported features as opposed to learned features." | Let the question decide the data, line 208 |
| "The return's reported line items, one row per return." | Pick the information that helps select a case, line 272 |
| "Information that can be compared with the return, such as third-party statements." | Pick the information that helps select a case, line 273 |
| "The outcome of past examinations, ..." | Pick the information that helps select a case, line 274 |
| "A model trained only on returns chosen because they scored high ..." | Pick the information that helps select a case, line 252 |
| "Applied to a model, the test for each field is whether the prediction needs it." | Leave out what the use does not need, line 306 |
| "A field that names the taxpayer, ..." | Leave out what the use does not need, line 307 |
| "needed, with the reason; not needed, so left out; or needed but to be transformed, which Tuesday handles." | Leave out what the use does not need, line 330 |
| "derived data keeps the class of its source." | Leave out what the use does not need, line 298 |
| "the target decides who carries the burden." | Leave out what the use does not need, line 313 |

## Findings of the linter inside quotes

- The kind `past outcomes` quote: 30 words in one sentence (line 274 of the curated file).
- The verdicts quote: two semicolons (line 330).
- The name quote: 30 words in one sentence (line 307).
