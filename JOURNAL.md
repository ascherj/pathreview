## Week 7 — Issue selection

**Issue link:** [https://github.com/ascherj/pathreview/issues/149]

**Issue title:** [Structural chunker silently drops documents that contain no headings
]

**Tier:** [#] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**

The function, StructuralChunker.chunk(), returns an empty list for any document without markdown headings, and it removes the entire document from the RAG index instead of being it chunked as a single block or falling back to another strategy. I will reproduce the error and then work with the test_document_with_no_headings in tests/unit/test_structural_chunker.py to show a successful fix

**Branch name:** [149-structural-chunker-silently-drops-documents-that-contain-no-headings]

**Setup confirmation:** [#] App runs locally at localhost:5173

**Cohort ledger:** [#] Issue added to cohort ledger