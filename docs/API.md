# API Reference

Base URL: `http://localhost:8000`

Authenticated endpoints require a JWT from `POST /auth/login` (or `POST /auth/register`) in the `Authorization: Bearer <token>` header.

## Endpoints

### Health

`GET /health` — Returns service status and dependency health.

### Authentication

`POST /auth/register` — Create a new account.
`POST /auth/login` — Obtain a JWT access token.

### Profiles

`POST /profiles` — Create a profile with resume and GitHub username.
`GET /profiles/{profile_id}` — Retrieve a profile.
`DELETE /profiles/{profile_id}` — Delete a profile and associated data.

#### `POST /profiles` request body

**Auth required.** Content-Type: `multipart/form-data` (form fields and optional file — not JSON).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `github_username` | string | no | GitHub username (max 255 characters) |
| `portfolio_url` | string | no | Portfolio URL (max 500 characters) |
| `resume_file` | file | no | Resume upload; must be PDF or Markdown (`application/pdf`, `text/markdown`, or `text/plain`). Other types return **422**. |

All fields are optional; an empty multipart body is a valid create request.

Example field values:

```text
github_username=octocat
portfolio_url=https://octocat.dev
resume_file=@./resume.pdf
```

### Reviews

`POST /reviews` — Request a new portfolio review for a profile.
`GET /reviews/{review_id}` — Retrieve a completed review.
`GET /reviews` — List reviews for the authenticated user (paginated).

#### `POST /reviews` request body

**Auth required.** Content-Type: `application/json`.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `profile_id` | UUID | yes | ID of the profile to review |

Example:

```json
{
  "profile_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

## Interactive Docs

When the API is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
