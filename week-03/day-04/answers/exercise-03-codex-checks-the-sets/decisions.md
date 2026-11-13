# Exercise 3: decisions

For the trainer. Exercise 3, "Codex checks your three sets; you approve each command", follows the demo in which Codex answers the same kind of question about Monday's table and the trainer declines one command (deck slides 45 to 48 show the loop and the note). The one new thing is judging each command Codex proposes. Modelled on GitHub Skills, "Create applications with the Copilot CLI" (https://github.com/skills/create-applications-with-the-copilot-cli; 138 stars and 99 forks on 2026-11-13, a count of interest, not of completions; "This exercise takes less than 60 minutes to complete."), its step "Practice iterative development by working together with Copilot on the command line": a coding agent in the terminal, its work checked. Here the agent is Codex, the work is Databricks commands, and the check is the four questions before each command and Catalog Explorer after. Codex's settings follow OpenAI's "Agent approvals and security" page (https://developers.openai.com/codex/agent-approvals-security, now served at https://learn.chatgpt.com/docs/agent-approvals-security). Shape: "Direct an AI tool, check what it made". Every page below was opened on 2026-11-13.

Where it ran: nowhere with Databricks or Codex. The course team ran the check on this machine on the starting notes, this kept answer and one wrong record (`commands.sh`). The kept answer judges the fallback transcript, `week-03/setup/day-04-codex-transcript.md`, which the course wrote: the one run that does not vary. The run on a Workstation is a trainer gap: `week-03/setup/day-04-setup.md` § Not yet checked, items 5 and 6.

## 1. Why the column must be gone (the explain question)

- **The answer.** `tax_added_by_exam` is known only after an examination. On the selection day it does not exist, so a model that trains on it learns the answer it is meant to predict. The three sets are what the model trains and is tested on, so they must not hold it.
- **Wednesday's lines.** `days/day-03/curated.md` § Remove features the selection day cannot know: "anything else written after selection, such as the tax amount an examination added"; the leakage check, item 5: "No feature column is marked no in the known-on-selection-day record." Wednesday's exercise 4 plants this column and drops it.
- **What else the check accepts.** Any sentence of 5 words or more that says when the value is known (after, known, leak, selection, selected or before).

## 2. Each command, by the four questions

| Command | Reads or changes | Profile | Target | Safeguard removed | Decision | Why |
|---|---|---|---|---|---|---|
| `databricks tables list course learner_07 -p course` | reads | yes | yes | no | approve | lists the schema named, with the profile named |
| `databricks tables get course.learner_07.train -p course` | reads | yes | yes | no | approve | the same, for one table |
| `databricks tables get course.learner_07.valid` | reads | no | yes | no | decline | no `-p`: the CLI picks a profile, perhaps another workspace's |
| `databricks tables get course.learner_12.test -p course` | reads | yes | no | no | decline | another learner's schema, not the one named |
| `databricks jobs delete 731042 -p course` | changes | yes | no | no | decline | it deletes a job no one named; the request asked only to read |
| `databricks tables get course.learner_07.features -p course` | reads | yes | yes | no | approve | the schema named, with the profile named |

- **The day's lines.** `curated.md` § Read each command before Codex runs it, the loop, step 3: "Is it the profile you meant? Is the command one that reads (`list`, `get`) or one that changes something (`create`, `delete`, `cancel-run`, `update`)? Is the target the one you named, or one Codex picked? Does it carry an option that removes a safeguard, such as `--force`?" Command 5 is the day's "cancel my job" case: "the specific target may not have been what the user intended, and could have been owned by someone else."
- **Why the profile matters.** Global flags (https://docs.databricks.com/aws/en/dev-tools/cli/commands): `-p`, "If this flag is not specified then if it exists, the profile named `DEFAULT` is used." The day adds the `DATABRICKS_CONFIG_PROFILE` variable and `default_profile` before it (`curated.md` Step 3).
- **Why Codex stops.** Codex's page: in the default preset, "Codex can read files, make edits, and run commands in the working directory automatically."; "Codex asks for approval to edit files outside the workspace or to run commands that require network access." Every `databricks` command reaches the workspace across the network. "You can disable approval prompts with `--ask-for-approval never` or `-a never` (shorthand)": the exercise keeps the default.
- **The commands.** Tables commands (https://docs.databricks.com/aws/en/dev-tools/cli/reference/tables-commands): "databricks tables list CATALOG_NAME SCHEMA_NAME [flags]", "databricks tables get FULL_NAME [flags]". Jobs commands (https://docs.databricks.com/aws/en/dev-tools/cli/reference/jobs-commands): "databricks jobs delete JOB_ID [flags]".
- **What else the check accepts.** For a learner's own run: 2 commands or more, each judged by the same rules. A read command that names no schema and no id (such as `databricks catalogs list -p course`) may be approved or declined; the decision must follow the learner's own target answer. The check names the answer that does not fit the command, never the right one.

## 3. Codex's answer, beside Catalog Explorer

- **The answer.** `train`, `valid` and `test` each have `exam_changed_tax`, and none has `tax_added_by_exam`. `features` still has `tax_added_by_exam`: Wednesday's exercise 4 drops each column marked no from the DataFrame it splits (`kept = features.drop(*dropped)`, its cell 4) and leaves the `features` table as exercise 2 wrote it. So Codex's answer does not agree: it says the column is absent from `features`, while its own command 6 printed it and Catalog Explorer shows it. Its part on `valid` and `test` rests on no command: both were declined, so Codex never read them.
- **The day's line.** The loop, step 5: "open the workspace and check the result there". Slide 45: "Check the workspace, not the summary".
- **What else the check accepts.** Any yes or no on the seven lines, read from the learner's own tables; `agree` yes or no; a sentence of 5 words or more. The check never reads the catalog. If Wednesday's notebook is changed to rewrite `features` without the column, `tax_added_features` becomes `no` and Codex's answer agrees; the transcript's command 6 then needs its output changed.

## 4. The optional part

`databricks jobs create` and `databricks jobs run-now` change the workspace: they save a job in the learner's name. The learner asked for them, so they may be approved after the four questions. Jobs commands: "databricks jobs create [flags]", "databricks jobs run-now JOB_ID [flags]". Not checked by `check.py`.
