# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/152

**Issue title:** Faithfulness checker can never mark short claims as supported

**Tier:**
- [x] Tier 1
- [ ] Tier 2
- [ ] Tier 3

**Problem summary:**
The faithfulness checker in rag/evaluator/faithfulness_checker.py determines whether claims in generated feedback are supported by retrieved context. Its current logic requires at least two meaningful overlapping tokens, which causes valid short claims such as "Knows Python" to be marked unsupported even when the context clearly mentions Python expertise. This causes partial-support and multiple-skill examples to incorrectly receive scores of zero. A successful fix will normalize tokens and allow short factual competency claims to be recognized while preserving stricter checks for longer claims.

**Selection notes and scope reasoning:**
- The issue was open and had no linked branch or pull request when I selected it.
- I commented on the issue to claim it before beginning implementation.
- The issue includes a reproducible example and identifies the failing tests.
- The affected behavior is primarily contained in `rag/evaluator/faithfulness_checker.py`.
- The expected behavior is clear and testable.
- The issue does not require a database, API, or architectural redesign.
- I reproduced the failures locally before modifying the implementation.
- The issue is appropriately scoped for completion during Module 3.

**Branch name:** `fix/152-short-claim-support`

**Setup confirmation:**
- [x] App runs locally at `http://localhost:5173`

**Cohort ledger:**
- [x] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [Issue #152 reproduction commit](https://github.com/JohnThantSynHtet/pathreview/commit/19eafd5)

**Reproduction summary:**
I checked out the original base commit `664c3d7` and ran three focused faithfulness checker tests. All three failed with scores of `0.0`, confirming that supported short claims were incorrectly marked unsupported; after returning to my fix branch, the same three tests passed.

**PLAN.md link:** [Solution plan](https://github.com/JohnThantSynHtet/pathreview/blob/fix/152-short-claim-support/PLAN.md)

**Walkthrough video (recommended):** Not recorded.

**Blockers or open questions:**
No current blockers. The main risk going into Week 9 is ensuring that the relaxed threshold for short claims does not create false positives or change the expected behavior for longer claims.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
I implemented normalized token matching in `rag/evaluator/faithfulness_checker.py`, added support for short claims using one meaningful overlapping token, and updated the claim-extraction behavior for short competency statements. The three issue-related regression tests now pass.

**Next steps:**
I will add a direct regression test for the issue's `"Knows Python. Knows SQL."` example, run `make check` and `make test-unit`, review the implementation for false-positive and scope risks, open a draft PR, and request peer or mentor feedback.

**Blockers:**
None currently.

---
