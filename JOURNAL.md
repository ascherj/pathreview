# Module 3 Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/157

**Issue title:** Relevance scorer "partial overlap" test fixture actually has full query overlap

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The `RelevanceScorer` in `rag/evaluator/relevance_scorer.py` scores a chunk by
what fraction of the query's tokens appear in the chunk (`overlap / len(query_tokens)`).
The unit test `test_query_with_partial_overlap` claims to exercise a *partial*
overlap case, but its fixture query "Python Django web framework" is checked
against a chunk ("Django is a Python web framework for rapid development") that
contains all four query tokens — so the scorer correctly returns 1.0, and the
test's assertion `0.3 < score < 0.9` fails against working code. The bug is in
the test fixture, not the scorer. A successful fix rewrites the fixture so the
chunk genuinely covers only some of the query terms, making the assertion pass
because the code is actually producing a mid-range partial score.

**"Is this right for me?" checklist reasoning:**
- *Scope:* Contained to a single test file (`tests/unit/test_relevance_scorer.py`);
  the production scorer stays untouched. Low blast radius.
- *Reproducible:* `pytest tests/unit/test_relevance_scorer.py -q` fails on
  `assert 1.0 < 0.9` — a clear, deterministic repro.
- *Understandable:* I read both the scorer and the test and can explain exactly
  why the assertion is wrong (chunk contains every query token → full coverage).
- *Right size for Tier 1:* Yes — a focused fixture correction plus a green test
  run, no new architecture or cross-module changes.

**Branch name:** test/157-relevance-scorer-partial-overlap

**Setup confirmation:** [ ] App runs locally at localhost:5173
> Pending: Docker Desktop must be running before `docker compose up -d` and
> `make setup`. `.env.example` defaults `LLM_PROVIDER=mock`, so no API key is
> required for local development — just `cp .env.example .env`.

**Cohort ledger:** [ ] Issue added to cohort ledger
> Pending: add name, GitHub username (TaoTDM), and issue #157 to the Section 1A
> tab of the cohort ledger.
