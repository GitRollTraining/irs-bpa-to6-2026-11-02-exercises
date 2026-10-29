# The course's answer: what each change closes

The check reads each setting as the documentation of its tool describes it. `docs/pilot.md` lists
these pages. The course read them on 2026-10-28.

| Problem | The change | Its rule | The check also accepts |
|---|---|---|---|
| 1. The agent can read real notes through the `case-files` server. | Claude Code: remove `.mcp.json`, `enabledMcpjsonServers` and `mcp__case-files__*`. Codex: remove `[mcp_servers.case-files]`. | Section 1.1: a coding agent can send out "Whatever it can open". Section 1.3: return information is "Confidential by default", and "A model provider is not on that list". So the agent must not reach a real note at all, with or without your yes. | Claude Code: a `disabledMcpjsonServers` entry, or a deny rule for the server. Codex: `enabled = false`, or `enabled_tools = []`. |
| 2. The agent can act without your yes. | Claude Code: remove `Edit(/**)` and `Bash(git push *)` from allow. Codex: set `sandbox_mode = "read-only"`. | The six settings, row Approvals: "All but reads and test runs". In the pilot, a person pushes the branch. | Claude Code: `Bash(git push *)` in ask or in deny. Codex: the built-in `:read-only` permission profile. |
| 3. The agent can search the web. | Claude Code: add `WebSearch` to deny. Codex: set `web_search = "disabled"`. | The six settings, row Network: "Only what the task needs". The pilot downloads nothing. | Codex: `web_search = "cached"`, which gives results from an index that OpenAI keeps. |
| 4. Nobody named who must agree. | Name the accountable agency official. A developer of the contractor starts the agent, so name IRS Cybersecurity and the Contracting Officer too. | Section 1.3, Who decides: "The use: an accountable agency official" and "Contractors: also IRS Cybersecurity and the Contracting Officer". | The check looks for the three roles only. "Yours" is not a sign-off: section 1.3 gives you "a proposal concrete enough for yes or no". This configuration is that proposal. |

The starting files already close the other settings that the check reads. For Claude Code, the
sandbox is on, and no command can run again outside it. For Codex, `[history]` keeps each session.
