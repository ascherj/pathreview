## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/150

**Issue title:** Tech detector counts vendored and build-output files, skewing language detection

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The tech_detector.py script counts files in node_modules/ and build/ directories when analyzing a repository's primary language, causing incorrect language detection. A repo with 2 Python source files and 6 JavaScript files in node_modules gets detected as primarily JavaScript instead of Python. The fix should exclude vendored and build-output paths from the detection logic so only source code is counted.

**Branch name:** fix/tech-detector-vendored-files

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

---

## Is This Issue Right for Me?

### Part 1 — Understanding the Issue
- [x] I can explain the problem and the expected behavior in 2–3 sentences without reading the issue.
- [x] Do I understand which part of the app is affected? The tech_detector.py module that analyzes repository language composition.
- [x] I can describe what "done" looks like: tech_detector.py excludes node_modules/ and build/ directories so language detection only counts actual source files.

### Part 2 — Tier Fit
- [x] Is the tier a realistic match for where I am right now? Yes, this is a Tier 1 fix (self-contained, single/few files, no cross-module understanding needed).

### Part 3 — Codebase Readiness
- [x] I've found and read the tech_detector.py file and understand the surrounding context.
- [x] I understand the code well enough to predict what a change will break.
- [x] I've found and read the test file (tests/unit/test_tech_detector.py) and understand existing tests.

### Part 4 — Scope and Time
- [x] How many others are already working on this issue? Checked — minimal claims on this issue.
- [x] Is the scope realistic for Weeks 8–9? Yes, estimated 3–6 hours for a Tier 1 fix.
- [x] This issue has no open blockers or dependencies on other unresolved issues.

### Verdict
Ready to proceed.

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** [link to commit documenting the reproduced issue]

**Reproduction summary:**
[1–2 sentences: How did you reproduce the issue? What did you observe?]

**PLAN.md link:** [link to PLAN.md in your fork]

**Walkthrough video (recommended):** [link to your Loom video, ≤2 min — shared for early feedback]

**Blockers or open questions:**
[Anything you're still uncertain about going into Week 9, or leave blank]