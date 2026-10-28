# Exercise: Tighten your coding agent's configuration for the extractor's pilot

Tighten your coding agent's configuration for a repository that could reach return information: the extractor's pilot.

**Scenario:** A teammate configured both coding agents for the extractor's pilot, on a workstation that reaches real notes, saying it follows section 1.3's regulated column. From: GitHub's Secure Code Game (https://github.com/skills/secure-code-game) and the chapter's case-notes extractor.

**Success criterion:** from `lab`, `python3 ../check.py` prints `Done:`. Once your change is committed, the check reads each changed agent's files without starting the agent, and lists what they still let it reach or do that `docs/pilot.md` and section 1.3 rule out.

**Where you work:** VS Code in your hosted workspace: your coding agent's files in `lab` (Claude Code: `.claude/settings.json`, `.mcp.json`; Codex: `.codex/config.toml`), `docs/pilot.md`, and the terminal inside `lab`. AI tools: none.

**Start from:** the folder `agent-boundary`: `python3 ~/practice/reset.py agent-boundary`, which prints `agent-boundary is back as it was supplied.`; then `cd ~/practice/week-01/day-01/agent-boundary/lab`. To get it again: the same reset; it removes your commits.

**What you have:** in `lab`, the extractor's repository, the teammate's commit tagged `pilot-draft`; `docs/pilot.md`, the pilot's facts and the pages documenting each agent's files; `../check.py`, the check. The week 1 chapter, section 1.3, "Tighten the defaults where a repository could reach return information": remove "the combinations that would let a bad choice do damage".

## Steps

1. See what you start from: `git log --oneline -3`, `git show --stat pilot-draft` and `docs/pilot.md`. You should see: the teammate's commit, changing three files.
2. Decide before the check does: in your coding agent's files, change whatever lets it reach or do, asked or not, what the pilot's facts and section 1.3 rule out (the pages `docs/pilot.md` lists explain each setting), keeping edits with your yes and test runs. Commit; run `python3 ../check.py`. You should see: `Not yet:` and what is left.
3. Close what is left; commit; run the check. You should see: `Not yet:` and one line, about `docs/pilot.md`.
4. Name the sign-off on the last line of `docs/pilot.md`: who must agree before the agent runs there, in section 1.3's words. Commit; run the check. You should see: `Done:`.

**Answer:** `~/practice/week-01/day-01/answers/agent-boundary/`: both agents' files, `decisions.md` (each change's rule; what else the check accepts) and `commands.sh`, ending `Done:`.

## Afterwards, together

Beside `decisions.md`, what had your first commit closed? Which setting looked closed and was not? What could a developer's own settings still undo? Who must sign off, and why?
