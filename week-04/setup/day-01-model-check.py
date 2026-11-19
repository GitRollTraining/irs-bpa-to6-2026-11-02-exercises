"""The measurement behind week 4's data: run it on any computer, no Databricks needed.

    uv run --no-project --python 3.12 --with scikit-learn==1.5.2 --with pandas==3.1.1 python week-04/setup/day-01-model-check.py

It reads day-01-course-data.py beside it, trains the week's three candidates on model_train's
examined returns (the features in FEATURES, an empty amount read as 0), scores model_valid's examined
returns, and prints: the three accuracies; the same under ten tree seeds, 1,000 resamples of
model_valid and 19 other generator seeds; case 123's scores and pushes; the selection rate in each
made-up channel; the planted feature in each channel; and the ten returns for Wednesday.
"""
import os
import statistics
import warnings

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("error", category=UserWarning)  # a fit that does not converge stops the run
warnings.filterwarnings("ignore", message="Unknown solver options: iprint")  # newer SciPy, older scikit-learn
course = {"__name__": "course_data"}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "day-01-course-data.py"), encoding="utf-8").read(), course)
FEATURES = course["FEATURES"]


def with_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Add deduction_missing, the flag Monday's exercise 3 adds: 1 when deduction_amt is empty."""
    return df.assign(deduction_missing=df["deduction_amt"].isna().astype(int))


def labelled(name: str, seed: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """One set's examined returns: the rows, the feature columns (empty read as 0), and the label as 1 or 0."""
    df = with_flag(pd.DataFrame([r for r in course["set_rows"](name, seed) if r["exam_changed_tax"] is not None]))
    return df, df[FEATURES].fillna(0), (df["exam_changed_tax"] == "yes").astype(int)


def candidates(seed: int, tree_seed: int = 0) -> dict:
    """Train the three candidates on model_train and return their accuracy on model_valid."""
    _, Xt, yt = labelled("model_train", seed)
    va, Xv, yv = labelled("model_valid", seed)
    lr = make_pipeline(StandardScaler(), LogisticRegression()).fit(Xt, yt)
    dt = DecisionTreeClassifier(random_state=tree_seed).fit(Xt, yt)
    return {"baseline": float((yv == yt.mode()[0]).mean()), "logistic": float((lr.predict(Xv) == yv).mean()),
            "tree": float((dt.predict(Xv) == yv).mean()), "lr": lr, "dt": dt, "va": va, "Xv": Xv, "yv": yv, "Xt": Xt}


def in_order(a: dict) -> bool:
    """True when the three accuracies stand baseline, then tree, then logistic regression."""
    return a["baseline"] < a["tree"] < a["logistic"]


SEED = course["SEED"]
c = candidates(SEED)
print(f"1. Course data (seed {SEED}), model_valid's 200 examined returns: baseline {c['baseline']:.3f}, "
      f"logistic regression {c['logistic']:.3f}, decision tree {c['tree']:.3f}")
trees = [candidates(SEED, s)["tree"] for s in range(10)]
print(f"2. Tree under random_state 0 to 9: {min(trees):.3f} to {max(trees):.3f}")
rng = np.random.default_rng(0)
lr_right = (c["lr"].predict(c["Xv"]) == c["yv"]).to_numpy()
dt_right = (c["dt"].predict(c["Xv"]) == c["yv"]).to_numpy()
base_right = (c["yv"] == 0).to_numpy()
kept = 0
for _ in range(1000):
    i = rng.integers(0, len(lr_right), len(lr_right))
    kept += base_right[i].mean() < dt_right[i].mean() < lr_right[i].mean()
print(f"3. Order baseline < tree < logistic kept in {kept} of 1000 resamples of model_valid")
others = [candidates(s) for s in range(1, 21) if s != SEED]
print(f"4. Order kept in {sum(map(in_order, others))} of {len(others)} other generator seeds; means: baseline "
      f"{statistics.mean(a['baseline'] for a in others):.3f}, logistic {statistics.mean(a['logistic'] for a in others):.3f}, "
      f"tree {statistics.mean(a['tree'] for a in others):.3f}")

va = c["va"].assign(logistic=c["lr"].predict_proba(c["Xv"])[:, 1], tree=c["dt"].predict_proba(c["Xv"])[:, 1])
case = va[va.case_id == 123].iloc[0]
rank = int((va.logistic > case.logistic).sum()) + 1
scaler, model = c["lr"][0], c["lr"][1]
pushes = pd.Series(model.coef_[0] * (c["Xv"][va.case_id == 123].iloc[0] - scaler.mean_) / scaler.scale_, index=FEATURES)
top = pushes.reindex(pushes.abs().sort_values(ascending=False).index)[:3]
print(f"5. Case 123 ({case.return_id}, label {case.exam_changed_tax}): logistic {case.logistic:.3f} (rank {rank} of 200), "
      f"tree {case.tree:.0f}; largest logistic pushes from the training mean, on the log-odds scale: "
      + ", ".join(f"{k} {v:+.2f}" for k, v in top.items()))
allv = with_flag(pd.DataFrame(course["set_rows"]("model_valid")))
allv["selected"] = c["lr"].predict(allv[FEATURES].fillna(0))
rates = allv.groupby("made_up_channel")["selected"].agg(["sum", "count"])
print("6. Logistic at 0.5, all 250 of model_valid: " + ", ".join(
    f"channel {g} {int(r['sum'])} of {int(r['count'])} selected ({r['sum'] / r['count']:.1%})" for g, r in rates.iterrows()))
feats = pd.DataFrame(course["feature_rows"]())
med = feats.groupby("made_up_channel")["other_income_amt"].median()
share = feats.assign(o=feats.other_income_amt > 5000).groupby("made_up_channel")["o"].mean()
print(f"7. other_income_amt median: channel A {med['A']:,.0f}, channel B {med['B']:,.0f}; above 5,000: "
      f"A {share['A']:.0%}, B {share['B']:.0%}")
va["cell"] = np.where(va.logistic >= 0.5, np.where(va.exam_changed_tax == "yes", "TP", "FP"),
                      np.where(va.exam_changed_tax == "yes", "FN", "TN"))
picked = va[va.case_id.isin(course["WEDNESDAY_TEN"])].sort_values("case_id")
print("8. Wednesday's ten, logistic at 0.5: " + ", ".join(f"{int(r.case_id)} {r.cell} {r.logistic:.2f}" for r in picked.itertuples())
      + f"; cells {picked.cell.value_counts().to_dict()}")
