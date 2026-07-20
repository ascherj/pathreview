# JOURNAL

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/82

**Issue title:** Concurrent review requests for the same profile can produce inconsistent results

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
When two review requests come in for the same profile at almost the same time, both kick off the agent review loop against whatever profile state is currently in the database, with no coordination between the two runs. If the first request modifies the profile mid-flight, the second loop can still be working from the state it read before that change, so its output doesn't reflect the latest data. The fix is to add a per-profile lock so a second review request for the same profile is serialized behind the first instead of running concurrently against shared state. This mainly touches the review submission endpoint in `api/routes/reviews.py` and the orchestration logic in `core/services/review_service.py`.

**Is this right for me? — checklist reasoning:**

- *Understanding the issue:* When a user fires off two review requests for the same profile close together, both spawn independent `process_review` background tasks that read and write the same profile/review state with no coordination between them. Whichever task's writes land last wins, so the first task's work can be silently overwritten, or the second task can act on ingestion/profile data the first task already changed underneath it. "Done" looks like: submitting two reviews for the same profile back-to-back no longer risks one clobbering or reading stale state from the other — the second request waits for the first to finish before it starts.
- *Tier fit:* This is my first *open-source* contribution, but not my first time in a large codebase — I have around 2 years of professional experience, including work on production systems with concurrency bugs similar to this one so this is a considered Tier 3 pick, not a "challenge myself" pick.
- *Codebase readiness:* Read `create_review_endpoint` in `api/routes/reviews.py` (creates the review row, then fires `process_review` via an unguarded `BackgroundTasks.add_task` call — no locking or dedup on `profile_id`) and `process_review` in `core/services/review_service.py` (reads the profile, runs ingestion → agent orchestration → RAG → safety checks → writes `review.status`/`sections`, with no per-profile synchronization anywhere in that path). Confirmed the race concretely: two requests for the same `profile_id` each call `_run_ingestion_pipeline`, which writes its own `IngestedSource` rows and commits independently, so concurrent runs duplicate ingestion data. Checked `tests/unit/test_review_service.py` — it only covers `create_review`, `get_review`, and `list_reviews` with mocked DB sessions; there is no existing coverage for `process_review` or any concurrency behavior, so tests for this fix will need to be written from scratch (likely simulating two concurrent `process_review` calls with `asyncio.gather`).
- *Scope and time:* No "blocked by" language or dependencies found on the issue. Since there's no existing lock/concurrency pattern in the codebase to follow and no test coverage to build from, I'm budgeting toward the higher end of the 6–9 hour estimate.

**Branch name:** fix/82-concurrent-review-race-condition

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
