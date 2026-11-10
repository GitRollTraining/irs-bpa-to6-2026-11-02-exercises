"""The done check for exercise 2. In the notebook it is the last cell; in a terminal in the course
folder: python3 week-02/day-02/exercise-02-test-plan-to-branch-coverage/check.py

It reads your test plan and checks each expected value against the rule. It runs your tests, measures
their branch coverage of rules.py, and runs them once more on a copy whose cap is 9 months, where they
must fail. No model is called and no agent starts.
"""
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE / "lab"
RESET = f"python3 reset.py {HERE.name}"
NEEDED = {  # each partition or boundary the plan must hold, and the row that covers it
    "negative months, an error": lambda m, t: m < 0,
    "on time, 0 months": lambda m, t: m == 0 and t > 0,
    "the first month late, 1": lambda m, t: m == 1 and t > 0,
    "the last month before the cap, 10": lambda m, t: m == 10 and t > 0,
    "the first capped month, 11": lambda m, t: m == 11 and t > 0,
    "nothing owed, unpaid_tax 0": lambda m, t: t == 0 and m > 0,
}


def rule(months_late: int, unpaid_tax: float) -> float | str:
    """The rule, as TEST_PLAN.md states it: what each row should expect."""
    if months_late < 0:
        return "error"
    return round(unpaid_tax * 0.01 * min(months_late, 10), 2) if unpaid_tax > 0 else 0


def plan_rows() -> list[tuple[int, float, str, str]]:
    """The rows of TEST_PLAN.md's table: months_late, unpaid_tax, Expected, and the row's name."""
    rows = []
    for line in (LAB / "TEST_PLAN.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) == 4:
            try:
                rows.append((int(cells[1]), float(cells[2].replace(",", "")), cells[3].lower(), cells[0]))
            except ValueError:
                pass
    return rows


def test_tuples() -> set[tuple[float, ...]]:
    """Every group of three numbers in the test files: a tuple, or a pytest.param(...) call."""
    found = set()
    for path in (LAB / "tests").glob("test_*.py"):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Call) and getattr(node.func, "attr", "") == "param":
                node = ast.Tuple(elts=node.args)
            if isinstance(node, ast.Tuple) and len(node.elts) == 3:
                try:
                    found.add(tuple(float(ast.literal_eval(e)) for e in node.elts))
                except (ValueError, TypeError):
                    pass
    return found


def coverage_with_branches() -> bool:
    """Whether the learner's last coverage run, lab/.coverage, measured branches."""
    from coverage import CoverageData

    data = CoverageData(basename=str(LAB / ".coverage"))
    data.read()
    return data.has_arcs()


def pytest(folder: Path, *extra: str) -> subprocess.CompletedProcess:
    """Run the tests in a folder, as the learner does."""
    return subprocess.run([sys.executable, *extra, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no"],
                          cwd=folder, capture_output=True, text=True)


def check() -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    if not (LAB / ".git").is_dir():
        return [f"lab/ is not there yet. In a terminal in the course folder, run {RESET}. See Start from."]
    left = []
    rows = plan_rows()
    for name, covers in NEEDED.items():
        if not any(covers(m, t) for m, t, *_ in rows):
            left.append(f"TEST_PLAN.md has no row for {name}. Step 2.")
    for m, t, expected, _ in rows:
        want = rule(m, t)
        if want == "error" and "error" not in expected or want != "error" and expected.replace(",", "") not in (
                f"{want:g}", f"{want:.2f}", str(want)):
            left.append(f"TEST_PLAN.md row {m}, {t:g}: Expected should be {want if want == 'error' else f'{want:g}'}. "
                        "Work it out from the rule. Step 2.")
    tuples = test_tuples()
    missing = [f"({m}, {t:g}, {e})" for m, t, e, name in rows if e != "error" and "penalty_for" not in name
               and not any(x[:2] == (m, t) and abs(x[2] - float(rule(m, t))) < 0.005 for x in tuples)]
    if missing:
        left.append(f"Rows of the plan in no parametrize list yet: {', '.join(missing)}. Step 3.")
    if any(e == "error" for _, _, e, _ in rows) and not any(
            "pytest.raises" in p.read_text(encoding="utf-8") for p in (LAB / "tests").glob("test_*.py")):
        left.append("No test expects the error for negative months (pytest.raises). Step 3.")
    run = pytest(LAB)
    if run.returncode:
        last = (run.stdout.strip() or run.stderr.strip()).splitlines()[-1]
        left.append(f"The tests do not pass ({last}). Each expected value comes from the plan. Step 3.")
    with tempfile.TemporaryDirectory() as tmp:
        data, report = Path(tmp) / "data", Path(tmp) / "coverage.json"
        subprocess.run([sys.executable, "-m", "coverage", "run", "--branch", f"--data-file={data}", "-m", "pytest",
                        "-q", "-p", "no:cacheprovider"], cwd=LAB, capture_output=True)
        subprocess.run([sys.executable, "-m", "coverage", "json", f"--data-file={data}", "-o", str(report)],
                       cwd=LAB, capture_output=True)
        measured = next(iter(json.loads(report.read_text())["files"].values()), {}) if report.is_file() else {}
        totals = measured.get("summary", {})
        if totals.get("missing_branches", 1) or totals.get("missing_lines", 1):
            lines = ", ".join(str(n) for n in measured.get("missing_lines", [])) or "none"
            left.append(f"Branch coverage of rules.py is not full: {totals.get('missing_branches', '?')} branches "
                        f"not run. Lines not run: {lines}. Step 4.")
        copy = Path(tmp) / "lab"
        shutil.copytree(LAB, copy, ignore=shutil.ignore_patterns(".git", ".coverage", "__pycache__"))
        rules = copy / "payment_job" / "rules.py"
        rules.write_text(re.sub(r"CAP_MONTHS = 10", "CAP_MONTHS = 9", rules.read_text(encoding="utf-8")))
        if run.returncode == 0 and pytest(copy).returncode == 0:
            left.append("Your tests still pass when the cap is 9 months. Add the rows at 10 and 11. Step 2.")
    if not (LAB / ".coverage").is_file():
        left.append("You have not measured coverage yet. Run cell 2 with coverage's --branch flag. Step 4.")
    elif not coverage_with_branches():
        left.append("Your coverage run did not measure branches. Run cell 2 with --branch. Step 4.")
    return left


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: every plan row is a test, the tests pass, every branch of rules.py ran, and the tests catch a cap "
          "one month early.")
    for line in left:
        print("- " + line)
