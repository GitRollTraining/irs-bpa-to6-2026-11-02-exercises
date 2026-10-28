# Exercise: Classify ten proposed uses of AI tools, and route those not yours to decide

After this you can classify what federal data rules permit and require of a proposed use of an AI tool, and route one that is not yours to decide to its owner.

**Scenario:** Your office will pilot the case-notes extractor on real notes; before any AI tool touches the lab repository, you answer for ten uses of AI tools its team proposes. From: Microsoft Learn, "Privacy, security, and responsible AI practices", https://learn.microsoft.com/en-us/training/modules/privacy-security-responsible-ai-practices/, restated; and the chapter's case-notes extractor.

**Success criterion:** from `lab`, `python3 ../check.py` prints `Done:`. Once your answers are committed, it compares each with the course's, accepting either answer where the rules allow two, and checks that no AI-tool commit came before them.

**Where you work:** VS Code in your hosted workspace: the file `docs/data-rules-check.md` in the repository `lab`, and the terminal, inside `lab`. AI tools: none.

**Start from:** the folder `data-rules-check`: `python3 ~/practice/reset.py data-rules-check`, which prints `data-rules-check is back as it was supplied.`; then `cd ~/practice/week-01/day-01/data-rules-check/lab`. To get it again: the same reset; it removes your commits.

**What you have:** in `lab`, one commit by the course team and `docs/data-rules-check.md`, uncommitted, all made up: the pilot's approvals, its ten uses, and a table whose Permitted?, Who decides and Why are yours. `../check.py`, the check. The week 1 chapter's part 1, "What may go into an AI tool", which quotes the rules; its section 1.2, "Work out what a federal rule requires of this task, and who decides", whose data-rules check classifies "combinations, each an item of information and a tool" as permitted or not, or "Not yours to decide".

## Steps

1. See where you start: `git log --oneline`, `git status --short`. You should see: one commit, and `?? docs/data-rules-check.md`.
2. Answer before the check compares: read the approvals and uses as your own office's, and fill each row as the file asks, citing the rule and the fact it turns on.
3. Commit, then run the check: `git add docs/data-rules-check.md`, `git commit -m "Answer the data-rules check"`, `python3 ../check.py`. You should see: `Not yet:` and each use the course answers otherwise, or `Done:`.
4. For each use it names, find the fact you missed, change answer and reason, commit, and rerun the check. You should see: `Done:` and your first commit's count.

**Answer:** `~/practice/week-01/day-01/answers/data-rules-check/`: the kept answers, the others the check accepts, and `commands.sh`, ending `Done:`.

## Afterwards, together

How many did your first commit match, and which fact did each miss turn on? Where two answers were accepted, which did you give, and why?
