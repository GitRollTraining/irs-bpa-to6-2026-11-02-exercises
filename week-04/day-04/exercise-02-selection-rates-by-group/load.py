"""Given code for exercise 2: cell 1 runs it. It reads the course's training and validation sets,
course.returns.model_train and course.returns.model_valid, and all 1,000 returns of
course.returns.model_features, and adds Monday's flag deduction_missing: 1 where deduction_amt is
empty. It also gives cell 4 the rates at two other thresholds and the past labels by channel, and the
optional last step its medians. It changes no table. You do not need to read it."""
import pandas as pd

NAMES = ("model_train", "model_valid", "model_features")

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


def by_channel(on: pd.Series) -> dict:
    """Each channel's returns in model_valid and its returns on the list, from a 1-or-0 column."""
    table = scores.assign(_on=on.astype(int)).groupby("made_up_channel")["_on"].agg(["size", "sum"])
    return {name: (int(row["sum"]), int(row["size"])) for name, row in table.iterrows()}


def said(counts: dict) -> str:
    """Two channels' rates with their counts, and the gap."""
    (a_on, a_all), (b_on, b_all) = counts["A"], counts["B"]
    return (f"channel A {a_on} of {a_all} ({a_on / a_all:.3f}), channel B {b_on} of {b_all} ({b_on / b_all:.3f}); "
            f"the gap {abs(a_on / a_all - b_on / b_all):.3f}")


def compare() -> None:
    """Print the rates on a list of 50 and at 0.5, beside the list of 25, then the past labels by channel."""
    ranked = scores["logistic_score"].sort_values(ascending=False)
    at_50 = ranked.iloc[49]
    print("\nFor comparison, the same 250 returns at two other thresholds:")
    at_50_counts = by_channel(scores["logistic_score"] >= at_50)
    print(f"- a list of 50 (threshold {at_50:.3f}): " + said(at_50_counts) + ".")
    print(f"  Your guess for channel B's rate on the list of 50: {guess_50}. Its rate: "
          f"{at_50_counts['B'][0] / at_50_counts['B'][1]:.3f}.")
    print(f"- at 0.5 ({int((scores['logistic_score'] >= 0.5).sum())} on the list): " +
          said(by_channel(scores["logistic_score"] >= 0.5)) + ".")
    examined = all_returns[all_returns["exam_changed_tax"].notna()]
    labels = examined.groupby("made_up_channel")["exam_changed_tax"].agg(
        change=lambda s: int((s == "yes").sum()), examined="size")
    print("The past labels, the examined returns of all four tax years: " + "; ".join(
        f"channel {name} {int(row['change'])} of {int(row['examined'])} labelled change "
        f"({row['change'] / row['examined']:.3f})" for name, row in labels.iterrows()) + ".")
    print("In the course's made-up past, an examination's outcome follows the amounts on the return, never the "
          "channel: a gap in the labels says the past decisions differ, not that either channel's filers comply less.")


def medians(*names: str) -> str:
    """Each feature's typical value, its median, in each channel, over all 1,000 returns."""
    table = all_returns.groupby("made_up_channel")[list(names)].median()
    sizes = all_returns.groupby("made_up_channel").size()
    lines = [f"{'median over all 1,000 returns':<32}" + "".join(f"{'channel ' + c + ' (' + str(sizes[c]) + ')':>18}"
                                                             for c in table.index)]
    for name in names:
        lines.append(f"{name:<32}" + "".join(f"{table.loc[c, name]:>18,.0f}" for c in table.index))
    return "\n".join(lines)
