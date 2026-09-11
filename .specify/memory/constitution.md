<!--
Sync Impact Report
- Version change: unversioned scaffold -> 1.0.0
- Modified principles: principle placeholder 1 -> I. Product-First Simplicity;
	principle placeholder 2 -> II. Grounded Vehicle Knowledge;
	principle placeholder 3 -> III. One Clear AI Orchestration Path;
	principle placeholder 4 -> IV. Secure, Isolated User Data;
	principle placeholder 5 -> V. Testable, Observable Delivery
- Added sections: Product and Technical Constraints; Development Workflow and Quality Gates
- Removed sections: None
- Follow-up TODOs: TODO(RATIFICATION_DATE) requires the original adoption date.
-->

# AI Car Advisor Constitution

## Core Principles

### I. Product-First Simplicity
The product MUST help a user make a better car-buying decision through a clear,
conversational flow. User-facing behavior MUST prioritize recommendations, useful
follow-up questions, comparison, car details, favourites, and financial estimates
over technical demonstrations. The application MUST avoid unnecessary services,
agents, screens, and terminology. This keeps the capstone understandable,
trustworthy, and valuable as an end-to-end product.

### II. Grounded Vehicle Knowledge
Vehicle recommendations, details, and comparisons MUST be grounded in the curated
vehicle knowledge base through the RAG retrieval path. Vehicle documents MUST be
stored locally in a structured, extensible format and indexed in persistent
ChromaDB storage. The assistant MUST state when information is unavailable and
MUST NOT invent specifications, prices, availability, or safety claims. User-facing
responses MUST communicate that prices and specifications can vary and require
verification with a manufacturer or dealer. Grounding reduces hallucination and
keeps the assistant's advice accountable to known data.

### III. One Clear AI Orchestration Path
The application MUST use one LangChain-based agent to coordinate requirement
understanding, retrieval, recommendations, comparisons, and tool use. Gemini MUST
be accessed through a configurable environment-selected model. Deterministic EMI
and fuel-cost calculations MUST be delegated to programmatic MCP tools; the model
MUST interpret their results rather than replace their mathematics. The product
MUST NOT add multiple specialised agents or expose hidden chain-of-thought. A
single explicit orchestration path keeps behavior explainable and the architecture
within capstone scope.

### IV. Secure, Isolated User Data
Passwords MUST be securely hashed and MUST never be stored or logged in plain
text. Secrets and model credentials MUST come from environment variables, with
`.env` excluded from version control and `.env.example` committed. Authenticated
endpoints MUST enforce ownership for conversations, messages, and favourites.
Validation MUST reject malformed or unauthorized requests without exposing stack
traces, secrets, system prompts, or internal reasoning. These controls protect
personal data and make the local application safe to demonstrate.

### V. Testable, Observable Delivery
Core calculations, validation, RAG ingestion and retrieval, authentication, chat
history, favourites, API contracts, and representative agent tool flows MUST have
automated tests. The application MUST provide explicit loading and user-safe error
states, and the backend MUST expose a health check. GitHub Actions MUST run backend
checks and the frontend build on pushes and pull requests. This makes regressions
visible and keeps the demonstrated product reliable as features are added.

## Product and Technical Constraints

- The backend MUST use Python, FastAPI, SQLAlchemy, and SQLite unless an amendment
	explicitly changes the stack.
- The frontend MUST use React or Next.js and MUST remain usable on desktop and
	mobile layouts.
- The AI layer MUST use Gemini through Google AI Studio, LangChain, ChromaDB, and
	curated Markdown vehicle documents as specified by the approved feature plan.
- The initial knowledge base MUST contain approximately 30 manually curated cars
	covering petrol, diesel, EV, and hybrid or other supported powertrain types.
- The system MUST keep application state in SQLite and vectorized vehicle knowledge
	in ChromaDB; it MUST NOT introduce a second application database or vector store
	without an amended decision.
- The MCP server MUST expose the EMI and fuel-cost calculators as deterministic,
	validated tools and MUST share calculation logic with dedicated calculator APIs
	where practical.
- The product MUST NOT scrape live prices, process purchases, provide dealership or
	insurance booking, or become a marketplace. Demonstration pricing and
	specifications MUST carry an informational disclaimer.
- Conversation context MUST be bounded to relevant history so prompts remain
	responsive and do not grow without control.

## Development Workflow and Quality Gates

- Feature work MUST begin with an approved specification and implementation plan
	that identify user value, data boundaries, API contracts, and validation strategy.
- Changes MUST preserve the ownership boundary between frontend, backend,
	retrieval, agent, MCP tools, and application persistence. Cross-boundary changes
	MUST include an integration test or an explicit documented reason why one is not
	practical.
- Every pull request MUST include relevant tests and documentation updates when
	behavior, configuration, or user-facing limitations change.
- CI MUST pass backend tests, configured quality checks, and the frontend build
	before a change is considered ready for demonstration or merge.
- Secrets, generated vector stores, local databases, and runtime artifacts MUST NOT
	be committed unless a documented fixture is required for a test.
- New dependencies and architectural complexity MUST be justified by a concrete
	product or reliability need and MUST not duplicate an existing capability.

## Governance

This constitution is the highest-level project guidance. If another document or
implementation choice conflicts with it, the conflict MUST be resolved in favor of
this constitution or recorded as an amendment before implementation proceeds.

Amendments MUST identify the affected principles or sections, explain the reason
for the change, update the Sync Impact Report, and update the version and amendment
date. A change that removes or redefines a non-negotiable principle is a MAJOR
version change. A new principle or materially expanded requirement is a MINOR
version change. Clarifications, wording fixes, and other non-semantic refinements
are PATCH changes. The version MUST follow `MAJOR.MINOR.PATCH` format.

Every feature review MUST check compliance with the principles, technical
constraints, security requirements, and quality gates. Exceptions MUST be written
in the relevant plan or pull request with their scope, rationale, owner, and
follow-up date. Temporary exceptions MUST NOT silently become project defaults.

The constitution MUST be reviewed whenever the stack, data-handling model, AI
orchestration boundary, security model, or release quality gates change materially.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date is not recorded | **Last Amended**: 2026-09-10
