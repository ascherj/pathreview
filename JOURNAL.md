## Week 7 — Issue selection

**Issue link:** (https://github.com/ascherj/pathreview/issues/146)

**Issue title:** [PII scrubber fails to redact parenthesized US phone numbers
 #146

**Tier:** [X] Tier 1  [ ] Tier 2  [ ] Tier 3

**Problem summary:**
The PII scrubber currently recognizes US phone numbers written with dashes (such as 555-123-4567), but it does not detect or redact the common parenthesized format (555) 123-4567. As a result, scrub() leaves these numbers unredacted, and detect() incorrectly reports that no PII is present. This issue affects the phone number matching logic in pii_scrubber.py. A successful fix would update the phone number pattern so both dashed and parenthesized US phone number formats are correctly detected and redacted, allowing the related unit tests to pass.

**Branch name:** fix/146-pii-scrub-phone-num

**Setup confirmation:** [X] App runs locally at localhost:5173

**Cohort ledger:** [X] Issue added to cohort ledger