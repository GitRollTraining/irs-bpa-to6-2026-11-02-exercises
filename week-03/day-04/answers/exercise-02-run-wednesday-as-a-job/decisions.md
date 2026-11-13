# Exercise 2: decisions

For the trainer. Exercise 2, "Run Wednesday's notebook as a one-off job", follows the demo that submits the same job file and reads the run with `get-run` (deck slides 35 to 37). The one new thing is a job. Modelled on Microsoft Learning's DP-750T00 lab 12, part 3, "Deploy and Verify the Bundle with the Databricks CLI" (https://microsoftlearning.github.io/DP-750T00-Implement-Data-Engineering-Solutions-using-Azure-Databricks/Instructions/Labs/12-implement-development-lifecycle-processes-in-azure-databricks.html): deploy a job from the CLI, then verify it with the CLI and in the workspace. Here the job is a one-off run, not a bundle; the run is verified with `jobs get-run` and a row count. The command follows Databricks' jobs command group (https://docs.databricks.com/aws/en/dev-tools/cli/reference/jobs-commands). Shape: "Follow and confirm". Every page below was opened on 2026-11-13.

Where it ran: nowhere with Databricks. The course team ran the check on this machine on the starting files, the kept answer and one wrong record (`commands.sh`). The counts (52, the number of returns in the trainer's XML files, as Wednesday's kept answer reads it) and the run id in `notes.md` are a stand-in for the run on a Workstation. The run on a Workstation is a trainer gap: `week-03/setup/day-04-setup.md` § Not yet checked, items 3 and 4.

## 1. The count before, and the prediction (the predict question)

- **The answer.** The same count before and after: the notebook writes each table with overwrite, from the same return files, so a rerun replaces the table with the same rows.
- **Reason.** A job's code says the run ended; only the table says what it wrote.
- **Where it comes from.** Wednesday's plan: "The notebook writes them with overwrite, so it reruns top to bottom as a job." The README states it in step 1, so the reason is in the steps.
- **What else the check accepts.** Any prediction of 5 words or more that gives a reason (same, overwrite, rewrite, replace or files).

## 2. job.json

- **The answer.** `run_name` ends in the learner number; `notebook_path` holds the learner's user name; nothing else changes. The path ends `week-03/day-03/wednesday-tables`, Wednesday's one notebook, with no `.ipynb`: the notebook task page shows a file extension only for a Git provider's relative path ("`etl/bronze/ingest.py`"), and a notebook in the workspace has no extension. Not confirmed: trainer gap, item 4. `python3 -m json.tool job.json` prints the file, exit status 0.
- **Reason.** A notebook task reads the notebook from a path the learner can reach, and the job runs as the learner.
- **Pages.** Notebook task for jobs (https://docs.databricks.com/aws/en/jobs/notebook): "Your notebook must be in a location accessible by the user configuring the job." Jobs API, the run's fields (https://docs.databricks.com/api/workspace/jobs/submit): `notebook_path` "The path of the notebook to be run in the <Databricks> workspace or remote repository."; `source` `WORKSPACE`, "Notebook is located in <Databricks> workspace."
- **No compute in the file.** The file names no cluster, so the run takes the workspace's default for jobs. Configure compute for jobs (https://docs.databricks.com/aws/en/jobs/compute): "serverless compute is the default for all tasks that support it." Where the workspace has no serverless compute for jobs, the trainer adds a cluster to the file before class (trainer gap, item 3).
- **A difference from the brief.** The brief had the learner change only the profile and the learner number. The notebook sits in the learner's Git folder, which is inside the learner's own user folder, so the path holds the learner's user name; the learner writes it. A file per learner from the trainer would avoid it, but each Workstation would need its own copy.

## 3. Submit, and the run id

- **The answer.** `databricks jobs submit --json @job.json --no-wait -p course` prints the run id at once; exit status 0.
- **Pages.** Jobs commands: `jobs submit` will "Create and trigger a one-time run."; `--json` "The inline JSON string or the @path to the JSON file with the request body."; `--no-wait` "do not wait to reach TERMINATED or SKIPPED state"; "Jobs submitted with `databricks jobs submit` are not saved as a job." "They do not show up in the UI, and do not retry when they fail."
- **Why `--no-wait`.** Without it the command waits up to 20 minutes ("default 20m0s"), and the learner reads nothing until it ends. The plan asks the learner to read the run id and poll `get-run`.

## 4. get-run, and the final state

- **The answer.** `status.state` `TERMINATED`, `status.termination_details.code` `SUCCESS`, and `none` after `failed_task:` and `error:`. On a failed run: the task's `task_key` (`features`) and the `message`.
- **Pages.** Jobs commands: "databricks jobs get-run RUN_ID [flags]", "Retrieves the metadata of a job run." Jobs API, get a run (https://docs.databricks.com/api/workspace/jobs/getrun): `state` is "Deprecated. Please use the `status` field instead."; `status.state` values `BLOCKED`, `PENDING`, `QUEUED`, `RUNNING`, `TERMINATING`, `TERMINATED`, `WAITING`; `termination_details`, "If the run is in a TERMINATING or TERMINATED state, details about the reason for terminating the run."; `run_page_url`, "The URL to the detail page of the run."
- **What else the check accepts.** A run that ended with another code is done when the failed task and its error (5 words or more) are written: the plan's "or the failed task and its error".

## 5. The count after

- **The answer.** The same as before.
- **What else the check accepts.** Any count, with a sentence of 5 words or more. A different count is a finding to show the trainer, not a failure of the exercise.
