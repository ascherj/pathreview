# Development Journal

## Environment Setup

- **OS:** Windows 11 (Git Bash)
- **Python:** 3.11+ (project venv at `.venv/`)
- **Node.js / npm:** 18+ / 9+
- **Docker:** backing services (PostgreSQL on `5433`, Redis on `6379`) via `docker compose up -d`

### Setup verified

- `docker compose up -d` — `db` and `redis` containers healthy
- `alembic upgrade head` — migrations applied against Postgres on port 5433
- `scripts/seed_db.py` — seeded the three sample accounts (`user1..3@example.com`)
- Frontend dependencies installed (`cd frontend && npm install`)
- Backend reachable at http://localhost:8000/docs, frontend at http://localhost:5173

### Notes

- On Windows, force UTF-8 output (`PYTHONUTF8=1`) so the seed script's Unicode
  status glyphs don't crash on the cp1252 console codepage.
- `LLM_PROVIDER=mock` is the default and requires no API key for local development.

## Work Log

- Set up local development environment and verified the full stack runs.
- Created branch `test/156-readme-scorer-fixture-word-count` for issue #156
  (README scorer test fixture too short for its word-count assertion).

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/156

**Issue title:** README scorer test fixture is too short for its own word-count assertion

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `readme_scorer` agent tool assigns a README a `word_count` and a
`word_count_category` (e.g. "comprehensive") based on how long the README is.
Its unit test `test_readme_with_all_quality_signals` claims to exercise the
"comprehensive" path, asserting `word_count > 100` and
`word_count_category == "comprehensive"`, but the fixture README it feeds in
is only ~51 words long. The scorer behaves correctly and returns 51, so the
assertion `51 > 100` fails — the test, not the code, is wrong. A successful
fix extends the fixture README past 100 words (or corrects the assertion) so
the test genuinely validates the comprehensive-length branch it was meant to
cover. This lives in `tests/unit/test_readme_scorer.py` against the
`agent` scorer tool.

**Branch name:** test/156-readme-scorer-fixture-word-count

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
