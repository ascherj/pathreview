## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/149

**Issue title:** Structural chunker silently drops documents that contain no headings

**Tier:** [x] Tier 1 [ ] Tier 2 [ ] Tier 3

**Problem summary:**

The structural chunker doesn't handle documents that don't contain Markdown headings. Instead of creating at least one chunk, it returns an empty list, so those documents are skipped, and they never make it into the RAG index. This affects the ingestion pipeline because plain text documents cannot be processed correctly.

A successful fix would make sure documents without headings still get chunked, such as by treating the whole document as a single chunk or using a fallback approach.

**Branch name:** fix/149-structural-chunker-no-headings

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger
