# Architecture

The project is a small monorepo with one browser application, one FastAPI application, and one local MCP process.

## Request flow

The React client sends credentialed requests to `/api`. FastAPI resolves the opaque HttpOnly session, applies ownership predicates, and delegates to services. Vehicle facts come from the Markdown catalog; the advisor can rank only catalog vehicles. The REST calculators and MCP tools both call the same deterministic functions.

## Persistence

SQLite stores users, sessions, conversations, messages, preference state, and favourites. Alembic owns schema history. Runtime databases and Chroma data live under `.local/` and are ignored by source control.

## AI boundary

`backend/app/agents/advisor.py` is the single orchestration boundary. It accepts structured preferences and catalog evidence, returns bounded visible results, and never persists internal reasoning or provider traces. `GeminiProvider` is injectable and optional so tests do not need an API key.

## Catalog and retrieval

The source of truth is `backend/data/cars/*.md`. `CatalogService` validates stable identifiers and normalized metadata. `CatalogRetriever` is the local retrieval seam; deterministic embeddings support offline tests and can be replaced by a Chroma-backed implementation without changing API contracts.

## Security and errors

Passwords are Argon2id hashes. Session tokens are generated once, hashed at rest, and sent only as HttpOnly `SameSite=Lax` cookies. User-owned resources are queried by both resource ID and current user ID. Public errors use a small `{error:{code,message,fields}}` envelope.
