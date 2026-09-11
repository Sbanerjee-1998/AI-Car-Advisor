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

## GitHub Pages

The frontend can be deployed to GitHub Pages by the workflow in
`.github/workflows/pages.yml`. In the repository settings, set Pages' source to
GitHub Actions. The published frontend URL is:
`https://Sbanerjee-1998.github.io/AI-Car-Advisor/`.

GitHub Pages hosts only the static React frontend. The FastAPI backend, SQLite
database, Gemini key, and MCP server must run on a separate service. Set the
repository variable `VITE_API_BASE_URL` to the public backend origin before the
Pages build. Configure the backend's `FRONTEND_ORIGIN` to the Pages origin and
use a production-safe cross-origin session configuration before relying on
authentication from the hosted frontend.
