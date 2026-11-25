#!/bin/sh
# Every exercise starts from a state the course supplies, never from a learner's earlier work.
# Weeks 1 to 3 were taught before this rule and are kept as taught; every later week is checked.
fail=0
for week in week-*; do
  [ -d "$week" ] || continue
  case "$week" in week-01|week-02|week-03) continue ;; esac
  python3 .github/check_exercise_self_contained.py "$week" || fail=1
done
exit $fail
