## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/129

**Issue title:** Add a database migration validation step to CI that checks all migrations can be applied cleanly #129

**Tier:** [ ] Tier 1  [ ] Tier 2  [X] Tier 3

**Problem summary:**
The current issue is that the database migration validation would be done manually which is prone to many errors. Instead, what I need to fix/include is a database migration validation step to when CI is run to ensure that the current migration and any prior migrations should run successfully from start to finish, and the resulting database schema should match what's defined in the SQLAlchemy models. The current files relevant to this are `.github/workflows/ci.yml` and `scripts/validate_migrations.sh`, meaning that I will be looking at these two specific files to understand how to add an automated validation pipeline for the CI. 

**Problem Scope:** This problem is right for me because it is quite challenging and deals with cross-cutting concerns which I think I have the skillset for. Furthermore, I will have the time to commit to a PR of this difficulty and scale. With all of this in mind, I believe that a problem of this score is well within my skillset and a good fit for me to tackle. 

**Branch name:** `chore/129-migration-validation-ci`

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

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
So far I have created and implemented the validation script: `scripts/validate_migrations.sh` which essentially uses `alembic upgrade head` to run every migration in order and then `alembic check` to compare the finished database against the code's models. I also included a `migrations` job in `.github/workflows/ci.yml` to run the script anytime a job starts a throwaway PostgreSQL database. This makes it so that the check will run automatically on every pull request.

**Next steps:**
For the rest of the week I am going to be testing to make sure that it functions properly and is not breaking any systems. This means that I will likely build a test script to ensure that it works and to provide proof in the PR that it is functional. Furthermore, I will remove any old broken migrations that I used to test how the system was broken. This is simply because I want my PR to be clean and leaving a broken migration can be confusing. 

**Blockers:**
N/A

---

### Check-in 2 (end of week)

**PR link:** https://github.com/ascherj/pathreview/pull/181

**Branch:** `chore/129-migration-validation-ci`

**What you built:**
I built a CI migration-validation step. The file `scripts/validate_migrations.sh` applies every migration to a fresh, empty database (`alembic upgrade head`) and then confirms the resulting schema matches the SQLAlchemy models (`alembic check`), failing the build if a migration is broken or the schema has drifted. A new `migrations` job in `.github/workflows/ci.yml` runs the script against a throwaway PostgreSQL service on every pull request, essentially automating the check. While validating, the check surfaced a real pre-existing drift — migration `001` created a redundant `uq_users_email` unique constraint the models don't declare — which I fixed with a new migration `003`, then removed the deliberately-broken reproduction migration.

**Tests added or updated:**
I added `tests/unit/test_migrations.py` — static checks over the migration history (no database required): exactly one base revision, exactly one head, and every `down_revision` points to a known revision. These guard the single-linear-history invariant the CI job relies on (e.g. the multiple-heads case that would make `upgrade head` ambiguous). Verified the script itself end-to-end against a local Postgres container: it fails with the broken migration present and passes once the repo is clean.

**Self-review confirmation:** [X] make check passes  [X] make test-unit passes

**Draft PR feedback received from:** none
