# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/34

**Issue title:** Implement a re-ranking step that uses an LLM to score retrieved chunks before generation

**Tier:** [ ] Tier 1  [ ] Tier 2  [x] Tier 3

**Problem summary:**
The RAG retriever currently ranks chunks with a purely mechanical score — a
weighted blend of vector cosine similarity and BM25 keyword scores in
`HybridRetriever.retrieve()`. That blended score measures surface-level
similarity, not whether a chunk actually answers the query, so genuinely
relevant chunks can be pushed below the top-k cutoff and passed over before
generation. This issue asks for an optional second-stage re-ranking pass: after
hybrid retrieval produces its candidate set, prompt a smaller LLM to score each
candidate's relevance to the query and reorder them, so the top-k handed to the
generator reflects semantic relevance rather than just lexical/embedding
overlap. A successful fix adds a new `rag/retriever/reranker.py`, wires it into
`hybrid.py` behind a toggle (so the existing behavior stays the default), and is
covered by at least one new unit test — improving answer quality without
breaking the current retrieval path.

**Branch name:** feat/34-llm-chunk-reranking

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

---

### "Is this right for me?" checklist reasoning

**Part 1 — Understanding the issue**
- *Explain in my own words:* Retrieval today ranks chunks only by a blend of
  vector + BM25 scores. I need to add an optional pass where an LLM re-scores the
  retrieved chunks for actual relevance to the query and reorders them before the
  top-k go to the generator. ✅
- *Which part of the app:* The `rag` module — specifically the retriever
  subpackage. Confirmed the referenced files exist:
  `rag/retriever/hybrid.py` (`HybridRetriever.retrieve()` does the current
  blend + sort + top-k), and I'll add the new `rag/retriever/reranker.py`. ✅
- *What "done" looks like:*
  - *Before:* `retrieve()` returns chunks ordered by
    `vector_weight * vector_score + keyword_weight * keyword_score`; a chunk that
    is lexically/embedding-similar but not actually responsive can outrank a
    better one.
  - *After:* with re-ranking enabled, the candidate chunks are re-scored by an
    LLM for query relevance and reordered, so the top-k passed to generation are
    the most genuinely relevant. Re-ranking is opt-in, so the default hybrid path
    is unchanged. ✅

**Part 2 — Tier fit**
- Issue is labeled **tier-3** (rag / AI-pipeline modification). It touches the
  retrieval→generation flow and adds an LLM call, so the tier-3 label is
  accurate. Estimated effort in the issue is 7–10 hours, which fits the Weeks 8–9
  window. I'm accepting the tier-3 scope knowingly (see time note below). ✅

**Part 3 — Codebase readiness**
- *Found and read the specific code:* Read `HybridRetriever.retrieve()` in
  `rag/retriever/hybrid.py` end to end — I can see exactly where the sorted,
  filtered `final_results` are produced (the natural insertion point for a
  re-rank hook, right before returning the top `max_chunks`). ✅
- *Understand surrounding context:* Read the retriever subpackage
  (`vector_store.py`, `keyword_search.py`, `hybrid.py`) and understand the chunk
  dict shape (`id`, `text`, `metadata`, `score`, `vector_score`,
  `keyword_score`), so I can predict what a re-order affects downstream. ✅
- *Read the relevant test file:* Reviewed `tests/unit/test_keyword_search.py`
  (closest existing retriever test) for fixture/assertion/mock patterns. There's
  no dedicated hybrid/reranker test yet, so I'll add at least one new unit test
  for the reranker with the LLM call mocked. ✅

**Part 4 — Scope and time**
- *Others working on it:* Will confirm the Claims count in the cohort ledger and
  the issue comments before/when I claim; I'm fine sharing the issue since grades
  come from my own artifacts. ⬜ (to confirm on the ledger)
- *Realistic for Weeks 8–9:* 7–10h estimate fits my two-week window. ✅
- *Blockers/dependencies:* Issue lists no "blocked by" dependencies; the files it
  references already exist in the repo. ✅

**Verdict:** All understanding/codebase boxes are checked. Remaining actions
before I fully claim: start the dev server to confirm localhost:5173, and add the
issue to the cohort ledger.
