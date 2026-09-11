# Research: AI Car Advisor

## Scope

This research resolves implementation choices for the approved feature specification. It follows the project constitution, the product requirements document, and the requirements checklist. The application is a local capstone web application, so choices favor understandable boundaries, deterministic tests, and minimal operational infrastructure.

## Backend and Frontend Boundaries

**Decision:** Use one monorepo with three deliberately small boundaries:

- `frontend/`: React, Vite, TypeScript, and the API client.
- `backend/`: FastAPI modular monolith containing authentication, persistence, catalog access, retrieval, one LangChain agent, and response shaping.
- `mcp/`: one local MCP server exposing the EMI and fuel-cost tools.

The backend is the only application service. The frontend never accesses SQLite, ChromaDB, Gemini, or MCP directly. The canonical calculator functions live in a backend domain module and are called by both REST endpoints and MCP adapters.

**Rationale:** This keeps product state, AI orchestration, and UI responsibilities easy to locate while satisfying the required Python/FastAPI and MCP stack. It also avoids duplicating arithmetic or exposing credentials to the browser.

**Alternatives considered:** Separate auth, catalog, RAG, and recommendation services were rejected as unnecessary for the capstone. A Next.js-only application was rejected because it would duplicate the required Python AI backend. Multiple specialized agents were rejected by the constitution.

## Frontend Framework

**Decision:** Use React with Vite and TypeScript. Configure the Vite development server to proxy `/api` requests to FastAPI.

**Rationale:** The product is an authenticated application and has no stated SEO or server-rendering requirement. Vite provides a quick local loop while the proxy gives the browser a same-origin API experience during development.

**Alternatives considered:** Next.js and server-rendered templates were considered but rejected because the mandated FastAPI backend already owns server-side application behavior.

## Authentication and Ownership

**Decision:** Use email/password authentication with Argon2id password hashing and opaque server-side sessions stored in SQLite. The browser receives an HttpOnly cookie with an expiry, `SameSite=Lax`, and `Secure` enabled outside local HTTP development.

Normalize emails before the unique constraint. Store only a hash of each session token. Every protected query includes the current user ID. Conversations and messages are isolated by ownership; unauthorized resource lookups use a generic `404` where appropriate. Favourites have a unique `(user_id, vehicle_id)` pair.

**Rationale:** Server-side sessions make logout and revocation explicit and keep bearer tokens out of browser JavaScript. Query-level ownership checks prevent identifier substitution and satisfy cross-user isolation requirements.

**Alternatives considered:** JWTs in local storage were rejected because JavaScript-readable tokens increase theft impact. OAuth/social login is outside the first-release scope. Cookie JWTs were deferred because session rows are simpler to revoke in a small SQLite application.

## SQLite Persistence

**Decision:** Use SQLAlchemy 2 with explicit models and Alembic migrations. Use synchronous database sessions initially. Persist `User`, `AuthSession`, `Conversation`, `Message`, `ConversationPreference`, and `Favourite` with UTC timestamps, indexed foreign keys, and database-level uniqueness constraints.

Vehicle profiles remain canonical in curated Markdown documents with stable slugs in front matter. ChromaDB stores chunks and retrieval metadata. Recommendations, comparisons, and financial estimates are response DTOs or transient service results; the visible assistant message is the durable conversation record.

**Rationale:** SQLite fits the expected local workload and avoids external infrastructure. SQLAlchemy and migrations provide clear ownership relationships and a path for schema evolution without duplicating the vehicle catalog in the application database.

**Alternatives considered:** `create_all()` without migrations was rejected because schema changes would be fragile. PostgreSQL and storing the full catalog in SQLite were rejected by the constitution and source-of-truth requirements.

## Curated Catalog and Ingestion

**Decision:** Store one manually curated Markdown document per vehicle under `backend/data/cars/`. Use front matter for machine-readable fields such as slug, price range, fuel type, transmission, body type, and seating capacity, with Markdown sections for readable guidance. The ingestion command validates every document, creates semantic section chunks, attaches normalized metadata, and idempotently upserts stable document IDs into one local ChromaDB collection.

Invalid documents fail ingestion rather than producing partial catalog data. A catalog release identifier and ingestion manifest may be recorded for reproducibility, while generated ChromaDB data remains runtime output.

**Rationale:** This preserves an editable, reviewable catalog for approximately 30 Indian vehicles and supports semantic retrieval, hard metadata filters, repeatable rebuilds, and precise source attribution.

**Alternatives considered:** JSON/YAML-only files, one large catalog file, live scraping, and a second catalog database were rejected because they reduce readability, violate scope, or create an unwanted second source of truth.

## ChromaDB Retrieval

**Decision:** Use one persistent local ChromaDB collection. Combine semantic similarity with metadata filters for hard constraints, return bounded evidence containing vehicle ID, section, metadata, and content, group chunks by vehicle, remove duplicates, and cap user-facing recommendations at three vehicles.

If exact filters produce no matches, report the empty result to the agent so it can explain the constraint or ask permission to broaden it. Do not silently discard hard preferences.

**Rationale:** Metadata filtering is required for constraints such as EV-only, automatic transmission, budget, or seating capacity; semantic similarity handles natural-language fit. Vehicle-level consolidation makes the result stable for structured responses.

**Alternatives considered:** Pure vector search cannot reliably enforce hard constraints. Keyword-only search cannot represent natural-language fit. A second search engine or vector store is prohibited.

## One LangChain Agent and Gemini Adapter

**Decision:** Run one LangChain agent per assistant request. It receives bounded conversation context, structured active preferences, and retrieved vehicle evidence. It may use retrieval, EMI, and fuel-cost capabilities, but it cannot invent catalog fields or perform financial arithmetic.

Create Gemini through one provider adapter. Read API key, model name, temperature, and output limits from environment variables. Return a structured result with a bounded kind such as `ask_followup`, `recommend`, `compare`, or `calculation`. Validate vehicle IDs and fields against retrieved catalog evidence before display or persistence.

**Rationale:** One orchestration path satisfies the constitution and gives tests a small boundary. Structured results let the frontend render recommendation cards and actions without parsing prose.

**Alternatives considered:** Multiple agents, direct unstructured Gemini calls, and a fully deterministic rules engine were rejected because they add complexity or cannot support natural-language follow-up and explanation.

## MCP Calculator Tools

**Decision:** Implement EMI and fuel-cost formulas once as pure validated Python functions. Expose exactly two MCP tools, `calculate_emi` and `calculate_fuel_cost`, and make both REST calculators call the same functions. Validate finite values, reject invalid or non-positive inputs, allow zero annual interest, and return numeric results rounded to two decimal places.

The model may extract inputs and explain results but never computes them. Tool responses include normalized inputs, outputs, and safe validation errors.

**Rationale:** A single calculation boundary guarantees consistent results in dedicated and conversational flows and keeps deterministic mathematics outside the model.

**Alternatives considered:** Model-generated arithmetic, duplicated API/MCP formulas, and text-only tool responses were rejected because they are less reliable or harder to validate.

## Context Window Management

**Decision:** Store complete conversations in SQLite but send bounded context to Gemini. Preserve active preferences, unresolved follow-up state, and recent vehicle IDs in structured context. Pack input in this priority order: safety and grounding instructions, current user message, active structured state, retrieved evidence, and recent complete turns. Truncate only at message boundaries and reserve output capacity.

Start with a configurable 8,000-token input budget and approximately 1,500 tokens of reserved output capacity; tune after fixture tests.

**Rationale:** Users retain their full history while prompts remain predictable. Structured preferences preserve facts such as budget and daily distance after older turns leave the prompt.

**Alternatives considered:** Sending full history grows without bound. Keeping only the latest messages loses important constraints. A second summarization agent or external memory service adds unnecessary model and infrastructure failure paths.

## Testing Strategy

**Decision:** Make model, retriever, embeddings, MCP client, and database dependencies injectable. CI uses fake Gemini responses, deterministic embeddings or a fake vector-store adapter, temporary SQLite, and temporary ChromaDB. Test invariants such as supported vehicle IDs, calculator tool usage, ownership isolation, and safe errors rather than exact generated prose.

Test layers include pure calculator/context/parser tests, API and persistence integration tests, OpenAPI/Pydantic contract checks, ingestion and retrieval fixtures, mocked-agent tests, React Testing Library/Vitest tests, and one optional Playwright smoke journey.

**Rationale:** Core correctness stays reproducible without a Gemini key, network access, or model wording stability. A manual opt-in smoke test can still exercise real Gemini locally.

**Alternatives considered:** Live Gemini calls in CI, exact prose snapshots, and end-to-end-only testing were rejected as costly, flaky, and difficult to localize.

## Development Defaults

**Decision:** Standardize on Python 3.11 and Node.js 20 LTS. Use `backend/.env.example` or a root `.env.example`, commit dependency lock information, ignore `.env`, `.local/`, caches, SQLite files, and ChromaDB data. Run FastAPI at `http://localhost:8000`, Vite at `http://localhost:5173`, SQLite at `.local/app.db`, and ChromaDB at `.local/chroma/`.

**Rationale:** These defaults support a reproducible local and GitHub Actions workflow without Docker or hosted services. CI can validate all deterministic paths without external credentials.

**Alternatives considered:** Docker Compose, hosted databases/vector stores, and a deployed MCP service were deferred because the first release has no external service requirement.

## Resolved Defaults

- Vehicle identity is a stable slug such as `tata-nexon-2025`, shared by Markdown, ChromaDB metadata, API responses, comparisons, and favourites.
- Conversation preferences are conversation-scoped with latest-value-wins updates; a global profile is optional and not required for MVP.
- Ordinary JSON responses are the initial transport. Streaming is deferred until persistence, retries, and error handling are stable.
- The exact supported LangChain Gemini package and model are selected during implementation and kept configurable behind the provider adapter.
- Initial retrieval tuning targets section chunks of roughly 300-700 tokens, about eight retrieved chunks, and at most three distinct vehicle candidates; fixture tests determine final values.
