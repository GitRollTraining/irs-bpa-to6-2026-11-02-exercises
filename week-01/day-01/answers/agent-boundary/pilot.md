# The extractor's pilot: what a coding agent in this repository could reach

The course made up this pilot. Read it as your own team's pilot.

The team will run the case-notes extractor on real case notes, on a workstation that holds this
repository. A coding agent will go on working in the repository there. Real case notes are return
information. A person runs the extractor. The agent never needs a real note.

## The pilot's facts

- **The team:** two developers who work for the IRS, and one developer of the contractor that supports
  the office under its IRS contract. Each of them starts the agent in this repository.
- **The agent's work:** changes to the extractor's code and tests, on the simulated notes in
  `notes/`. The tests run on recorded replies and call no model. The pilot downloads nothing.
- **Where real notes are:** the team's `case-files` tool server reads them from the case system. On
  the pilot workstation, this server is the only way to a real note.
- **The branch:** the agent commits on its own branch. A person pushes the branch and opens the pull
  request. Nobody merges without review.
- **The record:** the team keeps each agent session as evidence, beside the audit trail of the case
  system.

## The files of each coding agent, and the pages that document them

The course read these pages on 2026-10-28.

| Coding agent | Its files in this repository | Documented at |
|---|---|---|
| Claude Code | `.claude/settings.json`, `.mcp.json` | https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/mcp |
| Codex | `.codex/config.toml` | https://learn.chatgpt.com/docs/config-file/config-reference, https://learn.chatgpt.com/docs/config-file/config-sample, https://learn.chatgpt.com/docs/agent-approvals-security |

## Sign-off

Who must agree before the agent runs here: an accountable agency official, who approves the use. A developer of the contractor starts the agent too, so IRS Cybersecurity and the Contracting Officer must also agree (section 1.3).
