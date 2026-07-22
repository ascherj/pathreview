## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/106

**Issue title:** Shared test fixture for a sample user profile is missing from `tests/fixtures/`

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
A JSON fixture file at `tests/fixtures/sample_profiles/basic_profile.json` was deleted from the repository. Multiple integration tests depend on this file to run, and without it they silently skip instead of executing. The file is supposed to contain a realistic sample portfolio — a GitHub username, a resume, and data for two repositories. The fix is to recreate the missing directory and file with valid sample data so the skipped tests can run again. No logic changes are needed anywhere else in the codebase.

**Branch name:** fix/106-restore-basic-profile-fixture

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
