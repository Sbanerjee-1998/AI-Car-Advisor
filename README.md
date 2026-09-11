# AI Car Advisor

AI Car Advisor is a local-first authenticated Indian car discovery workspace. It keeps recommendations grounded in a curated Markdown catalog, persists private conversations in SQLite, and exposes deterministic finance tools through both REST and a local MCP server.

## Boundaries

- `frontend/`: React, Vite, and TypeScript workspace UI.
- `backend/`: FastAPI modular monolith, SQLAlchemy models, catalog, retrieval, advisor boundary, and REST API.
- `mcp/`: local stdio MCP server with EMI and fuel-cost tools.
- `specs/001-build-ai-car-advisor/`: approved product specification, plan, contracts, and executable task list.

## Local development

Use Python 3.11 or later and Node.js 20 or later. Create a virtual environment, install `backend/requirements.txt`, and copy `.env.example` to `.env`.

```bash
alembic -c backend/alembic.ini upgrade head
PYTHONPATH=. python -m backend.app.rag.ingest
PYTHONPATH=. uvicorn backend.app.main:app --reload
npm --prefix frontend install
npm --prefix frontend run dev
```

The API runs at `http://localhost:8000`; the Vite workspace runs at `http://localhost:5173`. Gemini is optional for local deterministic development. See [the quickstart](specs/001-build-ai-car-advisor/quickstart.md) and [the architecture notes](docs/architecture.md) for the full workflow.
