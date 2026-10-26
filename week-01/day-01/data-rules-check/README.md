# Exercise: Write the extractor's data requirements, then pass the data-rules check

After this you can work out what a federal data rule requires of the case-notes extractor, write it as requirements a reviewer can check, route each open question to the role that answers it, and pass the data-rules check before any AI tool touches the repository.

**Success criterion:** from `lab`, `python3 ../check.py` prints a line starting `Done:`: the check's six answers are the course's, each with a reason, and each reason for an answer other than Yes ends with the section its rule is in; the TODO cells of `docs/requirements.md` are filled; and both files are committed, with no commit an AI tool made before them. Until then it prints `Not yet:` and what is left. The check tests that each reason and requirement is there and in that shape, not how good it is. Nothing is handed in; the class talks it through when the exercise ends.

**Where you work:** VS Code in your hosted workspace: the files `docs/data-rules-check.md` and `docs/requirements.md` in the repository `lab` in the folder `data-rules-check`, and the terminal (Terminal > New Terminal), inside `lab`. AI tools: none; no AI tool is opened until the check is committed, and this exercise opens none.

**Start from:** the folder `data-rules-check` in the practice kit: `python3 ~/practice/reset.py data-rules-check`, then `cd ~/practice/week-01/day-01/data-rules-check/lab`. The reset command builds the repository `lab` and prints `data-rules-check is back as it was supplied.` To get it again: the same reset command, which also removes your commits. Git commits under the name and email you gave it in the practice environment's set-up.

## Steps

1. In the terminal, inside `lab`, see where you start and what is left: `git log --oneline`, `git status --short`, then `python3 ../check.py`. You should see: one commit by the course team, `?? docs/data-rules-check.md` and `?? docs/requirements.md` (two files not committed), and `Not yet:` naming the empty rows, the TODO cells and the two files.
2. Take the check: in the Explorer on the left, open `practice`, then `week-01`, `day-01`, `data-rules-check`, `lab` and `docs`, then `data-rules-check.md`. In each of the six rows, write in Permitted? Yes, No, or Not mine to decide where the answer is someone else's to give, and the reason in Why; in each row that is not Yes, end the reason with the section of the chapter whose rule it rests on, written (section 1.1), (section 1.2) or (section 1.3). Save it (File > Save), then run `python3 ../check.py`. You should see: `Not yet:` naming no row of `docs/data-rules-check.md`; a row it names is not answered as the course's check answers it, and the check tells you to compare the table in section 1.2.
3. Write the requirements and route the questions: open `requirements.md`, in the same `docs` folder. In its table of requirements, the first column of each of the three TODO rows already says what that requirement covers. In each, replace the TODO in Requirement a reviewer can check with a line a reviewer can check from the repository alone, and the TODO in Where they check it with the file or folder where they check it, in backticks, such as `extractor.py`; a file the lab adds later in the week, as it adds `extractor.py`, may be named. Then, in the table of open questions, write in Who answers it the role the chapter's fifth move names for each question, in the chapter's words. Save, then run `python3 ../check.py`. You should see: `Not yet:` naming only the two files as not committed yet.
4. Commit both, before any AI tool touches the repository: `git add docs/data-rules-check.md docs/requirements.md`, then `git commit -m "Record the data-rules check, passed, and the extractor's requirements"`, then `python3 ../check.py` and `git log --oneline`. You should see: `2 files changed`, a line starting `Done:`, and your commit above the course team's.

**Answer:** `~/practice/week-01/day-01/answers/data-rules-check/` in the practice kit: `data-rules-check.md` and `requirements.md` filled in, and `commands.sh`, the commands in order, each with a note; run from `lab` after the reset command, it ends with `Done:`.

## Afterwards, together

Which requirement did you rewrite most before a reviewer could check it? Why does the course train you to notice the row that is not yours to decide?
