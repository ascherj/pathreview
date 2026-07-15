## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/150

**Issue title:** Tech detector counts vendored and build-output files, skewing language detection

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The tech_detector.py script counts files in node_modules/ and build/ directories when analyzing a repository's primary language, causing incorrect language detection. A repo with 2 Python source files and 6 JavaScript files in node_modules gets detected as primarily JavaScript instead of Python. The fix should exclude vendored and build-output paths from the detection logic so only source code is counted.

**Branch name:** fix/tech-detector-vendored-files

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger