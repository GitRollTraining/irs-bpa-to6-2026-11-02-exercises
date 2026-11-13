"""The done check for exercise 1. In Databricks, the notebook's last cell runs it: it reads your three
tables in your schema, counts the return files in the volume, and counts the dependents again with
week 2's reader. Without Databricks, from the course folder:

    python3 week-03/day-03/exercise-01-keyed-tables/check.py --start
    python3 week-03/day-03/exercise-01-keyed-tables/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import os
import sys
from pathlib import Path

VOLUME = "/Volumes/course/returns/raw/"
KEPT = ["return_id", "filer_key", "tax_year", "filing_status", "wages_amt", "total_income",
        "agi_amt", "total_tax_amt", "exam_changed_tax", "tax_added_by_exam", "file_name"]
START = {"schema": "course.learner_NN", "tables": {}, "files": 0, "predict_file_name": ""}


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: schema, tables (each table's rows and columns, or missing), files, the
            counts the tests compare, and predict_file_name.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    if f["schema"].endswith("_NN") or not f["schema"].startswith("course.learner_"):
        out.append("Cell 1 still names course.learner_NN. Type your own number. Step 1.")
    if f["predict_file_name"].strip().lower() not in ("yes", "no"):
        out.append('Cell 3 has no prediction yet. Type "yes" or "no" before you run it. Step 2.')
    elif f["predict_file_name"].strip().lower() != "no":
        out.append("Your prediction was yes. Read again why file_name was missing: the column is hidden until the read names it. Step 2.")
    t = f["tables"]
    for name in ("return_table", "dependents", "w2s"):
        if name not in t:
            out.append(f"{f['schema']}.{name} is not there yet. Run cell 5. Step 4.")
    if "return_table" in t:
        rt = t["return_table"]
        extra = sorted(set(rt["columns"]) - set(KEPT))
        missing = sorted(set(KEPT) - set(rt["columns"]))
        if missing:
            out.append(f"return_table has no column {', '.join(missing)}. Add _metadata.file_name to the read in cell 2. Step 2.")
        if extra:
            out.append(f"return_table keeps {', '.join(extra)}, which Tuesday's record leaves out. Use the select of cell 3 as given. Step 2.")
        if rt["rows"] != f["files"]:
            out.append(f"return_table has {rt['rows']} rows, and the folder holds {f['files']} files. One file is one return. Step 4.")
        if f.get("distinct_files") != f["files"]:
            out.append("Not every file shows in file_name. A file is missing or read twice. Step 4.")
        if f.get("duplicate_ids", 0):
            out.append(f"{f['duplicate_ids']} return_id values show twice in return_table. Step 4.")
    if "dependents" in t:
        if t["dependents"]["rows"] != f.get("reader_dependents"):
            out.append(f"dependents has {t['dependents']['rows']} rows, and week 2's reader counts {f.get('reader_dependents')}. Step 3.")
        if f.get("orphan_dependents", 0):
            out.append(f"{f['orphan_dependents']} dependent rows have a return_id that return_table does not hold. Step 3.")
    if "w2s" in t:
        if "wages_amt" not in t["w2s"]["columns"] or "return_id" not in t["w2s"]["columns"]:
            out.append("w2s needs the columns return_id and wages_amt. Step 3.")
        if t["w2s"]["rows"] != f.get("w2_elements"):
            out.append(f"w2s has {t['w2s']['rows']} rows, and the files hold {f.get('w2_elements')} IRSW2 elements. Explode IRSW2, the W-2 element. Step 3.")
    if not f.get("tests_ran"):
        out.append("The three count tests have not passed yet. Write tests 2 and 3, then run cell 6. Step 4.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        rt = f["tables"]["return_table"]["rows"]
        return (f"Done: {f['schema']} holds return_table ({rt} rows, one for each file), "
                f"dependents ({f['tables']['dependents']['rows']} rows) and w2s ({f['tables']['w2s']['rows']} rows).")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def _count_elements(path: str, tag: str) -> int:
    """Count the elements with this local name in one XML file."""
    import xml.etree.ElementTree as ET
    return sum(1 for e in ET.parse(path).iter() if e.tag.split("}")[-1] == tag)


def in_notebook(spark: object, schema: str, values: dict, course_folder: str) -> str:
    """Read the learner's tables with spark, then return what the check cell prints.

    Args:
        spark: the notebook's Spark session.
        schema: the learner's schema, such as course.learner_07.
        values: predict_file_name and tests_ran, as the cells hold them.
        course_folder: the course's Git folder, where week 2's reader is.
    """
    sys.path.append(os.path.join(course_folder, "week-02", "day-03", "answers", "exercise-04-a-repeated-element", "files"))
    from form1040 import dependent_relationships
    files = sorted(os.path.join(VOLUME, n) for n in os.listdir(VOLUME) if n.endswith(".xml"))
    facts = {"schema": schema, "files": len(files), "tables": {}, **values,
             "reader_dependents": sum(len(dependent_relationships(p)) for p in files),
             "w2_elements": sum(_count_elements(p, "IRSW2") for p in files)}
    for name in ("return_table", "dependents", "w2s"):
        if spark.catalog.tableExists(f"{schema}.{name}"):
            df = spark.table(f"{schema}.{name}")
            facts["tables"][name] = {"rows": df.count(), "columns": df.columns}
    if "return_table" in facts["tables"] and "file_name" in facts["tables"]["return_table"]["columns"]:
        rt = f"{schema}.return_table"
        facts["distinct_files"] = spark.sql(f"SELECT COUNT(DISTINCT file_name) AS n FROM {rt}").first()["n"]
        facts["duplicate_ids"] = spark.sql(f"SELECT COUNT(*) - COUNT(DISTINCT return_id) AS n FROM {rt}").first()["n"]
        if "dependents" in facts["tables"]:
            facts["orphan_dependents"] = spark.sql(
                f"SELECT COUNT(*) AS n FROM {schema}.dependents d LEFT ANTI JOIN {rt} r ON d.return_id = r.return_id").first()["n"]
    return report(facts)


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
