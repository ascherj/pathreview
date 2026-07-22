## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/151

**Issue title:** Bias detector patterns are too narrow to match common phrasings

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The bias detector in `safety/bias_detector.py` uses regular-expression patterns to identify potentially biased language in generated feedback. The existing educational-bias patterns were too narrow, so common statements about bootcamp graduates, self-taught developers, and online-course students were not consistently detected. This meant biased wording could pass through the detector even though it expressed the same assumptions as phrases the system already recognized. A successful fix would broaden the patterns while preserving the detector’s existing behavior and would include regression tests confirming that the additional phrasings are detected.

**Branch name:** `fix/bias-detector-patterns-151`

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

### Issue selection notes — “Is this right for me?”

I selected a Tier 1 issue because this was my first contribution to a large, multi-module codebase and I wanted an issue with a focused and realistic scope. The change was limited mainly to `safety/bias_detector.py` and its unit tests, so I could understand the affected behavior without making architectural changes across the application. The issue matched my familiarity with Python, regular expressions, testing, and debugging. I also confirmed that the expected result could be validated with clear regression tests, which made the issue appropriate for my current skill level.
