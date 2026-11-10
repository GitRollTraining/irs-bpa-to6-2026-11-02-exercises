"""The done check for exercise 1. In the notebook it is the last cell; in a terminal in the course
folder: python3 week-02/day-02/exercise-01-write-a-mapping-skill/check.py

It reads lab/ through Git: the skill, the two commits of CODEMAP.md, and the map's import arrows,
which it compares with the import graph pydeps finds. No model is called and no agent starts.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE / "lab"
SKILL = ".agents/skills/map-codebase/SKILL.md"
ARROW = re.compile(r"([\w./]+)\s*(?:->|→)\s*([\w./]+)")
RESET = f"python3 reset.py {HERE.name}"


def git(*args: str) -> str:
    """Run a Git command in lab/ and return what it printed."""
    return subprocess.run(["git", "-C", str(LAB), *args], capture_output=True, text=True).stdout


def file_name(name: str) -> str:
    """Turn payment_job.reader, payment_job/reader.py or reader into reader.py."""
    name = name.strip("`*.,;:()").split("/")[-1]
    name = name.removeprefix("payment_job.").removesuffix(".py")
    return name.split(".")[-1] + ".py"


def map_arrows(text: str) -> set[tuple[str, str]]:
    """Return the arrows under the map's Imports heading."""
    part = re.split(r"(?im)^#+\s*imports\b.*$", text, maxsplit=1)
    if len(part) < 2:
        return set()
    section = re.split(r"(?m)^#+\s", part[1], maxsplit=1)[0]
    return {(file_name(a), file_name(b)) for a, b in ARROW.findall(section)}


def graph_arrows(options: list[str]) -> set[tuple[str, str]]:
    """Return the arrows pydeps finds between the package's own modules."""
    run = subprocess.run([sys.executable, "-m", "pydeps", *options, "--show-deps", "--no-output"],
                         cwd=LAB, capture_output=True, text=True)
    if run.returncode:
        raise SystemExit("pydeps did not run: " + (run.stderr.strip().splitlines() or ["no message"])[-1])
    deps = json.loads(run.stdout)
    return {(file_name(name), file_name(other)) for name, info in deps.items()
            if name.startswith("payment_job.") for other in info.get("imports", [])
            if other.startswith("payment_job.")}


def show(arrows: set[tuple[str, str]]) -> str:
    """Write arrows as a list a person reads."""
    return ", ".join(f"{a} -> {b}" for a, b in sorted(arrows)) or "none"


def check() -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    if not (LAB / ".git").is_dir():
        return [f"lab/ is not there yet. In a terminal in the course folder, run {RESET}. See Start from."]
    left = []
    skill = (LAB / SKILL).read_text(encoding="utf-8") if (LAB / SKILL).is_file() else ""
    description = re.search(r"(?m)^description:\s*(.*)$", skill)
    if "name: map-codebase" not in skill or not description or description[1].strip() in ("", "TODO"):
        left.append(f"{SKILL} has no description yet. Write it: step 2.")
    if "TODO" in skill or "CODEMAP.md" not in skill.split("---")[-1]:
        left.append(f"The steps of {SKILL} are not written yet, or do not name CODEMAP.md as the output. Step 2.")
    commits = git("log", "--format=%H", "start..HEAD", "--", "CODEMAP.md").split()
    if not (LAB / "CODEMAP.md").is_file():
        left.append("lab/CODEMAP.md is not there yet. Start Codex with $map-codebase: step 3.")
    elif not commits:
        left.append("CODEMAP.md is not in a commit yet. Commit Codex's map as it is: step 4.")
    else:
        first = git("show", f"{commits[-1]}:CODEMAP.md")
        last = git("show", "HEAD:CODEMAP.md")
        if len(commits) < 2 or first == last:
            left.append("No commit holds a correction to Codex's map yet. Correct it and commit: step 6.")
        if git("status", "--porcelain", "--", "CODEMAP.md").strip():
            left.append("CODEMAP.md has changes after your last commit. Commit them: step 6.")
        graph = graph_arrows(["payment_job", "--max-bacon", "0"])
        arrows = map_arrows(last)
        if arrows != graph:
            left.append(f"The committed map's Imports do not match the graph. In the map only: {show(arrows - graph)}. "
                        f"In the graph only: {show(graph - arrows)}. Step 5.")
        risky = re.split(r"(?im)^#+\s*risky spots\b.*$", last, maxsplit=1)
        if len(risky) < 2 or "settings.py" not in re.split(r"(?m)^#+\s", risky[1], maxsplit=1)[0]:
            left.append("The map's Risky spots do not name settings.py, which reads a file when a module imports it. Step 5.")
    return left


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: your skill wrote CODEMAP.md, a commit holds your correction, and its imports match the graph.")
    for line in left:
        print("- " + line)
