## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/158

**Issue title:** review_service unit tests misconfigure async mocks — 13 of 19 tests fail

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The unit test suite for the review service subsystem is currently broken because the mock database session is returning asynchronous coroutines where synchronous result objects are expected. Specifically, the production code in `core/services/review_service.py` properly awaits `db.execute()`, but the subsequent chained calls to `.scalars().first()` or `.scalars().all()` crash because the test setup incorrectly applies `AsyncMock` to the resulting database response object. This causes 13 out of 19 CRUD tests to fail with an `AttributeError`. A successful fix will reconfigure the test fixtures and mock structures so that `db.execute` correctly returns a synchronous mock object, allowing the existing service assertions to pass without modifying the underlying production logic.

**Selection Notes & Scope Reasoning:**
I selected this issue because it is categorized as Tier 1, meaning it is strictly scoped to a single file (`tests/unit/test_review_service.py`) and does not require complex cross-module architectural updates. As a data professional working with asynchronous testing environments, this is an excellent fit for my current skill level; it allows me to resolve a blocking test environment issue without changing core application workflows.

* **Part 1 — Understanding the Issue:** Verified. I can clearly explain the asynchronous mock regression in plain words. I have located the target test file and confirmed that the explicit goal is to get the 13 failing unit tests passing by matching the mock behavior to what the production CRUD methods expect.
* **Part 2 — Tier Fit:** Verified. This is a Tier 1 issue because it is an isolated, self-contained test environment bug. It is a highly realistic match for orienting myself in the PathReview codebase during the first week of the module.
* **Part 3 — Codebase Readiness:** Verified. I have opened, read, and successfully run the test suite for `tests/unit/test_review_service.py` locally in my environment, reproducing the precise `AttributeError` tracebacks. I understand the mock configuration patterns currently in use.
* **Part 4 — Scope and Time:** Verified. The scope is tight and well-defined, taking an estimated 2–4 hours of focused work. This is perfectly achievable around my ongoing professional and graduate coursework commitments, and there are no external engineering blockers.

**Branch name:** fix/158-review-service-async-mocks
**Setup confirmation:** [x] App runs locally at localhost:5173
**Cohort ledger:** [x] Issue added to cohort ledger