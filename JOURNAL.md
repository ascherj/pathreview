## Week 7 — Issue selection

**Issue link:** [github.com/ascherj/pathreview/issues/158](https://github.com/ascherj/pathreview/issues/158)

**Issue title:** review_service unit tests misconfigure async mocks — 13 of 19 tests fail

**Tier:** [Yes ] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The test mocks are set up incorrectly for async database operations. The service code does await
  db.execute(...) and then calls .scalars().first() or .scalars().all() on the result. But the mock returns a coroutine
  object instead of a result object, so when the service tries to call .first() or .all() on it, it crashes with: AttributeError: 'coroutine' object has no attribute 'first'. A root causec is result.scalars() is mocked as an async method (returning a coroutine) when it should be a regular synchronous method returning a mock result object. A possible fix will be to use AsyncMock for db.execute() and a plain MagicMock for the result object — without modifying the service code
  itself.

**Branch name:** fix/158-unit-tests-misconfigure-async-mocks, currently 13 out of 19 tests fail

**Setup confirmation:** [Yes ] App runs locally at localhost:5173

**Cohort ledger:** [Yes ] Issue added to cohort ledger
