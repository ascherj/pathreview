# PathReview: Concurrent Review Locking Fix (#82)

## Current Status

**Issue:** Concurrent review requests for the same profile produce inconsistent results (#82)

**Branch:** `fix/82-concurrent-review-locking`

**Progress:** Bug reproduced and regression test in place. Implementation pending.

## Problem Summary

When a user submits two review requests for the same profile at nearly the same time, both invoke `process_review()` in `core/services/review_service.py` against the same `profile_id` with no synchronization. The second request can start, run, and complete entirely while the first request is still mid-pipeline holding a stale snapshot of the profile. When the first request eventually resumes and commits its changes, it overwrites or ignores edits from the second request, producing inconsistent review results.

### Root Cause

`process_review()` fetches a `Profile` snapshot, then runs a multi-step pipeline (ingestion → agent orchestration → RAG → safety checks) with several `await` points and `db.commit()` calls. Nothing prevents two concurrent calls for the same `profile_id` from interleaving against shared profile state.

### Expected Behavior

A second review request for a profile that already has a review in progress should wait for the first to fully complete before starting, ensuring one of two non-interleaved orders: `[A_start, A_end, B_start, B_end]` or `[B_start, B_end, A_start, A_end]`.

### Actual Behavior

Both loops run concurrently, producing interleaved order like `[A_start, B_start, B_end, A_end]` where B's changes land between A's snapshot read and commit.

## Reproduction

The regression test at `tests/integration/test_review_concurrency.py` deterministically pins the bug via monkeypatched ingestion steps (no flaky timing races). It requires Postgres (docker-compose.yml, port 5433) and is designed to skip gracefully if unavailable. On unfixed code, the test fails with `AssertionError: expected non-interleaved execution, got ['A_start', 'B_start', 'B_end', 'A_end']`.

**Verified reproduction commands:**
```bash
docker compose up -d db
export DATABASE_URL="postgresql+asyncpg://pathreview:pathreview@localhost:5433/pathreview_dev"
make migrate
.venv/Scripts/pytest tests/integration/test_review_concurrency.py -v -m integration
```

## Solution Design

### Files to Modify

- `core/services/review_service.py`: Add module-level per-profile lock registry and wrap `process_review()` body in lock acquisition/release.
- `api/routes/reviews.py`: No changes (endpoint already returns "pending" immediately).
- `tests/integration/test_review_concurrency.py`: Use as pass/fail baseline, no changes.

### Implementation Plan

1. Add a module-level dict mapping `profile_id` → `asyncio.Lock`, created lazily on first use.
2. At the start of `process_review()`, acquire the profile's lock (blocking until released by any prior call).
3. Release the lock after the review reaches a terminal status (complete or failed), covering all exit paths including exceptions.
4. Verify regression test passes with both non-interleaved orders.
5. Run `make check && make test-unit` per CONTRIBUTING.md.

### Why This Approach

- In-process async lock is sufficient since `process_review()` runs as a FastAPI background task in a single worker.
- No new dependencies: `asyncio.Lock` is stdlib.
- Respects existing repository patterns: exception handling, database session management, and logging all remain unchanged.
- Locks are released on every exit path, preventing deadlock from partial failures.

## Code Conventions & Constraints

**No new dependencies:** All modifications must use only the dependencies already in `pyproject.toml`. The fix uses `asyncio.Lock` from Python stdlib, which is already available.

**Existing abstractions:** The fix must not bypass or duplicate existing patterns in the codebase:
- Follow the async/await patterns already used in `process_review()` and the database layer.
- Use `structlog` for logging, matching the existing log statements in the service.
- Respect the exception handling structure already in place.
- Do not introduce new classes, utilities, or helper functions beyond what the lock registry requires.

**Code style:** Format with `black`, lint with `ruff`, type-check with `mypy`. All three must pass: `make check`.

**Documentation:** No new docstrings beyond a single-line comment on the lock registry explaining its purpose.

## Known Limitations & Out of Scope

**Unbounded lock registry:** Locks are never removed, so the registry grows by one per unique `profile_id` over the process lifetime. The memory footprint is small (one `asyncio.Lock` per profile), but a production system with millions of profiles should implement periodic cleanup or weak references. Out of scope for #82.

**Single-process only:** In-memory locks only serialize within a single worker process. Multi-worker deployments need distributed locking (e.g., Postgres advisory locks). Out of scope for #82; flag as a deployment constraint.

**Ingestion silent failure:** `_run_ingestion_pipeline()` constructs `IngestedSource(raw_data=...)`, but `raw_data` is not a field on the `IngestedSource` model. Ingestion currently fails silently every time (caught by broad `except` clause). Worth its own issue/fix, separate from #82.

## Testing Strategy

- **Regression test:** Confirm `call_order` equals one of the two non-interleaved sequences.
- **Timing edge cases:** The test's 0.2s and 0.05s sleeps should serialize; verify lock works as timing windows narrow toward zero.
- **Multiple concurrent requests:** Confirm third, fourth, etc. requests for the same profile queue correctly.
- **Exception paths:** Verify lock is released even when the pipeline fails partway through.
- **Deadlock prevention:** Structurally impossible here (one lock per profile, no nested locks), but confirm via inspection.

## Integration with Agent Orchestrator

Per ARCHITECTURE.md, `process_review()` feeds the agent orchestrator state data from the ingestion pipeline. The per-profile lock ensures the agent orchestrator never sees interleaved state for a given profile, maintaining plan consistency and execution correctness as documented in ARCHITECTURE.md.

## References

- JOURNAL.md: Issue selection, problem visualization, and reproduction steps
- PLAN.md: Detailed solution plan with edge cases and risks
- tests/integration/test_review_concurrency.py: Regression test
- docs/ARCHITECTURE.md: Agent orchestrator and data flow
- docs/CONTRIBUTING.md: Code style and testing conventions
