"""The done check for exercise 1. In the notebook it is the last cell; in a terminal in the course
folder: python3 week-02/day-03/exercise-01-review-a-teammates-pull-request/check.py

It reads the team repository, remote/team.git, through Git: the Code Review Rules in AGENTS.md on
main, your review-rules branch, and whether main took it as one squashed commit. It looks for your
teammate's branch in lab/, and reads lab/review.md. No model is called and no agent starts.
"""
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE / "lab"
REMOTE = HERE / "remote" / "team.git"
RESET = f"python3 reset.py {HERE.name}"
RULE = re.compile(r"^\s*(\d+)\.\s+\S")
CITES = re.compile(r"^\s*(?:[-*]\s*)?Rule (\d+):\s*\S", re.IGNORECASE)


def git(*args: str, where: Path = REMOTE) -> subprocess.CompletedProcess:
    """Run a Git command in the team repository, or in lab/."""
    return subprocess.run(["git", "-C", str(where), *args], capture_output=True, text=True)


def rules_on(ref: str) -> list[str]:
    """The numbered lines under ## Code Review Rules in AGENTS.md at a branch of the team repository."""
    shown = git("show", f"{ref}:AGENTS.md")
    if shown.returncode:
        return []
    section = re.split(r"^## Code Review Rules[^\n]*\n", shown.stdout, maxsplit=1, flags=re.MULTILINE)
    if len(section) < 2:
        return []
    body = re.split(r"^## ", section[1], maxsplit=1, flags=re.MULTILINE)[0]
    return [line for line in body.splitlines() if RULE.match(line)]


def rules_left() -> list[str]:
    """What is left of steps 2 and 3: your rules, the requested change, and the squash merge."""
    if git("rev-parse", "--verify", "-q", "refs/heads/review-rules").returncode:
        return ["The team repository has no review-rules branch yet. Commit your rules on it and push: step 2."]
    left = []
    rules = rules_on("review-rules")
    if len(rules) < 4:
        left.append(f"review-rules has {len(rules)} numbered rules under ## Code Review Rules in AGENTS.md; "
                    "write at least 4. Step 2.")
    if int(git("rev-list", "--count", "start..review-rules").stdout.strip() or 0) < 2:
        left.append("review-rules holds one commit. Make the change your teammate requested in a second "
                    "commit, and push it: step 3.")
    if not any("100" in rule for rule in rules):
        left.append("No rule on review-rules says a pull request is about 100 lines. That is your teammate's "
                    "requested change: step 3.")
    if git("show", "main:AGENTS.md").stdout != git("show", "review-rules:AGENTS.md").stdout:
        left.append("main on the team repository does not hold review-rules' AGENTS.md yet. Squash-merge "
                    "review-rules into main and push main: step 3.")
    elif git("merge-base", "--is-ancestor", "review-rules", "main").returncode == 0:
        left.append("main holds review-rules' own commits, so it was merged without squashing. Squash-merge: "
                    "start again from the reset and use git merge --squash. Step 3.")
    elif git("rev-list", "--merges", "start..main").stdout.strip():
        left.append("main has a merge commit. A squash merge makes one ordinary commit. Step 3.")
    return left


def lines_under(text: str, heading: str, template: str) -> list[str]:
    """The lines you wrote under one heading of review.md, without the template's own lines."""
    def body(source: str) -> list[str]:
        part = re.split(rf"^## {re.escape(heading)}\s*\n", source, maxsplit=1, flags=re.MULTILINE)
        part = re.split(r"^## ", part[1], maxsplit=1, flags=re.MULTILINE)[0] if len(part) == 2 else ""
        return [line.strip() for line in part.splitlines() if line.strip()]
    given = set(body(template))
    return [line for line in body(text) if line not in given]


def review_left(count: int) -> list[str]:
    """What is left of step 4: your teammate's branch in lab/, and lab/review.md."""
    left = []
    if git("rev-parse", "--verify", "-q", "refs/remotes/origin/add-penalty-cap", where=LAB).returncode:
        left.append("lab/ has not fetched your teammate's branch add-penalty-cap yet. Run teammate.py, then "
                    "git fetch: step 4.")
    text = (LAB / "review.md").read_text(encoding="utf-8") if (LAB / "review.md").is_file() else ""
    template = (HERE / "review.md").read_text(encoding="utf-8")
    mine = lines_under(text, "My comments", template)
    codex = lines_under(text, "Codex's comments", template)
    asked = [line for line in lines_under(text, "The change I request", template) if CITES.match(line)]
    if not any(CITES.match(line) for line in mine):
        left.append('review.md has no comment of yours under "My comments" that starts with the rule it '
                    'cites, such as "Rule 2:". Step 4.')
    if not codex:
        left.append('review.md has nothing under "Codex\'s comments" yet. Copy Codex\'s review there: step 4.')
    if not lines_under(text, "Compared", template):
        left.append('review.md has nothing under "Compared" yet. Step 4.')
    if not asked:
        left.append('review.md has no line under "The change I request" that starts with a rule, such as '
                    '"Rule 2:". Step 4.')
    elif count and not 1 <= int(CITES.match(asked[0]).group(1)) <= count:
        left.append(f"The change you request cites a rule your AGENTS.md does not have: it has rules 1 to {count}.")
    return left


def check() -> list[str]:
    """Return what is left: one line for each thing that is not yet right."""
    if not (LAB / ".git").is_dir() or not REMOTE.is_dir():
        return [f"lab/ is not there yet. In a terminal in the course folder, run {RESET}. See Start from."]
    return rules_left() + review_left(len(rules_on("main")))


if __name__ == "__main__":
    left = check()
    print(f"Not yet: {len(left)} left." if left else
          "Done: main holds your Code Review Rules as one squashed commit, with the change your teammate "
          "requested, and review.md compares your review of add-penalty-cap with Codex's and requests one "
          "change, citing a rule.")
    for line in left:
        print("- " + line)
