# Exercise 2: Run Wednesday's notebook as a one-off job

**Goal:** After this exercise, you can run Wednesday's notebook as a one-off job from the terminal and read its final state.

**Scenario:** On Wednesday you ran your notebook `wednesday-tables` cell by cell in the workspace. Today you send it from the Workstation, and the workspace runs it as a job. A job is work the workspace runs and records. The workspace gives the run a run id, the number that names it. You read the run back by its run id, and you check that the notebook wrote the same features table.

**Where you work:** the Workstation's terminal, in this folder: `week-03/day-04/exercise-02-run-wednesday-as-a-job/` in your course folder. You change `job.json` and write in `notes.md`. Open both in the editor: select them in the Explorer panel on the left. You read one count in the workspace's SQL editor, as on Monday.

**Done when:** `python3 check.py`, in this folder, prints `Done:`.

**Optional part, after step 4:** copy the address after `"run_page_url"` into the browser. It opens the run's page. Which cell took the longest?

**What you have:**

- Your profile `course` from exercise 1.
- Your schema `course.learner_NN`, with Wednesday's tables, `features` among them. `NN` is your learner number. The course made up every row.
- `job.json`, in this folder: the job's settings, from the trainer. It names one task, `features`. The task runs your copy of Wednesday's notebook, from your Git folder of the course in the workspace (`"source": "WORKSPACE"`). It names no compute (the machines that run it). The workspace then uses its default compute for jobs.
- `notes.md` and `check.py`, in this folder.

**Start from:** the trainer just ran the same file with `jobs submit`, then read the run with `jobs get-run`. Open a terminal in your course folder, then go into this folder:

Terminal:

```text
cd week-03/day-04/exercise-02-run-wednesday-as-a-job
```

To start again, put `job.json` back as the course gave it:

Terminal:

```text
git restore job.json
```

Then delete what you typed in `notes.md`. In `notes.md`, type each answer after its colon, on the same line.

### Step 1. Count Wednesday's features table, then predict

Why: you need a number from before the job runs. A job that ends well and writes a different table did not do the same work.

In the workspace's left bar, select **SQL Editor**. Select the SQL warehouse the trainer names, as on Monday. Run this query, with your learner number in place of `NN`:

SQL editor:

```sql
SELECT count(*) AS returns FROM course.learner_NN.features
```

Write the number after `features_before:`.

Then predict: after the job runs, will the count be the same? Wednesday's notebook writes each table with overwrite: it replaces the whole table, from the same return files. Write your answer and why after `predict_after:`.

### Step 2. Put your two values into job.json

Why: "Your notebook must be in a location accessible by the user configuring the job." The file names your copy of the notebook, in your own folder of the workspace. So the job runs your code, as you.

File: `job.json`. Change two values, and nothing else:

| Find | Write in its place | Why |
|---|---|---|
| `NN` in `run_name` | your learner number, such as `07` | the trainer finds your run by its name |
| `YOUR_USER_NAME` in `notebook_path` | your workspace user name, as the workspace's top bar shows it (usually your email address) | your Git folder of the course is inside your own user folder |

Save the file. Then check that it is still valid JSON:

Terminal:

```text
python3 -m json.tool job.json
```

You should see the file printed again. Then type `echo $?`. Write the number after `json_exit:`. Any number but `0` means a quote or a comma is missing. Read the error line, which names the line of the file.

### Step 3. Submit the run

Why: `jobs submit` will "Create and trigger a one-time run." The run is "not saved as a job". So you keep its run id: it is how you find the run again.

Terminal:

```text
databricks jobs submit --json @job.json --no-wait -p course
```

The `@` tells the CLI to read the file. `--no-wait` gives you the prompt back at once. You should see a short JSON text with `"run_id"` and a number. Write the number after `run_id:`. Write the exit status after `submit_exit:`.

### Step 4. Read the run back until it ends

Why: `jobs get-run` "Retrieves the metadata of a job run." The run goes on in the workspace while you wait. Nothing on the Workstation shows it.

Terminal:

```text
databricks jobs get-run <run-id> -p course
```

Put your run id in place of `<run-id>`. It prints the run as JSON. Look for `"status": {`. Inside it, read `"state"`:

| `state` | What it means | What you do |
|---|---|---|
| `QUEUED`, `PENDING` or `RUNNING` | the run has not ended | wait one minute, then run the command again |
| `TERMINATED` | the run ended | inside `"status"`, find `"termination_details"`: its `"code"` says how the run ended, and `"message"` says why |

When the state is `TERMINATED`, write it after `final_state:`. Write the `code` after `end_code:`.

If the code is `SUCCESS`, write `none` after `failed_task:` and after `error:`. If it is not, look for `"tasks": [`. Find the task whose own `"status"` did not end with `SUCCESS`. Write its `"task_key"` after `failed_task:`. Copy its `"message"` after `error:`. Then tell the trainer.

### Step 5. Count again, and compare

Why: the code says the notebook ended. The count says it wrote what you expected.

Run the query of step 1 again. Write the number after `features_after:`. After `compare:`, write one sentence: is it the same as `features_before`, and why?

### Step 6. Check

Terminal:

```text
python3 check.py
```

It prints `Done:` when `job.json` holds your two values and each line of `notes.md` fits. Otherwise it prints `Not yet:` and each thing still to do. It never runs a `databricks` command.

### Afterwards, together

1. The submit command came back in a second, and the run took minutes. Where did the notebook run, and what kept it going?
2. A submitted run is not in the workspace's jobs list. Why did you still find it?
3. The run ended with `SUCCESS`. What would have told you it wrote the wrong table?

The answer, after you try: [`answers/exercise-02-run-wednesday-as-a-job`](../answers/exercise-02-run-wednesday-as-a-job/).
