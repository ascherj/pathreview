## Week 7 — Issue selection

**Issue link:** [[Issue Link](https://github.com/ascherj/pathreview/issues/147)]

**Issue title:** Resume section detection fails on text with leading whitespace
 #147

**Tier:** [x] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
_detect_sections() in resume_parser.py identifies resume sections (Education, Skills, Experience, etc.) by matching each section keyword against patterns anchored with ^ or \n, using re.MULTILINE so ^ matches at the start of every line. The bug is that these patterns expect the keyword to appear immediately at that line-start position, with no allowance for leading whitespace — so text like "    Education:" (common in PDF-extracted text, which often preserves indentation) never matches, even though re.MULTILINE is correctly making ^ check every line. As a result, detected_sections comes back empty for indented resume text, even when section headers are clearly present. A successful fix would update the patterns (e.g. adding \s* after ^/\n) so section headers are still recognized when preceded by leading whitespace, without introducing false positives. This affects the _detect_sections method in ingestion/parsers/resume_parser.py.

**Branch name:** fix/147-resume-section-leading-whitespace

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [x] Issue added to cohort ledger