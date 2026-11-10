# Exercise 1: decisions

For the trainer. The exercise is deck slide 21, "Review a teammate's pull request". Each section gives one thing the learner does, the reason, the notebook line it rests on, and what else the check accepts. The check is `check.py` in the exercise folder.

## 1. Write the Code Review Rules on the branch review-rules

- **The change.** The learner adds a section `## Code Review Rules` to `AGENTS.md`, with at least four numbered rules. The learner commits it on the branch `review-rules` and pushes it. `files/AGENTS.first-commit.md` holds the kept answer for this commit: four rules, on design, functionality, complexity and tests.
- **Reason.** A review comment cites a rule by its number. So each rule must be a thing a reviewer can check in a change. The four topics are the four checks that the day's reading gives.
- **The notebook line.** "Number the rules: a review comment cites a rule by its number."
- **What else the check accepts.** Any wording. Any topic. More than four rules. The check counts the lines under the heading that start with a number and a full stop. It does not read what a rule says.

## 2. Add the rule on size that the teammate asks for

- **The change.** The learner adds a fifth rule, in their own words, with the number 100 in it. The learner commits it as a second commit on `review-rules` and pushes it. `files/AGENTS.md` holds the kept answer.
- **Reason.** A reviewer needs a rule to cite when a pull request is too large. The teammate's request is part of the scenario. The learner makes the change in a second commit, so the squash merge in section 3 has two commits to join.
- **The notebook line.** "Add that rule as the next numbered line of your section, in your own words, with the number 100 in it."
- **What else the check accepts.** Any numbered line that holds the text `100`. The line need not be the last one. The check needs at least two commits on `review-rules` after the start.

## 3. Squash-merge into main and push main

- **The change.** The learner switches to `main`, runs `git merge --squash review-rules`, makes one commit, and pushes. The kept commit message is "Add Code Review Rules".
- **Reason.** A squash merge puts the whole branch on `main` as one commit. So `main` keeps one commit for each pull request. The branch's own two commits stay on the branch.
- **The notebook line.** "`git merge --squash` stages the branch's whole change and does not commit it."
- **What else the check accepts.** Any commit message. The check passes when `AGENTS.md` on `main` equals `AGENTS.md` on `review-rules`, when none of the branch's commits is on `main`, and when `main` has no merge commit since the start. A plain merge or a fast-forward fails the check, with a message that says to start again.

## 4. Fetch the teammate's branch and switch to it

- **The change.** The learner runs `python3 ../teammate.py`, then `git fetch` and `git switch add-penalty-cap`.
- **Reason.** The review needs the teammate's branch beside `main`, with the learner's rules already in it. `teammate.py` starts the branch from `main` as it is now.
- **The notebook line.** "`teammate.py` pushes the branch `add-penalty-cap` to the team repository. It starts from `main` as it is now, with your rules in it."
- **What else the check accepts.** The check looks for the fetched branch `origin/add-penalty-cap` in `lab`. The `git switch` is not tested.

## 5. Review the teammate's change, beside Codex, and fill review.md

- **The change.** The learner reads the diff with `git diff main...add-penalty-cap`, runs Codex's `/review` against `main`, and fills the four parts of `lab/review.md`. `files/review.md` holds the kept answer.
- **Reason.** Two reviews of one change show what each reviewer sees and misses. The learner checks every rule that Codex cites against the diff. The comparison and the request make the learner decide which comment to act on.
- **What the review finds.** The teammate's change caps each penalty at 500 dollars. It wraps one line of arithmetic in a class with an on and off flag that nothing uses. That breaks the complexity rule. It adds no test of the cap. That breaks the tests rule.
- **The notebook line.** "Check every rule that Codex cites against the diff yourself."
- **What else the check accepts.**
  - Under "My comments": at least one line that starts with `Rule`, a number and a colon, with text after it. The line may start with a dash or a star, and capitals do not matter.
  - Under "Codex's comments": any line.
  - Under "Compared": any line.
  - Under "The change I request": a first line that starts the same way. Its rule number must be between 1 and the number of rules on `main`.
  - The lines of the form's own template do not count. The check does not read the diff. It does not test whether a comment is right.
- **Where the kept Codex lines come from.** A stand-in agent wrote them, because Codex was not installed where the kept run ran. `kept-run.md` lists the Codex steps that the run did not test.

## Where each quote comes from

The curated file is the day's own file, `days/day-03/curated.md`. All headings below sit under the heading "Review a teammate's change before it reaches main". The deck is the day's `deck.json`. Slide numbers count its `slides` from 1.

| Quote in the notebook | Curated file: heading and line | Deck slide |
|---|---|---|
| "The most important thing to cover in a review is the overall design" | Check four things in every review, line 129 | deck slide 10 |
| "Does this CL do what the developer intended?" | Check four things in every review, line 130 | not on a slide (deck slide 10 asks it in other words) |
| "where developers have made the code more generic than it needs to be, or added functionality that isn’t presently needed by the system." | Check four things in every review, line 134 | not on a slide (deck slide 10 says it in other words) |
| "Will the tests actually fail when the code is broken?" | Check four things in every review, line 132 | deck slide 10 |
| "`git merge --squash` stages the branch's whole change and does not commit it." | Choose a merge method, line 196 | not on a slide (deck slide 16 says it in other words) |
| "Codex reads AGENTS.md files before doing any work." | Run a coding agent as a second reviewer, line 218 | deck slide 12 |
| "should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn’t perfect." | Approve a change that improves the code, line 146 | not on a slide (deck slide 11 says it in other words) |
| "Check every rule that Codex cites against the diff yourself." | Run a coding agent as a second reviewer, line 237 | not on a slide (deck slide 12 says it in other words) |
| "preserves every commit from the pull request branch and adds an explicit merge point." | Choose a merge method, line 169 | not on a slide (deck slide 15 says it in other words) |

## Quotes with no source in the day's files

- "Add a rule on size, so a reviewer can ask for a split: a pull request holds one self-contained change of about 100 lines; a larger one is split." This is the teammate's request in the scenario. The notebook writes it. The curated file names the idea in two places. Line 103 quotes a guide's number, "100 lines is usually a reasonable size". Line 281 gives an example rule, "about 100 lines".

## Findings of the linter inside quotes

The linter flags three quotes. The words stay as the source has them.

- The quote on over-engineering holds one present perfect. The finding is advisory.
- The quote on approving a change holds one long sentence and one passive. The passive finding is advisory.
- The teammate's request in the scenario holds one long sentence and one semicolon.
