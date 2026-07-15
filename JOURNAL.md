## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/155

**Issue title:** Health check references `settings.redis_host`, which does not exist on Settings

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `/health` endpoint appears to read `settings.redis_host`, but that field is not defined on the app’s Settings model. Because of that, the health check can raise an AttributeError before it can report Redis status. A successful fix would make the health endpoint use Redis configuration that actually exists and return health information without crashing.

**Branch name:** fix/155-health-check-redis-settings

**Setup confirmation:** [ ] App runs locally at `localhost:5173`

**Cohort ledger:** [x] Issue added to cohort ledger