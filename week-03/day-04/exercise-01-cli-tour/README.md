# Exercise 1: A tour of the Databricks CLI

**Goal:** After this exercise, you can sign in with the Databricks CLI and tell from each command's exit status whether it worked.

**Scenario:** From Monday to Wednesday you worked inside Databricks. Today you reach the same workspace from the Workstation's terminal. You sign in once. Then you look at Monday's return table and your own schema with typed commands, and you check that each command worked.

**Where you work:** the Workstation's terminal, in this folder: `week-03/day-04/exercise-01-cli-tour/` in your course folder. You type each command at the prompt. You write what you see in `notes.md`, in this folder. Open `notes.md` in the editor: select it in the Explorer panel on the left.

**Done when:** `python3 check.py`, in this folder, prints `Done:`.

**Optional part, after step 4:** run `databricks catalogs get course -p course`. Find `owner`. That person gives the rights on the catalog.

**What you have:**

- The Databricks CLI, which the trainer installed on your Workstation.
- The workspace address (its URL). The trainer writes it on the board.
- Your schema `course.learner_NN`. The trainer gave it to you, as on Wednesday. `NN` is your learner number, such as `07`.
- `notes.md` and `check.py`, in this folder.
- Monday's return table `course.returns.return_header`. The course made up every row.
- Your Monday notes on two of its columns: cell 3 of Monday's notebook `week-03/day-01/exercise-03-find-and-check-two-drafts/exercise.ipynb`. Open it in the workspace, in your Git folder of the course (the copy of this course that you opened on Monday).

**Start from:** the trainer showed the same commands, in the same order, just before this exercise. Open a terminal in your course folder. Get today's files:

Terminal:

```text
git pull
```

Then go into this folder:

Terminal:

```text
cd week-03/day-04/exercise-01-cli-tour
```

`notes.md` has empty answers. To start again, delete what you typed after each colon.

### How to write in notes.md

Type each answer after its colon, on the same line. Where you write several names, put a comma between them.

### How to read what a command gives back

A command gives back its output, its errors (in the same window) and its exit status, a number the terminal shows only when you ask. "`$?` holds the exit status of the last command (0 = success)." Any other number means that the command failed: read the error. After each command, type this:

Terminal:

```text
echo $?
```

Write the number it prints in `notes.md`.

### Step 1. Check that the CLI is there

Why: every other step uses the program `databricks`. Its version "should be 0.205.0 or above".

Terminal:

```text
databricks -v
```

You should see one line with a version number, such as `Databricks CLI v0.278.0`. Write it after `version:`. Then type `echo $?`. Write the number after `version_exit:`.

### Step 2. Make one mistake on purpose

Why: a mistyped program name is the first error most people see. When you know how it looks, you know what to do when it comes back.

Terminal:

```text
databrick -v
```

The name has no `s`. You should see a line with `command not found` in it. Copy that line after `miss_message:`. Then type `echo $?`. Write the number after `miss_exit:`. It is not `0`.

### Step 3. Sign in, and save the sign-in as a profile

Why: a profile is the CLI's saved sign-in to one workspace. Every later command names it with `-p`. Then the command acts as you, in the workspace you meant.

Terminal:

```text
databricks auth login --host <workspace-url>
```

Type the trainer's address in place of `<workspace-url>`, without the brackets. The CLI asks for a profile name. Type `course`, then press Enter. A browser sign-in starts. Sign in as yourself, as you do in the workspace. You should see a line that says the CLI saved the profile `course`. Write `course` after `profile:`. Write the exit status after `login_exit:`.

If the sign-in does not complete, stop and ask the trainer. The trainer helps you make the same profile with a token, a password-like key. Never paste a token into Codex.

Then list your profiles:

Terminal:

```text
databricks auth profiles
```

You should see one line for each profile: its name, its host and the column `Valid`. `Valid` shows `YES` when the sign-in works, and `NO` when it does not. Write what it shows for `course` after `profile_valid:`.

### Step 4. Predict, then list the catalogs you can use

Why: the list shows only the catalogs you own or have the right to use. On Tuesday you read your rights (your grants). A catalog that you do not see is a missing right, not a fault.

First, predict. Which catalogs do you expect? Think of the catalog you used from Monday to Wednesday, and of any other right you know you have. Write them after `predicted_catalogs:`, then the reason.

Terminal:

```text
databricks catalogs list -p course
```

You should see one line for each catalog. Write their names after `listed_catalogs:`. Write the exit status after `catalogs_exit:`. After `catalogs_match:`, write one sentence: why the list matches your prediction, or why it does not.

### Step 5. List the tables of two schemas

Why: a table's full name is catalog, schema, table. The CLI asks for the catalog and the schema as two separate words. To find the command, ask the CLI with `-h`, its help option.

Terminal:

```text
databricks tables -h
```

You should see the commands of the group `tables`. `get` and `list` are among them. Then list the tables of the course's schema. `course` is the catalog, and `returns` is the schema:

Terminal:

```text
databricks tables list course returns -p course
```

You should see one line for each table. The line starts with the table's name, alone or as its full name. Write the table names after `returns_tables:`. Write the exit status after `returns_exit:`.

Then list your own schema. Put your learner number in place of `NN`:

Terminal:

```text
databricks tables list course learner_NN -p course
```

Write your schema after `my_schema:`, such as `course.learner_07`. Write the table names after `my_tables:`, or `none`. Write the exit status after `my_tables_exit:`. Wednesday's notebook wrote these tables.

### Step 6. Read two columns of Monday's return table

Why: on Monday you checked two columns of this table and wrote notes. Monday saved no draft. So the catalog still shows the comment the course wrote, or no comment where the course wrote none. Where your notes differ from the catalog, you name the difference. You do not fix it.

Terminal:

```text
databricks tables get course.returns.return_header -p course
```

It prints the table as JSON, a long text. Look for `"columns": [`. Below it is one entry for each column, between `{` and `}`. Each entry holds `"name"`, `"type_name"` and, when the column has a comment, `"comment"`. Write the exit status after `get_exit:`.

Then fill these lines in `notes.md`. Your first column is `total_income`, as on Monday. Your second column is the other one you checked on Monday.

| Write after | What to write | Why |
|---|---|---|
| `column_1_type:` | the `type_name` of `total_income` | "Compare the entry's type with the column's type in the catalog." |
| `column_1_comment:` | its `comment`, or `none` when its entry has no `comment` | "Compare the entry's description with the column's comment, where one exists." |
| `column_1_monday:` | what your Monday entry says for the same column: its `type`, and its `comment_and_tags` | you compare the two side by side |
| `column_2:` | the name of your second column, such as `wages_amt` | a column of `return_header` |
| `column_2_type:`, `column_2_comment:`, `column_2_monday:` | the same three things for it | the same reasons |
| `difference:` | one sentence: what differs between your notes and the catalog, or "no difference" and what you compared | you name a difference, and you do not fix it |

### Step 7. Check

Why: the check reads `notes.md`. It names each line that is still empty, or does not fit what the commands give.

Terminal:

```text
python3 check.py
```

It prints `Done:` when each line fits. Otherwise it prints `Not yet:` and each thing still to do. It never runs a `databricks` command.

### Afterwards, together

1. `databrick -v` and `databricks -v` differ by one letter. Why does the first one never reach Databricks?
2. Your catalog list and your neighbour's list can differ. What makes a catalog appear in one list and not in the other?
3. The command printed `total_income` with no comment. Why does that not mean your Monday check was wrong?

The answer, after you try: [`answers/exercise-01-cli-tour`](../answers/exercise-01-cli-tour/).
