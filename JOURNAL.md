# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/154

**Issue title:** Health check DB probe passes a raw SQL string, which fails under SQLAlchemy 2.x

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `/health` endpoint's PostgreSQL probe in `api/routes/health.py` runs
`await db.execute("SELECT 1")`, passing the query as a bare Python string.
SQLAlchemy 2.x no longer accepts raw textual statements and raises an
`ArgumentError` telling you to wrap them in `text()`. Because the health
handler catches that exception, Postgres gets reported as `unhealthy` and the
endpoint returns a 503 even when the database is actually up and reachable — a
false-negative outage. A successful fix wraps the query with
`sqlalchemy.text()` (`db.execute(text("SELECT 1"))`) so the probe runs, the
endpoint reports accurate database status, and monitoring stops firing on a
healthy DB. The change is confined to the API module's health route and its
accompanying unit test.

**Branch name:** fix/154-health-check-sql-text

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

---

### Selection notes — "Is this right for me?" reasoning

- **Scope is tiny and localized.** The fix is one import plus one line in a
  single file (`api/routes/health.py`), plus a unit test — no sprawling change.
- **No cross-module knowledge required.** It lives entirely in the API module;
  I don't need to understand the RAG, agent, or ingestion pipelines to fix it.
- **Well-defined bug with a standard, known fix.** SQLAlchemy 2.x's `text()`
  requirement is documented behavior, so there's little ambiguity about the
  correct solution.
- **Reproducible and testable without secrets.** It can be exercised via a unit
  test against a DB session and doesn't depend on the `OPENROUTER_API_KEY` or
  any external AI service.
- **Correct difficulty match.** Labeled `good first issue` + `tier-1`, which
  fits a first contribution to a large codebase.
