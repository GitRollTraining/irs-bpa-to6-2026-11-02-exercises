"""The done check for exercise 1. In Databricks, cell 5 of the notebook runs it with the tests of
cell 2, and runs each test's rule again on both batches with spark. Without Databricks, from the
course folder:

    python3 week-03/day-02/exercise-01-tests-that-fail-the-dirty-batch/check.py <values.json>
    python3 week-03/day-02/exercise-01-tests-that-fail-the-dirty-batch/check.py --start

runs each rule on the setup's made-up rows (week-03/setup/day-02-course-data.py) in SQLite. It
checks what each test does on the two batches, never the wording of a name or a reason.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent if "__file__" in globals() else None
KINDS = ("completeness", "validity", "uniqueness", "consistency", "freshness")
ACTIONS = ("warn", "drop", "fail")
PREDICTIONS = ("fails", "passes")
EMPTY = {"name": "", "kind": "", "action": "", "rule": "", "predict": "", "passed_why": ""}
GIVEN = {"name": "each return_id once", "kind": "uniqueness", "action": "fail",
         "rule": "count(*) OVER (PARTITION BY return_id) = 1", "predict": "", "passed_why": ""}
START = {"tests": [dict(EMPTY), dict(EMPTY), dict(GIVEN), dict(EMPTY)]}


def test_left(n: int, test: dict, failing: dict) -> list[str]:
    """What is left in one test.

    Args:
        n: the test's number, 1 to 4.
        test: the test as cell 2 holds it.
        failing: rows that break the rule, per batch ("clean", "dirty"); None for a rule that does not run.

    Returns:
        One line per problem.
    """
    if not (test.get("rule") or "").strip():
        return [f"Test {n} has no rule yet. Step {2 if n < 4 else 5}."]
    out = []
    if len((test.get("name") or "").split()) < 2:
        out.append(f"Test {n}: give it a name of 2 words or more: what it expects. Step 2.")
    if (test.get("kind") or "").strip().lower() not in KINDS:
        out.append(f"Test {n}: its kind is one of the five kinds, word for word. Step 2.")
    if (test.get("action") or "").strip().lower() not in ACTIONS:
        out.append(f"Test {n}: its action is warn, drop or fail. Step 2.")
    if (test.get("predict") or "").strip().lower() not in PREDICTIONS:
        out.append(f"Test {n}: before you run cell 4, write fails or passes in predict. Step 2.")
    if failing is None:
        out.append(f"Test {n}: its rule does not run. Read the error under cell 3. Step 3.")
        return out
    if failing["clean"]:
        out.append(f"Test {n} fails the clean batch ({failing['clean']} rows). A rule that fails a good batch "
                   "is too strict, or the wrong way round. Step 3.")
    if failing["dirty"] == 0 and len((test.get("passed_why") or "").split()) < 5:
        out.append(f"Test {n} passed the dirty batch. In passed_why, write why, in 5 words or more. Step 4.")
    return out


def left(values: dict, failing: list) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        values: the tests, as cell 2 holds them.
        failing: per test, the rows that break its rule in each batch, or None.
    """
    tests = values.get("tests") or []
    if len(tests) < 4:
        return ["Cell 2 needs four tests. Step 5."]
    out = []
    for n, (test, fail) in enumerate(zip(tests[:4], failing[:4]), 1):
        out += test_left(n, test, fail)
    used = {(t.get("kind") or "").strip().lower() for t in tests[:3]}
    fourth = (tests[3].get("kind") or "").strip().lower()
    if fourth and fourth in used:
        out.append(f"Tests 1 to 3 already use test 4's kind, {fourth}. Choose a kind they do not use. Step 5.")
    return out


def report(values: dict, failing: list) -> str:
    """Return what cell 5 prints: Done, or Not yet with each thing left."""
    out = left(values, failing)
    if not out:
        said = ", ".join(f"{t['kind'].strip().lower()} {'fails' if f['dirty'] else 'passes'}"
                         for t, f in zip(values["tests"][:4], failing[:4]))
        return f"Done: 4 tests pass the clean batch; on the dirty batch: {said}."
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + line for line in out])


def in_notebook(spark: object, values: dict) -> str:
    """Run each rule on both batches with spark, then return what cell 5 prints."""
    from pyspark.sql import functions as F
    failing = []
    for test in values.get("tests") or []:
        rule = (test.get("rule") or "").strip()
        if not rule:
            failing.append(None)
            continue
        try:
            counts = {}
            for batch in ("clean", "dirty"):
                rows = spark.table(f"course.returns.batch_{batch}").withColumn("_ok", F.expr(rule))
                counts[batch] = rows.filter("NOT _ok").count()
            failing.append(counts)
        except Exception:  # a rule that does not run
            failing.append(None)
    return report(values, failing)


def course_db() -> object:
    """The setup's made-up rows, loaded into SQLite."""
    data = {"__name__": "course_data"}
    exec((HERE.parents[1] / "setup" / "day-02-course-data.py").read_text(encoding="utf-8"), data)
    return data["local_db"]()


def local_failing(values: dict) -> list:
    """Run each rule on the made-up rows, as cell 4 runs it in Databricks."""
    db = course_db()
    failing = []
    for test in values.get("tests") or []:
        rule = (test.get("rule") or "").strip()
        if not rule:
            failing.append(None)
            continue
        try:
            failing.append({b: db.execute(f"SELECT count(*) FROM (SELECT ({rule}) AS _ok FROM batch_{b}) "
                                          "WHERE NOT _ok").fetchone()[0] for b in ("clean", "dirty")})
        except Exception:  # a rule that does not run
            failing.append(None)
    return failing


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given, local_failing(given)))
