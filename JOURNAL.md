# JOURNAL

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/47

**Issue title:** Agent state isn't persisted across API restarts, causing in-progress reviews to be lost

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
When the agent runs a long review (multiple repos/tools), it tracks progress only
in the orchestrator's local memory and writes that progress to Redis a single
time, after every tool in the plan has finished. If the API process restarts
while a review is still in progress — a deploy, a crash, anything — none of the
work done so far is saved, and the review has to start completely over. The
code lives in `agent/orchestrator.py` (the `Orchestrator.run()` loop) and
`agent/memory/session_store.py` (the Redis-backed store it writes to). A
successful fix checkpoints each tool's result to Redis as soon as that tool
finishes, and on a fresh run checks that saved state first so completed tools
are skipped and only the unfinished ones actually re-execute.

**Scope reasoning ("Is this right for me?"):** This is a Tier 3 issue, a bigger
jump than the recommended Tier 1 starting point for a first contribution. I
chose it deliberately over the smaller Tier 1 health-check bug I'd originally
selected (#154). It's still tractable: it touches two files I could read in
full, the fix is a scoped change to *when* an existing Redis write happens
(not a new subsystem), and I verified my understanding by reading both files
end-to-end before writing any code. The estimated effort in the issue (7–10
hours) is real, mostly because a correct fix needs a second behavior beyond
checkpointing — actually skipping already-completed tools on resume — which
isn't obvious from the issue title alone.

**Branch name:** fix/47-persist-agent-progress-across-restarts

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
