# The answer to "Tighten your coding agent's configuration for the extractor's pilot".
# Run it from ~/practice/week-01/day-01/agent-boundary/lab, after python3 ~/practice/reset.py agent-boundary:
#   sh ../../answers/agent-boundary/commands.sh
# It makes the four fixes of the exercise's table, commits them, and runs the check, which prints Done:.
# decisions.md says what each change closes, and what else the check accepts.
set -e
ANSWER="$(cd "$(dirname "$0")" && pwd)"

cp "$ANSWER/claude-settings.json" .claude/settings.json
git rm -q .mcp.json
cp "$ANSWER/codex-config.toml" .codex/config.toml
cp "$ANSWER/pilot.md" docs/pilot.md
git add .claude/settings.json .codex/config.toml docs/pilot.md
git commit -q -m "Tighten the agent's configuration for the pilot"
python3 ../check.py
