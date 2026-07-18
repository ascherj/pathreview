# API Reference

Base URL: `http://localhost:8000`

Start PathReview with `make run` before using these examples.

## Before you begin

The examples below use shell variables so that the commands are easier to
copy and reuse.

```bash
export API_URL="http://localhost:8000"
export TOKEN="<access-token>"
export PROFILE_ID="<profile-id>"
export REVIEW_ID="<review-id>"
```

Obtain `TOKEN` by registering or logging in. Obtain `PROFILE_ID` and
`REVIEW_ID` from the responses returned when creating a profile and review.

## Health

### Check service health

`GET /health` returns the service status and dependency health.

```bash
curl --request GET "${API_URL}/health"
```

The endpoint may return `503 Service Unavailable` when a required local
dependency, such as PostgreSQL or Redis, is not running.

## Authentication

### Register an account

`POST /auth/register` creates a new account and returns a JWT access token.

```bash
curl --request POST "${API_URL}/auth/register" \
  --header "Content-Type: application/json" \
  --data '{
    "email": "new.user@example.com",
    "password": "password123"
  }'
```

Use a different email address if the example account has already been
registered.

### Log in

`POST /auth/login` accepts OAuth2 form data rather than JSON. The `username`
field contains the user's email address.

```bash
curl --request POST "${API_URL}/auth/login" \
  --header "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=user1@example.com" \
  --data-urlencode "password=password1"
```

Copy the `access_token` value from the response:

```bash
export TOKEN="<paste-access-token-here>"
```

Protected endpoints below require this header:

```text
Authorization: Bearer <access-token>
```

## Profiles

### Create a profile

`POST /profiles` creates a profile using multipart form data. The GitHub
username, portfolio URL, and resume file are optional.

```bash
curl --request POST "${API_URL}/profiles" \
  --header "Authorization: Bearer ${TOKEN}" \
  --form "github_username=octocat" \
  --form "portfolio_url=https://example.com" \
  --form "resume_file=@./resume.md;type=text/markdown"
```

The resume must be a PDF, Markdown, or plain-text file. Omit the
`resume_file` line when testing without a resume.

Copy the profile `id` from the response:

```bash
export PROFILE_ID="<paste-profile-id-here>"
```

### Retrieve a profile

`GET /profiles/{profile_id}` returns a profile owned by the authenticated
user.

```bash
curl --request GET "${API_URL}/profiles/${PROFILE_ID}" \
  --header "Authorization: Bearer ${TOKEN}"
```

### Delete a profile

`DELETE /profiles/{profile_id}` deletes the profile and its associated data.

Run this example after finishing the review examples below because they
depend on an existing profile.

```bash
curl --request DELETE "${API_URL}/profiles/${PROFILE_ID}" \
  --header "Authorization: Bearer ${TOKEN}"
```

A successful deletion returns `204 No Content` with an empty response body.

## Reviews

### Create a review

`POST /reviews` starts a portfolio review for an existing profile.

```bash
curl --request POST "${API_URL}/reviews" \
  --header "Authorization: Bearer ${TOKEN}" \
  --header "Content-Type: application/json" \
  --data "{\"profile_id\":\"${PROFILE_ID}\"}"
```

The initial response normally has a pending status because review processing
runs asynchronously.

Copy the review `id` from the response:

```bash
export REVIEW_ID="<paste-review-id-here>"
```

### Retrieve a review

`GET /reviews/{review_id}` returns a review owned by the authenticated user.

```bash
curl --request GET "${API_URL}/reviews/${REVIEW_ID}" \
  --header "Authorization: Bearer ${TOKEN}"
```

### List reviews

`GET /reviews` lists reviews belonging to the authenticated user. The
`page` and `page_size` query parameters control pagination.

```bash
curl --request GET "${API_URL}/reviews?page=1&page_size=20" \
  --header "Authorization: Bearer ${TOKEN}"
```

## Interactive documentation

When the API is running, additional interactive documentation is available
at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc