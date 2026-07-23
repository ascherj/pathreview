## Week 7 — Issue Selection

**Issue link:** [https://github.com/ascherj/pathreview/issues/82]

**Issue title:** [Concurrent review requests for the same profile can produce inconsistent results - #82]

**Tier:** [ ] Tier 1  [ ] Tier 2  [ X ] Tier 3

**Problem summary:**
<!-- [In 3–5 sentences, in your own words: what the issue is (not a copy-paste of
the title), what is currently broken or missing, and what a successful fix
would accomplish. Naming the part of the codebase it affects is helpful context.] -->

This issue is a race condition that occurs when a user submits two review requests for the same profile at the same time. Both requests trigger the agent loop against the same profile state, so the second agent loop can end up reading data that the first loop has already modified, since there is nothing preventing the two loops from overlapping. This produces inconsistent review results for the profile. The fix is to add a per-profile lock (mutex) in the review submission flow so that concurrent requests for the same profile are serialized rather than processed in parallel. This affects the review submission endpoint in `api/routes/reviews.py` and the review creation logic in `core/services/review_service.py`.

**Is this issue right for me? Scope reasoning:**

I can explain the problem and the expected behavior in my own words without rereading the issue, as shown in the problem summary above. The affected area is the API layer, and the issue is labeled as an enhancement. The relevant files are `api/routes/reviews.py`, `core/services/review_service.py`, and the corresponding test file `tests/unit/test_review_service.py`, all of which I have located and confirmed exist in the codebase. Done looks like a per-profile mutex that serializes concurrent review requests for the same profile, so a second request for a profile that already has a review in progress waits for the first to complete instead of racing against it and producing inconsistent results.

I am treating Tier 3 as a realistic fit given my current experience. I work as an Associate Developer Co-op at IBM on microservice architectures for banking clients, so I am comfortable navigating and modifying industry sized codebases under concurrency constraints. I have read through the relevant route handler, service logic, and existing unit tests closely enough to sketch a rough implementation plan without needing to look anything up further. The scope feels realistic for the Week 8 to 9 window given the estimated six to nine hour effort, and I have checked the issue for blockers or dependencies on other unresolved issues and found none.

**Branch name:** `fix/82-concurrent-review-locking`

**Setup confirmation:** [ X ] App runs locally at localhost:5173

**Cohort ledger:** [ X ] Issue added to cohort ledger

## Issue Visualization

```mermaid
sequenceDiagram
    participant A as Request A<br/>process_review(profile_id=1)
    participant DB as Profile (shared state)
    participant B as Request B<br/>process_review(profile_id=1)

    A->>DB: 1. A_start: read Profile snapshot
    activate A
    Note over A: 2. A awaits mid-pipeline<br/>(ingestion -> orchestration, no lock held)
    B->>DB: 3. B_start: read Profile snapshot
    activate B
    Note over B: 4. B edits Profile, runs full pipeline
    B->>DB: 5. B commits changes
    B-->>B: 6. B_end: review complete
    deactivate B
    Note over A: 7. A resumes using STALE<br/>snapshot from before step 5
    A->>DB: 8. A commits changes (based on stale data)
    A-->>A: 9. A_end: review complete
    deactivate A

    Note over A,B: call_order = [A_start(1), B_start(3), B_end(6), A_end(9)]<br/>Result: inconsistent profile state<br/>Step 8 can silently overwrite or ignore step 5's edits
```

**What the diagram shows:** Request A begins first and holds an in-memory `Profile` snapshot across several `await` points (ingestion, orchestration, RAG, safety checks). Since nothing keys off `profile_id`, Request B is free to start, run to completion, and commit its own changes while A is still suspended mid-pipeline. When A eventually resumes and commits, it does so against its now stale snapshot, producing the interleaved `["A_start", "B_start", "B_end", "A_end"]` order the regression test asserts against. A per-profile lock would force B to wait until A releases the lock, guaranteeing one of the two non-interleaved orders instead.

## How to Reproduce

**Root cause:** `process_review()` in `core/services/review_service.py` fetches its own `Profile` snapshot, then runs a multi-step pipeline (ingestion → agent orchestration → RAG → safety checks) with several `await` points and `db.commit()` calls in between. Nothing keys off `profile_id` to prevent two calls from running concurrently, so two review requests submitted for the same profile close together interleave freely against shared profile state instead of being serialized.

The regression test at [`tests/integration/test_review_concurrency.py`](tests/integration/test_review_concurrency.py) pins this down deterministically (no flaky timing races) by monkeypatching the ingestion step of two concurrent `process_review()` calls to record when each starts/finishes, and forcing review A to pause mid-flight while review B's profile edit and full run land in between.

To reproduce it yourself, from the repo root:

```bash
# 1. Start the real Postgres the app uses (docker-compose.yml service is named `db`,
#    mapped to host port 5433)
docker compose up -d db

# 2. Point the app at it (matches .env.example)
export DATABASE_URL="postgresql+asyncpg://pathreview:pathreview@localhost:5433/pathreview_dev"

# 3. Apply migrations so the schema exists
make migrate

# 4. Run the regression test directly -- on unfixed code this FAILS
.venv/Scripts/pytest tests/integration/test_review_concurrency.py -v -m integration
```

(On macOS/Linux, use `.venv/bin/pytest` per the Makefile's `VENV_BIN` convention.)

**Expected result on current, unfixed code:** the test fails with

```
AssertionError: expected non-interleaved execution, got ['A_start', 'B_start', 'B_end', 'A_end']
```

Review B starts and *completes entirely* while review A is still mid-flight, still holding a profile snapshot from before review B's own edit & submit sequence landed. There is no lock forcing one loop to wait for the other; the two loops for the same `profile_id` simply race.

**Expected result once fixed:** a per-profile lock must serialize the two loops so `call_order` comes back as either `["A_start", "A_end", "B_start", "B_end"]` or `["B_start", "B_end", "A_start", "A_end"]`, one loop fully finishing (and releasing its per-profile lock) before the other is allowed to begin. The test asserts exactly this.

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [4fdd789](https://github.com/DasEd955/pathreview/commit/4fdd789e6873107519a7a3636470dbbfe868945f)

**Reproduction summary:**

I reproduced the issue by simulating concurrency and latency: two `process_review()` calls are kicked off for the same `profile_id`, with review A's ingestion step monkeypatched to pause mid-flight while review B runs to completion in that window, then A resumes and finishes. Since nothing keys off `profile_id`, the two calls interleave freely against the shared profile state instead of running serially, and the regression test I wrote codifies this bug by asserting `call_order` against the non-interleaved orders.

**PLAN.md link:** [PLAN.md](https://github.com/DasEd955/pathreview/blob/fix/82-concurrent-review-locking/PLAN.md)

**Blockers or open questions:**

None at this moment, but I'm eager to sanity check once the fix is implemented whether I considered enough edge cases and whether my prework analysis was thorough enough.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**

Plan items #1 through #4 from [PLAN.md](PLAN.md) are implemented in `core/services/review_service.py`. There's now a module level Redis client built from `settings.redis_url`, and `process_review()` acquires a per-profile lock at the start, keyed by `profile_id` with a 300 second TTL. The lock wraps the full pipeline span, from status set to processing through the terminal commit. It's released on every exit path, including the exception handler, and an already expired lock on release is treated as a logged warning rather than a crash. The regression test from commit [4fdd789](https://github.com/DasEd955/pathreview/commit/4fdd789e6873107519a7a3636470dbbfe868945f) now passes against this implementation.

**Next steps:**

I still need to work through plan items #5 through #7. That means writing the new lock lifecycle, expiration, and contention tests called out in the [Testing Strategy](PLAN.md#testing-strategy) section of PLAN.md. Then running the full test suite to confirm everything passes together, followed by a final cleanup pass before considering this ready for PR.

**Blockers:**

None right now. I'm eager to get the expanded test coverage written and to verify my commit passes the linter, formatter, and the rest of the repo's code conventions cleanly.