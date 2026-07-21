## Week 7 — Issue selection

**Issue link:** (https://github.com/ascherj/pathreview/issues/147)

**Issue title:** Resume section detection fails on text with leading whitespace
 

**Tier:** [Y] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The issue talks about the whitespace detection on resume where it is not appropriate. It appears that when working with PDF's, if the output shows inappropraotely whitespaces in education, experience, and certificates. the section-header regex patterns are anchored to ^ / \n without allowing for leading whitespace, so indented resume text (common from PDF extraction) never matches. I'll be checking _strip_markdown() for the same issue while I'm in there. 

**Branch name:** fix/147-resume-parser-index-error

**Setup confirmation:** [Requirement	Minimum	Check command
Git	2.39	git --version
Python	3.11	python --version
Node.js	18	node --version
npm	9	npm --version
Docker	24	docker --version
Docker Compose	2.20	docker compose version
RAM	8 GB	—
Free disk	20 GB	— ] App runs locally at localhost:5173

**Cohort ledger:** [Y] Issue added to cohort ledger