# Authentication Contract

All endpoints are rooted at `/api`. Protected endpoints use the server-managed `HttpOnly` session cookie. The browser does not send a user ID as an authority.

## `POST /api/auth/register`

Create an account and establish an authenticated session.

Request:

```json
{
  "name": "Asha Rao",
  "email": "asha@example.com",
  "password": "a-strong-password"
}
```

Response `201`:

```json
{
  "user": {
    "id": "user-id",
    "name": "Asha Rao",
    "email": "asha@example.com"
  }
}
```

The response sets the session cookie. Duplicate normalized email returns `409` with the safe error envelope.

## `POST /api/auth/login`

Request:

```json
{
  "email": "asha@example.com",
  "password": "a-strong-password"
}
```

Response `200` has the same public user shape and sets a new session cookie. Invalid credentials return a generic `401` without revealing whether the email exists.

## `POST /api/auth/logout`

Requires an active session. Revokes the current session and clears the cookie. Response `204`.

## `GET /api/auth/me`

Requires an active session. Response `200`:

```json
{
  "id": "user-id",
  "name": "Asha Rao",
  "email": "asha@example.com"
}
```

Unauthenticated requests return the safe `401` error envelope.
