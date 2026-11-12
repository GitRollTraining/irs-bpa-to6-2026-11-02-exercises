"""The done check for exercise 4, the extra exercise. In the notebook it is the last cell; in a
terminal in the course folder: python3 week-02/day-03/exercise-04-a-repeated-element/check.py

It finds the tests that are new since the start. It runs them on your form1040.py with
dependent_relationships put back as it started, where they must fail (red), and runs every test on
your form1040.py, where they must pass (green). It reads three returns with your function, and reads
your commit through Git. No model is called and no agent starts.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE / "lab"
RESET = f"python3 reset.py {HERE.name}"
NOT_WRITTEN = '''

def dependent_relationships(path):
    raise NotImplementedError("dependent_relationships is not written yet")
'''
PROBE = '''
import xml.etree.ElementTree as ET
from form1040 import dependent_relationships
EFILE = "{http://www.irs.gov/efile}"
tree = ET.parse("returns/sample-return.xml")
form = tree.getroot().find(EFILE + "ReturnData/" + EFILE + "IRS1040")
form.remove(form.find(EFILE + "DependentDetail"))
tree.write("no-dependents.xml", xml_declaration=True, encoding="UTF-8")
said = [dependent_relationships(p) for p in ("returns/two-dependents.xml", "returns/sample-return.xml", "no-dependents.xml")]
want = [["DAUGHTER", "SON"], ["DAUGHTER"], []]
names = ["two dependents", "one dependent", "no dependent"]
wrong = [f"for {n} it gives {s}, not {w}" for n, s, w in zip(names, said, want) if s != w]
print("; ".join(wrong) or "ok")
'''


def git(*args: str) -> str:
    """Run a Git command in lab/ and return what it printed."""
    return subprocess.run(["git", "-C", str(LAB), *args], capture_output=True, text=True).stdout


def run(folder: Path, *args: str) -> subprocess.CompletedProcess:
    """Run Python in a folder, as the learner does in lab/."""
    return subprocess.run([sys.executable, *args], cwd=folder, capture_output=True, text=True)


def tests(folder: Path) -> set[str]:
    """The test ids pytest collects in a folder."""
    out = run(folder, "-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider").stdout
    return {line.strip() for line in out.splitlines() if "::" in line}


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
    with tempfile.TemporaryDirectory() as tmp:
        start = Path(tmp) / "start"
        start.mkdir()
        archive = subprocess.run(["git", "-C", str(LAB), "archive", "start"], capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(start)], input=archive, check=True)
        new = sorted(tests(LAB) - tests(start))
        if not new:
            left.append("No test is new since the start. Write the test for two dependents first: step 2.")
        elif run(copy_of_lab(tmp, "red", NOT_WRITTEN), "-m", "pytest", "-q", "-p", "no:cacheprovider",
                 *new).returncode == 0:
            left.append(f"The new test passes when dependent_relationships is not written, so it was never "
                        f"red ({new[0]}). It must call dependent_relationships. Step 2.")
        green = run(copy_of_lab(tmp, "green"), "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no")
        if green.returncode:
            last = (green.stdout.strip() or green.stderr.strip()).splitlines()[-1]
            left.append(f"The tests do not pass on your form1040.py ({last}). Step 3.")
        said = run(copy_of_lab(tmp, "probe"), "-c", PROBE)
        said = said.stdout.strip() or (said.stderr.strip().splitlines() or ["it stopped with an error"])[-1]
        if said != "ok":
            left.append(f"dependent_relationships is not right yet: {said}. Step 3.")
    if git("status", "--porcelain", "--", "form1040.py", "tests").strip():
        left.append("form1040.py or tests/ has changes that are not in a commit. Commit them: step 4.")
    elif not git("diff", "--name-only", "start", "HEAD", "--", "form1040.py", "tests").strip():
        left.append("No commit holds the change yet. Commit it: step 4.")
    return left


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: the new test was red before dependent_relationships was written and every test is green "
          "now, a repeated element comes back as a list, and a commit holds the change.")
    for line in left:
        print("- " + line)
