## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/152

**Issue title:** Faithfulness checker can never mark short claims as supported

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The faithfulness checker currently prevents short claims from being marked as supported, even when there is sufficient evidence. This results in valid short claims being incorrectly classified as unsupported. The issue appears to be in the evaluation logic rather than the retrieval of evidence. A successful fix will allow short claims to be evaluated fairly while maintaining the existing validation process.

**Branch name:** fix/152-short-claims-faithfulness

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger