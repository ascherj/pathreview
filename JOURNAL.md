# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/117

**Issue title:** API docs don't include example `curl` commands

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The API reference explains which PathReview endpoints exist, but it does not give copy-pasteable `curl` examples for testing them from the command line. This makes first-time setup harder because a contributor can see routes like `/health`, `/auth/register`, `/auth/login`, `/profiles`, and `/reviews`, but cannot quickly verify that the local API is responding correctly. The issue affects `docs/API.md`, which currently lists the base URL and endpoint descriptions. A successful fix would add clear `curl` examples with sample request bodies and authorization-header placeholders so developers can test the API during local development.

**Selection notes / “Is this right for me?” checklist reasoning:**
I chose this issue because it is Tier 1, documentation-focused, and scoped to one file: `docs/API.md`. The issue describes the missing behavior clearly and estimates the work at 2–3 hours, so the scope feels realistic for a first contribution. I should be able to validate the work by running the app locally, checking the API at `localhost:8000`, and trying the new `curl` examples against the dev server. The risk is low because the fix should not require backend logic changes, database schema changes, or frontend state changes.

**Branch name:** docs/117-add-api-curl-examples

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
