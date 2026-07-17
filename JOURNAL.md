## Week 7 — Issue selection

**Issue link:** [https://github.com/ascherj/pathreview/issues/82]

**Issue title:** [Concurrent review requests for the same profile can produce inconsistent results - #82]

**Tier:** [ ] Tier 1  [ ] Tier 2  [ X ] Tier 3

**Problem summary:**
<!-- [In 3–5 sentences, in your own words: what the issue is (not a copy-paste of
the title), what is currently broken or missing, and what a successful fix
would accomplish. Naming the part of the codebase it affects is helpful context.] -->

This issue is a race condition that occurs when a user submits two review requests for the same profile at the same time. Both requests trigger the agent loop against the same profile state, so the second agent loop can end up reading data that the first loop has already modified, since there is nothing preventing the two loops from overlapping. This produces inconsistent review results for the profile. The fix is to add a per-profile lock (mutex) in the review submission flow so that concurrent requests for the same profile are serialized rather than processed in parallel. This affects the review submission endpoint in `api/routes/reviews.py` and the review creation logic in `core/services/review_service.py`.

**Is this issue right for me? Scope reasoning:**

I can explain the problem and the expected behavior in my own words without rereading the issue, as shown in the problem summary above. The affected area is the API layer, and the issue is labeled as an enhancement. The relevant files are `api/routes/reviews.py`, `core/services/review_service.py`, and the corresponding test file `tests/unit/test_review_service.py`, all of which I have located and confirmed exist in the codebase. Done looks like a per-profile mutex that serializes concurrent review requests for the same profile, so a second request for a profile that already has a review in progress waits for the first to complete instead of racing against it and producing inconsistent results.

I am treating Tier 3 as a realistic fit given my current experience. I work as an Associate Developer Co-op at IBM on microservice architectures for banking clients, so I am comfortable navigating and modifying industry sized codebases under concurrency constraints. I have read through the relevant route handler, service logic, and existing unit tests closely enough to sketch a rough implementation plan without needing to look anything up further. The scope feels realistic for the Week 8 to 9 window given the estimated six to nine hour effort, and I have checked the issue for blockers or dependencies on other unresolved issues and found none.

**Branch name:** `fix/82-concurrent-review-locking`

**Setup confirmation:** [ X ] App runs locally at localhost:5173

**Cohort ledger:** [ X ] Issue added to cohort ledger