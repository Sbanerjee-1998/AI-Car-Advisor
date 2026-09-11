# Quickstart: AI Car Advisor

This guide describes the intended local workflow for the first implementation. It is a validation guide, not a substitute for the application code or complete test suite.

## Prerequisites

- Linux or another environment with Python 3.11.
- Node.js 20 LTS and npm.
- GitHub Actions-compatible command-line tooling for local CI checks.
- A Gemini API key only for real provider smoke tests. Deterministic tests do not need it.

## Repository Setup

From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
npm --prefix frontend install
```

Create a local environment file from the committed example and set at least:

```text
DATABASE_URL=sqlite:///./.local/app.db
CHROMA_PATH=./.local/chroma
GEMINI_API_KEY=
GEMINI_MODEL=<configured-model-name>
GEMINI_TEMPERATURE=0.2
FRONTEND_ORIGIN=http://localhost:5173
SESSION_COOKIE_SECURE=false
```

Keep the real `.env` out of version control. In local development, `.local/app.db` and `.local/chroma/` are disposable runtime artifacts.

## Initialize Data

Run database migrations, then ingest the curated catalog:

```bash
mkdir -p .local
alembic -c backend/alembic.ini upgrade head
python -m backend.app.rag.ingest --source backend/data/cars --chroma-path .local/chroma
```

Ingestion must validate every Markdown file and fail rather than partially index an invalid catalog. Re-running ingestion should be idempotent for unchanged stable slugs.

## Start Local Services

Start FastAPI:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

Start the Vite frontend in another terminal:

```bash
npm --prefix frontend run dev -- --host 127.0.0.1
```

The frontend should be available at `http://localhost:5173` and proxy `/api` requests to `http://localhost:8000`. The local MCP server uses stdio and is launched or managed by the backend agent integration; it is not a public browser service.

Check the API:

```bash
curl http://localhost:8000/health
```

Expected shape:

```json
{"status":"ok","service":"ai-car-advisor"}
```

## Test and Build Commands

Backend checks:

```bash
pytest backend/tests mcp/tests
```

Frontend checks:

```bash
npm --prefix frontend run test
npm --prefix frontend run build
```

The CI workflow should also run formatting/lint checks and, where configured, a Playwright smoke test against local services. No CI command should require a Gemini key.

## Acceptance Flows

### Authentication and ownership

1. Register a user and verify the session remains active after a page refresh.
2. Log out and verify protected endpoints reject the old session.
3. Create a conversation and a favourite for user A.
4. Authenticate as user B and verify neither resource is visible, editable, or deletable.

### Recommendation and follow-up

1. Start a new chat.
2. Send a vague request such as “Help me choose a car.”
3. Verify the assistant asks a small number of useful follow-up questions.
4. Provide budget, usage, powertrain, and other preferences.
5. Verify the response contains at most three recommendations with grounded fit explanations, advantages, considerations, approximate pricing/specifications, and the verification disclaimer.
6. Change a preference and verify the latest explicit value controls subsequent recommendations.

### Grounding and retrieval

1. Ingest the curated Markdown catalog.
2. Search or ask for a constrained powertrain/body type/budget combination.
3. Verify returned vehicle IDs resolve to catalog documents and hard filters are respected.
4. Verify missing catalog fields render as unavailable or not applicable.
5. Verify no live web scraping is performed and no unsupported specification is displayed.

### History, comparison, and favourites

1. Reopen a previous conversation and verify visible messages and preference state persist.
2. Compare exactly two or three known vehicles.
3. Save one vehicle, reload the favourites view, and remove it.
4. Verify duplicate favourites are handled consistently and unknown vehicle IDs fail safely.

### EMI and fuel cost

1. Calculate EMI with a positive interest rate and verify the result against the pure calculator function.
2. Calculate EMI with zero interest and verify principal divided by term.
3. Submit invalid and negative values and verify field-level safe errors.
4. Calculate fuel cost and verify distance, efficiency, and price handling.
5. Trigger the same calculations through conversational tool use and verify REST and MCP results agree.

### CI and provider isolation

1. Run the complete test suite without `GEMINI_API_KEY`.
2. Verify fake Gemini, embeddings, retrieval, and MCP dependencies drive deterministic tests.
3. Run an opt-in local provider smoke test only when a valid key is configured.
4. Verify logs and API responses do not contain credentials, prompts, hidden reasoning, or stack traces.
