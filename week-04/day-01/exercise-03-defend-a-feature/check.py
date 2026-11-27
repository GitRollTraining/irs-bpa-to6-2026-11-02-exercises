"""The done check for exercise 3. In Databricks, cell 5 of the notebook runs it with the values of
cells 1 and 3. It reads the two tables you wrote, features_flagged and model_feature_record, and
compares your flag with the empty cells of course.returns.model_features. No model is called.
Without Databricks: week-04/day-01/answers/stand_in.py runs the whole notebook.
"""

SOURCE = "course.returns.model_features"
AMOUNT = "deduction_amt"
GIVEN = ("tax_to_agi", "tax_added_by_exam")


def flag_facts(spark: object, table: str, flag: str) -> dict:
    """Count the rows of the flagged table, and the rows whose flag disagrees with an empty deduction_amt."""
    row = spark.sql(f"SELECT COUNT(*) AS n, SUM({flag}) AS flagged, "
                    f"SUM(CASE WHEN ({AMOUNT} IS NULL) <> ({flag} = 1) THEN 1 ELSE 0 END) AS wrong FROM {table}").first()
    return {"rows": int(row["n"]), "flagged": int(row["flagged"] or 0), "wrong": int(row["wrong"] or 0)}


def record_left(rows: list[dict], flag: str) -> list[str]:
    """What is missing from the record: the two given rows, and a filled row for deduction_amt and the flag."""
    out = []
    by_feature = {str(r["feature"]).strip(): r for r in rows}
    for name in GIVEN:
        if name not in by_feature:
            out.append(f"Cell 4: keep the given row for {name}. Step 4.")
    for name in (AMOUNT, flag):
        row = by_feature.get(name)
        if row is None:
            out.append(f"Cell 4: the record has no row for {name}. Step 4.")
            continue
        if "12e" not in str(row["source_field"]):
            out.append(f"Cell 4: the source field of {name} names its line of the form, 12e. Step 4.")
        if len(str(row["reason"]).split()) < 6:
            out.append(f"Cell 4: write the reason for {name} in 6 words or more. Step 4.")
        known = str(row["known_at_selection"]).strip().lower()
        if known not in ("yes", "no"):
            out.append(f'Cell 4: type "yes" or "no" for {name}: is it known when the case is selected? Step 4.')
        elif known != "yes":
            out.append(f"Cell 4: read the timing of {name} again: is line 12e on the return when it is filed? Step 4.")
        if len(str(row["timing"]).split()) < 4:
            out.append(f"Cell 4: say why {name} is known at selection or not, 4 words or more. Step 4.")
    return out


def left(spark: object, values: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        spark: the notebook's Spark session.
        values: schema, empty_means, why_empty and flag, as cells 1 and 3 hold them.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    schema, flag = values["schema"].strip(), values["flag"].strip()
    if schema.endswith("_NN"):
        return ["Cell 1 still names course.learner_NN. Type the part of your schema's name after learner_, then run cells 1 to 5. Step 1."]
    out = []
    meaning = values["empty_means"].strip().lower()
    if meaning not in ("zero", "unknown"):
        out.append('Cell 3: type "zero" or "unknown" for empty_means. Step 3.')
    elif meaning == "zero":
        out.append("Cell 3: read again what line 12e holds, in the form's words, and what a return must put there. "
                   "Then decide again what an empty line 12e means. Step 3.")
    if len(str(values.get("why_empty", "")).split()) < 6:
        out.append("Cell 3: write why_empty, your reason, in 6 words or more. Step 3.")
    flagged = f"{schema}.features_flagged"
    if not flag:
        out.append("Cell 3: type the flag's name between the quotes. Step 3.")
    elif not spark.catalog.tableExists(flagged):
        out.append(f"{flagged} is not there yet. Run cell 3. Step 3.")
    elif flag not in spark.table(flagged).columns:
        out.append(f"{flagged} has no column {flag}. Run cell 3 again. Step 3.")
    else:
        facts = flag_facts(spark, flagged, flag)
        if facts["rows"] != spark.table(SOURCE).count():
            out.append(f"{flagged} has {facts['rows']} rows. Run cell 3 again. Step 3.")
        if facts["wrong"]:
            out.append(f"{facts['wrong']} returns have a flag that does not match an empty {AMOUNT}. Cell 2 names {AMOUNT}? Step 2.")
    record = f"{schema}.model_feature_record"
    if not spark.catalog.tableExists(record):
        out.append(f"{record} is not there yet. Run cell 4. Step 4.")
    else:
        out += record_left(spark.table(record).collect(), flag or "the flag")
    return out


def report(spark: object, values: dict) -> str:
    """Return what cell 5 prints: Done, or Not yet with each thing left."""
    out = left(spark, values)
    if not out:
        facts = flag_facts(spark, f"{values['schema'].strip()}.features_flagged", values["flag"].strip())
        return (f"Done: {values['flag'].strip()} flags the {facts['flagged']} returns whose {AMOUNT} is empty, "
                f"and your record defends {AMOUNT} and the flag beside the two given rows.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Return what cell 5 prints, from your two tables.

    Args:
        spark: the notebook's Spark session.
        values: schema, empty_means and flag, as cells 1 and 3 hold them.

    Returns:
        The Done or Not yet text.
    """
    return report(spark, values)
