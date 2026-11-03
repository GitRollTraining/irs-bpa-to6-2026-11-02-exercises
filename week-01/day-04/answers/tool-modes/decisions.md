# Answer: the kind of each mode of Codex, and its change

This answer is for the course's run of Codex on 2026-10-30, kept in `codex-run/`; `commands.sh` applies its change. The
modes in `modes.md`, and what each does, come from that run's `/permissions` list and, for Approve for me, Codex's
page "Permissions" (https://learn.chatgpt.com/codex/permission-modes). A new release of Codex can change them, so a
trainer compares them with what Codex shows in the workspace.

| Item | Answer | Reason |
|---|---|---|
| Codex asks if you trust this folder | Yes | The course team wrote each file here, and `ls -a` shows `.claude`, Claude Code's settings, and no `.codex`: no file holds settings or instructions for Codex. Instructions planted in the files that an agent reads are the risk (sections 1.3 and 4.4). |
| Codex asks to make the change in Read Only | No | A yes adds the line, and the run in Ask for approval adds it again. Git then shows the line two times, which the done-when does not allow. |
| The form of `git diff` | `HEAD` | Codex can leave its change staged or not, and `git diff HEAD` shows everything since the last commit, staged or not. Plain `git diff` misses a staged change, and `git diff --staged` misses an unstaged one (section 4.3, the figure of the four forms). |
| Kind, in each of the four rows of `modes.md` | `agent` | Each row says that Codex reads files and runs commands without your yes, in Read Only too. Only an agent uses tools such as these: completion suggests lines as you type, and chat reaches only what you paste into it. Read Only stops edits, not reads and commands, so it does not change the kind (section 4.4). |
| `Answer:` in `modes.md` | `yes` | In the course's run, Git shows only the request's line, at the end of `README.md`, and the done-when allows only that change; blank lines do not count. For an agent, you check its sandbox, approvals and tool access first, then its result against the done-when (section 4.4). |

The check reads the Kind cells, `Answer:`, and every change that Git shows since the start, committed or not. It does
not read your answers to Codex's questions or the form of `git diff`. For Kind, it accepts only agent, also in other
words such as "an agent"; a kind after "not", "no", "unlike" or "than" does not count, and two kinds in one cell are
not accepted. For `Answer:`, it accepts yes only where the one change is the request's line at the end of
`README.md`, blank lines aside, and no for any other change, such as the line in another place or two times, a
changed old line, new line ends (CRLF) or a new file. Where the line is at the end in another form, such as in
backticks or with no period, it accepts yes or no; the debrief starts from no, as the done-when names the line as the
request gives it. Passing does not show that Codex made the change: the check never asks who made it.
