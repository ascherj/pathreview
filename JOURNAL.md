## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/152

**Issue title:** Faithfulness checker can never mark short claims as supported

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The FaithfulnessChecker in rag/evaluator/faithfulness_checker.py scores
generated feedback claims against retrieved context, but short factual
claims (e.g. "Knows Python") could never be marked as supported even
when the context fully backed them up. Tracing the failing tests showed
three compounding causes: tokenization didn't strip punctuation (so
"python," never matched "python"), the overlap threshold was a flat
"2+ tokens must match" rule that a 2-token claim could never satisfy,
and per-claim scoring was all-or-nothing, so a compound sentence with
one true and one false fact could only score 0 or 1, never a middle
value. A successful fix makes the checker give proportional credit
based on how much of a claim's meaningful content is present in the
context, in rag/evaluator/faithfulness_checker.py.

**Branch name:** fix/152-faithfulness-short-claims

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger