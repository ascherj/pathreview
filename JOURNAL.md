# PathReview Contribution Journal

## Week 7 - Issue Selection

**Contributor:** Sharadha Kasiviswanathan  
**GitHub username:** SharadhaK30

**Issue link:** https://github.com/ascherj/pathreview/issues/53  
**Issue title:** Implement a `DependencyAuditTool` that flags outdated major dependencies in project repos

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
I am building a new tool for the AI agent called `DependencyAuditTool`. This tool will check a project's software packages and tell the agent if any packages are outdated or need to be updated. Right now, PathReview can review project content, but it does not have a dedicated agent tool for checking dependency freshness across files like `requirements.txt`, `package.json`, and `pyproject.toml`. A successful fix would add the new tool under `agent/tools/`, connect it to `agent/orchestrator.py`, and allow the agent to include dependency update information in its overall project review.

**Branch name:** `feat/53-dependency-audit-tool`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

**Selection notes / checklist reasoning:**
I chose Issue #53 because it offers a good balance between learning and implementation. It is not just fixing an existing bug; it involves building a new agent tool from scratch while following the project's existing architecture. It also matches my interest in AI-powered developer tools because the feature helps the agent give more useful feedback during project reviews. The issue covers parsing different dependency file formats and checking package versions, and the estimated 5-8 hour scope makes it challenging but manageable for this milestone.
