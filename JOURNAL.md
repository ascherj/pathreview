# JOURNAL.md

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/152

**Issue title:** Faithfulness checker can never mark short claims as supported

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The faithfulness checker requires at least two matching terms before it will mark any
claim as supported. That means a short claim like "Knows Python" can never pass, and the
example in the issue scores 0.0 against context that clearly mentions Python. The
evaluator ends up flagging grounded feedback as unsupported, and that misleading score
feeds into the overall quality metric. A good fix lets a single-term claim in the
"Knows X" reporting form count as supported when the context really does mention the
fact, without loosening the two-term rule for longer claims. The affected code is
`rag/evaluator/faithfulness_checker.py`; I also handled the `None` context crash from
issue #153 because it sits on the same code path.

**Branch name:** fix/152-faithfulness-short-claims

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### "Is this right for me?" notes

- Tier 1 and scoped to one module plus its test file, which felt right for my first
  contribution to a codebase this size.
- I could reproduce the failure in a few minutes using the example straight from the
  issue, so I had a concrete before and after to test against.
- The repo's failing tests basically act as the spec. I knew what done looked like
  before I started.
- Biggest scope risk I flagged before starting: drifting into general language handling
  like negation and qualifiers instead of the narrow short-claim rule the issue actually
  describes. I kept the fix to that rule.
