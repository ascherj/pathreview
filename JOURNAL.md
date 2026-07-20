# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/50

**Issue title:** Add a `has_tests` boolean to the repo analysis output

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The analysis output for a repo currently has no signal for whether it has tests. This logic lives in `agent/tools/github_tool.py`, in the `GitHubTool` class, which already fetches things like star count, language, and `has_readme` from the GitHub API. The pattern to follow already exists: there's a `_has_readme()` method that checks a repo via a GitHub API call, and `has_tests` would work the same way — checking for a `tests/`/`test/` folder, a `pytest.ini` file, or files matching `test_*.py`. This matters because the issue explicitly calls test coverage "a strong portfolio signal," so this feature makes the tool smarter about what makes a repo look good. Success looks like a new `has_tests` boolean appearing in the repo metadata dict alongside `has_readme` and `star_count`, backed by a test I write myself, since no test file exists yet for `github_tool.py`.

**Selection notes (is this issue right for me?):**
This task aligns well with my experience working on Python projects and navigating existing codebases. I've worked with repository structures and testing frameworks like pytest, and I'm confident I can contribute by implementing reliable test detection logic and integrating it cleanly into the analysis output.

**Branch name:** feat/50-has-tests-detection

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
