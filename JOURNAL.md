# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/153

**Issue title:** Faithfulness checker crashes when a context chunk has `text: None`

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The faithfulness checker (`rag/evaluator/faithfulness_checker.py`) builds the comparison context by calling `chunk.get("text", "")`, assuming that falls back to an empty string whenever a chunk has no usable text. But `dict.get()` only applies its default when the key is missing entirely — if a chunk instead stores `"text": None` (which happens when upstream parsing produces an empty chunk), `.get()` returns `None`, and the later `" ".join(...)` call crashes with a `TypeError`. In practice this means any RAG evaluation run that touches a document with even one malformed or empty chunk fails outright instead of just treating that chunk as having no content. A successful fix makes the checker handle the `None` case explicitly (e.g. `chunk.get("text") or ""`) so evaluation degrades gracefully rather than crashing, confirmed by the already-stubbed `test_none_context_chunk_text` test in `tests/unit/test_faithfulness_checker.py`.

**Scope check (issue checklist reasoning):** Single file to touch (`rag/evaluator/faithfulness_checker.py`), reproduction steps are already given in the issue, a failing test already exists to validate the fix, no new dependencies or schema changes involved, and the estimated effort (2-3 hours) fits a first issue. This made it a safer pick than the ingestion/pipeline issues, which touch multiple files and have less clear-cut reproduction steps.

**Branch name:** fix/153-faithfulness-checker-none-text

**Setup confirmation:** [ ] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger
