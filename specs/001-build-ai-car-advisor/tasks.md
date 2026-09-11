---

description: "Actionable implementation tasks for the AI Car Advisor feature"
---

# Tasks: AI Car Advisor

**Input**: Design documents from `specs/001-build-ai-car-advisor/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/`, and `quickstart.md`

**Tests**: Included because the constitution requires automated tests for core
calculations, validation, RAG, authentication, chat history, favourites, API
contracts, and representative agent tool flows.

**Organization**: Tasks are grouped by user story so each increment can be
implemented and validated independently after the shared foundation is complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other tasks in the same phase because it uses
  different files and has no dependency on incomplete work.
- **[Story]**: Maps a task to a user story from `spec.md`.
- Every task includes the concrete file path or paths it changes.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the monorepo boundaries and reproducible local development
configuration described in `plan.md`.

- [X] T001 Create the planned monorepo directories and package markers in `backend/app/`, `backend/tests/`, `frontend/src/`, `frontend/tests/`, `mcp/tools/`, `mcp/tests/`, `backend/data/cars/`, and `docs/`.
- [X] T002 [P] Initialize the Python backend dependency and quality configuration in `backend/requirements.txt` and `backend/pyproject.toml` for Python 3.11, FastAPI, SQLAlchemy 2, Alembic, Pydantic, Argon2id support, LangChain, Gemini integration, ChromaDB, MCP, pytest, and lint/format checks.
- [X] T003 [P] Initialize the React/Vite TypeScript frontend in `frontend/package.json`, `frontend/tsconfig.json`, and `frontend/vite.config.ts` with scripts for development, tests, production build, and `/api` proxying to FastAPI.
- [X] T004 [P] Initialize the local MCP package and stdio entry point in `mcp/server.py`, `mcp/tools/__init__.py`, and `mcp/tests/__init__.py` without exposing a browser-facing network service.
- [X] T005 [P] Add environment and runtime-artifact rules in `.env.example` and `.gitignore`, including Gemini configuration, `DATABASE_URL`, `CHROMA_PATH`, session-cookie settings, `.env`, `.local/`, SQLite files, ChromaDB data, caches, and generated build output.
- [X] T006 [P] Create developer-facing project orientation in `README.md` and `docs/architecture.md` describing the `frontend/`, `backend/`, and `mcp/` boundaries and linking to `specs/001-build-ai-car-advisor/quickstart.md`.
- [X] T007 Add the initial GitHub Actions job skeleton in `.github/workflows/ci.yml` for Python dependency installation, frontend dependency installation, and named placeholders for the backend checks and frontend build that later tasks complete.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement infrastructure required by every user story. No user story
work should begin until this phase is complete.

- [X] T008 Configure validated environment settings and safe defaults in `backend/app/config.py`, including Python 3.11 runtime assumptions, SQLite at `.local/app.db`, ChromaDB at `.local/chroma/`, configurable Gemini model settings, bounded context budgets, and local versus secure session-cookie behavior.
- [X] T009 Set up SQLAlchemy 2 database access and Alembic migrations in `backend/app/database/base.py`, `backend/app/database/session.py`, `backend/alembic.ini`, and `backend/app/database/migrations/env.py` with UTC timestamps, foreign-key enforcement, and test-database overrides.
- [X] T010 [P] Define the shared safe error envelope and exception handling in `backend/app/schemas/errors.py`, `backend/app/api/errors.py`, and `backend/app/main.py`; never return stack traces, prompts, credentials, raw provider errors, hidden reasoning, or database details.
- [X] T011 [P] Create the FastAPI application, `/health` route, router registration, and request lifecycle wiring in `backend/app/main.py` and `backend/app/api/health.py`; return only `{"status":"ok","service":"ai-car-advisor"}` from the health response.
- [X] T012 [P] Implement security primitives and current-user dependency boundaries in `backend/app/security.py` and `backend/app/api/dependencies.py` for Argon2id password hashing, opaque session tokens, hashed token lookup, HttpOnly cookies, `SameSite=Lax`, expiry, revocation, and generic `404` handling for unowned resources.
- [X] T013 [P] Create reusable backend test fixtures and factory helpers in `backend/tests/conftest.py` and `backend/tests/factories.py` for temporary SQLite, dependency overrides, authenticated sessions, isolated users, and safe fake AI/provider dependencies.
- [X] T014 [P] Create the frontend API client, session-aware request handling, and shared loading/error/empty state primitives in `frontend/src/services/api/client.ts`, `frontend/src/components/AsyncState.tsx`, and `frontend/src/components/ErrorMessage.tsx`.
- [X] T015 [P] Implement curated Markdown parsing and catalog validation in `backend/app/services/catalog.py` and `backend/app/schemas/cars.py`, requiring stable slugs and normalized `price_min_inr`, `price_max_inr`, `fuel_type`, `transmission`, `body_type`, and `seating_capacity` metadata.
- [ ] T016 Implement repeatable catalog ingestion and embedding-provider boundaries in `backend/app/rag/ingest.py` and `backend/app/rag/embeddings.py`; validate every document before indexing, create semantic section chunks, attach source metadata, and idempotently upsert stable ChromaDB document IDs.
- [ ] T017 Implement bounded ChromaDB retrieval with semantic similarity, hard metadata filters, source evidence, duplicate removal, vehicle grouping, and a maximum of three distinct user-facing vehicle candidates in `backend/app/rag/retriever.py`.
- [X] T018 [P] Add approximately 30 manually curated Indian vehicle Markdown documents under `backend/data/cars/`, covering petrol, diesel, electric, and hybrid powertrains with stable slugs, known specifications, advantages, considerations, use cases, and explicit unavailable fields where appropriate.
- [ ] T019 [P] Add ingestion and retrieval fixture tests in `backend/tests/rag/test_ingestion.py` and `backend/tests/rag/test_retriever.py` covering invalid-document failure, idempotent upsert, metadata filters, source metadata, no exact matches, and deterministic fake embeddings without a Gemini key.
- [X] T020 [P] Add the health and foundational API contract test in `backend/tests/contract/test_health_contract.py` and verify the response does not expose secrets, filesystem paths, credentials, or prompts.

**Checkpoint**: The application can start with configured local dependencies, expose a
safe health response, validate and index curated catalog data, and run foundational
tests without external credentials.

---

## Phase 3: User Story 1 - Create an Account and Start a Conversation (Priority: P1) MVP

**Goal**: Let a visitor register, sign in, create an empty conversation, sign out,
and sign back in without exposing another user's workspace.

**Independent Test**: Register a user, sign in, create a new chat, sign out, sign
back in, verify the conversation is listed, and verify protected data is unavailable
after logout.

### Tests for User Story 1

- [X] T021 [P] [US1] Add authentication contract tests for register, duplicate normalized email, login, logout, and `/api/auth/me` in `backend/tests/contract/test_auth_contract.py`.
- [X] T022 [P] [US1] Add the registration, session, new-chat, logout, and re-login integration journey in `backend/tests/integration/test_auth_workspace.py`, including rejection of invalid credentials and unauthenticated access.
- [X] T023 [P] [US1] Add frontend authentication and new-chat tests in `frontend/tests/auth-workspace.test.tsx` covering form validation, loading, success, duplicate-email error, logout, and protected workspace rendering.

### Implementation for User Story 1

- [X] T024 [P] [US1] Create the `User` model in `backend/app/models/user.py` with `name` required and bounded, `email_normalized` required/lowercase/trimmed/unique, `password_hash` required and Argon2id-only, and required UTC `created_at` and `updated_at` timestamps.
- [X] T025 [P] [US1] Create the `AuthSession` model in `backend/app/models/auth_session.py` with required indexed `user_id`, unique `token_hash` that is never returned, required `created_at`, future `expires_at`, and nullable `revoked_at`.
- [X] T026 [P] [US1] Create the `Conversation` model in `backend/app/models/conversation.py` with required indexed `user_id`, nullable bounded `title`, required `created_at`, and `updated_at` refreshed when a message is persisted.
- [X] T027 [US1] Generate the initial Alembic migration in `backend/app/database/migrations/versions/` for `User`, `AuthSession`, and `Conversation`, including unique normalized email and indexed ownership foreign keys.
- [X] T028 [US1] Implement registration, login, logout, and current-user services and routes in `backend/app/services/auth.py` and `backend/app/api/auth.py` using the safe error envelope and server-side HttpOnly session lifecycle.
- [X] T029 [US1] Implement authenticated empty-chat creation and recent conversation listing in `backend/app/services/chat.py` and `backend/app/api/chats.py`, deriving a bounded useful title when one is provided and filtering every query by the current user ID.
- [ ] T030 [US1] Build registration, login, logout, session restoration, and protected-route screens in `frontend/src/features/auth/`, `frontend/src/app/router.tsx`, and `frontend/src/services/api/auth.ts`.
- [X] T031 [US1] Build the authenticated workspace shell and New Chat interaction in `frontend/src/features/chat/Workspace.tsx`, `frontend/src/app/App.tsx` with desktop/mobile layouts and explicit loading, empty, and error states.
- [X] T032 [US1] Wire cookie credentials, logout cache clearing, and protected navigation between frontend and FastAPI in `frontend/src/services/api/client.ts` and `backend/app/api/dependencies.py`, ensuring private workspace data is not rendered after session loss.

**Checkpoint**: A user can complete the full account and new-conversation journey
without any recommendation or calculator dependency.

---

## Phase 4: User Story 2 - Receive a Personalised Car Recommendation (Priority: P1)

**Goal**: Turn a natural-language request into a concise follow-up or a grounded
shortlist of at most three vehicles with explanations, trade-offs, and disclaimers.

**Independent Test**: A signed-in user sends a budget and driving-needs message,
answers one contextual follow-up when requested, and receives only supported vehicle
IDs with fit reasons, advantages, considerations, approximate data, and a disclaimer.

### Tests for User Story 2

- [ ] T033 [P] [US2] Add the structured chat-message contract test in `backend/tests/contract/test_chat_message_contract.py` covering `conversation_id`, `user_message`, `assistant_message`, `recommendations`, `follow_up_required`, `available_actions`, and `disclaimer`.
- [ ] T034 [P] [US2] Add mocked-agent tests in `backend/tests/agent/test_advisor.py` for missing-information follow-ups, contextual replies, at most three recommendations, retrieved-vehicle ID validation, trade-offs, and no chain-of-thought persistence.
- [ ] T035 [P] [US2] Add grounded recommendation tests in `backend/tests/rag/test_recommendation_grounding.py` verifying hard filter behavior, unavailable fields, approximate-data disclaimers, and controlled closest alternatives when no exact match exists.
- [ ] T036 [P] [US2] Add frontend chat and recommendation rendering tests in `frontend/tests/chat-recommendations.test.tsx` for submit/loading/error states, follow-up prompts, recommendation cards, actions, and mobile-safe content.

### Implementation for User Story 2

- [X] T037 [P] [US2] Define Pydantic agent-result and recommendation schemas in `backend/app/schemas/advisor.py` with bounded result kinds, canonical vehicle IDs, fit summaries, advantages, considerations, supported specifications, and a maximum of three recommendations.
- [X] T038 [P] [US2] Implement token-aware bounded context packing in `backend/app/agents/context.py` with the priority order of safety instructions, current user message, structured preferences, retrieved evidence, and recent complete turns, using an 8,000-token input budget and approximately 1,500 tokens reserved for output.
- [ ] T039 [P] [US2] Implement the configurable Gemini provider adapter in `backend/app/agents/provider.py`, reading the API key, model name, temperature, and output limits from environment settings and supporting injectable fake models for CI.
- [ ] T040 [US2] Implement the single LangChain advisor orchestration path in `backend/app/agents/advisor.py` for requirement understanding, retrieval, follow-up questions, recommendation ranking, structured output, and post-validation against catalog evidence.
- [X] T041 [P] [US2] Create the `Message` model in `backend/app/models/message.py` with required indexed `conversation_id`, role restricted to `user` or `assistant`, required bounded `content`, required chronological UTC `created_at`, and no internal reasoning or tool traces.
- [X] T042 [US2] Implement message persistence and structured assistant response shaping in `backend/app/services/chat.py`, saving only accepted visible user and assistant messages and updating the conversation timestamp after successful persistence.
- [X] T043 [US2] Implement `POST /api/chats/{chat_id}/messages` in `backend/app/api/chats.py` with owned-conversation lookup, empty/whitespace/oversized input validation, bounded context, advisor execution, safe provider failure handling, and the documented structured response.
- [ ] T044 [P] [US2] Build the chat transcript, composer, follow-up prompt, and loading/error components in `frontend/src/features/chat/ChatView.tsx`, `frontend/src/features/chat/MessageComposer.tsx`, and `frontend/src/features/chat/AssistantMessage.tsx`.
- [X] T045 [P] [US2] Build grounded recommendation cards and action affordances in `frontend/src/features/cars/RecommendationList.tsx`, rendering unavailable fields explicitly and showing the approximate-data disclaimer.
- [ ] T046 [US2] Connect recommendation responses and recoverable input-preserving failures in `frontend/src/features/chat/chatApi.ts` and `frontend/src/features/chat/ChatView.tsx`, without exposing prompts, raw provider errors, or internal reasoning.

**Checkpoint**: The central assistant journey works independently for a signed-in
user and never presents unsupported vehicle facts or model internals.

---

## Phase 5: User Story 3 - Return to Previous Conversations (Priority: P1)

**Goal**: Persist and reopen a user's messages and preference context with useful
ordering, deletion, and strict cross-user isolation.

**Independent Test**: Exchange messages, leave and return, reopen the conversation,
continue it using relevant context, delete it, and verify another user cannot access it.

### Tests for User Story 3

- [ ] T047 [P] [US3] Add conversation-history contract tests in `backend/tests/contract/test_chat_history_contract.py` for list, detail, delete, chronological messages, preferences, and empty conversations.
- [ ] T048 [P] [US3] Add persistence and ownership integration tests in `backend/tests/integration/test_chat_history.py` for updated ordering, message continuity, cascade deletion, session loss, identifier substitution, and two-user isolation.
- [ ] T049 [P] [US3] Add history-sidebar and transcript-reopen tests in `frontend/tests/chat-history.test.tsx` for loading, empty state, deletion confirmation, ordering, and session-expired recovery.

### Implementation for User Story 3

- [ ] T050 [US3] Extend `backend/app/services/chat.py` with chronological message retrieval, bounded relevant-context loading, useful title updates from the first user message, and deletion transactions that remove dependent messages and preference state.
- [ ] T051 [US3] Complete `GET /api/chats/{chat_id}`, `DELETE /api/chats/{chat_id}`, and the owned recent-list behavior in `backend/app/api/chats.py`, returning generic `404` responses for missing or unowned conversations.
- [ ] T052 [US3] Add the conversation sidebar, reopen flow, delete confirmation, and empty-conversation handling in `frontend/src/features/chat/ConversationList.tsx`, `frontend/src/features/chat/ConversationItem.tsx`, and `frontend/src/features/chat/Workspace.tsx`.
- [ ] T053 [US3] Add the message and conversation cascade migration in `backend/app/database/migrations/versions/` and verify foreign-key cleanup for messages and future conversation preference state.
- [ ] T054 [US3] Update `backend/app/agents/context.py` and `backend/app/agents/advisor.py` to use structured active state plus relevant recent turns rather than sending unbounded full history, preserving contextual follow-up answers after reopening a chat.

**Checkpoint**: A returning user can continue or delete prior conversations, while
another authenticated user cannot infer or access them by changing identifiers.

---

## Phase 6: User Story 4 - Compare, Inspect, and Save Shortlisted Cars (Priority: P2)

**Goal**: Let users inspect curated vehicle details, compare two or three vehicles,
and save or remove user-owned favourites.

**Independent Test**: Open a catalog vehicle, compare two or three known slugs,
receive a priority-based conclusion, save one vehicle, reload favourites, and remove it.

### Tests for User Story 4

- [ ] T055 [P] [US4] Add contract tests for vehicle listing/detail, comparison, and favourites in `backend/tests/contract/test_catalog_workflows.py`, including two-to-three selection validation and unavailable fields.
- [ ] T056 [P] [US4] Add catalog and ownership integration tests in `backend/tests/integration/test_compare_favourites.py` for details, comparison trade-offs, duplicate saves, persistence across sign-in, removal, unknown IDs, and user isolation.
- [ ] T057 [P] [US4] Add frontend vehicle-workflow tests in `frontend/tests/vehicle-workflows.test.tsx` for detail views, comparison tables, conclusion rendering, save/remove states, and mobile-readable tables.

### Implementation for User Story 4

- [X] T058 [US4] Implement `GET /api/cars` and `GET /api/cars/{car_id}` in `backend/app/api/cars.py` and `backend/app/services/catalog.py`, exposing only curated data, supported fields, use cases, advantages, considerations, and explicit unavailable markers.
- [X] T059 [US4] Implement comparison schemas and service logic in `backend/app/schemas/cars.py` and `backend/app/services/comparison.py` and expose `POST /api/compare` in `backend/app/api/compare.py` for exactly two or three distinct supported vehicle IDs with priority-based trade-offs.
- [X] T060 [P] [US4] Create the `Favourite` model and migration in `backend/app/models/favourite.py` and `backend/app/database/migrations/versions/` with required indexed `user_id`, required stable `vehicle_id`, required UTC `created_at`, and unique `(user_id, vehicle_id)`.
- [X] T061 [US4] Implement favourite creation, listing, and removal in `backend/app/services/favourites.py` and `backend/app/api/favourites.py`, resolving vehicle slugs through the catalog and scoping every query to the current user.
- [ ] T062 [P] [US4] Build vehicle detail and comparison views in `frontend/src/features/cars/CarDetail.tsx`, `frontend/src/features/cars/ComparisonTable.tsx`, and `frontend/src/features/cars/CompareView.tsx`, marking unsupported values unavailable instead of inferring them.
- [ ] T063 [P] [US4] Build favourites state and save/remove interactions in `frontend/src/features/cars/FavouriteButton.tsx`, `frontend/src/features/cars/FavouritesView.tsx`, and `frontend/src/services/api/cars.ts` with duplicate and session-expired error states.

**Checkpoint**: Vehicle inspection, comparison, and favourites are usable without
requiring live prices, purchases, dealer booking, or marketplace behavior.

---

## Phase 7: User Story 5 - Estimate Loan and Fuel Costs (Priority: P2)

**Goal**: Provide reliable dedicated and conversational EMI and fuel-cost estimates
through shared deterministic functions and exactly two MCP tools.

**Independent Test**: Submit valid and zero-interest EMI cases, valid fuel inputs with
monthly driving days, and invalid values; verify exact rounded outputs and field errors
through dedicated and conversational paths.

### Tests for User Story 5

- [X] T064 [P] [US5] Add calculator tests in `backend/tests/test_foundation.py` for positive EMI, zero-interest EMI, total payment/interest, fuel daily/monthly/annual outputs, decimal rounding, and invalid values.
- [X] T065 [P] [US5] Add MCP tool tests in `mcp/tests/test_tools.py` for `calculate_emi` and `calculate_fuel_cost`, asserting their numeric results match the shared backend calculator functions and their validation errors are safe.
- [ ] T066 [P] [US5] Add REST calculator contract tests in `backend/tests/contract/test_calculator_contract.py` for `/api/emi`, `/api/fuel-cost`, field-level `422` errors, estimate disclaimers, and two-decimal outputs.
- [ ] T067 [P] [US5] Add conversational calculator integration tests in `backend/tests/integration/test_calculator_flows.py` with a scripted agent and MCP client, verifying tool invocation instead of model arithmetic and agreement with dedicated endpoints.
- [ ] T068 [P] [US5] Add frontend calculator tests in `frontend/tests/calculators.test.tsx` for valid results, zero-interest EMI, daily/monthly/annual fuel outputs, invalid fields, loading, and recoverable errors.

### Implementation for User Story 5

- [X] T069 [US5] Implement and document the shared validated formulas in `backend/app/services/calculators.py` and update `specs/001-build-ai-car-advisor/contracts/calculators.md` so fuel cost accepts daily distance, mileage, fuel price, and monthly driving days and returns daily cost, monthly consumption, monthly cost, and annual cost; use decimal-safe arithmetic and two-decimal rounding.
- [X] T070 [US5] Implement calculator request/response schemas and deterministic REST routes in `backend/app/schemas/calculators.py` and `backend/app/api/calculators.py`, allowing zero interest while rejecting invalid, non-positive, or non-finite inputs with the safe error envelope.
- [X] T071 [US5] Implement the local stdio MCP server and exactly two tools in `mcp/server.py` and `mcp/tools/calculators.py`, importing the canonical functions from `backend/app/services/calculators.py` rather than duplicating formulas.
- [ ] T072 [US5] Add validated calculator tool adapters to the single advisor path in `backend/app/agents/advisor.py` and `backend/app/agents/provider.py`, ensuring Gemini interprets returned results and never computes financial mathematics itself.
- [ ] T073 [P] [US5] Build dedicated EMI and fuel-cost forms and result panels in `frontend/src/features/calculators/EmiCalculator.tsx`, `frontend/src/features/calculators/FuelCostCalculator.tsx`, and `frontend/src/features/calculators/CalculatorDisclaimer.tsx`.
- [ ] T074 [US5] Connect calculator forms, conversational calculation actions, and input-preserving error states in `frontend/src/features/calculators/CalculatorView.tsx` and `frontend/src/services/api/calculators.ts`.

**Checkpoint**: Dedicated and conversational calculators return the same validated
results, show estimates clearly, and never rely on model-generated arithmetic.

---

## Phase 8: User Story 6 - Refine Discovery with Preferences and Filters (Priority: P3)

**Goal**: Preserve natural-language preferences, apply supported catalog filters, and
explain conflicts or empty exact matches without silently discarding constraints.

**Independent Test**: State a preference, request filtered vehicles, change it to a
conflicting value, and verify the newest value controls later results or the assistant
explains how to broaden an empty request.

### Tests for User Story 6

- [ ] T075 [P] [US6] Add preference merge and validation unit tests in `backend/tests/unit/test_preferences.py` for latest-value-wins updates, omitted values, budget bounds, fuel/transmission enums, seating positivity, daily distance, conflicts, and bounded preference text.
- [ ] T076 [P] [US6] Add preference-aware recommendation integration tests in `backend/tests/integration/test_preferences.py` for conversation-scoped persistence, contextual updates, hard filters, no exact match, and closest-alternative explanations.
- [ ] T077 [P] [US6] Add filtered catalog contract tests in `backend/tests/contract/test_catalog_filters_contract.py` for budget, fuel, transmission, body type, seating, usage, mileage, EV, and hybrid constraints.
- [ ] T078 [P] [US6] Add frontend filter and preference tests in `frontend/tests/preferences-filters.test.tsx` for filter selection, conflict messaging, empty results, reset/broaden actions, and updated recommendation requests.

### Implementation for User Story 6

- [X] T079 [US6] Create the `ConversationPreference` model and migration in `backend/app/models/conversation_preference.py` and `backend/app/database/migrations/versions/` with one-to-one conversation ownership, nullable structured fields, non-negative budgets/distances, positive seating when present, bounded usage/unresolved text, and bounded stable recent vehicle IDs.
- [X] T080 [US6] Implement preference extraction, validation, latest-value-wins merging, and conversation persistence in `backend/app/services/preferences.py` and `backend/app/schemas/chat.py` without treating omitted values as explicit resets.
- [ ] T081 [US6] Extend metadata-filter construction and no-match handling in `backend/app/rag/retriever.py` and `backend/app/services/catalog.py` so hard constraints are applied before semantic ranking and empty exact matches are reported rather than silently ignored.
- [ ] T082 [US6] Add filter query validation and preference-aware catalog/recommendation wiring in `backend/app/api/cars.py`, `backend/app/api/chats.py`, and `backend/app/agents/advisor.py` for budget, fuel, transmission, body type, seating, usage, mileage, EV, and hybrid requirements.
- [ ] T083 [P] [US6] Build filter controls and preference status UI in `frontend/src/features/cars/FilterPanel.tsx`, `frontend/src/features/cars/CatalogView.tsx`, and `frontend/src/features/chat/ActivePreferences.tsx` with desktop/mobile layouts.
- [ ] T084 [US6] Implement conflict, empty-result, and broaden-request rendering in `frontend/src/features/cars/FilterPanel.tsx`, `frontend/src/features/chat/AssistantMessage.tsx`, and `frontend/src/services/api/cars.ts` while preserving the user's entered filters.

**Checkpoint**: Preference-aware discovery improves relevance while retaining clear
user control over conflicts and hard constraints.

---

## Phase 9: Polish and Cross-Cutting Concerns

**Purpose**: Complete CI, security, responsive behavior, documentation, catalog
verification, and full acceptance validation across the delivered stories.

- [X] T085 [P] Complete push and pull-request CI in `.github/workflows/ci.yml` to install Python and Node dependencies, run backend/MCP tests, run frontend tests and build, and avoid requiring a Gemini API key.
- [ ] T086 [P] Harden configuration, structured diagnostics, and safe logging in `backend/app/config.py`, `backend/app/observability.py`, and `backend/app/main.py` so correlation IDs and server diagnostics are available without logging passwords, session tokens, prompts, credentials, or chain-of-thought.
- [ ] T087 [P] Verify responsive layouts and stable loading/error/empty states across the authenticated workspace, chat, catalog, comparison, favourites, and calculators in `frontend/src/styles/`, `frontend/src/app/App.tsx`, and the relevant `frontend/src/features/` components.
- [ ] T088 [P] Validate and update the setup, ingestion, startup, test, and acceptance commands in `specs/001-build-ai-car-advisor/quickstart.md`, including the actual module paths and local `.local/` locations.
- [ ] T089 Run the complete backend, MCP, frontend, and build validation commands from `specs/001-build-ai-car-advisor/quickstart.md` and record any resolved implementation deviations in `docs/architecture.md`.
- [ ] T090 Verify the initial catalog release in `backend/data/cars/`, the ingestion manifest in `backend/app/rag/ingest.py`, and the RAG fixture coverage in `backend/tests/rag/` include approximately 30 vehicles across petrol, diesel, electric, and hybrid powertrains.
- [ ] T091 Execute the end-to-end acceptance journey in `frontend/tests/e2e/ai-car-advisor.spec.ts` against local services, covering registration, new chat, grounded recommendation, history reopen, favourite, comparison, EMI/fuel estimates, filter refinement, logout, and health response.

---

## Dependencies and Execution Order

### Phase Dependencies

- **Phase 1 Setup** has no dependencies and establishes the repository and toolchain.
- **Phase 2 Foundational** depends on Setup and blocks all user-story phases.
- **User Story 1** depends on Foundational and is the strict MVP entry point.
- **User Story 2** depends on User Story 1 for authenticated conversations and on Foundational for catalog retrieval.
- **User Story 3** depends on User Stories 1 and 2 because it persists and reopens the message and advisor flow.
- **User Story 4** depends on Foundational and User Story 1 for catalog access and authenticated ownership; recommendation-card integration can follow User Story 2.
- **User Story 5** depends on Foundational for MCP/configuration and on User Story 2 only for conversational tool integration; dedicated calculator work can begin once Foundational is complete.
- **User Story 6** depends on Foundational and User Story 1 for conversation-scoped state; advisor integration builds on User Story 2.
- **Phase 9 Polish** depends on all desired user stories and their focused tests.

### User Story Completion Order

The recommended delivery order is `US1 -> US2 -> US3 -> US4 -> US5 -> US6`. After
Phase 2, US4 and the dedicated portion of US5 can proceed in parallel with US2 when
team capacity allows, but the integrated product demonstration should use priority
order.

### Within Each User Story

Tests are listed before implementation tasks and should fail or expose missing
behavior before the implementation is added. Models and schemas precede services;
services precede endpoints; endpoints precede frontend integration. A story is
complete only when its independent test criteria pass without relying on unfinished
lower-priority stories.

## Parallel Execution Examples

### Setup and Foundation

- T002, T003, T004, T005, and T006 can run in parallel after T001.
- T010, T011, T012, T013, T014, T015, and T020 can run in parallel after the base project files exist.
- T016 and T017 are sequential because retrieval depends on the ingestion and embedding boundary; T018 and T019 can proceed in parallel with the implementation once their fixture paths exist.

### User Story 1

- T021, T022, and T023 can run in parallel as tests.
- T024, T025, and T026 can run in parallel before T027.
- T030 and T031 can run in parallel after the API response shapes are agreed.

### User Story 2

- T033, T034, T035, and T036 can run in parallel as tests.
- T037, T038, T039, and T041 can run in parallel after the shared schemas are available.
- T044 and T045 can run in parallel after T043 defines the response shape.

### User Story 3

- T047, T048, and T049 can run in parallel as tests.
- T052 can proceed in parallel with T050 and T051 after the history contract is stable.

### User Story 4

- T055, T056, and T057 can run in parallel as tests.
- T058, T059, and T060 can proceed in parallel because they use separate service/model boundaries.
- T062 and T063 can proceed in parallel after their respective API contracts are stable.

### User Story 5

- T064, T065, T066, T067, and T068 can run in parallel as tests.
- T069, T070, and T071 are sequential around the shared formula contract, but T073 can proceed in parallel after the request/response schema is stable.

### User Story 6

- T075, T076, T077, and T078 can run in parallel as tests.
- T079, T080, and T083 can proceed in parallel after the preference field contract is fixed.
- T081 and T082 are sequential because the API and advisor depend on the filter builder.

## Implementation Strategy

### Strict MVP: User Story 1

1. Complete Phase 1 Setup.
2. Complete Phase 2 Foundational.
3. Complete User Story 1.
4. Run the independent account and workspace tests.
5. Demonstrate private registration, login, new chat, logout, and re-login.

### Recommended Product MVP: User Stories 1-3

After the strict MVP, add grounded recommendations and persistent conversation
history. This delivers the smallest coherent product loop: authenticate, ask for a
car, receive grounded help, leave, and continue later.

### Incremental Delivery

1. Setup plus Foundational establishes the API, database, catalog, retrieval, and test seams.
2. User Story 1 adds the private authenticated workspace.
3. User Story 2 adds the central recommendation value.
4. User Story 3 adds durable continuity.
5. User Stories 4 and 5 add shortlist decision tools and deterministic affordability/running-cost estimates.
6. User Story 6 improves relevance with explicit preference and filter control.
7. Phase 9 hardens CI, security, responsive behavior, documentation, and end-to-end acceptance.

## Completion Criteria

- `tasks.md` contains 91 sequential tasks in the required checkbox, ID, optional `[P]`, optional story-label, and file-path format.
- Every user story has an independent test criterion and focused tests before implementation tasks.
- Every planned contract, durable entity, RAG boundary, calculator, UI workflow, and constitution quality gate maps to one or more tasks.
- The strict MVP is User Story 1; the recommended coherent product MVP is User Stories 1 through 3.
