"""The done check for exercise 3. In the notebook it is the last cell; in a terminal in the course
folder: python3 week-02/day-03/exercise-03-a-return-reader-test-first/check.py

It finds your tests and runs them three times on copies of lab/: on your form1040.py, where they
must pass (green); on your file with read_form_1040 put back as it started, where they must fail
(red); and on your file with a read_form_1040 that crashes when an element is missing, where at
least one must fail. It also reads the sample return with your reader, and reads your commit
through Git. No model is called and no agent starts.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE / "lab"
RESET = f"python3 reset.py {HERE.name}"
SKILL = ".agents/skills/test-driven-development/SKILL.md"
NOT_WRITTEN = '''

def read_form_1040(path):
    raise NotImplementedError("read_form_1040 is not written yet")
'''
CRASHES_ON_MISSING = '''

def read_form_1040(path):
    import xml.etree.ElementTree as ET
    form = ET.parse(path).getroot().find("efile:ReturnData/efile:IRS1040", {"efile": "http://www.irs.gov/efile"})
    value = lambda tag: int(form.find("efile:" + tag, {"efile": "http://www.irs.gov/efile"}).text)
    return {"wages": value("WagesAmt"), "taxable_interest": value("TaxableInterestAmt"),
            "adjusted_gross_income": value("AdjustedGrossIncomeAmt")}
'''
PROBE = '''
import xml.etree.ElementTree as ET
from form1040 import read_form_1040
EFILE = "{http://www.irs.gov/efile}"
tree = ET.parse("returns/sample-return.xml")
form = tree.getroot().find(EFILE + "ReturnData/" + EFILE + "IRS1040")
form.remove(form.find(EFILE + "TaxableInterestAmt"))
tree.write("no-interest.xml", xml_declaration=True, encoding="UTF-8")
full = read_form_1040("returns/sample-return.xml")
part = read_form_1040("no-interest.xml")
want = {"wages": 52340, "taxable_interest": 120, "adjusted_gross_income": 52460}
if full != want:
    print(f"on the sample return it gives {full}, not {want}")
elif part != dict(want, taxable_interest=None):
    print(f"on a return with no TaxableInterestAmt it gives {part}, not taxable_interest None")
else:
    print("ok")
'''


def git(*args: str) -> str:
    """Run a Git command in lab/ and return what it printed."""
    return subprocess.run(["git", "-C", str(LAB), *args], capture_output=True, text=True).stdout


def run(folder: Path, *args: str) -> subprocess.CompletedProcess:
    """Run Python in a folder, as the learner does in lab/."""
    return subprocess.run([sys.executable, *args], cwd=folder, capture_output=True, text=True)


def pytest(folder: Path) -> subprocess.CompletedProcess:
    """Run every test in a folder."""
    return run(folder, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no")


def copy_of_lab(tmp: str, name: str, append: str = "") -> Path:
    """A copy of lab/ as it is now, without its Git history; append adds code to its form1040.py."""
    folder = Path(tmp) / name
    shutil.copytree(LAB, folder, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache"))
    reader = folder / "form1040.py"
    reader.write_text(reader.read_text(encoding="utf-8") + append, encoding="utf-8")
    return folder


def check() -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    if not (LAB / ".git").is_dir():
        return [f"lab/ is not there yet. In a terminal in the course folder, run {RESET}. See Start from."]
    left = []
    if not (LAB / SKILL).is_file():
        left.append(f"The skill is not in lab/{SKILL} yet. Install it: step 2.")
    collected = run(LAB, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider").stdout
    if "::" not in collected:
        left.append("lab/tests/ holds no test yet. Have Codex write the tests first: step 3.")
        return left + commit_left()
    with tempfile.TemporaryDirectory() as tmp:
        green = pytest(copy_of_lab(tmp, "green"))
        if green.returncode:
            last = (green.stdout.strip() or green.stderr.strip()).splitlines()[-1]
            left.append(f"The tests do not pass on your form1040.py ({last}). Step 3.")
        if pytest(copy_of_lab(tmp, "red", NOT_WRITTEN)).returncode == 0:
            left.append("The tests pass when read_form_1040 is not written, so they were never red. "
                        "They must call read_form_1040 and check what it returns. Step 3.")
        if pytest(copy_of_lab(tmp, "missing", CRASHES_ON_MISSING)).returncode == 0:
            left.append("No test reads a return where an element is missing: the tests pass on a reader "
                        "that crashes when TaxableInterestAmt is left out. Step 3.")
        said = run(copy_of_lab(tmp, "probe"), "-c", PROBE)
        said = said.stdout.strip() or (said.stderr.strip().splitlines() or ["it stopped with an error"])[-1]
        if said != "ok":
            left.append(f"read_form_1040 is not right yet: {said}. Step 3.")
    return left + commit_left()


def commit_left() -> list[str]:
    """What is left of the commit: step 4."""
    if git("status", "--porcelain", "--", "form1040.py", "tests").strip():
        return ["form1040.py or tests/ has changes that are not in a commit. Commit them: step 4."]
    if not git("diff", "--name-only", "start", "HEAD", "--", "form1040.py", "tests").strip():
        return ["No commit holds the reader and its tests yet. Commit them: step 4."]
    return []


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: the tests were red on the unwritten reader and are green on yours, one of them reads a "
          "return with a missing element, and a commit holds the reader and its tests.")
    for line in left:
        print("- " + line)
