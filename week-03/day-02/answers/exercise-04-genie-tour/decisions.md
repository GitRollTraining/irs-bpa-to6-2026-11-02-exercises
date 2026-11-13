# Exercise 4: decisions

For the trainer. Exercise 4, "Genie tour", is the first time learners open Genie (a first day in a tool gets a tour: the program owner, 2026-11-13). It follows the demo where the trainer asks a count question and selects **Show code**. Modelled on Databricks Academy's "Get Started with Databricks End to End" (https://www.databricks.com/training/catalog/get-started-with-databricks-end-to-end-6273, opened 2026-11-13), its section 5 "Demo: Genie Agents" then "Lab: Use a Genie Agent" (the lab's steps sit behind the Academy's sign-in; only the outline was read). Shape: "Follow and confirm". The check is `check.py` in the exercise folder.

## 1. Opening the Genie Agent

- **The steps.** Left bar, **Genie Agents**, then **Week 3 returns**; **New chat**. Pages opened 2026-11-13: Microsoft Learn, "Create and manage a Genie Agent" (https://learn.microsoft.com/en-us/azure/databricks/genie-agents/set-up): "Click **Genie Agents** in the sidebar."; users need "At least CAN VIEW/CAN RUN permissions on the Genie Agent" and "At least `SELECT` privileges on all of the Unity Catalog data objects used in the agent." Databricks, "Use a Genie Agent" (https://docs.databricks.com/aws/en/genie/talk-to-genie): "Click the New chat button to start a new conversation."

## 2. The answer, the table and the query

- **The answer (kept, from `genie-reply.md`).** "The clean batch holds 30 returns: 8 with filing status 1, 7 with 2, 5 with 3 and 10 with 4." Result table 1: 8, 2: 7, 3: 5, 4: 10. Query: `SELECT filing_status, COUNT(*) AS returns FROM course.returns.batch_clean GROUP BY filing_status ORDER BY filing_status`. Table read: `course.returns.batch_clean`.
- **Reason.** The setup's clean batch takes each return's filing status from Wednesday's returns: 8 of status 1, 7 of 2, 5 of 3, 10 of 4 (`week-03/setup/day-02-course-data.py`, `SHARED`). In the clean batch each return is one row, so `COUNT(*)` counts returns there.
- **The page line.** "Click Show code to inspect the query Genie generated." (Databricks' talk-to-Genie page, above).
- **What else the check accepts.** Any answer of 3 words or more and any result table with a number: it never judges Genie's answer. The query must start with `SELECT` or `WITH`, run, and name a table of `course.returns`; `table_read` must be a name in it, with or without backticks.

## 3. The second ask

- **The answer (kept).** `same`.
- **The notebook line.** "This means that you might receive different outputs when submitting the same prompt multiple times."
- **What else the check accepts.** `same`, or `changed` with `what_changed` of 4 words or more.

## Fallback

Genie's reply varies, and Genie may be off for the account. `genie-reply.md` beside the notebook is a reply the course wrote in Genie's form; its first lines say Genie did not write it. A learner uses it when Genie gives no answer or no **Show code**.

## Where it ran

- On the author's computer, 2026-11-13, without Databricks or Genie: `check.py` ran the kept query on the setup's rows in SQLite. Start: `Not yet: 5 left.` Answer: `Done: Genie read course.returns.batch_clean; the second answer was same.` The query was parsed by sqlglot 30.31.0, dialect `databricks`.
- Trainer gaps, at the run-through (`week-03/setup/day-02-setup.md`, Not yet checked, items 6 and 7): a learner with **CAN RUN** opens the agent and sees **Show code**; the check cell runs a pasted Genie query on the class compute.

## Where each quote comes from

| Quote | Where |
|---|---|
| "natural-language questions" | `days/day-02/curated.md`, Ask Genie a question of the governed tables, line 377 |
| "This means that you might receive different outputs ..." | `days/day-02/curated.md`, Check a Genie answer against its query, line 412 |
| "Click the New chat button ..."; "Click Show code ..." | Databricks' talk-to-Genie page, above: UI steps, not rules |

The deck's Genie exercise is slide 73, which still names one exercise of two questions.
