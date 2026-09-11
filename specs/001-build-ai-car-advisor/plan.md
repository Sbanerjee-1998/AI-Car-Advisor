# Implementation Plan: AI Car Advisor

**Branch**: `001-build-ai-car-advisor` | **Date**: 2026-09-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-build-ai-car-advisor/spec.md`

## Summary

Build a polished, authenticated car-buying workspace where a user can describe
their needs, receive grounded recommendations, compare and save vehicles, and
estimate EMI and fuel costs. Use a React/Vite frontend, a FastAPI modular backend,
SQLite application state, manually curated Markdown vehicle data indexed in
ChromaDB, one LangChain agent using configurable Gemini, and one local MCP server
for the two deterministic calculators.

The backend remains the only application service. It owns authentication,
ownership checks, persistence, catalog access, retrieval, agent orchestration, and
response shaping. The frontend receives structured responses so it can render
recommendations, comparisons, follow-up states, calculators, and safe errors
without parsing model prose.

## Technical Context

**Language/Version**: Python 3.11; TypeScript with Node.js 20 LTS

**Primary Dependencies**: FastAPI, SQLAlchemy 2, Alembic, Pydantic,
React, Vite, Vitest, React Testing Library, Playwright, ChromaDB, LangChain,
configurable Gemini integration, and one local MCP server

**Storage**: SQLite for application state and server-side sessions; curated
Markdown files as vehicle source data; persistent local ChromaDB for embeddings
and retrieval metadata; generated runtime data under `.local/`

**Testing**: pytest for backend unit, API, persistence, RAG, and mocked-agent
tests; Vitest and React Testing Library for frontend tests; Playwright for one
local end-to-end smoke journey; OpenAPI/Pydantic contract assertions

**Target Platform**: Linux local development and GitHub Actions CI; browser-based
desktop and mobile layouts; local backend at port 8000 and frontend at port 5173

**Project Type**: Authenticated web application with a Python API, React client,
local retrieval store, and local deterministic tool server

**Performance Goals**: Chat and catalog screens show loading feedback immediately;
chat history and catalog reads remain responsive for capstone-scale data; the
initial catalog supports approximately 30 vehicles; successful calculator results
are returned without model-dependent delay

**Constraints**: No live price scraping, purchase workflows, marketplace, or
additional application database/vector store; no API keys required for CI; prompts
use bounded relevant history; Gemini, ChromaDB, and MCP remain behind backend
adapters; prices and specifications are informational and require verification

**Scale/Scope**: One local capstone deployment, approximately 30 vehicle profiles,
authenticated users with isolated conversations and favourites, two calculator
tools, one agent path, and the MVP journeys in the approved specification

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Product-First Simplicity**: PASS. The design uses one backend service, one
  agent, one MCP server, and structured user journeys without adding marketplace
  or administrative scope.
- **II. Grounded Vehicle Knowledge**: PASS. Markdown is the catalog source of
  truth; ingestion, metadata filters, ChromaDB retrieval, stable vehicle IDs, and
  response validation prevent unsupported claims.
- **III. One Clear AI Orchestration Path**: PASS. One backend agent coordinates
  bounded context, retrieval, Gemini, and MCP tools; the frontend never calls
  model or vector services directly.
- **IV. Secure, Isolated User Data**: PASS. Argon2id password hashing,
  server-side opaque sessions, HttpOnly cookies, query-level ownership checks,
  generic unauthorized-resource responses, and environment-managed secrets are
  part of the design.
- **V. Testable, Observable Delivery**: PASS. Deterministic domain tests,
  temporary SQLite/ChromaDB fixtures, mocked agent tests, frontend tests, a health
  endpoint, user-safe error states, and push/PR CI gates are planned.
- **Technical constraints**: PASS. The selected stack is Python/FastAPI,
  SQLAlchemy/SQLite, React or Next.js, ChromaDB, LangChain, Gemini, and one MCP
  server, with no second database or vector store.
- **Quality gates**: PASS. The plan preserves frontend/backend/retrieval/agent/
  MCP/persistence boundaries, defines contracts and integration tests, and keeps
  secrets and runtime artifacts out of version control.
- **Post-design re-check (Phase 1)**: PASS. The research, data model, REST/MCP
  contracts, and quickstart preserve the five principles, keep the catalog and
  calculations grounded and deterministic, define ownership boundaries, and
  provide a credential-free CI path. No constitution violation or complexity
  exception was introduced.

## Project Structure

### Documentation (this feature)

```text
specs/001-build-ai-car-advisor/
├── plan.md              # This implementation plan
├── research.md          # Resolved architecture and integration decisions
├── data-model.md        # Durable entities and validation rules
├── quickstart.md        # Local setup and end-to-end validation guide
├── contracts/           # REST, chat, calculator, and MCP contracts
└── tasks.md             # Generated later by /speckit-tasks
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── chats.py
│   │   ├── cars.py
│   │   ├── favourites.py
│   │   ├── calculators.py
│   │   └── compare.py
│   ├── database/
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── catalog.py
│   │   ├── calculators.py
│   │   └── preferences.py
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   └── embeddings.py
│   └── agents/
│       ├── advisor.py
│       ├── context.py
│       └── provider.py
├── data/cars/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── rag/
│   └── agent/
└── requirements.txt

frontend/
├── src/
│   ├── app/
│   ├── components/
│   ├── features/
│   │   ├── auth/
│   │   ├── chat/
│   │   ├── cars/
│   │   └── calculators/
│   ├── services/api/
│   └── styles/
├── tests/
└── package.json

mcp/
├── server.py
├── tools/
│   ├── emi.py
│   └── fuel_cost.py
└── tests/

.local/
├── app.db
└── chroma/
```

**Structure Decision**: Use a small monorepo with explicit `frontend/`,
`backend/`, and `mcp/` boundaries. The backend is a modular monolith and the
only application service. The canonical calculator domain functions are shared
by backend REST routes and MCP adapters. Markdown vehicle files remain under
`backend/data/cars/`; SQLite and ChromaDB are disposable local runtime artifacts.
