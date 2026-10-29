# Exercise: Tighten your coding agent's configuration for the extractor's pilot

After this exercise, you can close the settings that let a coding agent reach real notes or act without your yes.

**Scenario:** A teammate configured two coding agents, Claude Code and Codex, for the extractor's pilot. The pilot runs on a workstation that can reach real notes. But the configuration still lets the agent read real notes, act without your yes, and search the web. Fix it before the agent runs there.

**Success criterion:** from `lab`, `python3 ../check.py` prints `Done:`.

**Where you work:** the folder `~/practice/week-01/day-01/agent-boundary/lab`, in VS Code and in a terminal. Each path in this exercise starts there. Do not use AI tools.

**Start from:** the folder `agent-boundary`. Run `python3 ~/practice/reset.py agent-boundary`. Then run `cd ~/practice/week-01/day-01/agent-boundary/lab`. To start again, run the same reset. The reset removes your commits.

**What you have:** in `lab`, the extractor's repository, and the teammate's commit on top of it, with the tag `pilot-draft`. The commit changes the files of both agents: `.claude/settings.json` and `.mcp.json` for Claude Code, and `.codex/config.toml` for Codex. `docs/pilot.md` holds the facts of the pilot. `../check.py` is the check. The week 1 chapter, section 1.3, has the rules.

## Steps

1. See the change. Run `git show --stat pilot-draft`. You should see one commit that changes three files.
2. Fix the four problems in the table by hand. Fix the files of both agents.
3. Commit, and run `python3 ../check.py`. You should see `Done:`. If you see `Not yet:`, fix what it names, and run the check again.

| Problem | The rule, in sections 1.1 and 1.3 | Fix it by hand |
|---|---|---|
| 1. The agent can read real notes through the `case-files` server. Claude Code gets the server from `.mcp.json`. Codex gets it from `[mcp_servers.case-files]`. | Section 1.1: a coding agent can send out "Whatever it can open". Section 1.3: return information is "Confidential by default", and "A model provider is not on that list". | Claude Code: remove the file `.mcp.json`. In `.claude/settings.json`, remove the lines `"enabledMcpjsonServers": ["case-files"],` and `"mcp__case-files__*",`. Codex: in `.codex/config.toml`, remove `[mcp_servers.case-files]` and the two lines below it. |
| 2. The agent can act without your yes. In Claude Code, `Edit(/**)` and `Bash(git push *)` in allow let it edit any file and push. In Codex, `sandbox_mode = "workspace-write"` lets it edit files and run commands. | The six settings in section 1.3, row Approvals: the regulated repository gets "All but reads and test runs". | Claude Code: in allow, remove the lines `"Edit(/**)",` and `"Bash(git push *)",`. Codex: change `sandbox_mode` to `"read-only"`. |
| 3. The agent can search the web. The deny list of Claude Code does not hold `WebSearch`. Codex has `web_search = "live"`. | The six settings in section 1.3, row Network: the regulated repository gets "Only what the task needs". The pilot downloads nothing. | Claude Code: in deny, add the line `"WebSearch",` below `"WebFetch",`. Codex: change `web_search` to `"disabled"`. |
| 4. The last line of `docs/pilot.md` does not name who must agree before the agent runs there. | Section 1.3, the list Who decides. "The use: an accountable agency official." "Contractors: also IRS Cybersecurity and the Contracting Officer." "Yours: a proposal concrete enough for yes or no." | Read The team, in `docs/pilot.md`. Then, on its last line, replace TODO with each role that must agree. |

**Answer:** `~/practice/week-01/day-01/answers/agent-boundary/` holds the fixed files, `decisions.md`, and `commands.sh`, which ends with `Done:`. `decisions.md` gives the rule for each change, and the other fixes that the check accepts.

## Afterwards, together

Which two settings together are a path out for a real note? The teammate gave the agent read-only access to the case files. Why does read-only access still let a real note out? Who must agree before the agent runs, and what do you give them?
