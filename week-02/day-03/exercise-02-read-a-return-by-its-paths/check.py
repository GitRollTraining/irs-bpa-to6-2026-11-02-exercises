"""The done check for exercise 2. In the notebook it is the last cell; in a terminal in the course
folder: python3 week-02/day-03/exercise-02-read-a-return-by-its-paths/check.py

It reads lab/paths.csv and follows each path in lab/returns/sample-return.xml with ElementTree, to
see that it reaches the field its row names. It compares each label with the field, and parses
lab/broken.xml to see that it is not well-formed and that lab/parse-error.txt names the line the
parser names. No model is called and no agent starts.
"""
import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE / "lab"
RESET = f"python3 reset.py {HERE.name}"
NS = {"efile": "http://www.irs.gov/efile", "course": "urn:course:instructor"}
FORM = "efile:ReturnData/efile:IRS1040/"
# Each row's field, the element it must reach, its label, and why that label.
FIELDS = {
    "wages on Form 1040": (FORM + "efile:WagesAmt", "made-up test value",
                           "an amount identifies no person, and the course added nothing here"),
    "the dependent's SSN on Form 1040": (FORM + "efile:DependentDetail/efile:DependentSSN", "protected data",
                                         "an SSN identifies a person, even when the course made it up"),
    "the review label on Form 1040": (FORM + "course:ReviewLabel", "instructor-only label",
                                      "the course added it, in its own namespace; no real return holds it"),
}


def check() -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    if not (LAB / ".git").is_dir():
        return [f"lab/ is not there yet. In a terminal in the course folder, run {RESET}. See Start from."]
    left = []
    root = ET.parse(LAB / "returns" / "sample-return.xml").getroot()
    with open(LAB / "paths.csv", newline="", encoding="utf-8") as file:
        rows = {row["field"]: row for row in csv.DictReader(file)}
    for field, (want, label, why) in FIELDS.items():
        row = rows.get(field)
        if row is None:
            left.append(f'paths.csv has no row for "{field}". Put the row back as the start has it.')
            continue
        problem = path_left(root, field, (row.get("path") or "").strip(), want)
        if problem:
            left.append(problem)
        given = (row.get("label") or "").strip().lower()
        if given != label:
            left.append(f'The label of "{field}" is "{given or "empty"}". Sort it by the rule in step 3.'
                        if given not in {"made-up test value", "protected data", "instructor-only label"} else
                        f'The label of "{field}" is not "{given}": {why}. Step 3.')
    left += parse_error_left()
    return left


def path_left(root: ET.Element, field: str, path: str, want: str) -> str:
    """What is wrong with one row's path, or an empty string when it reaches its field."""
    if not path:
        return f'The row "{field}" has no path yet. Step 2.'
    if "//" in path:
        return (f'The path of "{field}" uses //, which searches the whole tree. Write it from the root '
                "element, one step per element. Step 2.")
    try:
        found = root.find(path, NS)
    except (SyntaxError, KeyError) as error:
        return f'The path of "{field}" is not one ElementTree reads ({error}). Step 2.'
    if found is None:
        return f'The path of "{field}" finds nothing in the sample return. Step 2.'
    if found is not root.find(want, NS):
        return f'The path of "{field}" reaches {found.tag}, which is not that field. Step 2.'
    return ""


def parse_error_left() -> list[str]:
    """What is left of step 4: a broken copy, and the parser's line in parse-error.txt."""
    broken, said = LAB / "broken.xml", LAB / "parse-error.txt"
    if not broken.is_file():
        return ["lab/broken.xml is not there yet. Step 4."]
    try:
        ET.parse(broken)
        return ["lab/broken.xml is still well-formed: the parser reads it. Delete one closing tag. Step 4."]
    except ET.ParseError as error:
        line = error.position[0]
    text = said.read_text(encoding="utf-8") if said.is_file() else ""
    if not re.search(rf"\bline {line}\b", text):
        return [f"lab/parse-error.txt does not hold the parser's message yet. Copy the line cell 3 prints. Step 4."]
    return []


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: each path reaches its field from the root element, each field has its label, and "
          "parse-error.txt holds the line the parser names in your broken copy.")
    for line in left:
        print("- " + line)
