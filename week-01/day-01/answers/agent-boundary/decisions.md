# Answer: the pilot's agent boundaries

| Requirement | Change | Reason |
|---|---|---|
| No access to protected notes | Remove Claude Code's `.mcp.json`, `enabledMcpjsonServers`, and `mcp__case-files__*`; remove Codex's `[mcp_servers.case-files]` section. | Read-only access can still expose notes to a model provider (sections 1.1 and 1.3). |
| Approval before edits and pushes | Remove `Edit(/**)` and `Bash(git push *)` from Claude Code's allow list; set Codex's `sandbox_mode` to `"read-only"`. | The pilot permits only reads and test runs without approval; a person pushes the branch (section 1.3). |
| No web search | Add `WebSearch` to Claude Code's deny list; set Codex's `web_search` to `"disabled"`. | The pilot needs no web access (section 1.3). |
| Named approvers | Record the accountable agency official, IRS Cybersecurity, and the Contracting Officer in `docs/pilot.md`. | The proposed use needs approval, and the team includes a contractor (section 1.3). |

The starting files supply the other settings needed by the exercise. `docs/pilot.md` links to the tool documentation. Passing the check confirms these files meet the exercise's requirements; it does not demonstrate enforcement by a running agent.
