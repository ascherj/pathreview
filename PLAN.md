# Solution plan

**Issue:** [Agent state isn't persisted across API restarts, causing in-progress reviews to be lost (#47)](https://github.com/ascherj/pathreview/issues/47)

## Understand

**Root cause:** `Orchestrator.run()` in `agent/orchestrator.py` loaded prior
session state from Redis at the top of the method, but never consulted it
inside the tool-execution loop. Every tool in the plan ran unconditionally on
every call, regardless of whether a previous run had already completed it.
On top of that, the merged results were only written back to Redis once,
after the entire loop finished (`session_state.update(results)` +
`self.session_store.set(...)` sat *after* the `for` loop, not inside it).

**Expected behavior:** if the API process restarts mid-review, a fresh
`Orchestrator.run()` call for the same `profile_id` should skip tools that
already succeeded and only execute the tools that hadn't finished yet.

**Actual behavior (pre-fix):** a restart mid-review loses all progress. Even
in the narrow window where a full run *did* complete and got persisted, a
second call would still re-execute every tool from scratch, because nothing
in the loop ever read from the loaded `session_state` — it only used it as
the base dict to `.update()` at the very end.

## Map

- `agent/orchestrator.py` — `Orchestrator.run()` (the tool-execution loop and
  the checkpoint write) is the primary fix location.
- `agent/memory/session_store.py` — `SessionStore.get()` / `SessionStore.set()`,
  the Redis-backed store the orchestrator reads/writes. No behavior change
  needed here, but its `dict | None` return shape is what `run()` has to
  handle correctly (missing type annotations here were also blocking the
  mypy pre-commit hook on any orchestrator change).
- `agent/memory/context_manager.py` — imported by `orchestrator.py`; needed
  type-annotation fixes for the same pre-commit reason.
- `agent/error_handling.py` — `retry_with_backoff`, used by
  `_execute_with_timeout`; same pre-commit blocker.
- `tests/unit/test_orchestrator.py` — new test file; simulates a restart by
  constructing two `Orchestrator` instances that share one `session_store`.

## Plan

1. Load the previous session state at the top of `run()` (already existed)
   and, inside the tool loop, check per-tool whether `results.get(tool_name)`
   already holds a successful result. If so, log `tool_resumed_from_checkpoint`
   and `continue` instead of re-executing.
2. Treat a previously *failed* tool (`{"success": False, ...}`) as not-done,
   so it gets retried rather than skipped.
3. Move the `self.session_store.set(profile_id, results)` call inside the
   loop, immediately after each tool's result (success or failure) is
   recorded, so a crash between tool N and N+1 only loses the in-flight
   tool, not everything.
4. Add regression tests that simulate the exact restart scenario: run an
   `Orchestrator` through a partial plan, construct a second `Orchestrator`
   sharing the same `session_store`, and assert already-completed tools are
   not re-invoked (`tool.execute.call_count`) while incomplete/failed ones
   are.
5. Fix the missing type annotations in `error_handling.py`,
   `context_manager.py`, and `session_store.py` that were otherwise blocking
   the mypy pre-commit hook on this change.

## Inputs & outputs

- **Input:** `profile_id: str`, `profile_data: dict` (drives `_build_plan`),
  and whatever `self.session_store.get(profile_id)` returns — either `None`
  (no prior run) or a `dict` mapping `tool_name -> result` from an earlier,
  possibly-interrupted run.
- **Output:** an incrementally-updated Redis entry at `session:{profile_id}`
  (one `setex` call per completed tool, TTL 3600s), and the same return
  shape `run()` always produced: `{"profile_id", "tool_results", "cached_results"}`.

## Risks & unknowns

- `SessionStore.set()` round-trips through `json.dumps`/`json.loads`
  (`agent/memory/session_store.py:61`), so any tool result that isn't
  JSON-serializable would silently fail to persist (the `except Exception`
  there only logs). Not currently an issue with existing tools, but a new
  tool returning something like a `datetime` would break checkpointing
  quietly.
- "Already done" is inferred from dict shape
  (`previous.get("success") is False` means retry, anything else means
  skip) — a tool that returns a truthy dict without a `success` key on
  partial failure would be incorrectly treated as complete.
- The Redis TTL is a fixed 3600s (`session_store.py:56`). A review that
  stays interrupted for longer than an hour loses its checkpoints entirely,
  which the fix doesn't address — resuming from a very stale restart still
  reverts to running everything.
- No coverage for two orchestrator instances processing the same
  `profile_id` concurrently (race on the Redis key) — not a scenario the
  current single-worker deployment hits, but worth flagging if that changes.

## Edge cases

- All tools in the plan already have successful results in
  `session_store` → `run()` should execute nothing and just return the
  cached results.
- A tool previously recorded `{"success": False, ...}` → must be retried,
  not skipped.
- `session_store` is `None` (persistence not configured) → behavior must be
  unchanged from before the fix: every tool executes, nothing is checkpointed,
  no exception raised.
- `profile_data` changes between the interrupted run and the resumed run
  (e.g., a project's `github_repo` changes), so `_build_plan` produces a
  tool name that isn't a key in the old `results` dict → treated as not-done
  and executed normally, since `results.get(tool_name)` returns `None`.
- Redis returns corrupted/non-JSON data on `get()` → already handled by
  `SessionStore.get()`'s `except json.JSONDecodeError: return None`, so the
  orchestrator falls back to running everything rather than crashing.
