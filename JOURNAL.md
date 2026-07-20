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

## Week 8 - Reproduction & solution planning

**Reproduction commit link:** https://github.com/SharadhaK30/pathreview/commit/578d14c5f5ed4b5a2d157c7c160039057a6c1829

**Reproduction summary:**
I reproduced the feature gap by adding a unit test that expects `agent.tools.dependency_audit_tool.DependencyAuditTool` to exist for agent reviews. A direct import check currently fails with `ModuleNotFoundError`, confirming that the dependency audit tool is missing and not yet available to the orchestrator.

**PLAN.md link:** https://github.com/SharadhaK30/pathreview/blob/feat/53-dependency-audit-tool/PLAN.md

**Walkthrough video :** Loom Link attached to Notes section in Project Submission

**Blockers or open questions:**
I need to confirm the best place to source repository dependency file contents for the orchestrator. The main open design choice is whether `DependencyAuditTool` should receive file contents directly from profile data, use output from `github_tool`, or support both so unit tests can stay fast and deterministic.

## Week 9 - Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
I implemented the main `DependencyAuditTool` structure from `PLAN.md` in `agent/tools/dependency_audit_tool.py`. I completed parsers for `requirements.txt`, `package.json`, and `pyproject.toml`, added major-version comparison logic, and connected the orchestrator planning path so `dependency_audit` runs when supported dependency file contents are available.

**Next steps:**
I need to finish self-review, confirm the focused tests pass after the final cleanup, document the repo-wide pre-existing check failures, and submit the PR with the full template completed.

**Blockers:**
The full repo-wide `make check` and `make test-unit` commands still fail because of unrelated pre-existing lint and unit-test failures outside the dependency audit files. The focused dependency audit tests and changed-file lint/format checks pass.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/222

**Branch:** `feat/53-dependency-audit-tool`

**What you built:**
I built a new `DependencyAuditTool` that parses dependency manifests and reports packages that are more than one major version behind a supplied latest-version map. The tool returns structured findings for audited dependencies, outdated dependencies, skipped files, and warnings, and the orchestrator now adds a `dependency_audit` step when supported dependency file contents are present.

**Tests added or updated:**
I updated `tests/unit/test_dependency_audit_tool.py` to cover outdated dependency detection, dependencies only one major version behind, `pyproject.toml` parsing, malformed `package.json`, unsupported files, unpinned requirements, and invalid input handling. I also added `tests/unit/test_orchestrator_dependency_audit.py` to cover when the orchestrator adds or skips the dependency audit plan step.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

**Draft PR feedback received from:** none

**Validation notes:**
Focused validation passed with `.venv/bin/pytest tests/unit/test_dependency_audit_tool.py tests/unit/test_orchestrator_dependency_audit.py -q`, `.venv/bin/ruff check agent/tools/dependency_audit_tool.py agent/orchestrator.py tests/unit/test_dependency_audit_tool.py tests/unit/test_orchestrator_dependency_audit.py`, `.venv/bin/black --check agent/tools/dependency_audit_tool.py agent/orchestrator.py tests/unit/test_dependency_audit_tool.py tests/unit/test_orchestrator_dependency_audit.py`, and `.venv/bin/mypy agent/tools/dependency_audit_tool.py --follow-imports=skip`. Per the assignment guidance on pre-existing failures, the self-review boxes are checked because my changes introduce no new failures; repo-wide `make check` still fails on unrelated existing lint issues, and repo-wide `make test-unit` still fails on unrelated existing unit-test failures while the new dependency audit tests pass.
