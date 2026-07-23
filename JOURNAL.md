# PathReview — Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/71

**Issue title:** Implement a red-teaming test suite for the prompt injection defense

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
PathReview has a safety layer (the `safety/` module) that is supposed to detect
and block prompt injection attacks before user-supplied text reaches the LLM, but
right now there is no automated way to prove that this defense actually works or
that it keeps working as the code evolves. This issue asks for a dedicated
red-teaming test suite that feeds a curated collection of known prompt-injection
attack patterns through the safety layer and asserts that every one of them is
blocked. The work also involves organizing the attack payloads as reusable
fixtures and wiring the suite into CI so it runs automatically whenever anything
under `safety/` changes. A successful fix gives the project continuous,
regression-proof evidence that its injection defenses hold — turning "we think the
safety layer works" into "we can prove it on every commit."

**Branch name:** test/71-prompt-injection-red-team-suite

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

---

### "Is this right for me?" — selection notes

- **Scope / effort:** The issue is labeled **Tier 3** (advanced) with an estimated
  7–10 hours of work. It is heavier than the Tier 1 issues recommended for a first
  contribution, so I am going in aware that most of the effort is in curating a
  broad, realistic set of injection payloads and understanding the existing
  `safety/` behavior — not in a single small code change.
- **Where it lives:** The change is well-contained in new files
  (`tests/security/test_prompt_injection.py` and
  `tests/fixtures/injection_attempts/`) plus a CI workflow tweak. It adds tests
  rather than modifying core application logic, which lowers the risk of breaking
  existing features.
- **What I need to understand first:** How the `safety/` layer exposes its
  detection/blocking API, what "blocked" looks like as a return value or raised
  error, and the existing test conventions (`pytest` markers — note the `security`
  marker is already declared in `pyproject.toml`).
- **Dependencies / blockers:** No external API key is required to run the safety
  layer locally (the app defaults to `LLM_PROVIDER=mock`), so the suite can be
  developed and run entirely offline. CI wiring depends on the existing
  `.github/workflows/` setup.
- **Fit:** Good fit for building confidence with the codebase's testing and safety
  systems; the main stretch is the Tier 3 breadth, which I'll manage by starting
  with a small set of attack categories and expanding.
