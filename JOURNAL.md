# Module 3 Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/148

**Issue title:** Skill extractor fails to detect JavaScript and TypeScript

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The skill extractor in the ingestion pipeline is supposed to look at source
text and report which languages, frameworks, and tools a candidate has used,
but its JavaScript/TypeScript detection almost never fires. In
`ingestion/parsers/skill_extractor.py`, `_detect_languages()` only flags JS when
the filename ends in `.js`/`.ts` or when the text matches `\b(import|require)\s+`
— so a real call like `require('fs')` (no space before the paren) slips through,
and TypeScript is only ever labeled from a `.ts` filename, never from actual TS
syntax such as `interface` or type annotations. As a result the extractor
returns an empty or Python-only list for clearly JS/TS code, and several unit
tests (`test_javascript_detection`, `test_text_with_typescript_files`) fail. A
successful fix makes detection content-based — recognizing JS/TS from
`require(...)` calls, `export`/`const`/arrow-function/`async` usage, and TS-only
signals like `interface` and typed declarations — so the four failing tests pass
without breaking the existing Python detection.

**Branch name:** fix/148-skill-extractor-js-ts

**Setup confirmation:** [ ] App runs locally at localhost:5173
<!-- Pending: this machine has no Docker installed and no .env yet. To confirm:
     install Docker Desktop, `cp .env.example .env` and add OPENROUTER_API_KEY,
     then `docker compose up -d && make setup && make run`, and check the box. -->

**Cohort ledger:** [ ] Issue added to cohort ledger
<!-- Pending: add name + GitHub username (ktran37) + issue #148 on your
     section's tab of the cohort ledger, then check this box. -->

### "Is this right for me?" checklist — scope reasoning

- **Tier 1 / good first issue:** Yes — labeled `tier-1`, `good first issue`,
  `ingestion`. Appropriate as a first contribution to a large codebase.
- **Self-contained:** The change is confined to one module,
  `ingestion/parsers/skill_extractor.py` (the `_detect_languages` method), with
  no API, database, or frontend changes required.
- **Clear definition of done:** Four named failing tests in
  `tests/unit/test_skill_extractor.py` (`test_javascript_detection`,
  `test_text_with_typescript_files`, `test_devops_tool_detection`,
  `test_docker_compose_detection`) define exactly when the fix is complete.
- **Reproducible:** The issue includes concrete repro snippets, and I can run
  the affected tests locally with `make test-unit`.
- **Estimated effort:** 2–3 hours per the issue label — realistic for the
  scope of extending the detection patterns.
