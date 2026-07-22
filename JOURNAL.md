# PathReview Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/88

**Issue title:** POST /reviews endpoint has no test for when the profile has no ingested documents

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
`tests/unit/test_review_routes.py` doesn't exist yet, so there is no route-level
test coverage for `POST /reviews` at all, including the case where a profile
has no ingested content. While tracing the code (`api/routes/reviews.py`,
`core/services/review_service.py`), I found that the endpoint doesn't actually
validate document presence anywhere: `create_review` always creates a
`status="pending"` review and returns 200 regardless of the profile's state,
and the background `process_review` pipeline produces placeholder feedback
and marks the review "complete" even when zero sources were ingested. A
successful fix for this ticket, scoped narrowly, is a test that documents
this real current behavior for a profile with no ingested sources; adding an
actual error response for that case would be a separate, larger change to
the route/service layer.

**Branch name:** test/88-review-no-ingested-documents

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
