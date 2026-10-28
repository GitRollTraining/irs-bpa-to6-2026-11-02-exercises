# The extractor's pilot: what a coding agent in this repository could reach

Pretend this is real. The team will run the case-notes extractor on real case notes in a pilot, on
a workstation that holds this repository, and a coding agent will go on working in the repository
there. Real case notes are return information. A person runs the extractor; the agent never needs a
real note.

## The pilot's facts

- **The agent's work:** changes to the extractor's code and tests, on the simulated notes in
  `notes/`. The tests run on recorded replies and call no model. Everything the work needs is
  installed before the pilot starts; nothing is downloaded during it.
- **Where real notes are:** the team's `case-files` tool server reads them from the case system. On
  the pilot workstation it is the only way to a real note.
- **The branch:** the agent commits on its own branch. A person pushes the branch and opens the pull
  request from their own terminal. Nothing is merged without review.
- **The record:** each agent session is kept as evidence, beside the audit trail the case system
  keeps itself.

## Each coding agent's files, and the pages that document them

Read on 2026-10-28.

| Coding agent | Its files in this repository | Documented at |
|---|---|---|
| Claude Code | `.claude/settings.json`, `.mcp.json` | https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/mcp |
| Codex | `.codex/config.toml` | https://learn.chatgpt.com/docs/config-file/config-reference, https://learn.chatgpt.com/docs/config-file/config-sample, https://learn.chatgpt.com/docs/agent-approvals-security |

## Sign-off

Who must agree before the agent runs here: TODO
