"""The done check for exercise 4. In Databricks, the notebook's check cell runs it: it reads
feature_record, train, valid and test in your schema. Without Databricks, from the course folder:

    python3 week-03/day-03/exercise-04-selection-day-and-split/check.py --start
    python3 week-03/day-03/exercise-04-selection-day-and-split/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

AFTER_SELECTION = {"tax_added_by_exam"}  # written after the return is selected: the one "no"
LABEL = "exam_changed_tax"
START = {"schema": "course.learner_NN", "tests_ran": False, "record": {}, "sets": {}, "shared_ids": None, "years": [],
         "features_columns": ["return_id", "filer_key", "tax_year", "filing_status", "wages_amt", "total_income",
                              "agi_amt", "total_tax_amt", "exam_changed_tax", "tax_added_by_exam", "file_name",
                              "tax_to_agi", "w2_wage_share", "mean_prior_wages", "wages_change_pct"]}


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: schema, tests_ran, the record's mark and reason for each feature, each set's
            rows, columns and tax-change cases, the returns two sets share, each set's years, and
            the columns of features.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    if f["schema"].endswith("_NN"):
        out.append("Cell 1 still names course.learner_NN. Type your own number. Step 1.")
    rec = f["record"]
    if not rec or not any(m for m, _ in rec.values()):
        out.append("feature_record has no marks yet. Type yes or no and why for each feature in cell 3, then run cell 4. Step 2.")
    else:
        for feature, (mark, why) in rec.items():
            want = "no" if feature in AFTER_SELECTION else "yes"
            if mark not in ("yes", "no"):
                out.append(f"{feature} has no mark. Type yes or no in cell 3. Step 2.")
            elif mark != want and want == "no":
                out.append(f"Your mark for {feature} is yes. Ask: does the examination write its value after selection? Step 2.")
            elif mark != want:
                out.append(f"Your mark for {feature} is no. Ask: is its value on file on the selection day? Step 2.")
            if len((why or "").split()) < 3:
                out.append(f"The reason for {feature} has fewer than 3 words. Say why in cell 3. Step 2.")
    sets = f["sets"]
    for name in ("train", "valid", "test"):
        if name not in sets:
            out.append(f"{f['schema']}.{name} is not there yet. Run cell 4. Step 3.")
            continue
        cols = sets[name]["columns"]
        leaked = sorted(set(cols) & {k for k, (m, _) in rec.items() if m == "no"} | (set(cols) & AFTER_SELECTION))
        if leaked:
            out.append(f"{name} still holds {', '.join(leaked)}, which the selection day cannot know. Mark it no and run cell 4. Step 3.")
        if LABEL not in cols:
            out.append(f"{name} does not hold the label {LABEL}. The label stays in each set. Step 3.")
    in_features = sorted(set(f.get("features_columns", [])) & ({k for k, (m, _) in rec.items() if m == "no"} | AFTER_SELECTION))
    if in_features:
        out.append(f"features still holds {', '.join(in_features)}. Cell 4 writes features again without it. Step 3.")
    if f["shared_ids"]:
        out.append(f"{f['shared_ids']} returns are in two sets. Run cell 4 as given. Step 3.")
    y = f["years"]
    if len(y) == 3 and all(y) and not (max(y[0]) < min(y[1]) and max(y[1]) < min(y[2])):
        out.append(f"The years of the sets overlap: {y}. Run cell 4 as given. Step 3.")
    if not f["tests_ran"]:
        out.append("The five leakage tests have not passed yet. Run cell 5. Step 4.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        s = f["sets"]
        cases = ", ".join(f"{n} {s[n]['rows']} returns with {s[n]['cases']} tax-change cases" for n in ("train", "valid", "test"))
        return f"Done: every feature has its mark, tax_added_by_exam is out, and the five tests pass. {cases}."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, schema: str, values: dict, course_folder: str) -> str:
    """Read the learner's tables with spark, then return what the check cell prints.

    Args:
        spark: the notebook's Spark session.
        schema: the learner's schema, such as course.learner_07.
        values: tests_ran, as cell 5 leaves it.
        course_folder: the course's Git folder (not used here).
    """
    facts = dict(START, schema=schema, record={}, sets={}, **values)
    rt = spark.table(f"{schema}.feature_record")
    if "known_on_selection_day" in rt.columns:
        facts["record"] = {r["feature"]: [r["known_on_selection_day"], r["why"]] for r in rt.collect()}
    facts["features_columns"] = spark.table(f"{schema}.features").columns
    ids, years = [], []
    for name in ("train", "valid", "test"):
        if spark.catalog.tableExists(f"{schema}.{name}"):
            df = spark.table(f"{schema}.{name}")
            cases = df.filter(f"{LABEL} = 'yes'").count() if LABEL in df.columns else None
            facts["sets"][name] = {"rows": df.count(), "columns": df.columns, "cases": cases}
            ids += [r[0] for r in df.select("return_id").collect()]
            years.append(sorted(r[0] for r in df.select("tax_year").distinct().collect()))
    facts["shared_ids"] = len(ids) - len(set(ids))
    facts["years"] = years
    return report(facts)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
