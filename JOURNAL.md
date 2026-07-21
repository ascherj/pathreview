# PathReview Contribution Journal

## Week 7 — Issue selection

**Issue link:** https://github.com/ascherj/pathreview/issues/86

**Issue title:** Add an API rate limiting header (`X-RateLimit-Remaining`) to responses

**Tier:** [ ] Tier 1  [x] Tier 2  [ ] Tier 3

**Problem summary:**
The API already enforces a rolling-window rate limit through `safety/rate_limiter.py`,
but that logic isn't actually wired into any request path, and clients have no way to
know how close they are to the limit until a request suddenly returns a 429. This
issue asks for a middleware in `api/middleware/` that calls into the existing
`RateLimiter` on every request and attaches standard `X-RateLimit-Limit` and
`X-RateLimit-Remaining` headers to the response, following the same pattern as the
existing `RequestIDMiddleware`. A successful fix lets API clients proactively back off
before hitting the limit instead of discovering it via failed requests.

**Branch name:** feat/86-rate-limit-headers

**Setup confirmation:** [x] App runs locally at localhost:5173

**Cohort ledger:** [ ] Issue added to cohort ledger

**Scope reasoning (Is this right for me? checklist):**
- The affected files (`api/middleware/`, `safety/rate_limiter.py`) were explicitly
  named in the issue, and the estimated effort (3-5 hours) matched what I found once
  I read the code: `RateLimiter.check_rate_limit` already returns `(allowed, remaining)`,
  so the missing piece is purely the middleware wiring, not new rate-limiting logic.
- There was a clear existing pattern to follow (`RequestIDMiddleware` in
  `api/middleware/request_id.py`), which de-risked the implementation approach.
- Several other cohort members had also commented interest on this issue; since the
  tracker doesn't formally assign issues, I claimed it via comment and proceeded,
  noting the possibility of an overlapping PR later in review.
