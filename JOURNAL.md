# Module 3 Journal — Addree Barua

## Week 7 — Issue selection

**Issue link:** https://github.com/jamjamgobambam/pathreview/issues/108

**Issue title:** No test verifies that the mock LLM provider returns responses in the expected format

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
PathReview uses two embedding providers: `MockEmbeddingProvider` for local development and testing, and `OpenAIEmbeddingProvider` for the production application. Both providers are expected to return embeddings in the same format so that the mock can accurately replace the real provider during testing. The current test suite (`tests/unit/test_llm_provider_contract.py`) thoroughly tests the mock provider but never verifies that its output matches the structure of the real OpenAI provider — the only test involving the real provider checks that an `embed` method exists, which does not confirm that both providers return compatible responses. As a result, the mock provider could drift away from the real provider over time, allowing all tests to pass while the application fails when using the actual OpenAI service. A successful fix adds a contract test ensuring both providers follow the same interface and output structure, making the test suite more reliable.

**Selection reasoning ("Is this right for me?" checklist):**
I selected Issue #108 after carefully evaluating several Tier 1 issues. I first investigated Issues #107, #123, and #106, but found that one could not be reproduced, another was already outdated because the fix already existed in the Makefile, and the third had already been claimed with an open pull request. Rather than choosing an issue without verifying it, I confirmed that Issue #108 was still unclaimed, reviewed the referenced test file end-to-end, and verified locally that the missing contract test described in the issue is genuinely absent. I chose this issue because it has a clear and manageable scope (Tier 1, centered on one test file), addresses a real testing gap in the codebase, and aligns with my previous experience reading existing code and writing unit tests, making it realistic to complete within the four-week timeline.

**Branch name:** test/108-mock-llm-provider-contract

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
