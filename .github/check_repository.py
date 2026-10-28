#!/usr/bin/env python3
"""The exercise repository's one check: python3 .github/check_repository.py

Fails, naming each problem, when:
  - a week-NN/day-NN/ folder, or an exercise folder inside one, has no README.md;
  - an exercise folder has no answer beside it, week-NN/day-NN/answers/<exercise>/;
  - a relative link in a Markdown file points at nothing in this repository.
Standard library only. Exit 0 prints "OK" and what was checked.
"""
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
NOT_EXERCISES = {"answers", "figures"}           # a day's folders that hold no exercise


def tracked() -> list[pathlib.Path]:
    """Every file git would commit here (tracked, or new and not ignored); every file on disk when
    this folder is not the top of its own Git checkout."""
    def git(*args: str) -> str:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout
    try:
        if pathlib.Path(git("rev-parse", "--show-toplevel").strip()).resolve() == ROOT:
            out = git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
            return [ROOT / p for p in out.split("\0") if p and (ROOT / p).is_file()]
    except (OSError, subprocess.CalledProcessError):
        pass
    return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.relative_to(ROOT).parts]


files = tracked()
problems = []
days = sorted(p for p in ROOT.glob("week-*/day-*") if p.is_dir())
exercises = 0
for day in days:
    if not (day / "README.md").is_file():
        problems.append(f"{day.relative_to(ROOT)}/: no README.md")
    for folder in (p for p in day.iterdir() if p.is_dir() and not p.name.startswith(".") and p.name not in NOT_EXERCISES):
        exercises += 1
        if not (folder / "README.md").is_file():
            problems.append(f"{folder.relative_to(ROOT)}/: no README.md")
        if not (day / "answers" / folder.name).is_dir():
            problems.append(f"{folder.relative_to(ROOT)}/: no answer at {day.relative_to(ROOT)}/answers/{folder.name}/")
for path in files:
    if path.suffix != ".md":
        continue
    for target in LINK.findall(path.read_text(encoding="utf-8")):
        if re.match(r"[a-z]+:", target) or target.startswith("/"):
            continue
        if not (path.parent / target).exists():
            problems.append(f"{path.relative_to(ROOT)}: the link {target} points at nothing")

for line in problems:
    print(line)
if problems:
    sys.exit(f"{len(problems)} problem(s)")
print(f"OK: {len(files)} files, {len(days)} day folders, {exercises} exercises each with a README and an answer, "
      "every link resolves")
