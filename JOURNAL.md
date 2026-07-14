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

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/jamespaek1/pathreview/commit/77b7e515ab14ddee9695bb3f0117a5b2a10e03ae

**Reproduction summary:**
I reproduced issue #117 as a documentation gap by inspecting `docs/API.md` and confirming that it lists the local API endpoints but does not include any copy-pasteable `curl` commands. I also traced the relevant FastAPI route files to confirm the expected request formats for health, auth, profile, and review endpoints before planning the docs update.

**PLAN.md link:** https://github.com/jamespaek1/pathreview/blob/docs/117-add-api-curl-examples/PLAN.md

**Walkthrough video (recommended):** Not recorded yet.

**Blockers or open questions:**
I need to decide whether to include `GET /reviews/{review_id}/status`, which exists in the route code but is not currently listed in `docs/API.md`, or keep the first docs update limited to the endpoints already documented.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
I implemented the main documentation update in `docs/API.md`. The API reference
now includes copy-pasteable `curl` examples for health checks, registration,
login, profile creation/retrieval/deletion, and review creation/retrieval/listing.
I also documented the required content types, bearer-token header, and reusable
profile and review ID placeholders.

**Next steps:**
I will run every example against the local API, run `make check` and
`make test-unit`, request feedback on the existing pull request, and make any
clarifications identified during testing or review.

**Blockers:**
None currently.

---

### Check-in 2 (end of week)

**PR link:** [add final PR link]

**Branch:** `docs/117-add-api-curl-examples`

**What you built:**
[Complete before submission.]

**Tests added or updated:**
[Complete before submission.]

**Self-review confirmation:** [ ] make check passes  [ ] make test-unit passes

**Draft PR feedback received from:** [name, Discord handle, or "none"]