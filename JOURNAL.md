## Week 7 — Issue selection

**Issue link:** [https://github.com/ascherj/pathreview/issues/24]

**Issue title:** [Hybrid retriever over-weights keyword results when query contains technology names #24]

**Tier:** [Tier 2 ]

**Problem summary:**
[ if BM25 score is high from common keywords while its vector score is low, that big BM25 half can still push the chunk's final score high enough to rank it near the top. This will affect the final score leading to a wrong context retrieval because BM25 itself has 50% wait on the entire output or final score.

A successfull fix is to rebalance that 50/50 to trust vector similarity more, or adjust weights based on the query so keyword only matches can't ride into the top results.]

**Affected parts of the codebase:**

- `rag/retriever/hybrid.py` — `HybridRetriever.retrieve()`. This is the core of the issue: the blend happens at `blended_score = self.vector_weight * vector_score + self.keyword_weight * keyword_score`. The weights are hardcoded constructor defaults — this is the single place the weights live and where any rebalancing/adaptive-weighting fix goes. **Fix applied:** rebalanced from 50/50 to **`vector_weight=0.8, keyword_weight=0.2`** so vector (meaning) similarity dominates and keyword-only matches on shared tech terms can't ride into the top results.
- `rag/retriever/keyword_search.py` — `KeywordSearcher.search()`. Produces the BM25 keyword score (via `rank_bm25.BM25Okapi`) that is over-rewarded for common tech terms. Tokenization is a naive lowercase whitespace split, which offers no protection against shared vocabulary across documents.
- `rag/retriever/vector_store.py` — `VectorStore.query()`. Produces the vector similarity score (`similarity = 1 / (1 + distance)` over ChromaDB distances) — the "meaning" half that gets drowned out.
- `rag/generator/review_generator.py` — `_format_context()` / `generate_section()`. The downstream consumer: it assembles the top retrieved chunks into the LLM prompt, so wrong chunks here become wrong context for the model's answer.
- Config: there is **no** weight constant in `core/config.py` or elsewhere — the weights only exist as the defaults in `hybrid.py:14`. Making them configurable is part of a clean fix.
- Caveat: `core/services/review_service.py` (`_run_rag_retrieval_generation()`) is still a placeholder and does not yet call `HybridRetriever`, so the scoring path isn't wired into the live request flow yet.

**Issue Fit and Selection Reasoning:**

- **Right tier / scope.** As a Tier 2 issue it's substantial enough to be meaningful but bounded — the root cause lives in a single function (`HybridRetriever.retrieve()`), so the change surface is small and easy to reason about.
- **Clear, single root cause.** The problem traces cleanly to one thing: the fixed blend weight giving BM25 too much say. There's no ambiguity about *where* to fix it, which lowers the risk of scope creep.
- **Well-understood behavior.** The failure mode (shared tech terms like "React"/"Python" inflating keyword scores and pulling in wrong-document chunks) is concrete and reproducible, making it straightforward to reason about before and after the change.
- **High-impact for low effort.** Retrieval quality directly determines the context the LLM answers from, so a small weight change has an outsized effect on end output quality — a good return on a modest fix.
- **Testable in isolation.** Because scoring is a pure blend of two normalized scores, the fix can be validated at the retriever level without needing the full generation pipeline (which is still a placeholder in `review_service.py`).
- **Room to extend.** The issue also opens a natural follow-up path (making weights configurable, or query-adaptive weighting), so it's a clean foundation rather than a dead-end patch.

**Branch name:** [fix/24-hybrid-scoring-weight-tuning]

**Setup confirmation:** [App runs locally at localhost:5173]

**Cohort ledger:** [Issue added to cohort ledger]
