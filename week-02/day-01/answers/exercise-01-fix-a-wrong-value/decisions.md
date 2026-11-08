# Exercise 1: the answer and its reasons

## The change

| What changes | The answer | Why | The line it rests on |
|---|---|---|---|
| `reference-app/templates/case.html`, the Balance due row | `{{ case.balance_due \| money }}` in place of `{{ case.assessed \| money }}` | The page showed the assessed amount in the Balance due row. The app already calculates the balance due in `cases.py`, and the page gets it as `case.balance_due`. So the fix uses that value and changes no calculation. | `reference-app/cases.py`, function `balance_due`: "Return the amount still owed: the assessed amount minus the amount paid." |

## The request and the prompts

| Step | The answer | Why | The line it rests on |
|---|---|---|---|
| The request to Codex | The page of case CS-2026-0001 shows Balance due $18,400. It must show $12,250, which is Assessed minus Paid. Find the cause and fix it. Do not change the data. | It names what the page shows and what it must show. Codex then finds the cause. | Monday's reading, section 1, "The exercise": "Describe what you see on the page and what it should show." |
| A prompt to change a file in `reference-app` | Yes | The fix is a change to the app, in your own copy. | Monday's reading, section 1, "When Codex asks permission": "Before you answer a prompt, read the command. Ask why this task needs it." |
| A prompt to start the app | No | `flask --app app run` keeps running, so Codex waits for it. You run the app in step 4. | The same line |
| A prompt to use the network or to change a file outside `reference-app` | No | The fix needs neither. | The same line |

## What else the check accepts

- Any change that makes every case page show Balance due as Assessed minus Paid, such as a calculation in the template. The check reads the pages, not the template.
- Changes to other files, while the data does not change and the app's tests pass.

## The kept run

`kept-run.md`: what the stand-in agent did, with its version and the date.
