# Exercise 3: the answer and its reasons

## The steps

| Step | The answer | Why | The line it rests on |
|---|---|---|---|
| The install command | `npx --yes skills@1.7.4 add OthmanAdi/planning-with-files --skill planning-with-files --agent codex --yes`, run in the exercise's `reference-app` folder | With no `-g`, the command puts the skill into this folder's `.agents/skills`, where Codex finds it for this app only. Nothing outside the folder changes. The version number keeps the command the same for every learner. | Monday's reading, section 3, "Use skills in Codex": "For repositories, Codex scans .agents/skills in every directory from your current working directory up to the repository root." |
| Read the skill before the install | Its description names `task_plan.md`, `findings.md` and `progress.md`, and says the skill keeps them on disk | A skill runs with the agent's permissions, so read what it does before you install it. | Monday's reading, section 3, "Where this goes wrong": "We recommend installing skills only from trusted sources." |
| The request, in the learner's words | One way to say it, folded in step 4 as a hint: `$planning-with-files Plan and make this change: on the case list page, show the words Review first next to each case whose selection score is 50 or more.` | `$` and the name tell Codex to use the skill. | Monday's reading, section 3, "Use skills in Codex": "In Codex CLI or the IDE extension, run /skills or type $ to mention a skill." |

## The skill's output in the kept run

- `task_plan.md` (93 lines), `findings.md` (54 lines), `progress.md` (75 lines), in the folder.
- Under Goal, `task_plan.md` still holds one template line of the skill: "State the intended end result in one clear sentence." The agent wrote its goal below it. The answer keeps the file as the run left it.

## The change in the kept run

- `cases.py`: `REVIEW_FIRST_SCORE = 50`, and `review_first` in each case's view.
- `templates/list.html`: "Review first" after the case number when `review_first` is true.
- `templates/base.html`: one style rule, `.flag`, for the label.
- `tests/test_cases.py`: two new tests, at a score of 49 and 50, and on the page.

## What else the check accepts

- Any wording of the request that starts with `$planning-with-files` and asks for the change. The check reads the skill's files, the case list and the tests, not the request.
- The three files in a task folder under `.planning/`, which the skill uses for parallel tasks.
- Any change that puts "Review first" in the row of each case with a score of 50 or more, and in no other row. The app's tests must pass. The check renders the case list.

## Where the notebook's quoted lines come from

The notebook quotes these lines without naming where they come from, so it stands alone for a learner who missed the talk.

| Where in the notebook | Its place in the day's material |
|---|---|
| The exercise as a whole | Deck slide 44, "Install a skill and use it on the app". It uses deck slide 35, "Using skills in Codex: call, install, and where they live", and deck slide 39, "Two ways a skill or server goes wrong". |
| Step 2: "We recommend installing skills only from trusted sources." | Monday's reading, section 3, "Where this goes wrong" |
| Step 3: "For repositories, Codex scans .agents/skills in every directory from your current working directory up to the repository root." | Monday's reading, section 3, "Use skills in Codex" |
| Step 4: "In Codex CLI or the IDE extension, run /skills or type $ to mention a skill." | Monday's reading, section 3, "Use skills in Codex" |
| Afterwards, question 1: "A new session with nothing loaded knows nothing about your project." | Monday's reading, section 2, "What the agent loses" |
| Afterwards, question 2: "Skills for every repository you work in go in your home folder's `.agents/skills`." | Monday's reading, section 3, "Use skills in Codex" |

## The kept run

`kept-run.md`: what the stand-in agent did, with its version and the date.
