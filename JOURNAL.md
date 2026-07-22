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

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/246

**Branch:** `fix/152-short-claim-support`

**What you built:**
Implemented Issue #152 by allowing short faithfulness claims to be supported when they reduce to a single concrete subject token found in the retrieved context. The implementation preserves stricter matching for ambiguous and multi-subject claims to reduce false positives.

**Tests added or updated:**
Updated `tests/unit/test_faithfulness_checker.py` with the exact Issue #152 regression case, negative tests for ambiguous and multi-subject short claims, and additional coverage for multi-skill support scenarios.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes

Pre-existing repository failures remain, but comparison against `upstream/main` confirmed that this branch introduces no new test, lint, formatting, or type-checking failures.

**Draft PR feedback received from:** none

## Week 10 — Iteration & reflection

### Reviewer feedback

**Feedback received:** [ ] Yes  [x] No — still awaiting review

**Summary of feedback:**
No reviewer or maintainer feedback had arrived on PR #246 at the time of this reflection. The pull request remains open and ready for review.

**How you responded:**
No response or code changes were required because no reviewer feedback had been received.

---

### Reflection

**What was harder than you expected?**
The hardest part was not the initial code change, but defining a rule that fixed Issue #152 without creating new false positives. Allowing any single overlapping token would have made claims such as `Strong API design.` appear supported when the context only mentioned API routes, so I had to narrow the one-token rule to short claims with one concrete subject. Comparing the branch against `upstream/main` was also more involved than expected because the repository already had failing tests and lint errors.

**What did you learn about working in a large codebase?**
I learned that contributing to an existing codebase requires understanding both the local component and the repository's broader conventions. Changes to `rag/evaluator/faithfulness_checker.py` had to match existing test patterns, type-checking requirements, formatting hooks, and contribution standards rather than simply producing the correct output. I also learned that pre-existing failures must be documented carefully instead of being mistaken for regressions caused by my branch.

**How did AI tools help — and where did they fall short?**
AI tools were most useful for exploring the faithfulness checker, identifying possible edge cases, reviewing the branch diff, and suggesting targeted regression tests. They also helped me interpret failures from Ruff, Black, mypy, and pytest more quickly. However, some AI-generated suggestions initially broadened the implementation too much, including claim-splitting behavior that was outside the issue's scope, so I had to review the output, compare it against the issue requirements, and narrow the solution manually.

**What would you do differently if you started over?**
I would begin by writing the exact Issue #152 regression test and several negative tests before changing the implementation. That would make the acceptable behavior and false-positive boundaries clear earlier and reduce the need for later revisions. I would also run the upstream baseline for `make check` and `make test-unit` at the beginning of the week so that pre-existing failures were documented before implementation.

**What are you most proud of from this module?**
I am most proud that I did not stop after making the three original failing tests pass. I reviewed the false-positive risk, added exact and negative regression coverage in `tests/unit/test_faithfulness_checker.py`, and refined the implementation until Ruff, Black, and mypy all passed. The final contribution is narrowly scoped to Issue #152 and includes enough documentation for another developer to understand both the fix and its limitations.


---
