# Start in Databricks

Fork the course repository, connect your fork, try one ungraded operation, then complete
[the task](CHALLENGE.md). No local installation is needed. Use the workspace link and compute
in the Classroom environment card; ask the trainer about missing access. Never save credentials
in a notebook, repository or prompt.

You can pull the course repository but not push to it, so you work and submit in your own
public fork of it. This task lives in its `week-04/day-05/` folder; every file path on this page
is relative to that folder.

## 1. Create and connect your fork

1. Open the course repository linked in Classroom. Choose **Fork → Create a new fork** and
   select your personal account. Keep the `main` branch. A fork of this public repository is
   public; confirm the **Public** label. Use your own fork throughout this task, not the course
   repository, and keep it public so the assessment service can read it without an invitation.
2. In Databricks, open your user menu → **Settings → Linked accounts → Add Git credential**.
   Select GitHub and link your own account, allowing access to your public fork. If you linked
   it for week 3's Challenge, it is already there.
3. Open **Workspace**, go to your own user folder, then **Create → Git folder**. Paste your
   fork's HTTPS URL, select GitHub and create the folder. Check its branch is `main`. This is a
   second Git folder beside your Git folder of the course: do the Challenge only in this one.
4. Open `week-04/day-05/notebook.py` in that folder and select the compute named in Classroom.
   Its setup cell names the input tables, your MLflow experiment and your own output schema
   (only if you save tables).

## 2. Try the connection (ungraded)

Add a SQL cell to the notebook, run `SELECT COUNT(*) FROM training.to6_challenge4_inputs.new_returns`,
and confirm it returns 500. This tests compute and read access, not the Challenge. Then save a
small practice file from a Python cell:

```python
from pathlib import Path
import json

# This notebook's own folder, found when the cell runs: no path is typed, so none is saved.
notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
task_root = Path("/Workspace" + notebook_path).parent
assert (task_root / "CHALLENGE.md").is_file(), "Check the Git folder path"
practice_result = spark.sql("SELECT 1 AS connection_check").first().asDict()
assert practice_result == {"connection_check": 1}
(task_root / "outputs").mkdir(exist_ok=True)
(task_root / "outputs/connection-practice.json").write_text(
    json.dumps(practice_result) + "\n", encoding="utf-8"
)
```

The filename is relative to this task's folder, `week-04/day-05/` in your Git folder. An
explicit path is needed because serverless compute does not guarantee the notebook's working
directory. Refresh the Workspace folder and open the file. This example only shows how to save
a file; it is not part of the task.

Open the Git dialog by clicking the branch name. Review the changes, enter a commit message,
then **Commit & Push**. Open your fork on GitHub and confirm the file changed in
`week-04/day-05/` on `main`. If a read, write or push fails, resolve it with the trainer before
starting the task. Do not turn in this practice result.

## 3. Do the task and save your evidence

Use the scaffold's headings for the outcomes in [CHALLENGE.md](CHALLENGE.md). The setup cell
defines `INPUT_SCHEMA`, `CLOSED_TABLE`, `NEW_TABLE` and `EXPERIMENT`. Read the input
descriptions in Catalog Explorer. Do not change the shared input tables.

Record your runs in the experiment the setup cell names; open it from the workspace's
**Experiments** page to see them. The notebook's given cell under heading 3 writes
`outputs/runs.csv` from the runs, keeping only the columns the brief lists. Genie Code may help if enabled; review and check its suggestions.

Edit `SUBMISSION.md` in the Databricks file editor, or write it from a notebook Python cell with
`(task_root / "SUBMISSION.md").write_text(your_text, encoding="utf-8")`. Use the practice
file-writing pattern for your exports under `outputs/`.

## 4. Submit the completed task

Review the deliverables in [CHALLENGE.md](CHALLENGE.md), then **Commit & Push** from the Git
dialog. In GitHub, open the resulting commit and check `week-04/day-05/notebook.py`,
`week-04/day-05/SUBMISSION.md` and both required exports in `week-04/day-05/outputs/`. Record
that commit's full SHA. Confirm your fork is **Public** so the assessment service can read it
without an invitation.

In Classroom, use **Add or create → Link** for your fork's base URL
(`https://github.com/YOUR-USERNAME/YOUR-FORK`). Add branch `main` and the final SHA in a private
comment, then **Turn in** by the assignment's deadline.

References: [Git folder operations](https://docs.databricks.com/aws/en/repos/git-operations-with-repos),
[writing workspace files](https://docs.databricks.com/aws/en/files/workspace-interact),
[MLflow experiments](https://docs.databricks.com/aws/en/mlflow/experiments),
[Genie Code](https://docs.databricks.com/aws/en/notebooks/code-assistant).
