## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/69
**Issue title:** Add a "feedback tone check" that ensures all generated feedback is written constructively
**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
The review pipeline generates feedback using an LLM but has no mechanism to verify that the output is actually constructive. The existing `ContentFilter` only blocks genuinely harmful content (e.g., self-harm phrases) — it does not catch feedback that is vague, discouraging, or dismissive. A successful fix adds a tone classification step after generation that uses an LLM-as-judge pattern to classify each feedback section as constructive or negative, and rejects or regenerates sections that fail the check. The affected code spans `safety/content_filter.py` and `rag/generator/review_generator.py`.

**Branch name:** feat/69-feedback-tone-check
**Setup confirmation:** [x] App runs locally at localhost:5173
**Cohort ledger:** [x] Issue added to cohort ledger
