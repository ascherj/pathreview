# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/68

**Issue title:** Add a safety event count to the health check endpoint

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**

The `/health` API endpoint currently reports the status of the application's services, but it does not include information about recent safety system activity. The safety monitoring module already handles safety-related events, but that information is not exposed through the health check response. This issue affects the health endpoint in `api/routes/health.py` and the monitoring logic in `safety/monitoring.py`. A successful fix will calculate the number of safety events recorded during the last hour and return that number in a new `safety_events_last_hour` response field.

**Selection notes — “Is this right for me?” checklist:**

I selected this issue because it is labeled Tier 1 and is estimated to take approximately two to four hours. The issue has a focused scope and identifies the two main files that are likely to require changes. I have previous experience working with Python APIs, backend routes, validation logic, and tests, so the issue matches skills I have practiced in earlier projects. The expected result is also specific and testable: the `/health` response should contain a safety event count for the previous hour.

**Branch name:** `fix/68-safety-event-health-count`

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
