## Week 7 — Issue selection

**Issue link:** (https://github.com/ascherj/pathreview/issues/59)

**Issue title:** Add an end-to-end agent test using a fully stubbed tool suite

**Tier:** [ ] Tier 1  [ ] Tier 2  [ x ] Tier 3

**Problem summary:**

The `Orchestrator` class in `agent/orchestrator.py` is the core of the application — it builds a plan, dispatches all five analysis tools, aggregates results, and persists state to Redis — but `tests/integration/` is currently empty, meaning there is zero test coverage of this lifecycle. Any change to the orchestrator, a tool interface, or the session store could silently break the full agent flow without any test catching it. A successful fix adds `tests/integration/test_agent_e2e.py` that exercises the complete run cycle using fully stubbed tools and a dict-backed session store, asserting that the correct tools are called for a given profile, results are aggregated properly, and tool failures are handled gracefully.

**Branch name:** test/59-end-to-end-agent-test

**Setup confirmation:** [ x ] App runs locally at localhost:5173

**Cohort ledger:** [ x ] Issue added to cohort ledger

## Issue Checklist — Is This Issue Right for Me?

### Part 1 — Understanding the Issue

**Can I explain what this issue is asking for in my own words?**
[x] Yes.

Issue #59 asks for an end-to-end integration test for the `Orchestrator` class in `agent/orchestrator.py`. The test must exercise the full agent lifecycle — plan building, tool dispatch, result aggregation, and session persistence — using stub/fake implementations of all five tools (`github_tool`, `tech_detector`, `readme_scorer`, `skill_extractor`, `market_analyzer`) and a stub `SessionStore`, so no real API calls or Redis connections are required. Currently `tests/integration/` exists but is completely empty.

**Do I understand which part of the app is affected?**
[x] Yes.

Relevant files confirmed to exist:
- `agent/orchestrator.py` — subject under test; `run()`, `_build_plan()`, `_execute_tool()`, `_execute_with_timeout()`
- `agent/tools/base.py` — `BaseTool` / `ToolResult` interface the stubs must implement
- `agent/memory/session_store.py` — Redis-backed store that needs a dict-based stub
- `agent/memory/context_manager.py` — used internally by orchestrator for caching
- `agent/error_handling.py` — `retry_with_backoff` wrapping every tool call
- `tests/integration/` — empty; the new test file goes here
- `tests/conftest.py` — fixture patterns to follow

**Do I understand what "done" looks like?**
[x] Yes.

*Before:* `tests/integration/` has only `__init__.py` — zero coverage of the Orchestrator lifecycle.
*After:* `tests/integration/test_agent_e2e.py` containing at minimum: a happy-path test (all five stubs called, full result dict returned), a partial-profile test (`_build_plan` skips tools whose data is absent), a tool-failure test (stub raises, orchestrator catches and returns `{"error": ..., "success": False}`), and a session-persistence test (stub store holds the merged results after `run()`).

---

### Part 2 — Tier Fit

**Is the tier a realistic match for where I am right now?**
[x] Yes — Tier 3 is the correct label and a reasonable choice.

*Scope reasoning:* This issue is not a localized bug or a two-module interaction. Writing the E2E test requires understanding the entire agent subsystem simultaneously: how `_build_plan()` conditionally populates the plan from profile fields, how `_execute_tool()` checks the `ContextManager` cache before calling a tool, how `retry_with_backoff(max_retries=2, backoff_factor=1.5)` wraps execution, how `ToolResult.data` is unwrapped in the results dict, and how `SessionStore.get/set` interacts across the lifecycle. That spans `agent/`, `agent/tools/`, `agent/memory/`, and `agent/error_handling.py` — which is the definition of Tier 3. A Tier 1 test would target a single tool in isolation (several already exist in `tests/unit/`); a Tier 2 test might cover orchestrator + one tool. A fully stubbed suite exercising the complete lifecycle is unambiguously Tier 3.

---

### Part 3 — Codebase Readiness

**Can I find the relevant code?**
[x] Yes — read `orchestrator.py` in full, `base.py`, `session_store.py`, `error_handling.py`, `context_manager.py` (via import inspection), `conftest.py`, and a representative unit test.

**Do I understand the surrounding code well enough to change it safely?**
[x] Yes.

Rough implementation plan (no lookups needed):
1. Define five stub tool classes inheriting `BaseTool` — each has a `name` class attr and `execute()` returning a hardcoded `ToolResult(success=True, data={...})`.
2. Define a `StubSessionStore` using a plain `dict` in place of Redis.
3. Write a pytest fixture that assembles `Orchestrator(tools={...}, session_store=stub_store)`.
4. Construct `profile_data` with all four optional fields populated so all five tools appear in the plan.
5. Assert `results["profile_id"]`, `results["tool_results"]` keys, and that `stub_store` holds the merged data.
6. Add a failure scenario by making one stub's `execute()` raise `RuntimeError` and asserting the error dict shape.

**Have I read the relevant test file?**
[x] Yes — read `tests/unit/test_skill_extractor.py` end-to-end: `@pytest.mark.unit` decorator, `@pytest.fixture` for the object under test, one fixture per class, `assert isinstance(result, ...)` plus domain-specific assertions. The integration test will mirror this pattern with `@pytest.mark.integration`.

---

### Part 4 — Scope and Time

**How many others are already working on this issue?**
[x] Four people have claimed this issue.

**Is the scope realistic for Weeks 8–9?**
[x] Yes. The implementation is self-contained in a single new file (`tests/integration/test_agent_e2e.py`) with no production code changes required. All stubs implement a single abstract method. Estimated 4–6 hours of focused work, well within the Tier 3 upper bound and the two-week window.

**Are there any blockers or dependencies?**
[x] No open blockers or upstream issues referenced in #59.

### Reasoning

Tier 3 is the right fit because the E2E test requires understanding the full agent subsystem at once: how `_build_plan()` conditionally selects tools, how `_execute_tool()` checks the `ContextManager` cache, how `retry_with_backoff` wraps each call, how `ToolResult.data` is unpacked into the results dict, and how `SessionStore` persists state — spanning `agent/`, `agent/tools/`, `agent/memory/`, and `agent/error_handling.py`. Single-tool isolation tests (Tier 1) already exist in `tests/unit/`; this issue specifically requires stitching all five tools and the session layer together, which is what makes it Tier 3.

---

## Initial State - Before working on anything
- Ran unit test suite, 35 failing before any work is done

---

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [link to commit documenting the reproduced issue]

**Reproduction summary:**
Ran `pytest tests/integration -v` and observed `collected 0 items` — the directory contains only `__init__.py` and no tests exist, confirming zero coverage of the Orchestrator lifecycle. Running `pytest tests/unit -v` shows the 35 pre-existing unit failures are unrelated to this issue; the integration gap is entirely the absence of `test_agent_e2e.py`.

**PLAN.md link:** [PLAN.md](./PLAN.md)

**Blockers or open questions:**
None — implementation path is clear going into Week 9.
