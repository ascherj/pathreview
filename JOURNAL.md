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

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger

---

### "Is this right for me?" checklist reasoning

- **Understand it:** I can explain it in my own words (add an optional LLM
  re-scoring pass over the hybrid-retrieved chunks before the top-k reach the
  generator), located the referenced files (`rag/retriever/hybrid.py` + new
  `reranker.py`), and can describe the before/after behavior. 
- **Tier fit:** Labeled **tier-3** (RAG/AI-pipeline change); 7–10h estimate fits
  the Weeks 8–9 window and I'm accepting that scope knowingly. 
- **Codebase readiness:** Read `HybridRetriever.retrieve()` and the retriever
  subpackage end to end, so I know the chunk dict shape and the insertion point
  for the re-rank hook; reviewed `tests/unit/test_keyword_search.py` for test
  patterns and will add a new unit test with the LLM mocked. 
- **Scope & time:** No blockers or dependencies, the files already exist, and the
  estimate is realistic for my two weeks; still need to confirm the Claims count
  on the ledger. 

**Verdict:** Understanding and codebase boxes checked. Remaining actions: confirm
localhost:5173 runs and add the issue to the cohort ledger.
