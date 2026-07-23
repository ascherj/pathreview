# Module 3 Progress Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/47

**Issue title:** Agent state isn't persisted across API restarts, causing in-progress reviews to be lost

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
Long-running reviews that span five or more repositories currently lose all progress when the server restarts because agent session data is stored only in memory. When the API process terminates (during maintenance or deployment), all in-flight review state is lost with no way to recover. The fix requires persisting the agent's memory context to Redis before shutdown and restoring it on startup. This will ensure that users don't lose progress on long-running reviews and allow the system to handle server restarts gracefully without data loss.

**Branch name:** fix/47-persist-agent-state-across-restarts

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

---

## Week 8 — Implementation
(To be completed)

## Week 9 — Testing & PR
(To be completed)

## Week 10 — Reflection
(To be completed)
