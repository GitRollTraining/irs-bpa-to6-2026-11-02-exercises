"""The done check for exercise 2. In Databricks, cell 5 of the notebook runs it with the values of
cells 2 to 4. It counts the labels of course.returns.model_train again with Spark and compares. No
model is called. Without Databricks: week-04/day-01/answers/stand_in.py runs the whole notebook.
"""

TABLE = "course.returns.model_train"
LABEL = "exam_changed_tax"


def counts(spark: object) -> dict:
    """Count each label value of the training set: {"yes": n, "no": n, None: n}."""
    rows = spark.sql(f"SELECT {LABEL} AS label, COUNT(*) AS n FROM {TABLE} GROUP BY {LABEL}").collect()
    return {r["label"]: int(r["n"]) for r in rows}


def as_share(value: object) -> float | None:
    """Read a prediction as a share from 0 to 1: 0.8, "0.8", "80%" and 80 all read as 0.8; else None."""
    try:
        share = float(str(value).strip().rstrip("%"))
    except (TypeError, ValueError):
        return None
    if 1 < share <= 100:
        share /= 100
    return share if 0 <= share <= 1 else None


def left(found: dict, values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        found: each label value of the training set and its count, from counts().
        values: column, prediction, most_common, right and labelled, as cells 2 to 4 hold them.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    labelled_rows = {k: v for k, v in found.items() if k is not None}
    top = max(labelled_rows, key=labelled_rows.get)
    if values["column"].strip() != LABEL:
        out.append(f'Cell 2 counts "{values["column"]}". Change it to "{LABEL}", the label, and run it again. Step 2.')
    if as_share(values["prediction"]) is None:
        out.append("Cell 3: type your guess after prediction =, a share from 0 to 1, such as 0.6. Step 3.")
    if str(values["most_common"]).strip().lower() != top:
        out.append("Cell 4: most_common is the label with the most rows in cell 2's counts. Step 4.")
    if values["right"] != labelled_rows[top]:
        out.append("Cell 4: right is how many returns the baseline predicts right: the count of its label. Step 4.")
    if values["labelled"] == sum(found.values()):
        out.append(f"Cell 4: labelled counts the {found.get(None, 0)} empty rows too. Leave them out: they have no label. Step 4.")
    elif values["labelled"] != sum(labelled_rows.values()):
        out.append("Cell 4: labelled is every return with a label, yes or no. Step 4.")
    return out


def report(found: dict, values: dict) -> str:
    """Return what cell 5 prints: Done, or Not yet with each thing left."""
    out = left(found, values)
    if not out:
        labelled_rows = {k: v for k, v in found.items() if k is not None}
        top = max(labelled_rows, key=labelled_rows.get)
        total = sum(labelled_rows.values())
        return (f'Done: always predicting "{top}" is right on {labelled_rows[top]} of the {total} labelled training returns: '
                f"accuracy {labelled_rows[top] / total:.2f}. Your prediction was {as_share(values['prediction']):.2f}.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Count the training set's labels with spark, then return what cell 5 prints.

    Args:
        spark: the notebook's Spark session.
        values: column, prediction, most_common, right and labelled, as cells 2 to 4 hold them.

    Returns:
        The Done or Not yet text.
    """
    return report(counts(spark), values)
