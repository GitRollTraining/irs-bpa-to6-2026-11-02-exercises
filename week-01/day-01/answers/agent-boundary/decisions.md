# The kept answer, decision by decision

What the teammate's configuration let the agent do in the pilot, the kept change, and the rule it
rests on. The week 1 chapter's section 1.3 removes "the combinations that would let a bad choice do
damage", so where a setting left something to a person's yes that the pilot rules out, the kept
change removes it rather than asking. Each tool's keys are read as its documentation, read on
2026-10-28, describes them (the table at the end of `docs/pilot.md`).

## Claude Code: `.claude/settings.json` and `.mcp.json`

| What the file let the agent do | Kept change | Rule | The check also accepts |
|---|---|---|---|
| Read real notes through the `case-files` server, approved in `enabledMcpjsonServers` and allowed by `mcp__case-files__*` | The server removed from `.mcp.json`; its tools denied, in case another settings file adds it | Section 1.1: "do not let the agent reach a file that holds it"; what it reads goes to its model's provider, so the agent always has the network half of section 1.3's combination | A `disabledMcpjsonServers` entry, or a deny rule for the server, in place of removing it |
| Edit any file without asking: `Edit(/**)` in `allow` pre-approves edits, whatever `defaultMode` says | `Edit(/**)` removed; Manual mode, `default`, kept | The regulated approvals row: a person says yes to every command that is not a read or a test run | Nothing else: auto mode, `acceptEdits` or no `defaultMode` leaves edits to a classifier or to no one |
| Push any branch, `main` included, without asking: `Bash(git push *)` in `allow` | Moved to `deny`, since a person pushes in the pilot | The pilot's facts, and the approvals row | Pushes left out of `allow`, or put in `ask` |
| Reach any host through `python3`, `git` or a test it wrote: the deny rules match only `curl`, `wget` and the two web tools by name | The sandbox on, with `allowedDomains` empty, no retry outside it (`allowUnsandboxedCommands: false`), and `autoAllowBashIfSandboxed: false`, so turning the sandbox on does not also run every sandboxed command without asking | Section 1.3: "None beyond what the task needs"; section 1.1: what stopped people "was a rule a machine enforced" | `deniedDomains` added as well |

## Codex: `.codex/config.toml`

| What the file let the agent do | Kept change | Rule | The check also accepts |
|---|---|---|---|
| Read real notes through `[mcp_servers.case-files]` | The table removed | As for Claude Code | `enabled = false`, or `enabled_tools = []` |
| Edit files and run commands in the repository without asking: `workspace-write`, under `on-request`, asks only to go beyond the sandbox | `sandbox_mode = "read-only"`, which asks before every edit and command | The approvals row; read-only also asks before test runs, which is stricter than the row | The built-in `:read-only` permission profile, in place of `sandbox_mode` |
| Search the live web: `web_search = "live"`, while `network_access = false` closes only the sandbox's commands | `web_search = "disabled"` | "None beyond what the task needs" | `"cached"`, which "returns pre-indexed results" from "an OpenAI-maintained index" (the sample configuration) |
| Keep no transcript: `persistence = "none"` | `persistence = "save-all"` | The record row: "The session log, plus the audit trail the system itself must keep" | Nothing else: leaving it out lets each developer's own file decide |

## Who must agree

Left to the debrief, and not judged by the check. Section 1.3: "the policy puts that with an
accountable agency official, and the contractor rule with IRS Cybersecurity and the Contracting
Officer." The configuration is a proposal for them.
