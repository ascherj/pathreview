# Journal

## Week 7 — Issue selection

**Issue link:** [\[Issue-68\]](https://github.com/ascherj/pathreview/issues/68)

**Issue title:** Add a safety event count to the health check endpoint #68

**Tier:** [ x ] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The /health endpoint return service status but no safety metrics. The safety events last hour field. At this time the value is hardcoded to 0 instead of grabbing the actual event count from redis. This will need to be updated.

**Branch name:** fix/68-health-check-safety-event

**Setup confirmation:** [ x ] App runs locally at localhost:5173

**Cohort ledger:** [ x ] Issue added to cohort ledger