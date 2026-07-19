## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/152

**Issue title:** Faithfulness checker can never mark short claims as supported

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The RAG faithfulness checker currently requires at least two meaningful
non-stopword tokens to overlap between a claim and its supporting context.
Short factual claims may contain only one meaningful token, so claims such as
“Knows Python” are marked unsupported even when the context clearly supports
them. This affects the `_is_supported()` logic in the faithfulness checker and
causes multiple unit tests to fail. A successful fix will allow short,
supported claims to receive credit while still preventing unrelated claims
from being classified as supported.

**Selection notes — “Is this right for me?” checklist reasoning:**
This issue is labeled Tier 1 and provides a clear reproduction example, the
specific function involved, and the names of related failing tests. Its scope
appears limited to the RAG faithfulness checker and its unit tests, rather than
requiring changes throughout the entire application. I should be able to
reproduce the bug locally and verify the solution using automated tests. Before
implementing the fix, I will inspect how short claims, stopwords, and token
overlap are currently handled so that the change does not introduce overly
permissive matching.

**Branch name:** fix/152-short-claim-faithfulness

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger