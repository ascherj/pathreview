# PathReview Development Journal

## Week 7

_(No Week 7 entry in this clone yet. Week 8 work continues on branch `week8/b-20-offline-eval`.)_

---

## Week 8 — Reproduction & solution planning

**Issue:** B-20 — Implement an offline eval runner that measures review quality across a benchmark portfolio set

**Reproduction commit link:** _(filled after push — see latest commit on this branch)_

**Reproduction summary:**
Ran `python3 scripts/run_evals.py`. The script prints that evaluation is complete and that results were written to `eval_results.json`, but the file is never created. There is also no `tests/fixtures/sample_profiles/` directory, and `EvalResult` has no `actionability_score` despite the stub TODO. Three failing tests in `tests/unit/test_run_evals_reproduction.py` lock this gap in.

**PLAN.md link:** [PLAN.md](./PLAN.md) on branch `week8/b-20-offline-eval`

**Walkthrough video (recommended):** _(optional — record ≤2 min Loom if desired)_

**Blockers or open questions:**
- No chat/mock LLM exists for `ReviewGenerator` (only mock embeddings). Week 9 plan uses a deterministic mock generator inside the runner when `LLM_PROVIDER=mock`.
- `HybridRetriever` never indexes BM25 before search — will fix as part of the offline pipeline so hybrid retrieval actually runs.

### What I observed

```text
$ python3 scripts/run_evals.py
Running RAG evaluation suite...
Evaluation complete. Results written to eval_results.json

$ ls eval_results.json
# → No such file or directory

$ ls tests/fixtures/sample_profiles/
# → No such file or directory

$ python3 -m pytest tests/unit/test_run_evals_reproduction.py -v
# → 3 failed (documents missing report file, fixtures, actionability field)
```

### Where the gap lives

| Location | Gap |
|----------|-----|
| `scripts/run_evals.py` | Stub only — TODOs, no real pipeline or file write |
| `rag/evaluator/eval_suite.py` | Relevance + faithfulness only; no actionability |
| `tests/fixtures/sample_profiles/` | Missing entirely |
| `.github/workflows/eval.yml` | Already expects `eval_results.json` after the stub runs |
