# Answer: directing Codex through one change, and what to check before the commit

Not yet run in the workstation. This answer is written from OpenAI's Codex documentation
(https://learn.chatgpt.com/docs, fetched 2026-11-05), not from a run of Codex. `commands.sh` copies in
the files a run would leave, then commits and checks them. A new release of Codex can change a
command's name or what its screen shows, so a trainer compares each step with what Codex shows in
the workstation.

| Requirement | Change | Reason |
|---|---|---|
| Record what Codex runs as | `/status`: model, approval policy, sandbox in `record.md`; Ask for approval selected | `/status` is there to "Confirm the active model, approval policy, writable roots" (Developer commands). Permissions: "For most work, start with Ask for approval." (deck 1.5) |
| Write the project's rules once | `/init`, then keep `Run the tests before you say a change is done.` in `AGENTS.md` | `/init`: "Generate an `AGENTS.md` scaffold in the current directory." "Codex reads AGENTS.md files before doing any work." (deck 1.3) |
| A prompt Codex can finish | `/plan` and four parts: goal, context, constraints, done when; see `record.md` | Best practices: "A good default is to include four things in your prompt:", and Plan mode builds "a stronger plan before implementation" (deck 1.5) |
| Each command Codex asks to run | Yes to reading files and running the tests in `work/`; no to anything outside it | Best practices names as a common mistake "Giving Codex full permission to your computer before you understand the workflow" (deck 1.5) |
| Your own read of the change | `/diff`: the `d` entry in `SECONDS`, the pattern, and the new `test_days`; no other file | `/diff`: "Review Codex's edits before you commit or run tests." "Fluent writing or a confident summary is not enough to establish that a task succeeded." (deck 1.4) |
| The tests, inside Codex | `!python3 -m pytest -q`: `5 passed` | "Prefix a line with ! to run a local shell command under the current approval and sandbox settings." (deck 1.4) |
| Checkpoints | `start.py` makes the commit before; you commit after | Codex CLI: "Create Git checkpoints before and after a task so you can revert changes." (deck 1.5) |

The check accepts any AGENTS.md that holds the tests line, in any case and with or without its full
stop, any change to a file whose name starts with `test_`, and any wording in `record.md` once each
line is filled. It runs `parse_duration("2d")` and the tests, so a commit without days does not pass.
Passing does not show that Codex made the change, that the new test checks days, or that the
learner read `/diff`: the check never asks who wrote the code, and the reflection is for the group.
