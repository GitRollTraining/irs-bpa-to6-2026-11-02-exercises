"""Given code for exercise 1: cell 1 runs it. It reads the course's training and validation sets,
course.returns.model_train and course.returns.model_valid, and adds Monday's flag deduction_missing:
1 where deduction_amt is empty. It changes no table. You do not need to read it."""
import pandas as pd

COPY = ("The tables course.returns.model_train and model_valid couldn't be read, so this notebook makes the "
        "same rows from the course's setup file, week-04/setup/day-01-course-data.py. Every number is the same.")
SETUP = f"{course_folder}/week-04/setup/day-01-course-data.py"


def course_rows(name: str) -> pd.DataFrame:
    """The rows of one of the course's sets, made by the course's setup file, as the table holds them."""
    made = {"__name__": "course_data"}
    exec(open(SETUP, encoding="utf-8").read(), made)
    return pd.DataFrame(made["set_rows"](name))


def load_sets(train_table, valid_table):
    """Return (train, valid) as pandas tables, from the course's tables or, when they cannot be read,
    from the course's setup file, with the flag deduction_missing: 1 where deduction_amt is empty."""
    try:
        train, valid = train_table.toPandas(), valid_table.toPandas()
        own = len(train) > 0 and len(valid) > 0
    except Exception:
        own = False
    if own:
        print("Using the course's tables course.returns.model_train and course.returns.model_valid.")
    else:
        train, valid = course_rows("model_train"), course_rows("model_valid")
        print(COPY)
    out = []
    for table in (train, valid):
        table = table.copy()
        table["deduction_missing"] = table["deduction_amt"].isna().astype(int)  # Monday's flag: 1 where empty
        table["exam_changed_tax"] = table["exam_changed_tax"].where(table["exam_changed_tax"].notna(), None)
        out.append(table.reset_index(drop=True))
    print(len(out[0]), "returns in model_train,", len(out[1]), "in model_valid")
    return out[0], out[1]
