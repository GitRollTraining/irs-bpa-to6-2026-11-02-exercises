# 1.3 Set agent boundaries

Limit what a coding agent can access and do, and identify who must approve its use.

A teammate configured Claude Code and Codex for an extractor pilot. The proposed workstation can reach protected notes, but the agents need only code and simulated data. Review both configurations before either agent runs. The pilot and its data are fictional.

## Start

Follow the [Day 1 setup](../README.md). Edit the files by hand; do not start either agent. In a new terminal in the course folder, create the workspace only if it is missing, then enter it:

```sh
test -d week-01/day-01/agent-boundary/lab/.git || python3 reset.py agent-boundary
cd week-01/day-01/agent-boundary/lab
```

All paths below are relative to `lab/`. Read `docs/pilot.md` and inspect the teammate's change:

```sh
git show --stat pilot-draft
```

Expect three changed files. Use sections 1.1 and 1.3 of the notebook to explain your changes.

## Restrict and record

Fix both agents' files: `.claude/settings.json`, `.mcp.json`, and `.codex/config.toml`.

| Problem | Change to make |
|---|---|
| The `case-files` server exposes protected notes. | Remove `.mcp.json` and the Claude Code entries `enabledMcpjsonServers` and `mcp__case-files__*`. Remove Codex's `[mcp_servers.case-files]` section. |
| Edits and pushes can happen without approval. | Remove `Edit(/**)` and `Bash(git push *)` from Claude Code's allow list. Set Codex's `sandbox_mode` to `"read-only"`. |
| Web search is enabled. | Add `WebSearch` to Claude Code's deny list. Set Codex's `web_search` to `"disabled"`. |
| Required approvers are missing. | Replace `TODO` in `docs/pilot.md` with the roles required by the pilot's team and the notebook's “Who decides” list. |

<details><summary>Why each change</summary>

| Problem | The rule, in sections 1.1 and 1.3 |
|---|---|
| The `case-files` server exposes protected notes. | Section 1.1: a coding agent can send out "Whatever it can open". Section 1.3: return information is "Confidential by default", and "A model provider is not on that list". |
| Edits and pushes can happen without approval. | The six settings in section 1.3, row Approvals: the regulated repository gets "All but reads and test runs". |
| Web search is enabled. | The six settings in section 1.3, row Network: the regulated repository gets "Only what the task needs". The pilot downloads nothing. |
| Required approvers are missing. | Section 1.3, the list Who decides. "The use: an accountable agency official." "Contractors: also IRS Cybersecurity and the Contracting Officer." "Yours: a proposal concrete enough for yes or no." |

</details>

Save your changes, then commit and check:

```sh
git add -A
git commit -m "Tighten the agent's configuration for the pilot"
python3 ../check.py
```

Finish when the check prints `Done:`. If it prints `Not yet:`, address the findings, commit, and check again. This checks configuration files; it does not run an agent or prove that a live workstation enforces them.

## Reflect

Why can read-only access to protected notes still disclose them? Who approves the pilot, and what evidence should your proposal give them?

[Worked answer](../answers/agent-boundary/) · [Start over](../../../README.md#start-an-exercise-again)
