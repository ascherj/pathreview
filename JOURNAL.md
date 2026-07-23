## Week 7 — Issue selection & setup

**Selected issue:** Health check references settings.redis_host, which does not exist on Settings ([Issue #155](https://github.com/ascherj/pathreview/issues/155))

**Branch:** fix/155-health-check-settings-mismatch

**Setup summary:**
- Confirmed local environment and branch setup for issue work.
- Identified validation commands from project docs (`make check`, `make test-unit`, targeted unit tests).

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [0a19d44](https://github.com/lovlynia/pathreview/commit/0a19d44)

**Reproduction summary:**
I reproduced the issue by tracing `api/routes/health.py` against `core/config.py` and confirming the old health check logic expected `settings.redis_host`/`settings.redis_port` while `Settings` provides `redis_url`. This mismatch causes the Redis probe path to fail and marks the health endpoint as unhealthy (HTTP 503).

**PLAN.md link:** [PLAN.md](PLAN.md)

**Walkthrough video (recommended):** [add Loom link, <=2 min]

**Blockers or open questions:**
- Need to verify whether any integration tests rely on the old Redis host/port behavior.
- Full-repo checks include unrelated baseline failures that should be called out separately from this issue scope.
