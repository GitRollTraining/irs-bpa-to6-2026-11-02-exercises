"""The done check for exercise 3. In the notebook it is the last cell; in a terminal in the course
folder: python3 week-02/day-02/exercise-03-add-a-rule-test-first/check.py

It finds the tests that are new since the start. It runs them on the start's rules.py, where they must
fail (red), and runs every test on your rules.py with the relief file removed, where they must pass
(green, with the file read stubbed). It tries the rule on two accounts, and reads your commit through
Git. No model is called and no agent starts.
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
TRY_RULE = """
from payment_job.reader import Account
from payment_job.rules import penalty_for
relief = penalty_for(Account("ACC-1", "AREA-7", 4, 2000))
other = penalty_for(Account("ACC-2", "AREA-3", 4, 2000))
print("ok" if relief == 0 and other == 80 else f"relief area: {relief}, other area: {other}")
"""


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


def copy_of_lab(tmp: str, name: str) -> Path:
    """A copy of lab/ as it is now, without its Git history."""
    folder = Path(tmp) / name
    shutil.copytree(LAB, folder, ignore=shutil.ignore_patterns(".git", "__pycache__", ".coverage"))
    return folder


def check() -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    if not (LAB / ".git").is_dir():
        return [f"lab/ is not there yet. In a terminal in the course folder, run {RESET}. See Start from."]
    left = []
    if not (LAB / SKILL).is_file():
        left.append(f"The skill is not in lab/{SKILL} yet. Install it: step 2.")
    with tempfile.TemporaryDirectory() as tmp:
        start = Path(tmp) / "start"
        start.mkdir()
        archive = subprocess.run(["git", "-C", str(LAB), "archive", "start"], capture_output=True).stdout
        subprocess.run(["tar", "-x", "-C", str(start)], input=archive, check=True)
        new = sorted(tests(LAB) - tests(start))
        if not new:
            left.append("No test is new since the start. Have Codex add the relief rule's test first: step 3.")
        else:
            red = copy_of_lab(tmp, "red")
            shutil.copy(start / "payment_job" / "rules.py", red / "payment_job" / "rules.py")
            if run(red, "-m", "pytest", "-q", "-p", "no:cacheprovider", *new).returncode == 0:
                left.append(f"The new test passes on the start's rules.py, so it was never red ({new[0]}). "
                            "It must test the relief rule. Step 3.")
        green = copy_of_lab(tmp, "green")
        (green / "data" / "relief_areas.txt").unlink(missing_ok=True)
        result = run(green, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no")
        if result.returncode:
            last = (result.stdout.strip() or result.stderr.strip()).splitlines()[-1]
            with_file = run(LAB, "-m", "pytest", "-q", "-p", "no:cacheprovider").returncode == 0
            left.append("A test reads data/relief_areas.txt. Stub load_relief_areas with monkeypatch: step 3."
                        if with_file else f"The tests do not pass ({last}). Step 3.")
        said = run(copy_of_lab(tmp, "rule"), "-c", TRY_RULE).stdout.strip() or "it stopped with an error"
        if said != "ok":
            left.append(f"penalty_for does not apply the relief rule yet ({said}). AREA-7 is on the list. Step 3.")
    if git("status", "--porcelain", "--", "payment_job", "tests").strip():
        left.append("payment_job/ or tests/ has changes that are not in a commit. Commit them: step 4.")
    elif not git("diff", "--name-only", "start", "HEAD", "--", "payment_job", "tests").strip():
        left.append("No commit holds the change yet. Commit it: step 4.")
    return left


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: the new test was red on the old rule and is green on yours, with the relief file stubbed, "
          "and a commit holds the change.")
    for line in left:
        print("- " + line)
