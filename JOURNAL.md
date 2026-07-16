## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/129

**Issue title:** Add a database migration validation step to CI that checks all migrations can be applied cleanly #129

**Tier:** [ ] Tier 1  [ ] Tier 2  [X] Tier 3

**Problem summary:**
The current issue is that the database migration validation would be done manually which is prone to many errors. Instead, what I need to fix/include is a database migration validation step to when CI is run to ensure that the current migration and any prior migrations should run successfully from start to finish, and the resulting database schema should match what's defined in the SQLAlchemy models. The current files relevant to this are `.github/workflows/ci.yml` and `scripts/validate_migrations.sh`, meaning that I will be looking at these two specific files to understand how to add an automated validation pipeline for the CI. 

**Branch name:** chore/129-migration-validation-ci

**Setup confirmation:** [X] App runs locally at localhost:5173

**Cohort ledger:** [X] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/Louis-Barbosa/pathreview/commit/6f6b982


**Reproduction summary:**
To reproduce the issue, I added migration `003`, which is deliberately broken (it renames `reviews.error_message`, drifting the schema away from the SQLAlchemy model). No CI job or script verifies migrations, so the broken migration passes with a green build and is allowed to reach main.


**PLAN.md link:** https://github.com/Louis-Barbosa/pathreview/blob/chore/129-migration-validation-ci/PLAN.md


**Walkthrough video (recommended):** [link to your Loom video, ≤2 min — shared for early feedback]

**Blockers or open questions:**
[Anything you're still uncertain about going into Week 9, or leave blank]