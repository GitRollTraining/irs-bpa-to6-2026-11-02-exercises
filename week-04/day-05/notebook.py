# Databricks notebook source
# MAGIC %md
# MAGIC # The Harbor group's list
# MAGIC Follow CHALLENGE.md. These headings are a starting point; implement and check each stage yourself.

# COMMAND ----------
import hashlib
from pathlib import Path

INPUT_SCHEMA = "training.to6_challenge4_inputs"
CLOSED_TABLE = f"{INPUT_SCHEMA}.closed_returns"
NEW_TABLE = f"{INPUT_SCHEMA}.new_returns"
workspace_user = spark.sql("SELECT current_user() AS username").first()["username"]
EXPERIMENT = f"/Users/{workspace_user}/week-04-challenge"  # your MLflow experiment for this task
OUTPUT_SCHEMA = "training.to6_c4_" + hashlib.sha256(workspace_user.encode("utf-8")).hexdigest()[:12]  # if you save tables
# This notebook's own folder, found when the cell runs: no path is typed into this file, so none is pushed.
_notebook_path = dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
TASK_ROOT = Path("/Workspace" + _notebook_path).parent
OUTPUTS = TASK_ROOT / "outputs"  # your exports go here
print({"closed": CLOSED_TABLE, "new": NEW_TABLE, "output_schema": OUTPUT_SCHEMA,
       "outputs": "week-04/day-05/outputs/ beside this notebook"})

# COMMAND ----------
# MAGIC %md
# MAGIC ## 1. Know the group's result

# COMMAND ----------
# Your work here.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 2. Choose what the model may learn from

# COMMAND ----------
# Your work here.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 3. Train and record two candidates
# MAGIC Record each candidate as its own run in `EXPERIMENT`. Then run the given cell after yours: it writes
# MAGIC `outputs/runs.csv` from the runs.

# COMMAND ----------
# Your work here.

# COMMAND ----------
# Given: write outputs/runs.csv from the runs as MLflow returns them. It keeps only the run ID, the run
# name, the parameters and the metrics: MLflow's other columns hold your user name and notebook path,
# and this file is pushed to your public fork.
import mlflow

_runs = mlflow.search_runs(experiment_names=[EXPERIMENT])
_keep = ["run_id", "tags.mlflow.runName"] + sorted(c for c in _runs.columns if c.startswith(("params.", "metrics.")))
OUTPUTS.mkdir(exist_ok=True)
_runs[_keep].rename(columns={"tags.mlflow.runName": "run_name"}).to_csv(OUTPUTS / "runs.csv", index=False)
print(f"Wrote outputs/runs.csv: {len(_runs)} runs, columns {', '.join(_keep)}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## 4. Set the group's list

# COMMAND ----------
# Your work here.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 5. Make the list defensible
# MAGIC The given cell below shows Thursday's pushes for one return, for either model type: call
# MAGIC `pushes(model, X_train, X_return)` with your chosen model (or its pipeline), the training rows
# MAGIC it learned from, and a one-row table for the return. Read the unit it prints before you
# MAGIC write a number: a logistic regression's pushes are in log-odds, a tree's in score.

# COMMAND ----------
# Given: each feature's push on one return's output, from SHAP, for a logistic regression or a tree.
import pandas as pd

try:
    import shap
except ImportError:
    raise ImportError("Run `%pip install shap` in a cell of its own, then run this cell again.")


def pushes(model, X_train: pd.DataFrame, X_return: pd.DataFrame) -> pd.DataFrame:
    """How far each feature moved X_return's output from that of a return with average values.

    model: a fitted LogisticRegression or DecisionTreeClassifier, or a Pipeline ending in one.
    X_train: the training rows, the features the model learned from. X_return: one row, the same columns.
    """
    steps = getattr(model, "steps", None)
    estimator = steps[-1][1] if steps else model
    background = model[:-1].transform(X_train) if steps else X_train
    row = model[:-1].transform(X_return) if steps else X_return
    if hasattr(estimator, "coef_"):
        values, unit = shap.LinearExplainer(estimator, background).shap_values(row), "log-odds"
    else:
        values, unit = shap.TreeExplainer(estimator, background).shap_values(row), "score"
    values = values[1] if isinstance(values, list) else values  # the class "change", where SHAP splits by class
    values = values[..., 1] if getattr(values, "ndim", 2) == 3 else values
    table = pd.DataFrame({"feature": list(X_train.columns), "value": X_return.iloc[0].tolist(),
                          "push": [round(float(v), 3) for v in values[0]]})
    print(f"Pushes in {unit}, largest first. A push is evidence of what moved the score, never a finding.")
    return table.reindex(table["push"].abs().sort_values(ascending=False).index).reset_index(drop=True)

# COMMAND ----------
# Your work here.

# COMMAND ----------
# MAGIC %md
# MAGIC ## 6. Two tasks: trained model or prompting; the report and the exports
# MAGIC For each task, write your choice, your reasons and who checks the output in SUBMISSION.md:
# MAGIC - the cover-sheet summary;
# MAGIC - letters about paying over time, each sent to one of three teams.
# MAGIC
# MAGIC Write SUBMISSION.md beside this notebook and the exports under `OUTPUTS`, in week-04/day-05/ of your fork's Git folder.

# COMMAND ----------
# Your work here.
