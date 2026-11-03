# Answer: your report on run 1, and whether to accept it

`agent-run/` holds run 1 as Codex and Claude Code made it on 2026-10-30, and `agent-run/README.md` says what each run
is. This answer is for the Codex run, which `commands.sh` copies into `lab/`. The check reads the run that is in
`lab/`, so it accepts your agent's run too.

| Item | Answer | Reason |
|---|---|---|
| The agent asks to break run 1's Constraints | No. Answer yes to a request that keeps them. | A yes lets the agent do it, such as a call to the model or an edit outside `schema/` and `tests/` (section 5.1, run 1's Constraints). |
| The done-when | Run it yourself, in your terminal: `python3 -m pytest tests/test_schema.py`. Its last line: `22 passed in 0.03s`. | The agent's report is only its word; your own run is evidence (section 5.2). |
| What to stage | `schema` and `tests`: `files = "schema tests"` in cell 2, or `git add schema tests`. | The Constraints let the run change only these two folders (section 5.1). |
| What to read first | The test files' staged diff: `form = "--staged"` in cell 2, which opens `tests.diff`, or `git diff --staged -- tests`. | The agent wrote the tests that decide whether it is done (section 5.2). The plain form compares your files with the staging area, so it misses staged changes (day 4, section 4.3). |
| `Done:` | `Done: met` | Your pytest run passed with both tests. `test_missing_field_fails` takes each required field out of an output, `amount_in_question` among them, and expects an error. `test_null_amount_passes` sets `amount_in_question` to None and expects no error. Both load the run's schema, `schema/case_notes.schema.json`, so the run meets both parts of its done-when (section 5.1). |
| `Proof:` | `Proof: python3 -m pytest tests/test_schema.py printed 22 passed in 0.03s. Must fail: test_missing_field_fails. Null passes: test_null_amount_passes.` For the Claude Code run: `19 passed`, `test_missing_amount_fails` and `test_null_amount_passes`. | The command, what it returned, and each test's name: anyone can run it again and find each test (section 5.2). |
| The commit | `git commit -m "Accept run 1"`, or `commit = True` in cell 3. | The commit records the run that you accepted; with the stored result, it is evidence (section 5.2). |
| Reflect: keeping run 2 off the accepted tests | For Claude Code, a deny rule: `claude-settings.json` adds `"Edit(/tests/test_schema.py)"` to the `deny` list of `.claude/settings.json`. For Codex, read the test files' diff after each run. | Section 5.2 says to make the tests read-only with a deny rule. The rule names the file, not `tests/`, because run 2 adds `tests/test_extractor.py`. The course found no Codex setting for one file ("Agent approvals & security", https://learn.chatgpt.com/docs/agent-approvals-security, read 2026-10-30). |

The check runs the done-when, then runs the tests on a copy of `lab/` after two changes to each JSON file in `schema/`
that defines `amount_in_question`: one makes it optional, the other forbids null. A test holds a part when it passes
on the run, fails or disappears after that part's change, and does not fail after a change in form only (an `allOf` or
an `anyOf`) that accepts the same outputs. So pytest can pass while Done is not met: tests on their own copy of the
schema hold no part, and neither does a test of the schema's form, such as the Claude Code run's
`test_schema_names_exactly_the_five_fields`. Where the schema is not a JSON file in `schema/`, the check cannot tell,
and a Done of met stands if the Proof names a test that passes. The check also accepts yes or no for Done, but not
"not yet met"; other words around the Proof's parts, such as `pytest -q`, or both test names without labels; the last
line with or without its time; a case such as `test_missing_field_fails[amount_in_question]`; and any number of
commits, yours or the agent's. It never asks to commit a run that misses a part. It does not read the agent's session
or how you read the diff, so passing does not show that the agent kept every Constraint. Nor did anyone compare the
schema with each rule of `docs/fields.md`: the report's other two fields, scope and not verified, hold such gaps
(section 5.2).
