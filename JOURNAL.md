# Module 3 Journal — PathReview

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/154

**Issue title:** Health check DB probe passes a raw SQL string, which fails under SQLAlchemy 2.x

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `GET /health` endpoint reports PostgreSQL as unavailable even when the
database is perfectly reachable. In `api/routes/health.py`, the database probe
calls `await db.execute("SELECT 1")` — passing a bare Python string. SQLAlchemy
2.x no longer accepts raw textual SQL and requires it to be wrapped in `text()`,
so this call raises an `ArgumentError` instead of running the query. The
surrounding `try/except` catches that error and misinterprets it as a
connectivity failure, marking Postgres `"unhealthy"` and flipping the whole
endpoint to a 503. A successful fix wraps the statement in `sqlalchemy.text()`
so the probe actually executes, letting the endpoint report Postgres as healthy
when it is up — while still correctly reporting unhealthy when the database is
genuinely down.

**Branch name:** fix/154-health-check-raw-sql

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

### "Is this issue right for me?" — selection notes

**Why this issue fits (scope reasoning):**
- **Tier and labels match my level.** It's labeled `tier-1`, `good first issue`,
  and `bug` — the recommended starting point for a first contribution to a large
  codebase.
- **I reproduced it before claiming it.** While setting up my environment,
  `GET /health` returned 503 and the server logged
  `postgres_health_check_failed error="Textual SQL expression 'SELECT 1' should be
  explicitly declared as text('SELECT 1')"`. That is the exact failure described
  in the issue, so I know the bug is real in my environment and I'll be able to
  verify a fix rather than guess at one.
- **The blast radius is small and well understood.** The defect is a single call
  on one line of one file (`api/routes/health.py`), inside a `try/except` that
  already isolates it. The fix is to import `text` from SQLAlchemy and wrap the
  statement — no schema changes, no API contract changes, no cross-module
  refactor, and no architectural decisions to negotiate.
- **Acceptance criteria are unambiguous.** The issue states the expected error and
  the expected behavior, so "done" is objectively testable.

**Scope risk I identified up front:**
The `/health` endpoint currently fails for **two independent reasons**. Besides
this SQL bug, the Redis probe also throws
`'Settings' object has no attribute 'redis_host'`, and the Chroma vector-db
container in `docker-compose.yml` crash-loops on a NumPy 2.0 incompatibility
(`chromadb 0.4.22` uses the removed `np.float_`). Those are **separate problems
and out of scope for #154.** This matters because fixing only the SQL probe may
not by itself turn `/health` green — the endpoint can still return 503 due to the
Redis check. So I will scope my acceptance criteria to the Postgres probe
specifically: the Postgres dependency must report `"healthy"` and the SQLAlchemy
`ArgumentError` must no longer appear in the logs. If I want the endpoint fully
green, that belongs in a separate issue rather than expanding this one.

**Environment setup notes:**
Backing services run via `docker compose` (Postgres on `5433`, Redis on `6379`).
Migrations applied with `alembic upgrade head` and the database seeded via
`scripts/seed_db.py`. Frontend confirmed running at `localhost:5173` (Vite) and
the API at `localhost:8000` (`/docs` returns 200).
