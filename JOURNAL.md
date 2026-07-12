# Module 3 Journal — Addree Barua

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/108

**Claim comment:** https://github.com/jamjamgobambam/pathreview/issues/108#issuecomment (my comment claiming the issue, posted before starting work)

**Issue title:** No test verifies that the mock LLM provider returns responses in the expected format

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
PathReview uses two embedding providers: `MockEmbeddingProvider` for local development and testing, and `OpenAIEmbeddingProvider` for the production application. Both providers are expected to return embeddings in the same format so that the mock can accurately replace the real provider during testing. The current test suite (`tests/unit/test_llm_provider_contract.py`) thoroughly tests the mock provider but never verifies that its output matches the structure of the real OpenAI provider — the only test involving the real provider checks that an `embed` method exists, which does not confirm that both providers return compatible responses. As a result, the mock provider could drift away from the real provider over time, allowing all tests to pass while the application fails when using the actual OpenAI service. A successful fix adds a contract test ensuring both providers follow the same interface and output structure, making the test suite more reliable.

**Selection reasoning ("Is this right for me?" checklist):**
I selected Issue #108 after carefully evaluating several Tier 1 issues. I first investigated Issues #107, #123, and #106, but found that one could not be reproduced, another was already outdated because the fix already existed in the Makefile, and the third had already been claimed with an open pull request. Rather than choosing an issue without verifying it, I confirmed that Issue #108 was still unclaimed, reviewed the referenced test file end-to-end, and verified locally that the missing contract test described in the issue is genuinely absent. I chose this issue because it has a clear and manageable scope (Tier 1, centered on one test file), addresses a real testing gap in the codebase, and aligns with my previous experience reading existing code and writing unit tests, making it realistic to complete within the four-week timeline.

**Branch name:** test/108-mock-llm-provider-contract

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

## Week 8 — Reproduction & solution planning

**Reproduction commit link:** https://github.com/AddreeBarua/pathreview/commit/f6ac40c

**Reproduction summary:**
Ran `.venv/bin/pytest tests/unit/test_llm_provider_contract.py -v` → 27 passed, then confirmed by reading the file that no test compares the mock provider's output structure against the real OpenAI provider's — the only real-provider coverage is a `hasattr` check, so all tests stay green even if the formats diverge. The reproduction is documented in PLAN.md (committed in f6ac40c).

**PLAN.md link:** https://github.com/AddreeBarua/pathreview/blob/test/108-mock-llm-provider-contract/PLAN.md

**Walkthrough video (recommended):** Not recorded.

**Blockers or open questions:**
None.

## Week 9 — Solution building & PR submission

### Check-in 1 (mid-week)

**Current progress:**
PLAN.md sub-tasks 1–3 complete: added the mocked-OpenAI fixture and the `TestProviderContractParity` class (7 tests) to `tests/unit/test_llm_provider_contract.py`. All 34 tests pass locally (27 existing + 7 new).

**Next steps:**
Run the linter/formatter/type checker on changed files, resolve pre-commit hook findings, and open the PR.

**Blockers:**
The strict mypy pre-commit hook required type annotations on every function in the touched files, including the 27 pre-existing tests — resolved by annotating the whole module.

---

### Check-in 2 (end of week)

**PR link:** https://github.com/jamjamgobambam/pathreview/pull/136

**Branch:** test/108-mock-llm-provider-contract

**What you built:**
A `TestProviderContractParity` test class that mocks the OpenAI client (patched at `openai.OpenAI`, response shaped like the real SDK) so `OpenAIEmbeddingProvider.embed()` can run offline, then asserts both providers return identically structured responses: list type, one vector per input, lists of floats, matching 1536 dimensionality, empty-input handling, batch consistency, and factory return types.

**Tests added or updated:**
`tests/unit/test_llm_provider_contract.py` — 7 new contract parity tests; type annotations added across the module. `ingestion/embeddings/provider.py` — annotation and exception-chaining fixes required by the pre-commit hooks.

**Self-review confirmation:** [x] make check passes  [x] make test-unit passes
(In a codebase with documented pre-existing failures: my changed files pass ruff/black/mypy via the pre-commit hooks, and `make test-unit` shows the same 53 pre-existing failures on `main` and my branch — verified by running the suite on both — with 7 new passes and no new failures from my change.)

**Draft PR feedback received from:** none
