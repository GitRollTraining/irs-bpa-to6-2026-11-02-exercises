"""The done check for exercise 2. In Databricks, cell 8 of the notebook runs it: it fits the two
candidates again on the rows the notebook holds, as cells 3 to 6 give them, and compares their
accuracies with yours. Without Databricks, from the course folder:

    python3 week-04/day-02/exercise-02-fit-two-candidates/check.py --start
    python3 week-04/day-02/exercise-02-fit-two-candidates/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import sys
from pathlib import Path

FEATURES = ["filing_status", "wages_amt", "taxable_interest_amt", "other_income_amt", "total_income", "agi_amt",
            "deduction_amt", "deduction_missing", "total_tax_amt", "withholding_amt", "tax_to_agi", "deduction_to_agi"]
GUESSES = ("a lot", "a little", "not better")
NAMES = ("logistic-regression", "decision-tree")
START = {"features": FEATURES, "guess": {name: "" for name in NAMES}, "results": {"baseline": 0.8}, "tree_depth": None,
         "expected": {"baseline": 0.8, "logistic-regression": 0.955, "decision-tree": 0.895}, "valid_rows": 200}


def plain(text) -> str:
    """A guess as the check reads it: lower case, with no spaces or full stop around it."""
    return str(text).strip().strip(".!").strip().lower()


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: features, guess, results (the accuracies cells 4 and 6 stored),
            tree_depth (the fitted tree's max_depth), expected (the same accuracies, fitted again
            by this check) and valid_rows.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    if list(f["features"]) != FEATURES:
        out.append("Cell 3 must list the twelve features known before selection, as the course gives them: " + ", ".join(FEATURES)
                   + ". Run cells 3 and 4 again. Step 1.")
    if any(plain(f["guess"].get(name, "")) not in GUESSES for name in NAMES):
        out.append('Cell 5: type "a lot", "a little" or "not better" for each candidate, before you fit it. Step 2.')
    for name, line in (("logistic-regression", "make_pipeline(StandardScaler(), LogisticRegression())"),
                       ("decision-tree", "DecisionTreeClassifier(max_depth=3, random_state=0)")):
        got, want = f["results"].get(name), f["expected"].get(name)
        if got is None:
            out.append(f"Cell 6 has not fitted {name} yet. Make its model line {line}, then run cells 6 and 7. Step 3.")
        elif name == "decision-tree" and f.get("tree_depth") != 3:
            out.append(f"The tree in cell 6 must be {line}: max_depth=3. Run cell 6 again. Step 3.")
        elif want is None or abs(got - want) > 0.0005:
            out.append(f"The accuracy of {name} does not match a fit of {line} on these rows. Run cells 3 to 7 "
                       "again, as the course gives them. Step 3.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        r = f["results"]
        return (f"Done: on the same {f['valid_rows']} validation rows, the baseline {r['baseline']:.3f}, "
                f"logistic-regression {r['logistic-regression']:.3f}, decision-tree "
                f"{r['decision-tree']:.3f}. Compare each with your guess.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out])


def expected(X_train, y_train, X_valid, y_valid) -> dict:
    """Fit the baseline and the two candidates as cells 4 and 6 give them; return each accuracy."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier
    out = {"baseline": accuracy_score(y_valid, ["no"] * len(y_valid))}
    for name, model in (("logistic-regression", make_pipeline(StandardScaler(), LogisticRegression())),
                        ("decision-tree", DecisionTreeClassifier(max_depth=3, random_state=0))):
        model.fit(X_train, y_train)
        out[name] = accuracy_score(y_valid, model.predict(X_valid))
    return out


def facts_of(g: dict) -> dict:
    """The facts, from the notebook's values."""
    tree = g.get("fitted", {}).get("decision-tree")
    return {"features": list(g["features"]), "guess": dict(g["guess"]),
            "results": {k: float(v) for k, v in g.get("results", {}).items()},
            "tree_depth": getattr(tree, "max_depth", None),
            "expected": {k: float(v) for k, v in expected(g["X_train"], g["y_train"], g["X_valid"], g["y_valid"]).items()},
            "valid_rows": len(g["y_valid"])}


def in_notebook(g: dict) -> str:
    """Return what the check cell prints, from the notebook's values (cell 8 passes them)."""
    return report(facts_of(g))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
