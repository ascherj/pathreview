# PLAN.md — Issue #108: Contract test for mock LLM provider response format

**Issue:** https://github.com/jamjamgobambam/pathreview/issues/108
**Branch:** test/108-mock-llm-provider-contract

## Problem

`ingestion/embeddings/provider.py` defines two providers behind one interface:
`MockEmbeddingProvider` (used in tests and local dev via `LLM_PROVIDER=mock`) and
`OpenAIEmbeddingProvider` (production, calls the OpenAI embeddings API). The existing
test file `tests/unit/test_llm_provider_contract.py` (27 tests, all passing) exercises
the mock provider in isolation. The only coverage of the real provider is
`hasattr(OpenAIEmbeddingProvider, 'embed')`, which checks a method exists but says
nothing about its response structure. If either provider's output format drifts, the
test suite stays green while the application breaks with the real provider.

## Reproduction

Ran `.venv/bin/pytest tests/unit/test_llm_provider_contract.py -v` → 27 passed.
Confirmed by reading the file that no test compares mock output structure against
real provider output structure. The real provider is never instantiated or exercised.

## Planned fix

Add a `TestProviderContractParity` class to `tests/unit/test_llm_provider_contract.py`
that verifies both providers honor the same contract, without requiring a real API key:

1. **Mock the OpenAI client** using `unittest.mock` so `OpenAIEmbeddingProvider.embed()`
   can be exercised in a unit test. The mocked client returns a realistic response
   object shaped like the OpenAI SDK's (`response.data[i].embedding` = list of floats).
2. **Structural parity tests:** for the same input texts, assert both providers return
   (a) a list, (b) one vector per input text, (c) vectors as lists of Python floats,
   (d) equal dimensionality (1536), and (e) `[]` for empty input.
3. **Factory contract:** assert `get_embedding_provider("mock")` and
   `get_embedding_provider("openai")` both return `EmbeddingProvider` instances.

## Files to change

- `tests/unit/test_llm_provider_contract.py` — add contract parity test class (only file)

## Risks / considerations

- The OpenAI client must be mocked at the right import point (`openai.OpenAI`) so no
  network call or API key is needed; tests must stay fast and offline.
- Tests must follow existing patterns: `@pytest.mark.unit`, class-based, docstrings,
  and pass `make check` (ruff, black, mypy).

## Definition of done

- New contract tests fail if either provider's response structure diverges.
- `make check` and `make test-unit` pass.
- PR references issue #108 and follows CONTRIBUTING.md conventions.
