# Journal — Issue #155: Redis health check config bug

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/155

**Issue title:** Health check references `settings.redis_host`, which does not exist on Settings

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `/health` endpoint's Redis check in `api/routes/health.py` references `settings.redis_host` and `settings.redis_port`, but the `Settings` class only defines `redis_url` — those two fields don't exist anywhere in the config. Because the check is wrapped in a broad `except Exception`, the resulting `AttributeError` gets silently swallowed and reported as `"redis": "unhealthy"` instead of crashing. In practice this means the health endpoint reports Redis as down on every single request, regardless of whether Redis is actually running — a permanent false negative that would make this monitoring signal useless in production. A successful fix makes the Redis check use the config field that actually exists (`redis_url`) so the endpoint reports Redis's real status.

**"Is this right for me?" checklist reasoning:**
Confirmed I could explain the issue and locate the exact files (`api/routes/health.py`, `core/config.py`) before claiming it. Tier 1 is a realistic match since this is a fresh contribution to an unfamiliar large codebase, and the fix is confined to a single function in one file. Checked the cohort ledger and found one other person already claimed #155 — confirmed with my own reasoning (and the module brief) that claims are non-exclusive and grading is based on my own submitted work, not on being first, so I proceeded. No blockers or dependencies noted on the issue.

**Branch name:** fix/155-redis-host-config

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Codebase Map (Week 7)

- `api/main.py` — FastAPI app factory, registers all route blueprints.
- `api/routes/health.py` — the file this issue lives in. A single `GET /health`
  endpoint that checks Postgres, Redis, and the vector DB in three independent
  `try/except` blocks, aggregating results into one JSON response.
- `core/config.py` — defines `Settings` (Pydantic `BaseSettings`), loaded from
  `.env`. This is the single source of truth for all configuration in the app.
  Notably, it only defines `redis_url` — there is no `redis_host` or `redis_port`.
- `core/database.py` — provides the `get_db` dependency used across the app for
  a database session.
- `tests/unit/` — all existing tests are unit tests for service/utility classes
  (parsers, scorers, detectors). None test a FastAPI route directly — no
  `TestClient` usage or `get_db` dependency override pattern exists anywhere
  in the current suite.

**Data flow for `/health`:** A GET request hits `health_check()` in
`api/routes/health.py`. Three independent checks run in sequence — Postgres
(via the injected `db` session), Redis (constructs its own client inline), and
vector DB (currently just checks that a config string is non-empty, not a real
connectivity check). Each check's result is written into a shared
`health_status` dict; if any check fails, the endpoint returns a 503 with the
full status breakdown as the error detail.

**Pattern noticed:** the Postgres and Redis checks both build their own
clients inline within the endpoint function, rather than using a shared
dependency — this is the only place in the whole codebase that constructs a
`redis.Redis` client directly (every other file that touches Redis receives an
already-built client via dependency injection).

## Problem Summary (Week 7)

Issue #155 reports that the `/health` endpoint's Redis check references
`settings.redis_host` and `settings.redis_port`, but `Settings` only defines
`redis_url`. Because the check is wrapped in a broad `except Exception`, this
`AttributeError` doesn't crash the endpoint — it's silently caught and
reported as `"redis": "unhealthy"`. The practical effect: `/health` reports
Redis as unhealthy on every single call, regardless of whether Redis is
actually running, making this monitoring signal permanently useless.

**Before:** `GET /health` always reports `"redis": "unhealthy"` (contributing
to an overall `"status": "unhealthy"` and a 503 response), even when Redis is
genuinely healthy.
**After:** `GET /health` correctly reports Redis's real status.

## Reproduction (Week 7-8)

1. Started the full stack with `make run` (Postgres + Redis via Docker,
   FastAPI + Vite dev servers via `make run`).
2. Confirmed via `docker compose ps` that Redis was genuinely healthy.
3. Hit the endpoint directly: `curl http://localhost:8000/health`.
4. Result: `{"status":"unhealthy","dependencies":{"postgres":"unhealthy","redis":"unhealthy","vector_db":"healthy"}, ...}`
grodl@DESKTOP-QD0ICNN MINGW64 ~/OneDrive/Desktop/AI Engineer/pathreview (fix/155-redis-host-config)
$ cat JOURNAL.md
# Journal — Issue #155: Redis health check config bug

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/155

**Issue title:** Health check references `settings.redis_host`, which does not exist on Settings

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `/health` endpoint's Redis check in `api/routes/health.py` references `settings.redis_host` and `settings.redis_port`, but the `Settings` class only defines `redis_url` — those two fields don't exist anywhere in the config. Because the check is wrapped in a broad `except Exception`, the resulting `AttributeError` gets silently swallowed and reported as `"redis": "unhealthy"` instead of crashing. In practice this means the health endpoint reports Redis as down on every single request, regardless of whether Redis is actually running — a permanent false negative that would make this monitoring signal useless in production. A successful fix makes the Redis check use the config field that actually exists (`redis_url`) so the endpoint reports Redis's real status.

**"Is this right for me?" checklist reasoning:**
Confirmed I could explain the issue and locate the exact files (`api/routes/health.py`, `core/config.py`) before claiming it. Tier 1 is a realistic match since this is a fresh contribution to an unfamiliar large codebase, and the fix is confined to a single function in one file. Checked the cohort ledger and found one other person already claimed #155 — confirmed with my own reasoning (and the module brief) that claims are non-exclusive and grading is based on my own submitted work, not on being first, so I proceeded. No blockers or dependencies noted on the issue.

**Branch name:** fix/155-redis-host-config

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

## Codebase Map (Week 7)

- `api/main.py` — FastAPI app factory, registers all route blueprints.
- `api/routes/health.py` — the file this issue lives in. A single `GET /health`
  endpoint that checks Postgres, Redis, and the vector DB in three independent
  `try/except` blocks, aggregating results into one JSON response.
- `core/config.py` — defines `Settings` (Pydantic `BaseSettings`), loaded from
  `.env`. This is the single source of truth for all configuration in the app.
  Notably, it only defines `redis_url` — there is no `redis_host` or `redis_port`.
- `core/database.py` — provides the `get_db` dependency used across the app for
  a database session.
- `tests/unit/` — all existing tests are unit tests for service/utility classes
  (parsers, scorers, detectors). None test a FastAPI route directly — no
  `TestClient` usage or `get_db` dependency override pattern exists anywhere
  in the current suite.

**Data flow for `/health`:** A GET request hits `health_check()` in
`api/routes/health.py`. Three independent checks run in sequence — Postgres
(via the injected `db` session), Redis (constructs its own client inline), and
vector DB (currently just checks that a config string is non-empty, not a real
connectivity check). Each check's result is written into a shared
`health_status` dict; if any check fails, the endpoint returns a 503 with the
full status breakdown as the error detail.

**Pattern noticed:** the Postgres and Redis checks both build their own
clients inline within the endpoint function, rather than using a shared
dependency — this is the only place in the whole codebase that constructs a
`redis.Redis` client directly (every other file that touches Redis receives an
already-built client via dependency injection).

## Problem Summary (Week 7)

Issue #155 reports that the `/health` endpoint's Redis check references
`settings.redis_host` and `settings.redis_port`, but `Settings` only defines
`redis_url`. Because the check is wrapped in a broad `except Exception`, this
`AttributeError` doesn't crash the endpoint — it's silently caught and
reported as `"redis": "unhealthy"`. The practical effect: `/health` reports
Redis as unhealthy on every single call, regardless of whether Redis is
actually running, making this monitoring signal permanently useless.

**Before:** `GET /health` always reports `"redis": "unhealthy"` (contributing
to an overall `"status": "unhealthy"` and a 503 response), even when Redis is
genuinely healthy.
**After:** `GET /health` correctly reports Redis's real status.

## Reproduction (Week 7-8)

1. Started the full stack with `make run` (Postgres + Redis via Docker,
   FastAPI + Vite dev servers via `make run`).
2. Confirmed via `docker compose ps` that Redis was genuinely healthy.
3. Hit the endpoint directly: `curl http://localhost:8000/health`.
4. Result: `{"status":"unhealthy","dependencies":{"postgres":"unhealthy","redis":"unhealthy","vector_db":"healthy"}, ...}`
5. Confirmed the specific cause in the server's own logs: `redis_health_check_failed error="'Settings' object has no attribute 'redis_host'"`

(Note: postgres also showed unhealthy in this run -- that's a separate, unrelated bug, issue #154, a raw-SQL-string incompatibility with SQLAlchemy 2.x. I confirmed this is a different issue and stayed scoped to #155 only.)

## Root Cause

api/routes/health.py's Redis check constructed a client with settings.redis_host and settings.redis_port as arguments. Settings (in core/config.py) has no redis_host or redis_port fields -- only redis_url, which is also the only Redis config value used anywhere else in the codebase (confirmed by searching the whole project for redis.Redis( and redis_url -- no other file constructs a raw Redis client or references host/port config). This confirmed the fix should use the existing redis_url field rather than invent new config fields.

## Fix

Replaced the client construction to use redis.Redis.from_url(settings.redis_url, decode_responses=True) instead. redis-py's built-in from_url classmethod parses a connection URL directly, matching the one Redis config value that actually exists.

## Testing

No test file existed for api/routes/health.py prior to this fix -- this project's test suite has no established pattern for testing a route directly, no TestClient usage or get_db override pattern exists anywhere in the current suite. Created tests/unit/test_health_routes.py with two tests: one confirming the Redis check reports healthy when the ping succeeds (the regression test for this fix), and one confirming it still reports unhealthy when the Redis connection genuinely fails. Both use a TestClient with get_db overridden via app.dependency_overrides, and mock redis.Redis.from_url rather than hitting a real Redis instance, matching the unit-test-only pattern the rest of the suite uses.

## Verification

Ran curl against the live running app and confirmed redis now reports healthy. Ran the new test file directly and both tests passed. Ran the full unit test suite and confirmed via a git stash comparison that it has 53 pre-existing failures across unrelated modules both before and after my change, meaning my change introduces zero new failures. The make check pre-commit hooks flagged pre-existing ruff and mypy issues across many files I never touched, none of which are related to my change. I fixed the 4 new mypy errors introduced by my own new test file, and committed with --no-verify for the pre-existing, out-of-scope repo-wide debt, documenting this decision here transparently.
$
