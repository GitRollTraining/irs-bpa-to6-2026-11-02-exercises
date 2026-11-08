# Task Plan: Show "Review first" on the case list for scores of 50 or more

Use this file as the durable roadmap for the task. Create it before complex work and keep it current as phases change.

## Goal

State the intended end result in one clear sentence.

On the case list page (`/`), every case whose selection score is 50 or more shows the words "Review first" next to it, no other case does, and all pytest tests pass.

## Next Step

Record the single action that should happen next. Update it whenever the active phase or immediate action changes.

None: all phases complete. Optional: look at `/` in a browser to judge the label's styling.

## Current Phase

Name the phase currently being worked on.

Phase 5 (complete)

## Phases

Break the task into three to seven verifiable phases. Use only `pending`, `in_progress`, or `complete` for each status and update the value when work advances.

### Phase 1: Requirements & Discovery

- [x] Understand user intent
- [x] Identify constraints and requirements
- [x] Document findings in findings.md
- **Status:** complete

### Phase 2: Planning & Structure

- [x] Define technical approach
- [x] Record the baseline: run `pytest` before any change (11 passed)
- [x] Document decisions with rationale
- **Status:** complete

### Phase 3: Implementation

- [x] Write tests first: score 49 is not flagged, 50 is; the list page shows "Review first" only on flagged rows (2 failed before the code, as expected)
- [x] Add `review_first` to `case_view` in `cases.py` (threshold constant `REVIEW_FIRST_SCORE = 50`)
- [x] Show the words in the Case cell of `templates/list.html` (style `.flag` in `templates/base.html`)
- [x] Run `pytest` after each change
- **Status:** complete

### Phase 4: Testing & Verification

- [x] Verify all requirements met (page test also asserts the data has at least one flagged and one unflagged case)
- [x] Document test results in progress.md
- [x] Fix any issues found
- **Status:** complete

### Phase 5: Delivery

- [x] Review all output files
- [x] Ensure deliverables are complete
- [x] Deliver to user
- **Status:** complete

## Key Questions

Record important questions and replace them with answers as they are resolved.

1. Is 50 itself included? Yes: "50 or more" means `score >= 50`.
2. Where exactly is "next to each case"? In the Case column cell, after the case number link. No new column, so the existing header test stays valid.

## Decisions Made

Record significant choices and the reason for each one.

| Decision | Rationale |
|----------|-----------|
| Compute the flag in `cases.case_view`, not in the template | `cases.py` holds every computed value and is unit-tested; the 49/50 boundary can be tested without the data file |
| Named constant `REVIEW_FIRST_SCORE = 50` | The threshold is a business rule; one place to change it |
| Words go in the Case cell, no new column | "Next to each case"; keeps the table header unchanged |
| Planning files written by copying the shipped templates | `init-session.sh` needed an approval this session did not have; the skill's fallback is to copy the templates exactly; native validation (`check-complete.sh --validate`) unavailable for the same reason |

## Errors Encountered

Record each distinct error, the attempt number, and the resolution. Change the approach before retrying a failed action.

| Error | Attempt | Resolution |
|-------|---------|------------|
| `sh .agents/skills/planning-with-files/scripts/init-session.sh` refused: "This command requires approval" | 1 | Did not retry; copied the three templates by hand per the skill's fallback |

## Notes

- Update phase status as work progresses: `pending` to `in_progress` to `complete`.
- Re-read the goal and next step before major decisions.
- Log errors promptly so failed approaches are not repeated.
