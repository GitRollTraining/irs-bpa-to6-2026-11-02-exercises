"""The done check for exercise 3. In Databricks, the notebook's check cell runs it: it reads features
and feature_record in your schema, and computes each filer's earlier wages again by a join of the
table with itself, not by a window. Without Databricks, from the course folder:

    python3 week-03/day-03/exercise-03-history-and-change/check.py --start
    python3 week-03/day-03/exercise-03-history-and-change/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

NAMED = "F-30037-2023"
START = {"schema": "course.learner_NN", "predict_mean": None, "predict_change": None, "named": None,
         "features_columns": [], "mean_mismatches": None, "change_mismatches": None, "record": []}


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: schema, the two predictions, the named return's two values, the columns of
            features, the rows whose values differ from the values computed again, the record's rows.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    if f["schema"].endswith("_NN"):
        out.append("Cell 1 still names course.learner_NN. Type your own number. Step 1.")
    for c in ("mean_prior_wages", "wages_change_pct"):
        if c not in f["features_columns"]:
            out.append(f"features has no column {c} yet. Run cells 4, 5 and 7. Step 3.")
    if f["mean_mismatches"]:
        out.append(f"{f['mean_mismatches']} rows have a mean_prior_wages that is not the mean of the filer's earlier wages. Read cell 4's column and frame. Step 3.")
    if f["change_mismatches"]:
        out.append(f"{f['change_mismatches']} rows have a wages_change_pct that is not the change since the year before (null for a first return). Read cell 5's LAG line. Step 3.")
    named = f["named"] or {}
    pm, pc = f["predict_mean"], f["predict_change"]
    if pm is None or pc is None:
        out.append(f"Cell 3 has no prediction yet. Work out both values of {NAMED} from the rows of cell 2. Step 2.")
    else:
        if named.get("mean_prior_wages") is None or abs(pm - named["mean_prior_wages"]) >= 1:
            out.append(f"predict_mean is not the mean of the wages before 2023: add the three earlier years and divide by 3. Step 2.")
        if named.get("wages_change_pct") is None or abs(pc - named["wages_change_pct"]) >= 0.002:
            out.append("predict_change is not (2023 wages - 2022 wages) / 2022 wages, as a fraction. Step 2.")
    rec = {r[0]: r for r in f["record"]}
    for name in ("mean_prior_wages", "wages_change_pct"):
        row = rec.get(name)
        if row is None:
            out.append(f"feature_record has no row for {name}. Type it in cell 7 and run it. Step 5.")
        elif any(not str(x).strip() for x in row):
            out.append(f"The record row for {name} has an empty field. Step 5.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        n = f["named"]
        return (f"Done: {NAMED} has mean_prior_wages {n['mean_prior_wages']:.0f} and wages_change_pct "
                f"{n['wages_change_pct']:.3f}, as you predicted. Both columns are in feature_record.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, schema: str, values: dict, course_folder: str) -> str:
    """Read the learner's tables with spark, then return what the check cell prints.

    Args:
        spark: the notebook's Spark session.
        schema: the learner's schema, such as course.learner_07.
        values: predict_mean and predict_change, as cell 3 holds them.
        course_folder: the course's Git folder (not used here).
    """
    facts = dict(START, schema=schema, **values)
    ft = spark.table(f"{schema}.features")
    facts["features_columns"] = ft.columns
    if {"mean_prior_wages", "wages_change_pct"} <= set(ft.columns):
        t = f"{schema}.features"
        again = spark.sql(f"""
            SELECT a.return_id, a.mean_prior_wages, a.wages_change_pct,
                   AVG(b.wages_amt) AS mean_again,
                   MAX(CASE WHEN b.tax_year = a.tax_year - 1 AND b.wages_amt > 0
                            THEN (a.wages_amt - b.wages_amt) / b.wages_amt END) AS change_again
            FROM {t} a LEFT JOIN {t} b ON a.filer_key = b.filer_key AND b.tax_year < a.tax_year
            GROUP BY a.return_id, a.mean_prior_wages, a.wages_change_pct, a.wages_amt, a.tax_year""")
        again.createOrReplaceTempView("ex3_again")
        facts["mean_mismatches"] = spark.sql("""SELECT COUNT(*) AS n FROM ex3_again
            WHERE NOT (mean_prior_wages <=> mean_again)
              AND COALESCE(ABS(mean_prior_wages - mean_again) >= 0.01, TRUE)""").first()["n"]
        facts["change_mismatches"] = spark.sql("""SELECT COUNT(*) AS n FROM ex3_again
            WHERE NOT (wages_change_pct <=> change_again)
              AND COALESCE(ABS(wages_change_pct - change_again) >= 0.0001, TRUE)""").first()["n"]
    t = f"{schema}.features"
    row = spark.sql(f"""
        SELECT AVG(b.wages_amt) AS mean_again,
               MAX(CASE WHEN b.tax_year = a.tax_year - 1 AND b.wages_amt > 0
                        THEN (a.wages_amt - b.wages_amt) / b.wages_amt END) AS change_again
        FROM {t} a JOIN {t} b ON a.filer_key = b.filer_key AND b.tax_year < a.tax_year
        WHERE a.return_id = '{NAMED}'""").first()
    facts["named"] = {"mean_prior_wages": row["mean_again"], "wages_change_pct": row["change_again"]} if row else None
    if spark.catalog.tableExists(f"{schema}.feature_record"):
        facts["record"] = [list(r) for r in spark.table(f"{schema}.feature_record")
                           .select("feature", "table_read", "columns_read", "code").collect()]
    return report(facts)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
