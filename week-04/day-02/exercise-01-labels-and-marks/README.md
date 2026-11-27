# Exercise 1: Count your labels, say their origin, mark each feature

**Goal:** After this exercise, you can record where your labels came from and mark each feature as known before or after selection.

**Scenario:** You were handed made-up returns, most of them labelled with an examination's result, and asked for a model. Before you train, you check the labels, and whether each column was known before the case was selected.

**AI tool:** none.

**Time:** 15 minutes: 12 to do it, 3 for setup problems.

**Where you work:** this notebook, `week-04/day-02/exercise-01-labels-and-marks/exercise.ipynb`, in your Git folder of the course in Databricks.

**Done when:** cell 8 prints `Done:`.

**Cells:** a cell's number is the `# N.` comment on its first line, such as `# 1.`; text cells have no number.

**Optional part:** Finished early? Cell 9 asks for one sentence.

**What you have:**

- `course.returns.model_train`, the course's training set, as on Monday. Its label `exam_changed_tax` is `yes` when an examination changed the tax, `no` when it did not, and empty when nobody examined the return. If it cannot be read, cell 2 makes the same rows from the course's setup file and says so.
- Monday's feature record, four rows, as Monday's exercise 3 ends: cell 2 prints it. You need nothing saved from Monday.
- `fields.csv`: two made-up columns, matched to the returns by `return_id`. Its first lines say what each column holds.
- `refund-held.csv` (the trainer's demo), `load.py` and `check.py` (given code).

**Start from:** this notebook as the course gives it, on the trainer's compute. No cell changes your tables. New here: a file of two more columns, `fields.csv`.

### Step 1. Load

1. Run cell 1. You should see your Git folder of the course.
2. Run cell 2. You should see which table it uses, then the four rows of Monday's feature record. You need nothing saved from Monday: the notebook gives the record.

Notebook cell 1:

```python
# 1. Find your Git folder of the course. Run it; you change nothing.
import os
course_folder = os.getcwd().split("/week-04/")[0]  # your Git folder of the course
print("Your Git folder of the course:", course_folder)
```

Notebook cell 2:

```python
# 2. Load the course's training set, the made-up columns, and Monday's feature record.
try:
    train_table = spark.table("course.returns.model_train")  # the course's training set
except Exception:
    train_table = None  # not there: load.py makes the same rows

# You do not need to read the lines below. They run load.py.
folder = f"{course_folder}/week-04/day-02/exercise-01-labels-and-marks"
exec(open(f"{folder}/load.py", encoding="utf-8").read())
train, record = load_day(train_table)
```

### Step 2. Count each value of your label

"A return with an empty label is not counted as either outcome, and it is left out of training." (the day's reading)

Cell 3 counts `refund_held`, the made-up label of the trainer's demo. In cell 3, type `exam_changed_tax`, the course's label, in its place, and run it. You should see Monday's counts: `no` 320, `yes` 80, `empty` 100.

Notebook cell 3:

```python
# 3. Count the values of one label in the training set.
label_column = "refund_held"  # the label to count: the demo's refund_held, or the course's exam_changed_tax

counts = train[label_column].value_counts(dropna=False)
for value, n in counts.items():
    print(f"{value if isinstance(value, str) else 'empty'}: {n} returns")
```

### Step 3. Write the labels' origin

"A *label's origin* is the answer to those three questions: which past decision made the label, who made it, and when." (the day's reading)

In cell 4, type an answer of two words or more between each pair of quotes, from the facts below. Run cell 4.

| Question | The fact that decides it |
|---|---|
| `decision` | `yes` means that the examination changed the tax |
| `made by` | the course's data: "The course's data gives some returns a label that stands for an examination's result." (the day's reading) On a real return, an examiner would make it. |
| `when` | an examination closes after the return was filed and selected |

Notebook cell 4:

```python
# 4. The labels' origin: one answer between each pair of quotes.
origin = {
    "decision": "",  # which past decision made the label
    "made by": "",   # who made it
    "when": "",      # when it was made
}
for question, answer in origin.items():
    print(f"{question}: {answer or '(not yet)'}")
```

### Step 4. Put each column of the file beside the label

"A feature that matches the label almost exactly is a warning sign of leakage." (the day's reading)

A column agrees with the label on a return when it is above zero and the label is `yes`, or zero and the label is `no`.

In cell 5, type `fields.csv` in place of `refund-held.csv`, and run it. For each column of the file, you should see how many labelled returns agree with the label, then what the file says of each column.

Notebook cell 5:

```python
# 5. Put each column of a file beside the label, and count how often each one agrees with it.
beside = "refund-held.csv"  # the file to read: the demo's refund-held.csv, or the exercise's fields.csv

columns = [c for c in read_csv(beside).columns if c not in ("return_id", "refund_held")]  # not the key or the demo's label
labelled = train[train[label_column].notna()]
agreement_label, agreement = label_column, {}
for column in columns:
    agree = (labelled[column] > 0) == (labelled[label_column] == "yes")  # above zero with yes, or zero with no
    agreement[column] = int(agree.sum())
    print(f"{column} agrees with {label_column} on {agreement[column]} of {len(labelled)} returns with a label.")
print(f"What {beside} says of each column:")
for column, note in read_notes(beside).items():
    print(f"  {column}: {note}")
```

### Step 5. Trace the column that matches

"When you find such a feature, trace it to where it came from: which table holds it, which step wrote it, and when. The answer to *when* decides." (the day's reading) The reading's *step* is a stage of the tax work, so the slot below is called `which stage wrote it`.

1. In cell 6, type the name of the column that agrees with the label on nearly every return.
2. Answer which stage of the tax work wrote it: what changes the tax on an account after a return is filed? The trace's first question, which table holds it, is filled in for you: `fields.csv`. The trace's last question, *when*, is answered by your mark (`before` or `after`) in cell 7. Run cell 6.

Notebook cell 6:

```python
# 6. Trace the column that agrees with the label on nearly every return.
suspect = ""  # its name, from cell 5's counts
trace = {
    "which table holds it": beside,  # given: the file cell 5 read
    "which stage wrote it": "",       # which stage of the tax work writes this column
}
print("The column:", suspect or "(not yet)")
for question, answer in trace.items():
    print(f"{question}: {answer or '(not yet)'}")
```

### Step 6. Mark each feature `before` or `after`

Ask one question of each feature: "was it known before the case was selected? Mark each feature *before* or *after*. Train only on the features marked *before*." (the day's reading)

The course supplies Monday's record, which already marks its four rows: cell 7 gives them. In cell 7, mark the column you traced: its slot already holds its name. Type `before` or `after`, then a reason of three words or more that says when the column was written. The other column cell 5 counted, `days_to_file`, is given, marked the same way. Run cell 7. You should see four features under `Train on:` and two under `Leave out:`.

Notebook cell 7:

```python
# 7. Mark each feature: "before" or "after" the case was selected, and why.
demo_marks = {  # the trainer's demo: two other features, as an example of the form
    "filing_status": ("before", "it is on the filed return"),
    "refund_hold_days": ("after", "counted from the day a refund hold started"),
}
marks = {  # supplied by the course: the four rows Monday's record marks
    "tax_to_agi": ("before", "both amounts are on the filed return"),
    "deduction_amt": ("before", "line 12e is on the filed return"),
    "deduction_missing": ("before", "whether line 12e is empty shows on the filed return"),
    "tax_added_by_exam": ("after", "written when the examination closed"),
}
file_marks = [  # each column of fields.csv: its name, "before" or "after", then a reason
    (suspect, "", ""),  # the column you traced in cell 6
    ("days_to_file", "before", "counted to the day the return arrived"),  # the other column cell 5 counted: given
]
marks.update({name: (mark, reason) for name, mark, reason in file_marks})
print("Train on:", ", ".join(f for f, (mark, _) in marks.items() if mark.strip().lower() == "before"))
print("Leave out:", ", ".join(f for f, (mark, _) in marks.items() if mark.strip().lower() == "after"))
```

### Step 7. Check

Run cell 8. It prints `Done:`, or `Not yet:` and what is left.

Notebook cell 8:

```python
# 8. Check. You do not need to read this code. It runs check.py, beside this notebook.
_check = {"__name__": "check"}
exec(open(f"{folder}/check.py", encoding="utf-8").read(), _check)
print(_check["in_notebook"]({
    "train": train, "label_column": label_column, "origin": origin, "beside": beside,
    "agreement_label": agreement_label, "agreement": agreement, "labelled": len(labelled),
    "suspect": suspect, "trace": trace, "marks": marks}, folder))
```

### Finished early?

Optional: cell 8 does not check it.

In cell 9, write one sentence: why does the column you traced miss one return labelled `yes`? What the file says of it holds the clue. Run cell 9.

Notebook cell 9:

```python
# 9. Optional: one sentence.
why_one_missed = ""
print(why_one_missed or "Write your sentence between the quotes.")
```

### Afterwards, together

1. Why is an empty label not counted as a no?
2. What would change your answer on who made these labels?
3. Why trace a matching feature before you strike it?

The answer, after you try: [`answers/exercise-01-labels-and-marks`](../answers/exercise-01-labels-and-marks/).
