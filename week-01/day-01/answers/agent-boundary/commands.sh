# The answer to "Tighten your coding agent's configuration for the extractor's pilot".
# Run it from ~/practice/week-01/day-01/agent-boundary/lab, after python3 ~/practice/reset.py agent-boundary:
#   sh ../../answers/agent-boundary/commands.sh
# It tightens both coding agents' files, as a learner who uses either one tightens that one's;
# decisions.md says why each change is made and what the check also accepts.
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

# Your change, committed before the check shows anything.
cp "$ANSWER/claude-settings.json" .claude/settings.json
git rm -q .mcp.json
cp "$ANSWER/codex-config.toml" .codex/config.toml
git add .claude/settings.json .codex/config.toml
git commit -q -m "Tighten both coding agents' configuration for the pilot"
python3 ../check.py || true    # Not yet: one line, about the sign-off in docs/pilot.md

# The sign-off, named, then the check.
cp "$ANSWER/pilot.md" docs/pilot.md
git add docs/pilot.md
git commit -q -m "Name who must agree before the agent runs in the pilot"
python3 ../check.py
