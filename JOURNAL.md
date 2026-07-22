## Week 7 — Issue selection

**Issue link:** [https://github.com/ascherj/pathreview/issues/155#issuecomment-4976060218]

**Issue title:** [Health check references settings.redis_host, which does not exist on Settings #155]

**Tier:** [X] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
[The /health endpoint in api/routes/health.py fails during runtime because it attempts to access a non-existent redis_host attribute on the Settings model. When a GET /health request is received, the handler immediately raises an AttributeError instead of completing its status check. This occurs because core/config.py does not declare redis_host within the application configuration schema. Resolving this issue requires defining the redis_host field in the Settings model so the health probe can properly inspect and report Redis connection health without crashing.]

**Branch name:** [fix/155-health-endpoint-attribute-error]

**Setup confirmation:** [X] App runs locally at localhost:5173

**Cohort ledger:** [X] Issue added to cohort ledger