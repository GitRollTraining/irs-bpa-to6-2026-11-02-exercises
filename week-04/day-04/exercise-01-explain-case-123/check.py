"""The done check for exercise 1. In Databricks, cell 7 of the notebook runs it: it reads the ranked
list and case #123's chart from the notebook's model, and compares them with what you typed. Without
Databricks, from the course folder:

    python3 week-04/day-04/exercise-01-explain-case-123/check.py --start
    python3 week-04/day-04/exercise-01-explain-case-123/check.py <facts.json>

reads the same facts from a JSON file (or the notebook's starting state). No model is called.
"""
import json
import re
import sys
from pathlib import Path

# The ranked list and case #123's chart on the logistic regression, as the day's reading gives them.
START = {"ranked": ["other_income_amt", "tax_to_agi", "wages_amt", "deduction_to_agi", "deduction_amt",
                    "total_tax_amt", "deduction_missing", "taxable_interest_amt", "filing_status", "agi_amt",
                    "total_income", "withholding_amt"],
         "chart": {"start": -4.55, "output": 3.28, "score": 0.964,
                   "pushes": {"other_income_amt": 3.8, "deduction_amt": 2.6, "tax_to_agi": 1.2}},
         "top_three": ["", "", ""], "case_id": None, "guess": None, "sentences": ""}
FINDING = re.compile(r"underreport|under-report|fraud|evad|evasion|cheat|\blied\b|\bhid\b|guilty|"
                     r"(tax|return) is wrong|wrong tax|identity theft", re.I)
AMOUNT = re.compile(r"\b(rais\w*|lower\w*|push\w*|mov\w*|increas\w*|add\w*|took|takes)\b[^.;]*?\bby\s+[+-]?\d", re.I)
UP = re.compile(r"\bup\b|\brais\w*|\bhigher\b|\bincreas\w*", re.I)


def plain(text) -> str:
    """A typed name as the check reads it: no spaces, quotes or backticks around it."""
    return str(text).strip().strip("`'\"").strip()


def sentence_count(text: str) -> int:
    """The number of sentences: each ends with a full stop, question or exclamation mark before a space or the end."""
    return len(re.findall(r"[.!?](?=\s|$)", text.strip()))


def left(f: dict) -> list[str]:
    """Return what is left: one line for each thing that is not yet right.

    Args:
        f: the facts: ranked (the model's features in order), chart (case #123's starting point, its
            largest pushes, its output and score), and what the learner typed in cells 3 to 6.

    Returns:
        One line per problem; an empty list when the exercise is done.
    """
    out = []
    typed = [plain(t) for t in (f["top_three"] or [])]
    ranked = list(f["ranked"])
    if len(typed) != 3 or typed[0] != ranked[0] or set(typed[1:]) != set(ranked[1:3]):
        out.append("Cell 3: type the three longest bars of the ranked list, the longest first, as the chart names "
                   "them. The ranked list is the whole model's chart, not case #123's. Step 2.")
    if str(f["case_id"]).strip().lstrip("#") != "123":
        out.append("Cell 4: type 123 as the case id, and run the cell. Step 3.")
    guess = f["guess"]
    if isinstance(guess, bool) or not isinstance(guess, (int, float)) or not 0 <= guess <= 1:
        out.append("Cell 5: type your guess as a number from 0 to 1, with no quotes. Any number counts. Step 4.")
    text = " ".join(str(f["sentences"]).split())
    if sentence_count(text) < 2:
        out.append("Cell 6: write two sentences, each ending with a full stop. Step 5.")
    elif len(text.split()) < 20:
        out.append(f"Cell 6: your two sentences have {len(text.split())} words. Give each push's value against the "
                   "training average, such as 28,500 against 7,584: about 20 words or more. Step 5.")
    if not re.search(r"0?\.96", text) or "average" not in text.lower():
        out.append("Cell 6: the first sentence gives case #123's score, 0.964, against what a return with average "
                   "values scores. Step 5.")
    other = re.search(r"other[ _]income", text, re.I)
    deduction = re.search(r"deduction(?![ _]to)", text, re.I)
    if not (other and deduction):
        out.append("Cell 6: the second sentence names the two largest pushes, in words an examiner reads: case "
                   "#123's other income and its deduction. Step 5.")
    elif other.start() > deduction.start():
        out.append("Cell 6: give the two largest pushes in their order, the largest first. Step 5.")
    if not UP.search(text):
        out.append("Cell 6: say the direction each pushed the score: up or down. Step 5.")
    pushes = [abs(v) for v in f["chart"]["pushes"].values()]
    found = [float(n) for n in re.findall(r"(?<![\d,])\d+\.\d+", text.replace(",", ""))]
    if AMOUNT.search(text) or any(abs(n - p) < 0.06 for n in found for p in pushes):
        out.append("Cell 6: the pushes are on the log-odds axis, so give their order and direction, not an amount "
                   "of score or of push. Step 5.")
    if FINDING.search(text):
        out.append("Cell 6: a push says where the model looked, not what the taxpayer did. Leave out any finding "
                   "about the taxpayer. Step 5.")
    return out


def report(f: dict) -> str:
    """Return what the check cell prints: Done, or Not yet with each thing left."""
    out = left(f)
    if not out:
        c = f["chart"]
        return (f"Done: your top three are {', '.join(f['ranked'][:3])}; case #123's pushes add up from "
                f"{c['start']:.2f} to {c['output']:.2f} on the log-odds axis, a score of {c['score']:.3f}; and your "
                "two sentences name its two largest pushes in order, with their direction and no amount.")
    return "\n".join([f"Not yet: {len(out)} left."] + ["- " + item for item in out])


def facts_of(g: dict) -> dict:
    """The facts, from the notebook's values: the model's ranked list and case #123's chart."""
    chart = g["case_chart"](123)
    largest = sorted(chart["pushes"], key=lambda name: -abs(chart["pushes"][name]))[:3]
    return {"ranked": list(g["ranked_features"]().index),
            "chart": {"start": chart["start"], "output": chart["output"], "score": chart["score"],
                      "pushes": {name: chart["pushes"][name] for name in largest}},
            **{name: g.get(name) for name in ("top_three", "case_id", "guess", "sentences")}}


def in_notebook(g: dict) -> str:
    """Return what the check cell prints, from the notebook's values (cell 7 passes them)."""
    if "logistic" not in g:
        return "Not yet: 1 left.\n- Run cells 1 and 2 first. Step 1."
    return report(facts_of(g))


if __name__ == "__main__":
    given = START if sys.argv[1:] == ["--start"] else json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(report(given))
