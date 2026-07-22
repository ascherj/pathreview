## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/155
**Issue title:** Health check references settings.redis_host, which does not exist on Settings

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `/health` endpoint in `api/routes/health.py` tries to connect to Redis using `settings.redis_host` and `settings.redis_port`, but `core/config.py` only defines a single `redis_url` field — it never defines separate host/port fields. This causes an `AttributeError` every time the Redis check runs, which is caught by the endpoint's exception handling and silently reported as `"redis": "unhealthy"`, so the health check always fails on Redis even when Redis is running fine. A successful fix would update the Redis check to use the existing `redis_url` field (either by parsing it or connecting via `redis.from_url()`) so the health check accurately reflects Redis's real status.

**Scope reasoning ("Is this right for me?" checklist):**
I chose issue #155 because it's a well-scoped Tier 1 fix: the bug is isolated to a single function (`health_check` in `api/routes/health.py`), the root cause is already clear from reading the code (two undefined config fields), and the fix doesn't require touching other modules or understanding unfamiliar business logic. It's also easy to verify locally — I can call `GET /health` before and after the fix and see the Redis status change. Since this is my first time contributing to a large codebase, this level of contained, single-function scope felt like the right entry point rather than something involving multiple files or unclear requirements.

**Branch name:** fix/155-health-check-redis-host

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/sandhya8109/pathreview/commit/53b4444a1a9e50870aa0875db85b7cc3f0955cf6

**Reproduction summary:**
Ran the app locally and called `GET http://localhost:8000/health`. The response returned a 503 with `"redis": "unhealthy"`, and the Uvicorn logs confirmed the exact root cause: `redis_health_check_failed error="'Settings' object has no attribute 'redis_host'"` — matching the issue exactly. (Note: `postgres` also showed unhealthy in this run, but that's a separate, unrelated SQLAlchemy 2.x text() issue — not part of #155.)

**PLAN.md link:** 
https://github.com/sandhya8109/pathreview/blob/fix/155-health-check-redis-host/PLAN.md

**Walkthrough video (recommended):** [optional — skip or add later]

**Blockers or open questions:**
Need to confirm whether other files in the codebase also reference `settings.redis_host`/`settings.redis_port` besides `health.py`, and haven't yet located the test file for this route.