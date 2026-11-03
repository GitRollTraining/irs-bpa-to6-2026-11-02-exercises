# 5.2 Direct and check run 1

Direct a coding agent with run 1's prompt, and check its done-when yourself before you accept the run.

Run 1 adds an output schema for the extractor, and tests that validate outputs against it. Your agent will report done, with all tests passing. That is a claim until you check it.

## Start

Follow the [Day 5 setup](../README.md). Use your coding agent, Codex or Claude Code, and no other AI tool. In a new terminal in the course folder, these commands create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-05/direct-run-one/lab/.git || python3 reset.py direct-run-one
cd week-01/day-05/direct-run-one/lab
```

All paths below are relative to `lab/`. Open run 1's prompt and your report:

```sh
code run1-prompt.txt run-1-record.md
```

## Direct, check and report

Start your agent in this terminal: `codex` or `claude`. When it asks if you trust this folder, answer yes: its settings start no program. Paste all of `run1-prompt.txt` as one message. If the agent asks to break the Constraints, answer no: a yes lets it do that. When it reports done, type `/exit`.

Run the done-when yourself. Then stage the only folders the Constraints let the run change, and read the test files' diff: the agent wrote the tests that decide whether it is done.

```sh
python3 -m pytest tests/test_schema.py
git add schema tests
git diff --staged -- tests
```

Expect a last line such as `22 passed in 0.03s`, then each line of the tests after `+`. Plain `git diff` misses staged changes. If the diff fills the screen, press `q`.

Find both tests of the Done row in the diff. In `run-1-record.md`, write the two lines below. Use sections 5.1 and 5.2 of the notebook to explain each answer.

| In `run-1-record.md` | What to write |
|---|---|
| `Done:`. The done-when asks for two tests. One expects an error when an output lacks `amount_in_question`, or each required field in turn. The other sets `amount_in_question` to None, Python's null, and expects no error. | `Done: met` if your pytest run passed with both tests. Else `Done: not met`. |
| `Proof:`. Anyone can run the command again, and find each test. | `Proof: python3 -m pytest tests/test_schema.py printed <its last line>. Must fail: <test name>. Null passes: <test name>.` |

<details><summary>Why each answer</summary>

| In `run-1-record.md` | Why |
|---|---|
| `Done:`. The done-when asks for two tests. One expects an error when an output lacks `amount_in_question`, or each required field in turn. The other sets `amount_in_question` to None, Python's null, and expects no error. | The done-when asks for two tests. One expects an error when an output lacks `amount_in_question`, or each required field in turn. The other sets `amount_in_question` to None, Python's null, and expects no error. Section 5.1, run 1's Done-when: "one output that must fail (amount_in_question missing) and one that must pass with amount_in_question null" |
| `Proof:`. Anyone can run the command again, and find each test. | Anyone can run it again, and find each test. Section 5.2, list "Have it show evidence": "The command it ran, and what it returned" |

</details>

Save the file. If Done is not met, do not commit: direct and check run 1 again. If Done is met, commit and check:

```sh
git commit -m "Accept run 1"
python3 ../check.py
```

Expect `Accept run 1` and the run's files only: Git does not track your report. Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. The check breaks the schema to see whether a test fails; it does not read your agent's session.

## Reflect

If pytest passes, when would Done still be not met? How would you stop run 2 from editing the tests you accepted? What did you not check in run 1, and who needs to know?

[Worked answer](../answers/direct-run-one/) · [Start over](../../../README.md#start-an-exercise-again)
