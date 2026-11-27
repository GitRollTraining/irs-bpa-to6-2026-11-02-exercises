"""Given code for exercise 1: cell 1 runs it. It reads the course's training and validation sets,
course.returns.model_train and course.returns.model_valid, and adds Monday's flag deduction_missing:
1 where deduction_amt is empty. It also gives cells 3, 4 and 5 their charts: the ranked list of
features, one return's pushes, and one return's score with one feature at its training average. The
pushes come from the SHAP library where it is on the compute, and from the same exact formula where
it is not. It changes no table. You do not need to read it."""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

NAMES = ("model_train", "model_valid")

COPY = ("The course's tables couldn't be read, so this notebook makes the same rows from the course's setup "
        "file, week-04/setup/day-01-course-data.py. Every number is the same.")
SETUP = f"{course_folder}/week-04/setup/day-01-course-data.py"


def course_rows(name: str) -> pd.DataFrame:
    """The rows of one of the course's tables, made by the course's setup file, as the table holds them."""
    made = {"__name__": "course_data"}
    exec(open(SETUP, encoding="utf-8").read(), made)
    rows = made["feature_rows"]() if name == "model_features" else made["set_rows"](name)
    return pd.DataFrame(rows)


def load_sets(*tables):
    """Return each table as a pandas table, from the course's tables or, when they cannot be read, from the
    course's setup file, with the flag deduction_missing: 1 where deduction_amt is empty."""
    names = NAMES[:len(tables)]
    try:
        out = [t.toPandas() for t in tables]
        own = all(len(t) > 0 for t in out)
    except Exception:
        own = False
    if own:
        print("Using the course's tables " + ", ".join(f"course.returns.{n}" for n in names) + ".")
    else:
        out = [course_rows(n) for n in names]
        print(COPY)
    ready = []
    for table in out:
        table = table.copy()
        table["deduction_missing"] = table["deduction_amt"].isna().astype(int)  # Monday's flag: 1 where empty
        table["exam_changed_tax"] = table["exam_changed_tax"].where(table["exam_changed_tax"].notna(), None)
        ready.append(table.reset_index(drop=True))
    print(", ".join(f"{len(t)} returns in {n}" for t, n in zip(ready, names)))
    return ready


AXIS = "log-odds: the model's output before the squeeze into a score"


def push_table(rows=None):
    """Return the starting point, each return's twelve pushes, and how they were computed.

    The pushes are SHAP values on the log-odds axis: shap.LinearExplainer on the fitted logistic
    regression, with the 400 training returns as the background. Where the SHAP library is not on
    the compute, the same numbers come from the exact formula for a logistic regression: each
    feature's weight times how far the return's value sits from the training average, on Tuesday's
    common scale. The starting point is the output of a return with every feature at its training
    average.
    """
    scaler, linear = logistic[0], logistic[-1]
    assert list(linear.classes_) == ["no", "yes"], "The model's second class should be yes."
    data = valid if rows is None else rows
    background = scaler.transform(X_train)
    scaled = scaler.transform(data[features].fillna(0))
    centre = background.mean(axis=0)
    exact = (scaled - centre) * linear.coef_[0]
    start = float(linear.intercept_[0] + centre @ linear.coef_[0])
    try:
        import shap
    except ImportError:
        return start, pd.DataFrame(exact, columns=features, index=data.index), "the exact formula (the SHAP library is not on this compute)"
    explainer = shap.LinearExplainer(linear, shap.maskers.Independent(background, max_samples=len(background)))
    result = explainer(scaled)
    values, base = np.asarray(result.values, dtype=float), float(np.ravel(result.base_values)[0])
    if abs(base - start) > 0.001 or np.abs(values - exact).max() > 0.001:
        print("Note for the trainer: the SHAP library's numbers differ from the exact formula's by more than 0.001.")
    return base, pd.DataFrame(values, columns=features, index=data.index), f"the SHAP library, version {shap.__version__}"


def ranked_features() -> pd.Series:
    """The ranked list: each feature's average size of push over the 250 returns of model_valid, largest first."""
    _, pushes, _ = push_table()
    return pushes.abs().mean().sort_values(ascending=False)


def draw_ranking() -> list:
    """Draw and print the ranked list, the longest bar first, and return the names in order."""
    ranked = ranked_features()
    plt.figure(figsize=(6, 3.4))
    plt.barh(ranked.index[::-1], ranked.values[::-1], color="#1f77b4")
    plt.title("Features the model leans on most")
    plt.xlabel("average size of push, log-odds, over the 250 returns of model_valid")
    plt.tight_layout()
    plt.show()
    plt.close()
    print("Features the model leans on most (average size of push, log-odds):")
    for name, value in ranked.items():
        print(f"{name:<22} {value:.1f}  {'#' * round(15 * value / ranked.iloc[0])}")
    return list(ranked.index)


def row_of(case_id) -> int:
    """The position in model_valid of the return with this case id."""
    found = valid.index[valid["case_id"] == int(str(case_id).strip().lstrip("#"))]
    assert len(found) == 1, f"No return {case_id} in model_valid. Type a case id such as 123."
    return int(found[0])


def case_chart(case_id) -> dict:
    """One return's chart as numbers: its starting point, its twelve pushes, its output and its score."""
    start, pushes, how = push_table()
    i = row_of(case_id)
    push = pushes.loc[i]
    score = float(logistic.predict_proba(valid.loc[[i], features].fillna(0))[0, 1])
    return {"case": int(valid.loc[i, "case_id"]), "start": start, "pushes": push.to_dict(),
            "output": start + float(push.sum()), "score": score, "how": how}


def shown(number) -> str:
    """A value as the table shows it: amounts in whole dollars, ratios and flags to four places."""
    if abs(number) >= 100 or float(number).is_integer():
        return f"{number:,.0f}"
    return f"{number:.4f}".rstrip("0").rstrip(".")


def one_place(push: float) -> str:
    """A push as the table shows it: to one place, with its sign, and 0.0 with none."""
    shown_push = round(push, 1) + 0.0
    return " 0.0" if shown_push == 0 else f"{shown_push:+.1f}"


def explain(case_id) -> dict:
    """Draw one return's chart and print it as a table, largest push first, with the sum."""
    chart = case_chart(case_id)
    i = row_of(case_id)
    order = sorted(features, key=lambda f: -abs(chart["pushes"][f]))
    value = valid.loc[i, features].fillna(0)
    average = X_train.mean()
    if chart["how"].startswith("the SHAP library"):
        import shap
        plt.figure(figsize=(7, 5))
        shap.plots.waterfall(shap.Explanation(values=np.array([chart["pushes"][f] for f in features]),
                                              base_values=chart["start"], data=value.values,
                                              feature_names=features), max_display=13, show=False)
    else:
        plt.figure(figsize=(6, 4))
        lefts = chart["start"] + np.cumsum([0] + [chart["pushes"][f] for f in order[:-1]])
        for n, f in enumerate(order):
            plt.barh(len(order) - n, chart["pushes"][f], left=lefts[n],
                     color="#ff0051" if chart["pushes"][f] > 0 else "#008bfb")
        plt.yticks(range(len(order), 0, -1), [f"{f} = {value[f]:g}" for f in order])
        plt.axvline(chart["start"], color="grey", linewidth=0.8)
        ends = np.concatenate([lefts, lefts + np.array([chart["pushes"][f] for f in order])])
        plt.xlim(ends.min() - 0.5, ends.max() + 0.5)
    plt.xlabel(AXIS)
    plt.title(f"Case #{chart['case']}: from a return with average values to its output")
    plt.tight_layout()
    plt.show()
    print(f"The pushes are computed by {chart['how']}.\n")
    print(f"{'case #' + str(chart['case']):<30} {'its value':>10} {'training average':>17} {'push':>7}")
    print(f"{'a return with average values':<30} {'':>10} {'':>17} {chart['start']:7.2f}")
    for f in order:
        print(f"{f:<30} {shown(value[f]):>10} {shown(average[f]):>17} {one_place(chart['pushes'][f]):>7}")
    print(f"{'case #' + str(chart['case']):<30} {'':>10} {'':>17} {chart['output']:7.2f} (a score of {chart['score']:.3f})")
    shown_sum = round(chart["start"], 2) + sum(round(p, 1) for p in chart["pushes"].values())
    print(f"\nThe sum: the exact pushes take {chart['start']:.2f} to {chart['output']:.2f}, a score of "
          f"{chart['score']:.3f}. The pushes shown, rounded to one place, add up to {shown_sum:.2f}.")
    print(f"The axis: {AXIS}.")
    return chart


def what_if(case_id, feature: str, guess) -> str:
    """The return's score with one feature set to its training average and everything else as filed,
    beside the learner's guess."""
    i = row_of(case_id)
    row = valid.loc[[i], features].fillna(0).copy()
    before = float(logistic.predict_proba(row)[0, 1])
    row[feature] = X_train[feature].mean()
    after = float(logistic.predict_proba(row)[0, 1])
    push = case_chart(case_id)["pushes"][feature]
    return (f"Your guess: {guess}. Case #{case_id} with {feature} at the training average, "
            f"{X_train[feature].mean():,.0f}, everything else as filed: a score of {after:.3f}, against {before:.3f}.\n"
            f"The push on the axis was {one_place(push).strip()} log-odds; the score moved {before - after:.3f}. "
            "A push is not an amount of score.\n"
            "This is not the reading's 0.904: that is the model fitted again without the feature. Here the same "
            "model scores the same return with one value changed.")
