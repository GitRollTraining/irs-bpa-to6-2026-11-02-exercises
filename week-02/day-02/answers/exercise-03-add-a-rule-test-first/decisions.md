# Exercise 3: the answer and its reasons

## The request

| Part | Why | The line it rests on |
|---|---|---|
| `$test-driven-development` first | Codex uses the skill without matching its description. | "Typing `$test-driven-development` skips the matching." |
| The function, the rule and `reader.load_relief_areas` | Codex needs where to put the rule and where its data comes from. | "The relief list is a file that `reader.py` loads." |
| Stub `load_relief_areas` with `monkeypatch` in every test that calls `penalty_for` | A unit test reads no file. After the change, each call of `penalty_for` reads the relief list. | "avoid hitting databases, the filesystem or firing HTTP queries"; "Stub your own reader, not a function built into Python" |
| Do not commit | The learner reads the change, then commits the two files. | none: a choice of this exercise |

## The change, `files/payment_job/rules.py` and `files/tests/test_rules.py`

- `penalty_for` returns 0.0 when `account.area` is in `reader.load_relief_areas()`.
- A new test replaces `reader.load_relief_areas` with `lambda: {"north"}` and expects 0 for an account in `north`. On the start's `rules.py` it fails with 80.0 where it expects 0: red, because the rule is missing.
- The older test of `penalty_for` gets a stub that returns an empty set. The kept run left it reading the real file (`files/tests/test_rules.codex.py`), and the check found that: with the file removed, that test stopped with an error.
- The commit holds `payment_job/rules.py` and `tests/test_rules.py`. The skill's folder and `skills-lock.json` stay out of it.

## What else the check accepts

- A stub on `rules.load_relief_areas` when `rules.py` imports the function by name, or any other stub that makes the tests read no file.
- A refactor in a second commit, the optional part.
- The skill's files in the commit too.

## Where the notebook's quoted lines come from

All are in the Program repository's day file `days/day-02/curated.md`, section 3. Write the test before the code. The exercise is deck slide 41 ("Add a rule test first").

| Quoted line | Heading |
|---|---|
| "Typing `$test-driven-development` skips the matching." | Read a test-first skill as a worked example |
| "avoid hitting databases, the filesystem or firing HTTP queries" | Replace the file read with a stub |
| "Stub your own reader, not a function built into Python" | Replace the file read with a stub |
| "Its description decides when it runs" | Read a test-first skill as a worked example |
| "Write the test first. Watch it fail. Write minimal code to pass." | Read a test-first skill as a worked example |
| "Fails because feature missing (not typos)" | Read a test-first skill as a worked example |
| "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST" | Read a test-first skill as a worked example |
| "But the skill states it more strongly than the evidence does." | Read a test-first skill as a worked example |
| "If you didn't watch the test fail, you don't know if it tests the right thing." | Read a test-first skill as a worked example |
| "The relief rule needs a stub, because the test checks the penalty, not how the code reads the file." | Replace the file read with a stub |
| "Sequencing, the order in which test and production code are written, had no important influence." | Run red, green, refactor |
