# Error Contract

Errors use a safe, stable envelope. Responses never include stack traces, internal prompts, credentials, raw provider errors, hidden reasoning, or database details.

```json
{
  "error": {
    "code": "validation_error",
    "message": "Please check the highlighted fields.",
    "fields": {
      "term_months": "Term must be greater than zero."
    }
  }
}
```

Recommended status mapping:

| Status | Codes | Use |
|---|---|---|
| `400` | `invalid_request` | Malformed or semantically invalid request |
| `401` | `authentication_required`, `invalid_credentials` | Missing/invalid session or login credentials |
| `404` | `not_found` | Missing or unowned resource |
| `409` | `conflict` | Duplicate account or favourite, if not idempotent |
| `422` | `validation_error` | Field-level validation failure |
| `429` | `rate_limited` | Optional provider or request limit |
| `500` | `internal_error` | Safe fallback for unexpected server failures |
| `503` | `provider_unavailable` | AI or retrieval dependency unavailable |

The frontend should render `message` and field errors, while logs retain a correlation identifier and server-side diagnostic context without exposing it to the user.

## `GET /health`

Response `200`:

```json
{
  "status": "ok",
  "service": "ai-car-advisor"
}
```

The health response must not expose secrets, filesystem paths, database credentials, or model prompts.
