# Feature Specification: AI Car Advisor

**Feature Branch**: `001-build-ai-car-advisor`

**Created**: 2026-09-10

**Status**: Ready for Planning

**Input**: User description: `#file:constitution.md #file:prd.md` — specify the AI Car Advisor product within the project constitution.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create an Account and Start a Conversation (Priority: P1)

As a car buyer, I want to create an account, sign in, and start a new conversation so
that my car-buying work is private and can continue across sessions.

**Why this priority**: An authenticated workspace is the entry point for the primary
product journey and is required to protect conversations and saved vehicles.

**Independent Test**: A new user can register, sign in, create a conversation, sign
out, and sign back in to see the conversation again.

**Acceptance Scenarios**:

1. **Given** a visitor has a valid name, email, password, and matching confirmation,
   **When** they submit registration, **Then** an account is created and the user
   enters the authenticated workspace.
2. **Given** an email is already registered, **When** another registration is
   submitted with that email, **Then** registration is rejected with a clear message
   and no second account is created.
3. **Given** a user enters invalid credentials, **When** they submit the login form,
   **Then** access is denied with a user-safe error and no private data is shown.
4. **Given** an authenticated user selects New Chat, **When** the workspace opens the
   conversation, **Then** an empty conversation is ready for the first message.
5. **Given** an authenticated user selects Logout, **When** the session ends, **Then**
   private workspace data is no longer accessible until the user signs in again.

---

### User Story 2 - Receive a Personalised Car Recommendation (Priority: P1)

As a car buyer, I want to describe my needs in natural language and receive a small
set of suitable cars so that I can make a confident shortlist without completing a
long form.

**Why this priority**: Personalised recommendations are the central user value of the
product and the main reason to use the assistant.

**Independent Test**: A signed-in user can describe a budget and driving needs in one
message, answer a follow-up question if needed, and receive a grounded shortlist with
clear reasons for each choice.

**Acceptance Scenarios**:

1. **Given** a user provides enough information about budget, usage, and preferences,
   **When** they send the request, **Then** the assistant presents up to three
   suitable vehicles with price guidance, powertrain, transmission, relevant mileage
   or range, key specifications, reasons they fit, advantages, and considerations.
2. **Given** a request is missing information that materially changes the shortlist,
   **When** the user sends it, **Then** the assistant asks only the most useful one or
   two follow-up questions before recommending cars.
3. **Given** the user answers a follow-up question with a short contextual reply such
   as a daily distance, **When** the assistant processes the reply, **Then** it uses
   that answer as part of the existing car-buying request rather than treating it as a
   new unrelated request.
4. **Given** no catalog vehicle satisfies every stated preference, **When** the user
   requests recommendations, **Then** the assistant explains the trade-off and offers
   the closest supported alternatives without inventing vehicle facts.
5. **Given** a recommendation includes prices or specifications, **When** it is shown
   to the user, **Then** it identifies the information as approximate and advises the
   user to verify final details with the manufacturer or dealer.

---

### User Story 3 - Return to Previous Conversations (Priority: P1)

As a returning car buyer, I want my conversations and messages to persist so that I
can continue evaluating cars without repeating my requirements.

**Why this priority**: Persistent context makes the assistant useful over multiple
sessions and supports the user's normal comparison and decision process.

**Independent Test**: A user can create a conversation, exchange messages, leave the
application, return later, reopen the conversation, and continue with the prior
context.

**Acceptance Scenarios**:

1. **Given** a user has exchanged messages in a conversation, **When** they return to
   the application, **Then** the conversation appears in the recent conversation list
   with a useful title and updated ordering.
2. **Given** a user opens a previous conversation, **When** the messages load, **Then**
   they appear in chronological order and the assistant can answer a follow-up using
   relevant earlier context.
3. **Given** a user deletes a conversation, **When** deletion is confirmed, **Then**
   it no longer appears in the user's conversation list and cannot be reopened.
4. **Given** two different users have conversations, **When** either user views their
   history, **Then** they can see only their own conversations and messages.
5. **Given** a conversation has no messages, **When** the user leaves or deletes it,
   **Then** the application handles the empty conversation without an error.

---

### User Story 4 - Compare, Inspect, and Save Shortlisted Cars (Priority: P2)

As a car buyer, I want to inspect vehicle details, compare shortlisted cars, and save
favourites so that I can narrow my decision using information that is easy to scan.

**Why this priority**: Comparison and saved shortlists turn a conversational answer into
an ongoing buying workflow.

**Independent Test**: A user can open a recommended car, select two or three cars for
comparison, receive a structured comparison and conclusion, and save or remove a
favourite.

**Acceptance Scenarios**:

1. **Given** a vehicle is shown in a recommendation, **When** the user opens its
   details, **Then** they can see supported information such as price guidance,
   powertrain, transmission, engine or battery, mileage or range, charging details
   where relevant, seating, boot space, safety, features, advantages, considerations,
   and best-use guidance.
2. **Given** a user selects two or three supported vehicles, **When** they request a
   comparison, **Then** the application shows a consistent table covering shared
   fields and clearly marks unavailable fields.
3. **Given** a comparison is displayed, **When** the assistant provides its conclusion,
   **Then** it explains which vehicle better fits the stated priorities and identifies
   the trade-off rather than declaring an unsupported universal winner.
4. **Given** a user saves a vehicle, **When** the save succeeds, **Then** the vehicle
   appears in that user's favourites and remains available after a later sign-in.
5. **Given** a vehicle is already saved, **When** the user removes it, **Then** it is
   removed from the user's favourites without changing another user's favourites.
6. **Given** a user requests a comparison with fewer than two or more than three
   vehicles, **When** the request is submitted, **Then** the application explains the
   supported selection size and lets the user correct it.

---

### User Story 5 - Estimate Loan and Fuel Costs (Priority: P2)

As a car buyer, I want to calculate loan payments and running fuel costs directly or
through the conversation so that I can evaluate affordability beyond the sticker price.

**Why this priority**: Financial estimates are important decision inputs, but the
product can still recommend cars if a user does not use a calculator.

**Independent Test**: A user can enter valid loan or fuel inputs, receive all requested
outputs, and see clear validation for invalid inputs.

**Acceptance Scenarios**:

1. **Given** a positive loan amount, interest rate, and loan duration, **When** the
   user calculates an EMI estimate, **Then** the application shows monthly payment,
   total interest, and total payment.
2. **Given** a zero-interest loan with a positive duration, **When** the user calculates
   an EMI estimate, **Then** the monthly payment equals the loan amount divided by the
   number of payments and the totals are consistent.
3. **Given** a negative, zero, or otherwise invalid loan input, **When** the user
   calculates an estimate, **Then** the application rejects the request with a clear
   correction message and does not show a misleading result.
4. **Given** valid daily distance, mileage, fuel price, and monthly driving-day inputs,
   **When** the user calculates fuel cost, **Then** the application shows daily cost,
   monthly consumption, monthly cost, and annual cost.
5. **Given** mileage, fuel price, or driving days are zero or invalid, **When** the user
   calculates fuel cost, **Then** the application explains the invalid field and does
   not divide by zero or return a misleading estimate.
6. **Given** a user asks for an EMI or fuel estimate in a conversation, **When** the
   assistant answers, **Then** it returns the same deterministic result and labels the
   values as estimates.

---

### User Story 6 - Refine Discovery with Preferences and Filters (Priority: P3)

As a car buyer, I want recommendations to reflect preferences such as fuel type,
transmission, body type, seating, usage, mileage, EV range, or hybrid preference so
that irrelevant vehicles are easier to exclude.

**Why this priority**: Preference-aware discovery improves recommendation quality while
remaining secondary to the core conversation and shortlist flow.

**Independent Test**: A user can set or state a preference, apply one or more supported
filters, and verify that returned vehicles reflect those constraints or explain why no
exact match exists.

**Acceptance Scenarios**:

1. **Given** a user states a preference during a conversation, **When** later
   recommendations are requested in that conversation, **Then** the assistant uses
   the preference unless the user changes it.
2. **Given** a user applies supported filters for budget, fuel, transmission, body type,
   seating, usage, mileage, EV, or hybrid, **When** matching vehicles are requested,
   **Then** the results reflect the selected filters.
3. **Given** filters conflict or produce no exact match, **When** the user requests
   results, **Then** the application identifies the conflict or empty result and offers
   a clear way to broaden the request.
4. **Given** a user provides a new preference that conflicts with an older preference,
   **When** the new preference is accepted, **Then** the newer preference is used for
   subsequent recommendations and the user is not required to edit a long form.

---

### Edge Cases

- A user submits an empty message, whitespace-only message, or an extremely long
  message; the application requests usable input without crashing.
- A user asks for a vehicle category without a budget or powertrain preference; the
  assistant asks a concise high-value follow-up question.
- A user gives contradictory requirements, such as an EV-only request and a petrol-only
  request; the assistant identifies the conflict and asks which priority to keep.
- A user asks about a vehicle or specification outside the curated catalog; the assistant
  states that the information is unavailable instead of guessing.
- A vehicle has no value for a field such as EV range, battery, or charging; the UI marks
  that field as not applicable or unavailable.
- A user loses an authenticated session while loading a chat, favourite, or calculator;
  the application asks them to sign in again without exposing private content.
- The recommendation service, catalog, or calculation service fails; the UI shows a
  user-safe error and preserves already entered input where possible.
- A user attempts to access another user's conversation or favourite by changing an
  identifier; the request is denied without revealing whether the record exists.
- A user requests prices, availability, or specifications as guaranteed current facts;
  the assistant repeats the informational disclaimer and does not claim live accuracy.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow a user to register with name, email, password, and
  password confirmation.
- **FR-002**: The system MUST reject malformed registration data, mismatched passwords,
  and duplicate email addresses with clear user-facing messages.
- **FR-003**: The system MUST allow a registered user to sign in, remain signed in for
  the active session, and sign out.
- **FR-004**: The system MUST prevent unauthenticated users from viewing another user's
  conversations, messages, preferences, or favourites.
- **FR-005**: The system MUST allow an authenticated user to create, open, continue, and
  delete conversations.
- **FR-006**: The system MUST save every accepted user and assistant message with its
  conversation and timestamp, and MUST display messages in chronological order.
- **FR-007**: The system MUST create a useful conversation title from the first user
  message or provide an equivalent identifiable title.
- **FR-008**: The assistant MUST retain relevant conversation context while avoiding
  unrelated or unnecessarily large history in later responses.
- **FR-009**: The assistant MUST understand, when provided, budget, fuel type,
  transmission, body type, seating, daily distance, city or highway usage, mileage,
  safety, EV range, hybrid preference, and performance needs.
- **FR-010**: The assistant MUST ask concise, materially useful follow-up questions when
  critical recommendation information is missing.
- **FR-011**: The assistant MUST provide approximately three suitable vehicles when
  enough information is available, and MUST provide fewer with an explanation when
  the supported catalog cannot supply three credible matches.
- **FR-012**: Each recommendation MUST include the vehicle name, approximate price,
  powertrain, transmission, mileage or EV range where applicable, key specifications,
  why it fits, advantages, and considerations.
- **FR-013**: Recommendations, comparisons, and vehicle details MUST use only supported
  information from the curated vehicle catalog and MUST clearly identify unavailable
  information.
- **FR-014**: The system MUST display an informational disclaimer explaining that prices,
  specifications, variants, and availability can change and must be verified before a
  purchase.
- **FR-015**: The system MUST allow a user to compare two or three selected vehicles in
  a consistent table covering price, powertrain, transmission, mileage or range,
  engine or battery, seating, boot space, safety, and key features when available.
- **FR-016**: A comparison MUST include a concise conclusion tied to the user's stated
  priorities and MUST identify meaningful trade-offs.
- **FR-017**: The system MUST provide a detailed view for each supported vehicle,
  including all available specifications, features, advantages, considerations, and
  best-use guidance.
- **FR-018**: The system MUST allow users to save, view, and remove favourite vehicles.
- **FR-019**: Favourites MUST be isolated per user and MUST persist across later sign-ins.
- **FR-020**: The system MUST support recommendation and retrieval constraints for budget,
  fuel, transmission, body type, seating, usage, mileage, EV, and hybrid preferences.
- **FR-021**: The system MUST update the active conversation's preferences when a user
  provides a new preference and MUST use the newest preference for later recommendations.
- **FR-022**: The system MUST provide an EMI estimate from loan amount, annual interest
  rate, and loan duration, returning monthly payment, total interest, and total payment.
- **FR-023**: EMI estimates MUST support zero interest and MUST reject non-positive or
  otherwise invalid loan values with clear validation messages.
- **FR-024**: The system MUST provide a fuel-cost estimate from daily distance, mileage,
  fuel price, and monthly driving days, returning daily cost, monthly consumption,
  monthly cost, and annual cost.
- **FR-025**: Fuel-cost estimates MUST reject non-positive or otherwise invalid values and
  MUST never return a division-by-zero or misleading result.
- **FR-026**: The assistant MUST use the same validated calculation rules for financial
  questions asked in conversation and for dedicated calculator interactions.
- **FR-027**: The UI MUST show loading, success, empty, and user-safe error states for
  authentication, conversation loading, assistant responses, favourites, vehicle data,
  comparisons, and calculations.
- **FR-028**: The catalog MUST support petrol, diesel, electric, and hybrid vehicles and
  MUST allow approximately 30 manually curated vehicles in the initial release.
- **FR-029**: The system MUST not present live prices, guaranteed availability, or
  unsupported vehicle claims, and MUST not support vehicle purchasing, dealership
  booking, insurance purchasing, or marketplace transactions.
- **FR-030**: The experience MUST be usable on desktop and mobile layouts without requiring
  users to understand the underlying AI, retrieval, database, or tool terminology.

### Key Entities

- **User Account**: A person's identity, sign-in credentials, and account timestamps.
- **Conversation**: A user's titled, timestamped workspace for an ongoing car-buying
  discussion.
- **Message**: A user or assistant contribution belonging to a conversation.
- **Vehicle Profile**: A curated vehicle record containing identity, pricing guidance,
  powertrain, specifications, features, advantages, considerations, and supported use
  cases.
- **User Preference**: A current or historical car-buying preference such as budget,
  fuel, transmission, body type, seating, usage, mileage, EV, or hybrid preference.
- **Recommendation**: A vehicle suggestion with its supporting fit explanation and
  limitations for the current request.
- **Favourite**: A user-owned saved reference to a vehicle profile.
- **Comparison**: A structured view of two or three vehicle profiles and a conclusion
  based on the user's priorities.
- **Financial Estimate**: A calculated EMI or fuel-cost result with its input values,
  output values, and estimate disclaimer.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of new users in acceptance testing can register or sign in
  and start a first conversation within two minutes without assistance.
- **SC-002**: For at least 90% of representative car-buying prompts, the assistant
  produces a credible shortlist or asks a materially useful follow-up question within
  the first two assistant responses.
- **SC-003**: In 100% of successful recommendation acceptance tests, every presented
  vehicle includes a fit explanation, at least one advantage, at least one
  consideration, and the applicable approximate-data disclaimer.
- **SC-004**: In 100% of authorization acceptance tests, a user cannot view, change,
  or delete another user's conversations, messages, preferences, or favourites.
- **SC-005**: At least 90% of returning-user acceptance tests can reopen a previous
  conversation and continue it without re-entering the original requirements.
- **SC-006**: At least 90% of comparison acceptance tests let a user compare two cars
  and reach a stated, priority-based conclusion within two minutes.
- **SC-007**: In 100% of valid calculator reference cases, EMI and fuel-cost outputs
  match independently calculated results after rounding to two decimal places.
- **SC-008**: In 100% of invalid calculator cases, the user sees a field-specific
  correction message and no misleading numeric result.
- **SC-009**: At least 90% of representative failure scenarios show a user-safe error
  state while preserving recoverable user input.
- **SC-010**: At least 90% of usability-test participants can complete the journey from
  describing needs to saving or comparing a car without learning technical product
  terminology.
- **SC-011**: The initial catalog provides credible options across petrol, diesel,
  electric, and hybrid powertrains and contains approximately 30 supported vehicles.

## Assumptions

- The initial audience is car buyers in India, and monetary examples use INR unless a
  later product decision expands currency support.
- Email and password authentication is the initial sign-in method; social login and
  password recovery are outside this feature's first release unless separately specified.
- Conversations, preferences, and favourites require an authenticated account. Public
  marketing pages are outside this feature.
- The initial vehicle catalog is manually curated and updated as a project data release;
  live price, inventory, and availability feeds are not required.
- The catalog contains approximately 30 vehicles across the supported powertrain types,
  with some fields legitimately unavailable for a given vehicle.
- The initial comparison experience supports two or three vehicles to keep the result
  readable and useful on mobile screens.
- Users expect estimates and decision support, not financial advice, a purchase
  guarantee, or a substitute for manufacturer or dealer verification.
- Standard web connectivity is available during use. When connectivity or an external
  assistant dependency fails, the application presents a recoverable error state.
- Natural-language conversation is the primary way to provide preferences; a long
  mandatory intake form is not required.
