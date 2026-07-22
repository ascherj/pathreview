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
