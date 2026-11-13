"""The done check for exercise 2. In Databricks, the notebook's last cell runs it: it reads features,
feature_record, return_table and w2s in your schema, and computes both ratios again from them.
Without Databricks, from the course folder:

    python3 week-03/day-03/exercise-02-features-and-a-ratio/check.py --start
    python3 week-03/day-03/exercise-02-features-and-a-ratio/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

START = {"schema": "course.learner_NN", "predict_rows": "", "return_rows": None, "features_rows": None,
         "features_columns": [], "share_mismatches": None, "tax_to_agi_mismatches": None, "record": []}


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: schema, predict_rows, the row counts, the columns of features, the rows
            whose ratios differ from the ratios computed again, and the record's rows.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    if f["schema"].endswith("_NN"):
        out.append("Cell 1 still names course.learner_NN. Type your own number. Step 1.")
    p = f["predict_rows"].strip().lower()
    if p not in ("more", "same", "fewer"):
        out.append('Cell 3 has no prediction yet. Type "more", "same" or "fewer". Step 3.')
    elif p != "more":
        out.append("Read your prediction again: a return with two W-2s gives two rows after the join. Step 3.")
    if f["features_rows"] is None:
        out.append(f"{f['schema']}.features is not there yet. Run cell 5. Step 4.")
    else:
        if f["features_rows"] != f["return_rows"]:
            out.append(f"features has {f['features_rows']} rows, and return_table has {f['return_rows']}. Sum the W-2s for each return before the join. Step 3.")
        for c in ("tax_to_agi", "w2_wage_share"):
            if c not in f["features_columns"]:
                out.append(f"features has no column {c}. Run cells 2 to 5 in order. Step 3.")
        if f["share_mismatches"]:
            out.append(f"{f['share_mismatches']} returns have a w2_wage_share that is not their W-2 wages over their wages (null where the wages are 0). Step 3.")
        if f["tax_to_agi_mismatches"]:
            out.append(f"{f['tax_to_agi_mismatches']} returns have a wrong tax_to_agi. Run cell 2 as given. Step 2.")
    rec = {r[0]: r for r in f["record"]}
    for name in ("tax_to_agi", "w2_wage_share"):
        row = rec.get(name)
        if row is None:
            out.append(f"feature_record has no row for {name}. Type it in cell 5. Step 4.")
        elif any(not str(x).strip() for x in row):
            out.append(f"The record row for {name} has an empty field. Step 4.")
        elif name == "w2_wage_share" and "w2s" not in row[1]:
            out.append("The record row for w2_wage_share must name the table w2s, which it reads. Step 4.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        return f"Done: features has {f['features_rows']} rows, one for each return, with tax_to_agi and w2_wage_share, and both are in feature_record."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, schema: str, values: dict, course_folder: str) -> str:
    """Read the learner's tables with spark, then return what the check cell prints.

    Args:
        spark: the notebook's Spark session.
        schema: the learner's schema, such as course.learner_07.
        values: predict_rows, as cell 3 holds it.
        course_folder: the course's Git folder (not used here).
    """
    facts = dict(START, schema=schema, **values)
    facts["return_rows"] = spark.table(f"{schema}.return_table").count()
    if spark.catalog.tableExists(f"{schema}.features"):
        ft = spark.table(f"{schema}.features")
        facts["features_rows"], facts["features_columns"] = ft.count(), ft.columns
        if {"tax_to_agi", "w2_wage_share"} <= set(ft.columns):
            facts["share_mismatches"] = spark.sql(f"""
                WITH s AS (SELECT return_id, SUM(wages_amt) AS w2 FROM {schema}.w2s GROUP BY return_id)
                SELECT COUNT(*) AS n FROM {schema}.features f LEFT JOIN s ON f.return_id = s.return_id
                WHERE NOT (f.w2_wage_share <=> CASE WHEN f.wages_amt > 0 THEN COALESCE(s.w2, 0) / f.wages_amt END)
                  AND COALESCE(ABS(f.w2_wage_share - CASE WHEN f.wages_amt > 0 THEN COALESCE(s.w2, 0) / f.wages_amt END) >= 0.0001, TRUE)
            """).first()["n"]
            facts["tax_to_agi_mismatches"] = spark.sql(f"""
                SELECT COUNT(*) AS n FROM {schema}.features
                WHERE NOT (tax_to_agi <=> CASE WHEN agi_amt > 0 THEN total_tax_amt / agi_amt END)
                  AND COALESCE(ABS(tax_to_agi - CASE WHEN agi_amt > 0 THEN total_tax_amt / agi_amt END) >= 0.0001, TRUE)
            """).first()["n"]
    if spark.catalog.tableExists(f"{schema}.feature_record"):
        facts["record"] = [list(r) for r in spark.table(f"{schema}.feature_record")
                           .select("feature", "table_read", "columns_read", "code").collect()]
    return report(facts)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
