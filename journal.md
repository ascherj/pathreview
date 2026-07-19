## Week 7 — Issue selection

**Issue link:** (https://github.com/ascherj/pathreview/issues/54)

**Issue title:** Add a plan validation step that checks tool prerequisites before executing the plan

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
The `Orchestrator` in `agent/orchestrator.py` builds a plan of tools to run based only on what raw profile data is available, then executes them in list order without ever checking whether a tool's actual prerequisites were satisfied first. For example, `market_analyzer` depends on `tech_detector` having already run, and `skill_extractor` depends on ingestion being complete, but nothing today stops a downstream tool from running with missing or failed upstream results. A successful fix adds a DAG-based validation step (a new `agent/tools/tool_dependencies.py`) that runs before execution begins and rejects or reorders any plan where a tool's dependencies aren't satisfied earlier in the plan. This affects the agent/orchestration subsystem specifically, not ingestion or the API layer.

**Scope reasoning ("Is this right for me?"):**
This is a Tier 3 issue, so I checked scope before committing: the fix is localized to two files (`agent/orchestrator.py` and a new `tool_dependencies.py`), the dependency graph is small and explicitly given in the issue (5 tools), and the required approach (DAG validation) is a well-known pattern rather than an open-ended design problem. The estimated 8-12 hours felt achievable, and understanding the orchestrator's plan/execute split first mattered more than the DAG logic itself, which is straightforward once the graph is defined.

**Branch name:** feat/54-plan-validation-tool-prerequisites

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger