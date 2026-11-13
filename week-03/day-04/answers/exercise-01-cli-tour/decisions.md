# Exercise 1: decisions

For the trainer. Exercise 1, "A tour of the Databricks CLI", follows the demo of the same commands in the same order (deck slides 14 and 37 show parts of it today; see the setup's In class). It is the first day in the Databricks CLI, so it is a tour, not a task (the program owner's ruling of 2026-11-13: a first day in a tool gets a tour first). The terminal and Codex were used in weeks 1 and 2; the one new thing is the Databricks CLI.

Modelled on Microsoft Learning's DP-750T00 lab 12, "Implement Development Lifecycle Processes in Azure Databricks" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/12-implement-development-lifecycle-processes-in-azure-databricks.html), its CLI steps before the bundle only: check the version, `databricks auth login` with the workspace URL, the saved profile ("Profile DEFAULT was successfully saved"). Its own words: "In this part, you create a bundle for the order processing job using the Databricks CLI on your local machine." The bundle is not used. The sign-in and profile steps follow Databricks' CLI tutorial (https://docs.databricks.com/aws/en/dev-tools/cli/tutorial). Shape: "Follow and confirm". Every page below was opened on 2026-11-13.

Where it ran: nowhere with Databricks. The course team ran the check on this machine against the starting notes, this kept answer and one wrong record (`commands.sh`); the column facts come from Monday's made-up rows, `week-03/setup/day-01-course-data.py`. No `databricks` command ran. The run on a Workstation is a trainer gap: `week-03/setup/day-04-setup.md` § Not yet checked, items 1 and 2.

## 1. The version and the deliberate miss

- **The answer.** `databricks -v` prints a version of 0.205.0 or above, exit status `0`. `databrick -v` prints `bash: databrick: command not found`, exit status `127`.
- **Reason.** The shell runs the first word as a program. No program is named `databrick`, so the shell reports it and the command never reaches the CLI. 127 is the shell's number for a command it cannot find; the check accepts any number but 0.
- **The day's lines.** `curated.md` § Read a command in the terminal: "`$?` holds the exit status of the last command (0 = success)."; the Carpentries' `ks` example, "if the command was mis-typed or if the program corresponding to that command is not installed." Deck slide 20 shows `databricks -v`, `ks`, `echo $?`.
- **Pages.** Databricks CLI tutorial: "This version should be 0.205.0 or above." Software Carpentry, The Unix Shell, episode 1 (https://swcarpentry.github.io/shell-novice/01-intro.html), the source of the miss.

## 2. Sign-in and profile

- **The answer.** Profile `course`; `login_exit` 0; `databricks auth profiles` shows `YES` under Valid for `course`.
- **Reason.** A profile is a named, saved sign-in. Each later command names it with `-p`, so it runs as the learner in the workspace meant.
- **The day's lines.** `curated.md` § Sign in to the workspace with the Databricks CLI, Step 2 and Step 3; deck slides 29 to 31.
- **Pages.** Databricks CLI tutorial: "Press `Enter` to accept the suggested profile name, or enter the name of a new or existing profile." Auth commands (https://docs.databricks.com/aws/en/dev-tools/cli/reference/auth-commands): `databricks auth profiles` will "List all available configuration profiles (at `~/.databrickscfg` by default) and check whether they are valid profiles."; "If the command succeeds, a `YES` is displayed; otherwise, a `NO` displays." Global flags (https://docs.databricks.com/aws/en/dev-tools/cli/commands): `-p, --profile`, "The name of the profile in the `~/.databrickscfg` file to use to run the command."
- **What else the check accepts.** Any profile name. The README asks for `course` so that every command it prints works as written.

## 3. The catalogs (the predict question)

- **The answer.** A prediction written first; a list that holds `course`; one sentence on why it matches or not.
- **Reason.** A learner sees only the catalogs they own or may use. Monday's setup gave the learners' group `USE CATALOG` on `course`, so `course` must be there. Other catalogs (such as `system`, or a workspace's own catalog) depend on the workspace.
- **The day's lines.** `curated.md` Step 4, quoting the catalogs reference; deck slide 32.
- **Pages.** Catalogs commands (https://docs.databricks.com/aws/en/dev-tools/cli/reference/catalogs-commands): "If the caller is the metastore admin, all catalogs will be retrieved. Otherwise, only catalogs owned by the caller (or for which the caller has the `USE_CATALOG` privilege) will be retrieved."
- **What else the check accepts.** Any list that holds `course`, any prediction of 3 words or more and any sentence of 5 words or more.

## 4. Two schemas' tables

- **The answer.** `course.returns`: `return_header`, `return_summary`, `batch_clean`, `batch_dirty`, `batch_governed` (`week-tables.md` of the round's plan). The learner's schema: Wednesday's eight tables, `return_table`, `dependents`, `w2s`, `features`, `feature_record`, `train`, `valid`, `test`.
- **Reason.** `tables list` takes the catalog and the schema as two words, in that order. The learner finds the group with `databricks tables -h`, as the day teaches: "For schemas and tables, find the command group with `databricks -h`".
- **Pages.** Tables commands (https://docs.databricks.com/aws/en/dev-tools/cli/reference/tables-commands): usage "databricks tables list CATALOG_NAME SCHEMA_NAME [flags]"; "databricks tables get FULL_NAME [flags]". Global flags: `-h` or `--help`, "Display help for the Databricks CLI or the related command group or the related command."
- **What else the check accepts.** `return_header` and `return_summary` must be in the first list (Monday's setup makes them; Tuesday's batches may be missing if Tuesday's setup did not run). The learner's list may be `none`: exercise 2 reruns the notebook that writes it.

## 5. Two columns beside Monday's notes

- **The answer.** `total_income`: `INT`, no comment. `wages_amt` (the learner's second column in this answer): `INT`, "Wages, salaries and tips the filer reported, in whole dollars." No difference from the Monday notes; Monday's draft for `total_income` was never saved, so the catalog has no comment.
- **Reason.** Monday's exercise 3 saved no draft (its step 2: "Do not select the check mark beside it"), so the catalog shows the course's comments. A learner whose Monday entry differs names the difference and does not fix it.
- **Monday's lines.** Monday's exercise 3 steps: "Compare the entry's type with the column's type in the catalog." "Compare the entry's description with the column's comment, where one exists."
- **Pages.** Unity Catalog's table object (https://docs.databricks.com/api/workspace/tables/get): `columns[].name` "Name of Column."; `columns[].comment` "User-provided free-form text description."; `type_name` values include `INT`.
- **What else the check accepts.** Any second column of `return_header` but `total_income`, with its type and the first five words of its comment, or `none` where it has none. The Monday notes need 2 words or more; the check does not compare them, since Monday's notebook is not on the Workstation.
