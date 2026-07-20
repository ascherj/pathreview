# PathReview Contribution Journal

## Week 7 - Issue Selection

**Contributor:** Sharadha Kasiviswanathan  
**GitHub username:** SharadhaK30

**Issue link:** https://github.com/ascherj/pathreview/issues/53  
**Issue title:** Implement a `DependencyAuditTool` that flags outdated major dependencies in project repos

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
PathReview needs a new agent tool that can inspect dependency files submitted with project repositories and identify packages that are more than one major version behind the current release. Right now, the agent system has tools for reviewing project content, but it does not appear to include a dedicated dependency freshness check across `requirements.txt`, `package.json`, and `pyproject.toml`. A successful fix would add a `DependencyAuditTool` under `agent/tools/`, register it with `agent/orchestrator.py`, and return clear findings that help reviewers spot dependency maintenance risks. This affects the agent tooling layer and likely needs tests around parsing dependency files and handling version comparison edge cases.

**Branch name:** `feat/53-dependency-audit-tool`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

**Selection notes / checklist reasoning:**
I chose this issue because it is clearly scoped to the agent tool system and names the main files involved, which makes the starting point easier to verify in the codebase. It is Tier 2, so it is more involved than a documentation-only or single-test issue, but it still has a concrete outcome: parse dependency manifests, compare major versions, and report outdated packages. The expected effort is 5-8 hours, which feels realistic for Weeks 8 and 9 if I first study the existing `BaseTool` pattern, the orchestrator registration flow, and the current test layout. The main scope risk is dependency version lookup, so I will plan to mock any external package registry responses in tests instead of relying on live network calls.
