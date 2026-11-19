"""The done check for exercise 1. In Databricks, cell 4 of the notebook runs it with the text of
cells 2 and 3. It reads that text and the column names of course.returns.model_returns. No model
is called. Without Databricks: week-04/day-01/answers/stand_in.py runs the whole notebook.
"""

TABLE = "course.returns.model_returns"
YES_OR_NO_LABEL = "exam_changed_tax"   # the one column of the table that records a yes-or-no past decision


def left(columns: list[str], values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        columns: the column names of course.returns.model_returns.
        values: answers (Q1 and Q2, each a label and a why) and needs, as cells 2 and 3 hold them.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    answers = values["answers"]
    q1 = answers["Q1"]["label"].strip().strip("`")
    q2 = answers["Q2"]["label"].strip().strip("`").lower()
    if not q1:
        out.append("Cell 2: type Q1's label, a column name. Step 2.")
    elif q1 not in columns:
        out.append(f'Cell 2: "{q1}" is not a column of {TABLE}. Look at the names cell 1 printed. Step 2.')
    elif q1 == "tax_added_by_exam":
        out.append("Cell 2: tax_added_by_exam is an amount. Q1 asks yes or no. Which column holds yes or no? Step 2.")
    elif q1 != YES_OR_NO_LABEL:
        out.append(f'Cell 2: "{q1}" is a value of the return, not a past decision. Step 2.')
    if not q2:
        out.append('Cell 2: type Q2\'s label: a column name, or "no label". Step 2.')
    elif q2 != "no label":
        out.append(f'Cell 2: Q2\'s label is "{q2}". Does that column record whether a past return was amended? Step 2.')
    for question in ("Q1", "Q2"):
        if len(answers[question]["why"].split()) < 6:
            out.append(f"Cell 2: write {question}'s why in 6 words or more. Step 2.")
    if len(values["needs"].split()) < 8:
        out.append("Cell 3: write what the table would have to record, in 8 words or more. Step 3.")
    return out


def report(columns: list[str], values: dict) -> str:
    """Return what cell 4 prints: Done, or Not yet with each thing left."""
    out = left(columns, values)
    if not out:
        return "Done: Q1 learns from exam_changed_tax, a past yes-or-no decision, and Q2 has no label in this table."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Read the table's column names with spark, then return what cell 4 prints.

    Args:
        spark: the notebook's Spark session.
        values: answers and needs, as cells 2 and 3 hold them.

    Returns:
        The Done or Not yet text.
    """
    return report(spark.table(TABLE).columns, values)
