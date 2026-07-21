# Contribution Journal

## Tier 2 — Intermediate Issues

### Issue #118 — Add a troubleshooting guide for the five most common setup failures

**Link:** https://github.com/jamjamgobambam/pathreview/issues/118

**Problem summary:**
Contributors frequently encounter the same five setup errors: Docker memory limits causing OOM kills, port conflicts with local services, missing `.env` variables, outdated Node.js versions, and mismatched Python versions. The existing SETUP.md has a brief troubleshooting section but doesn't document each error with cause, symptoms, and resolution. A successful fix creates a standalone `docs/TROUBLESHOOTING.md` that covers all five failures in a structured, easy-to-scan format.

**"Is this right for me?" checklist reasoning:**
- Documentation-only change — no code risk
- Requires understanding the Docker, Node, Python toolchain the project uses
- Cross-references SETUP.md so readers aren't sent to dead ends
- Files changed: `docs/TROUBLESHOOTING.md`

**Branch:** `docs/118-troubleshooting-guide`

---

### Issue #119 — Add inline docstrings to all public methods in `core/services/`

**Link:** https://github.com/jamjamgobambam/pathreview/issues/119

**Problem summary:**
The service layer (`profile_service.py`, `review_service.py`) has minimal one-line docstrings on most functions but no structured Args/Returns/Raises documentation. Developers reading the code can't tell what parameters do, what types are expected, or what exceptions might be raised. A successful fix adds Google-style docstrings to every public function covering description, Args, Returns, and Raises sections.

**"Is this right for me?" checklist reasoning:**
- Two files: `core/services/profile_service.py` and `core/services/review_service.py`
- No behavioral changes — documentation only
- Requires reading each function to understand its parameters and behavior
- Aligns with the Google-style convention already referenced in CONTRIBUTING.md

**Branch:** `docs/119-service-layer-docstrings`

---

### Issue #124 — Pre-commit hook for linting doesn't run on files modified by `git add -p`

**Link:** https://github.com/jamjamgobambam/pathreview/issues/124

**Problem summary:**
When developers stage partial file changes with `git add -p`, pre-commit hooks lint the entire working tree file instead of only the staged changes. This means unstaged code can block a commit. A successful fix ensures hooks operate on staged content only: switching ruff from `--fix` to `--diff` (report-only), adding explicit `stages: [pre-commit]`, and adding standard meta hooks (`check-added-large-files`, `check-merge-conflict`, `end-of-file-fixer`, `trailing-whitespace`) for better coverage.

**"Is this right for me?" checklist reasoning:**
- Single file change (`.pre-commit-config.yaml`)
- Understanding of pre-commit's staged-file behavior required
- No runtime code changes — config-only fix
- Meta hooks are zero-maintenance and catch common oversights

**Branch:** `fix/124-precommit-partial-staging`

---

## Tier 3 — Advanced Issues

### Issue #121 — Write a contributor onboarding guide that walks through a complete issue-to-PR lifecycle

**Link:** https://github.com/jamjamgobambam/pathreview/issues/121

**Problem summary:**
New contributors have no single document that walks them from forking the repo to getting a PR merged. They need to piece together information from SETUP.md, CONTRIBUTING.md, and the issue tracker. A successful fix creates `docs/ONBOARDING.md` covering: forking and cloning, environment setup, finding an issue, creating a branch, making changes, running tests, committing with Conventional Commits, opening a PR, and responding to review feedback.

**"Is this right for me?" checklist reasoning:**
- Documentation-only change — no code risk
- Requires understanding the full contributor workflow
- Cross-references SETUP.md and CONTRIBUTING.md to avoid duplication
- Files changed: `docs/ONBOARDING.md`

**Branch:** `docs/121-onboarding-guide`

---

### Issue #128 — Add a dependency vulnerability scan to the CI pipeline

**Link:** https://github.com/jamjamgobambam/pathreview/issues/128

**Problem summary:**
The project has no automated check for known security vulnerabilities in its Python or JavaScript dependencies. Contributors can unknowingly introduce vulnerable packages, and there's no CI gate to catch them. A successful fix adds an `audit` job to `.github/workflows/ci.yml` that runs `pip-audit` on Python dependencies and `npm audit --audit-level=high` on frontend dependencies, with `continue-on-error: true` so current findings don't block builds while providing visibility.

**"Is this right for me?" checklist reasoning:**
- Single file change (`.github/workflows/ci.yml`)
- Uses existing ecosystem tools (`pip-audit`, `npm audit`)
- `continue-on-error: true` ensures findings are visible but non-blocking
- Requires understanding GitHub Actions job structure

**Branch:** `ci/128-dependency-audit`

---

## Cohort Issue Ledger

| Issue | Tier | Branch | Status |
|-------|------|--------|--------|
| #118 | 2 | `docs/118-troubleshooting-guide` | Implemented |
| #119 | 2 | `docs/119-service-layer-docstrings` | Implemented |
| #124 | 2 | `fix/124-precommit-partial-staging` | Implemented |
| #121 | 3 | `docs/121-onboarding-guide` | Implemented |
| #128 | 3 | `ci/128-dependency-audit` | Implemented |

## Branches

Each branch follows the naming convention from CONTRIBUTING.md: `<type>/<issue-number>-<short-description>`.

Branch URLs:
- `docs/118-troubleshooting-guide`: https://github.com/Bobaninja21/pathreview/tree/docs/118-troubleshooting-guide
- `docs/119-service-layer-docstrings`: https://github.com/Bobaninja21/pathreview/tree/docs/119-service-layer-docstrings
- `fix/124-precommit-partial-staging`: https://github.com/Bobaninja21/pathreview/tree/fix/124-precommit-partial-staging
- `docs/121-onboarding-guide`: https://github.com/Bobaninja21/pathreview/tree/docs/121-onboarding-guide
- `ci/128-dependency-audit`: https://github.com/Bobaninja21/pathreview/tree/ci/128-dependency-audit
