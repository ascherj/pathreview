# JOURNAL

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/82

**Issue title:** Concurrent review requests for the same profile can produce inconsistent results

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
When two review requests come in for the same profile at almost the same time, both kick off the agent review loop against whatever profile state is currently in the database, with no coordination between the two runs. If the first request modifies the profile mid-flight, the second loop can still be working from the state it read before that change, so its output doesn't reflect the latest data. The fix is to add a per-profile lock so a second review request for the same profile is serialized behind the first instead of running concurrently against shared state. This mainly touches the review submission endpoint in `api/routes/reviews.py` and the orchestration logic in `core/services/review_service.py`.

**Branch name:** fix/82-concurrent-review-race-condition

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
