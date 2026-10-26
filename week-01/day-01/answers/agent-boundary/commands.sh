# The answer to "Probe the lab's agent boundary, then propose the regulated one".
# Run it from ~/practice/week-01/day-01/agent-boundary/lab, after
# python3 ~/practice/reset.py agent-boundary
# The probe is typed into Claude Code by you; its expected result: Claude Code tries the command and
# reports "Permission to use Bash with command curl -sI https://example.com has been denied."
# The proposal filled in: the file as supplied, with every TODO written.
cp ~/practice/week-01/day-01/answers/agent-boundary/boundary-proposal.md docs/boundary-proposal.md
python3 ../check.py
