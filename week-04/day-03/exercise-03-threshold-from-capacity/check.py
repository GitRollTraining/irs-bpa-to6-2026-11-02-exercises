"""The done check for exercise 3. In Databricks, cell 7 of the notebook runs it: it sorts the 250
returns of model_valid again by the scores cell 2 gave, reads the 25th score, and compares what you
typed with that. Without Databricks, from the course folder:

    python3 week-04/day-03/exercise-03-threshold-from-capacity/check.py --start
    python3 week-04/day-03/exercise-03-threshold-from-capacity/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import re
import sys
from pathlib import Path

CAPACITY = 25
NAMES = ("logistic-regression", "decision-tree")
DECISIONS = ("accept", "more capacity")
START = {"cost_sentence": "", "guess_30": None, "k": None, "threshold": None, "expected_threshold": 0.844,
         "missed_at_k": 20, "chosen": "", "why_chosen": "", "decision": "", "why": ""}
FORM = re.compile(r"a (false negative|false positive) costs? more than a (false negative|false positive),? because (.*)")


def plain(text) -> str:
    """A typed answer as the check reads it: lower case, with no spaces or full stop around it."""
    return str(text).strip().strip(".!").strip().lower()


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: cost_sentence, guess_30, k, threshold, expected_threshold (the 25th score of the
            logistic regression on model_valid, sorted again), missed_at_k (the returns labelled
            change off that list), chosen, decision and why.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    form = FORM.search(plain(f["cost_sentence"]))
    if not form or form.group(1) == form.group(2) or len(form.group(3).split()) < 5:
        out.append("Cell 3: write 'In this scenario a false negative costs more than a false positive, because ...' "
                   "or the other way round, with a reason of five words or more after because. Step 2.")
    guess = f.get("guess_30")
    if not isinstance(guess, (int, float)) or isinstance(guess, bool) or not 0 <= guess <= 40:
        out.append("Cell 4: type your guess for a list of 30, a whole number from 0 to 40, in place of None. Step 3.")
    if f["k"] != CAPACITY:
        out.append(f"Cell 4: k is the cases the examiners can take: {CAPACITY} of the 250 returns. Step 3.")
    if f["threshold"] is None:
        out.append("Cell 5: type the threshold, the score at place k of cell 4. Step 4.")
    elif not isinstance(f["threshold"], (int, float)):
        out.append("Cell 5: type the threshold as a number, with no quotes. Step 4.")
    elif round(float(f["threshold"]), 3) != round(float(f["expected_threshold"]), 3):
        out.append(f"Cell 5: the threshold is the score at place {CAPACITY} of cell 4, to three places. Step 4.")
    if plain(f["chosen"]) == "decision-tree":
        out.append("Cell 6: look again at the two things that decide the candidate: each one's precision and "
                   "recall at 0.5 in exercise 2, and whether its scores can choose a list of any size the capacity "
                   "asks for, such as 20 or 10 (cell 4 shows how many of the tree's returns share its highest "
                   "score). Step 5.")
    elif plain(f["chosen"]) not in NAMES:
        out.append("Cell 6: type logistic-regression or decision-tree as chosen. Step 5.")
    why_chosen = str(f.get("why_chosen", ""))
    if len(why_chosen.split()) < 8 or not re.search(r"\d", why_chosen):
        out.append("Cell 6: write why_chosen, why this candidate and not the other, in one sentence of eight words "
                   "or more, with counts. Step 5.")
    if plain(f["decision"]) not in DECISIONS:
        out.append("Cell 6: type more capacity or accept as decision. Step 5.")
    elif form and form.group(1) != form.group(2):
        want = "more capacity" if form.group(1) == "false negative" else "accept"
        if plain(f["decision"]) != want:
            out.append(f"Cell 6: your cost sentence says a {form.group(1)} costs more, so the decision is {want}: "
                       "if a missed return costs more, ask for more capacity; if an examiner's wasted hours cost "
                       "more, accept the list of 25. Step 5.")
    why = str(f["why"])
    if len(why.split()) < 8 or not re.search(r"\d", why):
        out.append("Cell 6: write why in one sentence of eight words or more, with the counts of cell 5. Step 5.")
    elif str(f["missed_at_k"]) not in re.findall(r"\d+", why):
        out.append(f"Cell 6: say in why how many returns labelled change the list of {CAPACITY} misses (cell 5): "
                   "that count is what the decision rests on. Step 5.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        return (f"Done: a list of {f['k']} at threshold {round(float(f['threshold']), 3)}, which misses "
                f"{f['missed_at_k']} of the 40 returns labelled change; your cost sentence decides "
                f"{plain(f['decision'])}; {plain(f['chosen'])}. Thursday starts from both.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out])


def facts_of(g: dict) -> dict:
    """The facts, from the notebook's values."""
    scores = g["scores"]
    top = scores.sort_values("logistic_score", ascending=False).head(CAPACITY)
    k = g.get("k")
    return {"cost_sentence": g.get("cost_sentence", ""), "guess_30": g.get("guess_30"),
            "k": k if isinstance(k, int) and not isinstance(k, bool) else None,
            "threshold": g.get("threshold"), "expected_threshold": float(top["logistic_score"].iloc[-1]),
            "missed_at_k": 40 - int((top["label"] == "change").sum()),
            "chosen": g.get("chosen", ""), "why_chosen": g.get("why_chosen", ""), "decision": g.get("decision", ""), "why": g.get("why", "")}


def in_notebook(g: dict) -> str:
    """Return what the check cell prints, from the notebook's values (cell 7 passes them)."""
    return report(facts_of(g))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
