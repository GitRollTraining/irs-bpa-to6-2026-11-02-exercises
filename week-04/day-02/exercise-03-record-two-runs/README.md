# Exercise 3: Record both fits as runs, and name the higher from the record

**Goal:** After this exercise, you can record two fits as MLflow runs and name the candidate with the higher accuracy from what the runs recorded. Wednesday judges the two.

**Scenario:** Three weeks from now, someone asks which of your two models had the higher accuracy, on which rows, and with which settings. You record both fits now, so that the answer comes from the record and not from memory.

**AI tool:** none.

**Time:** 15 minutes: 11 to do it, 4 for setup problems.

**Where you work:** this notebook, `week-04/day-02/exercise-03-record-two-runs/exercise.ipynb`, in your Git folder of the course in Databricks, then the workspace's Experiments page. Databricks may show tips under a cell, such as one about MLflow or Genie Code. Close them: they change nothing.

**Done when:** cell 8 prints `Done:`.

**Cells:** a cell's number is the `# N.` comment on its first line, such as `# 1.`; text cells have no number.

**Optional part:** Finished early? Cell 9 asks for one sentence on retraining.

**What you have:**

- `course.returns.model_train` and `course.returns.model_valid`, the course's training and validation sets. If they cannot be read, cell 2 makes the same rows from the course's setup file and says so.
- `load.py` and `check.py`: given code.

**Start from:** this notebook as the course gives it, on the trainer's compute. No cell changes your tables. Cell 3 makes an experiment, `week-04-candidates`, in your Home folder; cell 5 records 2 runs in it. New here: a run and its record.

### Step 1. Fit the two candidates again, and open your experiment

This is a new notebook, so exercise 2's candidates are not in its memory yet. Run cells 1 to 4. You do not need to change them. You should see:

1. The two candidates fitted again, and the split: the tax years of the training and validation rows.
2. Your experiment's name. Cell 3 makes it the first time.
3. What each run should record: exercise 2's two accuracies.

Notebook cell 1:

```python
# 1. Where the course's files are. You do not need to change this cell.
import os
course_folder = os.getcwd().split("/week-04/")[0]  # your Git folder of the course
print("Your Git folder of the course:", course_folder)
```

Notebook cell 2:

```python
# 2. Fit the two candidates of exercise 2 again, with the same cells.
try:
    train_table = spark.table("course.returns.model_train")  # the training set
    valid_table = spark.table("course.returns.model_valid")  # the validation set
except Exception:
    train_table, valid_table = None, None  # not there: load.py makes the same rows

# You do not need to read the lines below. They run load.py.
folder = f"{course_folder}/week-04/day-02/exercise-03-record-two-runs"
exec(open(f"{folder}/load.py", encoding="utf-8").read())
candidates, split = fit_candidates(train_table, valid_table)
```

Notebook cell 3:

```python
# 3. Your experiment: the place that holds your runs for this task.
import mlflow

user = spark.sql("SELECT current_user()").first()[0]  # your user name in the workspace
experiment = f"/Users/{user}/week-04-candidates"
mlflow.set_experiment(experiment)  # makes the experiment the first time; after that it opens it
print("Your experiment:", experiment)
```

Notebook cell 4:

```python
# 4. What each run should record: exercise 2's two accuracies, as cell 2 fitted them again.
expected = {name: round(accuracy, 3) for name, (_, accuracy) in candidates.items()}
for name, accuracy in expected.items():
    print(f"{name}: {accuracy:.3f}, as exercise 2's cell 7 showed")
```

### Step 2. Record each candidate as a run

"Two runs compare fairly only when they use the same data, the same split and the same measure." (the day's reading) So beside the model's settings, each run records the split and the measure.

1. Run cell 5. You should see `Recorded the run logistic-regression`.
2. In cell 5, type `decision-tree` in place of `logistic-regression`. Change nothing else. Run cell 5 again. You should see `Recorded the run decision-tree`.

What cell 5 calls:

- `start_run` starts a run.
- `log_param` writes one parameter into it: a setting, the split or the measure.
- `log_metric` writes the measured accuracy.
- `log_model` saves the fitted model with the run.
- `set_tag` notes that the model was saved.

Two warnings may show while the model is saved: `Encountered unexpected error during resolving tags` and `Model logged without a signature`. They are normal: the run is still saved.

Notebook cell 5:

```python
# 5. Record one candidate as a run. Change only the run name, then run this cell again.
run_name = "logistic-regression"  # the run's name: logistic-regression first, then decision-tree

assert run_name in candidates, "Type logistic-regression or decision-tree as the run name."
model, accuracy = candidates[run_name]
with mlflow.start_run(run_name=run_name):
    mlflow.log_param("model_type", model_name(model))     # a setting of the model: its type
    if run_name == "decision-tree":
        mlflow.log_param("max_depth", model.max_depth)    # the tree's setting
    mlflow.log_param("split", split)                      # the rows it was fitted and measured on
    mlflow.log_param("measure", "accuracy")               # how it was measured
    mlflow.log_metric("validation_accuracy", accuracy)    # a measured result
    try:
        mlflow.sklearn.log_model(model, name="model")     # the fitted model itself
    except TypeError:                                     # an older MLflow names it artifact_path
        mlflow.sklearn.log_model(model, artifact_path="model")
    mlflow.set_tag("model_logged", "yes")                 # reached only once the model is saved
print("Recorded the run", run_name)
```

### Step 3. Read both runs back

Run cell 6. It reads every run in your experiment and keeps the newest of each name. You should see one line for each run, with its model type, its accuracy and its split. If a line says `Not what cell 4 expects`, run cell 5 again for that run name.

Notebook cell 6:

```python
# 6. Read both runs back from the experiment. The newest run of each name counts.
runs = mlflow.search_runs(experiment_names=[experiment])          # every run, newest first
newest = runs.drop_duplicates("tags.mlflow.runName") if len(runs) else runs  # the newest run of each name
print(len(runs), "runs in your experiment. The newest of each name:")
for _, run in newest.iterrows():
    name, recorded = run["tags.mlflow.runName"], run["metrics.validation_accuracy"]
    print(f"{name}: {run['params.model_type']}, {run['params.measure']} {recorded:.3f}. Split: {run['params.split']}")
    if name in expected and abs(expected[name] - recorded) > 0.0005:  # you do not need to read this line and the next
        print(f"  Not what cell 4 expects ({expected[name]:.3f}). Run cell 5 again for {name}.")
```

### Step 4. Compare the two runs on the Experiments page

1. In the workspace's left sidebar, click **Experiments**, then **Owned by me**, then open `week-04-candidates`. Every learner's experiment has this name, so open your own. You should see one row for each run.
2. Tick the boxes of the two newest runs, one of each name, then click **Compare**. You should see each run's parameters and its `validation_accuracy`, the same numbers as cell 6. Use the **Bar Chart** tab: the plot of lines draws the logistic regression on the `max_depth` axis, which only the tree has.
3. Optional: open one run and look for its logged model. The trainer shows where it is.

This step has no cell.

### Step 5. Name the candidate with the higher accuracy, and check

1. In cell 7, type the name of the run that cell 6 shows with the higher validation accuracy. Run cell 7. You should see both runs' accuracies.
2. Run cell 8. It prints `Done:`, or `Not yet:` and what is left.

Notebook cell 7:

```python
# 7. The candidate with the higher accuracy, as the runs recorded it.
higher = ""  # type logistic-regression or decision-tree

for _, run in newest.iterrows():
    print(f"{run['tags.mlflow.runName']}: validation accuracy {run['metrics.validation_accuracy']:.3f}")
print("Higher:", higher or "(not yet)")
```

Notebook cell 8:

```python
# 8. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{folder}/check.py", encoding="utf-8").read(), _check)
check_now = _check["in_notebook"]
print(check_now(globals()))
```

### Finished early?

Optional: cell 8 does not check it.

"*Retraining* is the same recorded training, run again on newer labelled returns, on a schedule." (the day's reading) In cell 9, write one sentence: when should this model be retrained? Run cell 9.

Notebook cell 9:

```python
# 9. Optional: one sentence on retraining.
retrain = ""
print(retrain or "Write your sentence between the quotes.")
```

### Afterwards, together

1. Why compare from the runs and not from your notebook?
2. What makes two runs a fair comparison?
3. Asked for a model's parameters, what do you ask back?

The answer, after you try: [`answers/exercise-03-record-two-runs`](../answers/exercise-03-record-two-runs/).
