# Plan — Issue #152

## Issue
Faithfulness checker can never mark short claims as supported.

## Goal
Identify why short claims are always classified as unsupported and update the checker so supported short claims can pass without weakening the validation for unsupported claims.

## Steps
1. Locate the faithfulness checker implementation.
2. Find the tests related to faithfulness or claim support.
3. Reproduce the bug using a short supported claim.
4. Identify the condition causing short claims to fail.
5. Update the implementation.
6. Add or update tests for:
   - A short supported claim
   - A short unsupported claim
   - A longer supported claim
7. Run the test suite and confirm nothing else breaks.

## Expected Files
To be determined after reviewing the repository.

## Risks
The fix could make the checker too permissive, so tests should confirm unsupported short claims still fail.