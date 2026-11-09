# Exercise 2: the answer and its reasons

## AGENTS.md

| Line | Why | The line it rests on |
|---|---|---|
| `Run pytest in this folder after every change. Finish only when all tests pass.` | An agent runs a test command almost only when its context file names the command. With this line, a new session runs the tests after a change without a request. | Monday's reading, section 2, "What to put in it": "uv, pytest, or repository-specific tools (repo_tool) are used almost exclusively if they are mentioned in the context file." |
| `To run the app: flask --app app run. It keeps running until Ctrl+C, so check a change with the tests, not the app.` | The day plan asks for how to run the app. The second sentence stops the agent from starting a server in the middle of a task, where it waits. | Monday's reading, section 2, "The exercise": "write `AGENTS.md` with two things: how to run the application, and how to run its tests" |
| No overview of the project | Every line goes into every session, so each line costs on every task. An overview repeats the README. | Monday's reading, section 2, "What to put in it": "Human-written context files should only include instructions required for coding agents that are not already present in the README" |

The quoted lines keep the reading's words. `ste-lint.py` flags three findings inside them (two passive verbs and one sentence of 27 words): they stay as quoted. In the notebook, question 2's quoted line holds one passive verb, "is read": it stays as quoted.

## The request

`On the case list page, add a Balance due column after Status.` One small change, with no word about tests, so a test run comes from `AGENTS.md`.

## The change in the kept run

- `templates/list.html`: a Balance due header after Status, and a cell `{{ case.balance_due | money }}` in each row.
- `tests/test_cases.py`: one new test, `test_case_list_page_shows_balance_due_after_status`. The agent added it. The exercise does not ask for it.

## What else the check accepts

- Any wording of `AGENTS.md` that names `pytest` and `flask --app app run`. The two lines above are one way to say it, folded in step 2 as a hint.
- Any change to an app file (a `.py`, `.html` or `.json` file). The tests must run after that change and after `AGENTS.md`, and they must pass.
- A test run that the learner made by hand also passes the check. The exercise asks the learner not to run `pytest`, and the check cannot tell who ran it.

## Where the notebook's quoted lines come from

The notebook quotes these lines without naming where they come from, so it stands alone for a learner who missed the talk.

| Where in the notebook | Its place in the day's material |
|---|---|
| The exercise as a whole | Deck slide 31, "Tell Codex how to run the tests". It uses deck slide 27, "Codex reads AGENTS.md once, when a session starts", and deck slide 28, "AGENTS.md: write the commands, leave out the overview". |
| Step 2: "The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task." | Monday's reading, section 2, "What to put in it" |
| Afterwards, question 2: "Every line in `AGENTS.md` is read in every session, so it costs on every task." | Monday's reading, section 2, "The trade-off" |

## The kept run

`kept-run.md`: what the stand-in agent did, with its version and the date.
