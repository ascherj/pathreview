# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/149

**Issue title:** Structural chunker silently drops documents that contain no headings

**Tier:** [x] Tier 1 [ ] Tier 2 [ ] Tier 3

**Problem summary:**

The structural chunker currently returns an empty list when a document does not contain Markdown headings. This causes valid plain-text documents to be silently excluded from the RAG index. The issue affects `StructuralChunker.chunk()` in the ingestion module. A successful fix should preserve documents without headings by creating a valid chunk or using an appropriate fallback strategy.

**Selection reasoning — “Is this right for me?” checklist:**

This issue is a Tier 1 bug with a clearly identified function and failing unit test. The scope appears limited to the structural chunker and its related tests, so it should not require understanding the entire application. I also have experience with document chunking, embeddings, and RAG projects, which makes the problem relevant to my background. I expect the issue to be realistic to complete within the Week 8–9 timeline.

**Branch name:** `fix/149-handle-documents-without-headings`

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger