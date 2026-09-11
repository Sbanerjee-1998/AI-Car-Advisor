# AI Car Advisor — Product Requirements Document
---

## 1. Product Overview

AI Car Advisor is a personalised conversational car-buying assistant that helps users discover, compare, and evaluate cars based on their budget, driving habits, preferences, and financial requirements.

Users can create accounts, start multiple conversations, receive car recommendations, ask follow-up questions, compare cars, view detailed car information, save favourite cars, and calculate EMI and fuel costs.

The application will use a curated knowledge base of approximately 30 cars, Retrieval-Augmented Generation (RAG) with ChromaDB, a LangChain-based agent, Gemini accessed through Google AI Studio, and two MCP tools for EMI and fuel-cost calculations.

The product should feel like a polished consumer mini-product rather than a technical AI demonstration.

---

## 2. Product Vision

Build a simple, trustworthy, conversational AI assistant that helps a user answer:

> “Which car should I buy for my needs and budget?”

The assistant should understand natural-language requirements, ask useful questions when information is missing, retrieve relevant vehicle information, recommend suitable cars, explain the recommendations, compare options, and perform financial calculations.

The technical architecture should demonstrate modern AI application development without making the user experience feel unnecessarily complex.

---

## 3. Goals

### Primary Goals

- Provide personalised car recommendations.
- Understand natural-language car-buying requirements.
- Ask intelligent follow-up questions when requirements are incomplete.
- Ground recommendations in a curated vehicle knowledge base.
- Use RAG and ChromaDB for vehicle information retrieval.
- Use a LangChain-based AI agent to coordinate retrieval and tools.
- Use Gemini through Google AI Studio as the LLM.
- Use MCP for programmatic EMI and fuel-cost calculations.
- Provide persistent user accounts and chat history.
- Allow users to compare cars.
- Allow users to view detailed car information.
- Allow users to save favourite cars.
- Provide a polished, responsive frontend.
- Demonstrate testing and CI/CD through GitHub Actions.

### Secondary Goals

- Keep the architecture understandable enough for a beginner to explain.
- Make the application easy to extend with more cars later.
- Keep external dependencies and infrastructure minimal.

---

## 4. Non-Goals

The project will not attempt to:

- Scrape live car prices from the internet.
- Provide guaranteed real-time prices or availability.
- Build a complete automotive marketplace.
- Process real vehicle purchases.
- Provide dealership booking.
- Provide insurance purchasing.
- Build multiple specialised AI agents.
- Build a complicated multi-service cloud architecture.
- Require a large external production database.
- Create a full administrator dashboard.
- Build a separate car marketplace/catalogue experience.
- Expose internal chain-of-thought reasoning.
- Add unnecessary AI features purely for technical complexity.

---

## 5. Target Users

### Primary User

An Indian car buyer who is unsure which car best fits their needs.

Examples:

- First-time car buyer.
- Family looking for a practical car.
- Daily commuter.
- User looking for an EV.
- User comparing petrol, diesel, hybrid, and EV options.
- User with a fixed monthly EMI budget.
- User who wants to compare two or three shortlisted cars.

### Example User

> “I have a budget of ₹12 lakh. I drive around 40 km every day, mostly in the city. I want an automatic petrol car with good mileage and safety.”

The assistant should understand the requirement and either recommend cars or ask one or two useful follow-up questions.

---

## 6. Core User Experience

The primary flow is:

**Open Application → Login/Register → Chat → New Chat → Describe Requirements → Follow-Up Questions → Understand Requirements → Retrieve Vehicle Information → Recommend Cars → Compare / View Details / Save / Calculate EMI or Fuel Cost**

The experience should feel conversational and simple.

The user should not need to understand RAG, agents, MCP, vector databases, or any other technical implementation detail.

---

## 7. Authentication

The application will provide application-level authentication.

### Registration

Users should be able to register using:

- Name
- Email
- Password
- Confirm Password

### Login

Users should be able to log in using:

- Email
- Password

### Requirements

- Passwords must never be stored as plain text.
- Passwords must be securely hashed.
- Users must only access their own conversations and favourites.
- Authentication state should persist appropriately.
- Invalid credentials should produce clear errors.
- Duplicate email registration should be prevented.
- Logout should be supported.

Social login is not required.

---

## 8. Chat Interface

The main interface should resemble a modern ChatGPT-style conversational application.

### Sidebar

The sidebar should contain:

- Application name/logo.
- **New Chat** button.
- Recent conversations.
- Conversation titles.
- Current user/account area.
- Logout option.

### Main Chat Area

The chat area should contain:

- User messages.
- AI messages.
- Loading state.
- Error state.
- Message input.
- Send button.
- Useful action buttons when applicable.

The interface should be clean and uncluttered.

---

## 9. Chat History

Chat history must persist between sessions.

Each conversation should have:

- Conversation ID.
- User ID.
- Title.
- Creation timestamp.
- Updated timestamp.

Each message should contain:

- Message ID.
- Conversation ID.
- Role (`user` or `assistant`).
- Content.
- Timestamp.

### Required Actions

Users should be able to:

- Create a new chat.
- Open an old chat.
- Continue an old chat.
- Delete a chat.
- See recent chats in the sidebar.

Conversation titles can be automatically generated from the first user message.

---

## 10. Conversation Memory

The assistant should maintain context within a conversation.

Example:

User:

> “I need an automatic petrol car under ₹12 lakh.”

Assistant:

> “How much do you drive per day?”

User:

> “Around 40 km.”

The assistant should understand that “40 km” refers to the user's daily driving distance.

The system should retain relevant conversation context while avoiding unnecessarily large prompts.

Optional simple cross-conversation preferences may be stored, such as:

- Preferred fuel type.
- Approximate budget.
- Preferred transmission.
- Body type.

---

## 11. User Preferences

Users may have persistent preferences.

Potential preference fields:

- Budget.
- Fuel type.
- Transmission.
- Body type.
- Seating requirement.
- Daily driving distance.
- Mileage preference.
- EV preference.
- Hybrid preference.

Preferences can be updated when users provide new information.

The application should not require users to fill out a long form before using the assistant.

Natural conversation should be the primary input method.

---

## 12. Car Recommendation

The assistant should recommend approximately **3 suitable cars** when enough information is available.

It should understand requirements such as:

- Budget.
- Fuel type.
- Transmission.
- Body type.
- Daily usage.
- Mileage.
- Safety.
- Seating capacity.
- EV range.
- Hybrid preference.
- City/highway usage.
- Family requirements.
- Performance preferences.

Example:

> “I need a car under ₹15 lakh, mostly for city driving, automatic, good mileage, and safe for a family of five.”

The assistant should retrieve relevant vehicle information and recommend suitable options.

---

## 13. Follow-Up Questions

The assistant should ask intelligent follow-up questions when critical information is missing.

Example:

User:

> “Suggest me a good SUV.”

The assistant may ask:

> “Sure. What is your approximate budget, and do you prefer petrol, diesel, hybrid, or EV?”

Follow-up questions should:

- Be concise.
- Ask only useful questions.
- Avoid interrogating the user.
- Prioritise information that materially affects recommendations.
- Continue to recommendations once enough information is available.

---

## 14. Recommendation Output

A recommendation should include:

- Car name.
- Approximate price.
- Fuel type.
- Transmission.
- Mileage or EV range where applicable.
- Key specifications.
- Why it matches the user's requirements.
- Advantages.
- Disadvantages.

Recommendations should be easy to scan.

Example:

### Tata Nexon

**Why it fits:** Good safety, practical size, suitable budget, and multiple powertrain options.

**Advantages**
- Strong safety proposition.
- Good feature set.
- Practical for city use.

**Considerations**
- Exact pricing varies by variant/location.
- Some variants may exceed the user's budget.

---

## 15. Recommendation Explanation

The assistant should provide a safe user-facing explanation called:

**“Why this car?”**

This explanation should summarise the factors that make the vehicle suitable.

It must not expose internal chain-of-thought.

Example:

> “I picked this because it fits your budget, offers an automatic option, has good city usability, and matches your preference for safety and mileage.”

The system should explain conclusions without revealing hidden reasoning traces.

---

## 16. Car Comparison

Users should be able to compare cars.

Comparison can be initiated:

1. Through chat.
2. Through UI actions associated with recommended vehicles.

The comparison should provide a structured table.

Potential comparison fields:

- Price.
- Fuel type.
- Transmission.
- Mileage.
- EV range.
- Engine.
- Battery.
- Seating capacity.
- Boot space.
- Safety.
- Key features.

A concise final recommendation should be provided after the comparison.

Example:

> “For your city-heavy usage, Car A is the better choice for efficiency, while Car B is better if you prioritise space.”

---

## 17. Comparison Actions

Users should be able to:

- Ask “Compare these two.”
- Ask “Which one should I choose?”
- Select cars using UI controls.
- Compare two or more shortlisted cars where supported.
- Ask follow-up questions about the comparison.

Comparison should reuse the same grounded vehicle information used by recommendations.

---

## 18. Car Details

Users should be able to request detailed information about a vehicle.

Details may include:

- Price.
- Fuel type.
- Transmission.
- Engine.
- Mileage.
- Battery capacity.
- EV range.
- Charging information.
- Seating.
- Boot space.
- Safety.
- Features.
- Pros.
- Cons.
- Best use cases.

The information should be retrieved from the curated knowledge base wherever possible.

---

## 19. Favourite Cars

Users should be able to save cars as favourites.

Required actions:

- Save a car.
- Remove a car.
- View saved/favourite cars.

Favourites are associated with the authenticated user.

One user must not be able to see another user's favourites.

---

## 20. Vehicle Filtering

The application should support filtering/retrieval based on:

- Budget.
- Fuel.
- Transmission.
- Body type.
- Seating.
- Usage.
- Mileage.
- EV.
- Hybrid.

Filtering does not need to become a full standalone search engine.

It can support recommendation and retrieval workflows.

---

## 21. Supported Vehicle Types

The knowledge base should support:

- Petrol.
- Diesel.
- Electric Vehicle (EV).
- Hybrid.

The architecture should allow additional powertrain types later.

---

## 22. Vehicle Knowledge Base

The initial knowledge base should contain approximately **30 cars**.

The data will be manually curated.

Example initial categories:

### Hatchbacks

- Maruti Suzuki Baleno
- Hyundai i20
- Maruti Suzuki Swift
- Tata Altroz
- Maruti Suzuki Fronx

### Compact SUVs

- Tata Nexon
- Hyundai Venue
- Kia Sonet
- Maruti Suzuki Brezza
- Mahindra XUV 3XO

### SUVs

- Hyundai Creta
- Kia Seltos
- Tata Harrier
- Mahindra Scorpio-N
- Mahindra XUV700

### Sedans

- Honda City
- Skoda Slavia
- Volkswagen Virtus
- Hyundai Verna

### EVs

- Tata Nexon EV
- Tata Punch EV
- MG Windsor EV
- MG ZS EV
- Hyundai Creta Electric

### Hybrid / Other

Additional relevant hybrid/vehicle entries should be added to reach approximately 30 vehicles.

Because vehicle specifications and availability can change, exact current specifications should be verified when the application data is curated.

---

## 23. Vehicle Data Structure

Each vehicle document should contain structured information such as:

```text
id
name
brand
body_type
fuel_type
transmission
price_range
engine
mileage
battery_capacity
ev_range
charging
seating_capacity
boot_space
safety
features
pros
cons
best_for
usage
```

Not every field is required for every vehicle.

For example, an ICE vehicle may not have battery capacity or EV charging information.

---

## 24. Data Source Strategy

Vehicle information will be manually curated into local Markdown documents.

Example:

```text
backend/data/cars/tata_nexon.md
backend/data/cars/hyundai_creta.md
backend/data/cars/tata_nexon_ev.md
```

The project will not implement live price scraping.

A disclaimer should state that prices and specifications are for demonstration/informational purposes and may change.

Users should verify final pricing and specifications with the manufacturer or dealer before purchasing.

---

## 25. RAG Architecture

The RAG pipeline should follow this general architecture:

```text
Vehicle Documents
       ↓
Document Loader
       ↓
Text Chunking
       ↓
Embeddings
       ↓
ChromaDB
       ↓
User Query
       ↓
Query Embedding
       ↓
Similarity Search
       ↓
Relevant Vehicle Context
       ↓
Gemini
       ↓
Grounded Response
```

The goal is to reduce hallucination and ensure vehicle recommendations are based on the curated knowledge base.

---

## 26. ChromaDB

ChromaDB will be used as the vector database.

Responsibilities:

- Store document embeddings.
- Store vehicle knowledge chunks.
- Store useful metadata.
- Perform similarity search.
- Provide relevant vehicle context to the AI layer.

The vector store should be persisted locally for the capstone.

Potential metadata:

- Car ID.
- Brand.
- Model.
- Fuel type.
- Body type.
- Transmission.
- Price range.

---

## 27. LLM

The application will use **Gemini through Google AI Studio**.

Google AI Studio will be used as the developer platform for accessing/configuring the Gemini model.

The model name should be configurable through environment variables rather than hard-coded throughout the application.

The exact SDK/package configuration should be selected based on the current supported libraries during implementation.

The LLM should be responsible for:

- Understanding natural-language requests.
- Extracting requirements.
- Asking follow-up questions.
- Generating natural-language recommendations.
- Explaining recommendations.
- Producing comparison conclusions.
- Coordinating with the agent/tool layer.

It should not perform calculations that are explicitly delegated to programmatic tools.

---

## 28. LangChain Agent

The project will use **one LangChain-based agent**.

The agent will coordinate:

- Vehicle knowledge retrieval.
- Recommendation workflow.
- EMI calculation.
- Fuel-cost calculation.
- Follow-up questions.
- Comparison requests.

The project intentionally avoids multiple agents to keep the architecture understandable and within scope.

---

## 29. Agent Behaviour

The agent should:

1. Understand the user's request.
2. Identify relevant requirements.
3. Detect missing information.
4. Ask concise follow-up questions if needed.
5. Retrieve relevant vehicle context.
6. Recommend appropriate vehicles.
7. Explain why the vehicles fit.
8. Compare vehicles when requested.
9. Call the EMI tool when financial calculations are required.
10. Call the fuel-cost tool when fuel expenses are requested.
11. Avoid inventing vehicle information.
12. Clearly state when information is unavailable.

The agent should proactively use tools when appropriate rather than requiring users to know which tool exists.

---

## 30. MCP Architecture

The application will include one MCP server exposing two tools.

```text
LangChain Agent
      ↓
    MCP
      ↓
 ┌───────────────┬────────────────────┐
 │ EMI Calculator│ Fuel Cost Calculator│
 └───────────────┴────────────────────┘
```

The MCP tools must perform deterministic calculations programmatically.

The LLM should provide inputs and interpret the results, but should not replace the mathematical implementation.

---

## 31. MCP Tool — EMI Calculator

Tool name:

```text
calculate_emi
```

Inputs:

```text
principal
annual_interest_rate
loan_duration_months
```

Outputs:

```text
monthly_emi
total_interest
total_payment
```

The tool should validate inputs and return clear errors for invalid values.

Example use:

> “What would my EMI be for a ₹10 lakh loan at 9% for 5 years?”

The agent should call the MCP EMI tool.

---

## 32. MCP Tool — Fuel Cost Calculator

Tool name:

```text
calculate_fuel_cost
```

Inputs:

```text
daily_distance_km
mileage_km_per_litre
fuel_price_per_litre
driving_days_per_month
```

Outputs:

```text
daily_fuel_cost
monthly_fuel_consumption
monthly_fuel_cost
annual_fuel_cost
```

The tool should validate inputs.

Example:

> “I drive 40 km daily, my car gives 18 km/l, and petrol costs ₹100/l. What will I spend per month?”

The agent should call the MCP fuel-cost tool.

---

## 33. EMI Formula

For a standard reducing-balance loan:

```text
P = Principal
R = Monthly interest rate
N = Number of monthly payments

R = Annual interest rate / 12 / 100

EMI = P × R × (1 + R)^N / ((1 + R)^N - 1)
```

The implementation must also support a zero-interest case:

```text
EMI = P / N
```

The tool should return:

```text
monthly_emi
total_interest
total_payment
```

Calculations must be performed programmatically.

---

## 34. Fuel Cost Formula

Daily fuel consumption:

```text
daily_fuel_consumption =
daily_distance_km / mileage_km_per_litre
```

Daily fuel cost:

```text
daily_fuel_cost =
daily_fuel_consumption × fuel_price_per_litre
```

Monthly fuel consumption:

```text
monthly_fuel_consumption =
daily_fuel_consumption × driving_days_per_month
```

Monthly fuel cost:

```text
monthly_fuel_cost =
monthly_fuel_consumption × fuel_price_per_litre
```

Annual fuel cost:

```text
annual_fuel_cost =
monthly_fuel_cost × 12
```

The calculation must be performed by the MCP tool rather than the LLM.

---

## 35. Application Database

The application will use:

- SQLite.
- SQLAlchemy.

SQLite is appropriate for the capstone because it is simple, local, and requires minimal infrastructure.

The database should store application state, while ChromaDB stores vectorised vehicle knowledge.

---

## 36. Database Models

### User

```text
id
name
email
password_hash
created_at
```

### Conversation

```text
id
user_id
title
created_at
updated_at
```

### Message

```text
id
conversation_id
role
content
created_at
```

### Favourite

```text
id
user_id
car_id
created_at
```

### Optional User Preference

```text
id
user_id
preference_key
preference_value
updated_at
```

Foreign keys and appropriate indexes should be used where useful.

---

## 37. API Design

The backend will expose REST APIs.

Suggested endpoints:

```text
POST   /api/auth/register
POST   /api/auth/login
POST   /api/auth/logout
GET    /api/auth/me

GET    /api/chats
POST   /api/chats
GET    /api/chats/{chat_id}
DELETE /api/chats/{chat_id}

POST   /api/chats/{chat_id}/messages

GET    /api/cars
GET    /api/cars/{car_id}

GET    /api/favourites
POST   /api/favourites
DELETE /api/favourites/{car_id}

POST   /api/compare

POST   /api/emi
POST   /api/fuel-cost

GET    /health
```

The exact API structure may be adjusted during implementation if required by the final architecture.

---

## 38. Chat API

Example request:

```json
{
  "message": "I need an automatic petrol car under ₹12 lakh"
}
```

Example response:

```json
{
  "answer": "Based on your requirements, I can suggest a few suitable options...",
  "conversation_id": "123"
}
```

The API should:

- Authenticate the user.
- Load conversation context.
- Process the message.
- Invoke the AI/agent workflow.
- Persist the user message.
- Persist the assistant response.
- Return the response to the frontend.

---

## 39. Dedicated EMI Calculator

The application should provide a dedicated EMI calculator UI in addition to the conversational MCP tool.

Suggested inputs:

- Loan amount.
- Interest rate.
- Loan tenure.

Suggested outputs:

- Monthly EMI.
- Total interest.
- Total payment.

The UI should clearly indicate that the calculator is a financial estimate and actual loan terms may vary.

The calculator should reuse the same programmatic calculation logic as the MCP tool where practical.

---

## 40. Dedicated Fuel Cost Calculator

The application should provide a dedicated fuel-cost calculator UI.

Inputs:

- Daily distance.
- Mileage.
- Fuel price.
- Driving days per month.

Outputs:

- Daily fuel cost.
- Monthly fuel consumption.
- Monthly fuel cost.
- Annual fuel cost.

The UI should be simple and easy to understand.

---

## 41. Security Requirements

Security requirements include:

- Never store plain-text passwords.
- Hash passwords securely.
- Store secrets in environment variables.
- Provide `.env.example`.
- Add `.env` to `.gitignore`.
- Validate API inputs.
- Protect authenticated endpoints.
- Ensure user data isolation.
- Do not expose API keys.
- Do not log secrets.
- Do not expose system prompts.
- Do not expose internal chain-of-thought.
- Validate ownership before accessing chats or favourites.

---

## 42. Environment Variables

Example:

```text
GOOGLE_API_KEY=
MODEL_NAME=
DATABASE_URL=
CHROMA_PERSIST_DIRECTORY=
SECRET_KEY=
```

Exact environment variable names may be adjusted based on the current supported SDKs and implementation.

A `.env.example` file must be committed.

The real `.env` file must not be committed.

---

## 43. Recommended Project Structure

```text
ai-car-advisor/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── agents/
│   │   ├── rag/
│   │   ├── models/
│   │   ├── database/
│   │   └── services/
│   │
│   ├── data/
│   │   └── cars/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── mcp/
│   ├── server.py
│   ├── tools/
│   │   ├── emi.py
│   │   └── fuel_cost.py
│   ├── tests/
│   └── requirements.txt
│
├── docs/
│   ├── architecture.md
│   └── screenshots/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── .env.example
├── PRD.md
└── README.md
```

The structure can be simplified during implementation if a component is not required.

---

## 44. Frontend Requirements

The frontend should:

- Be responsive.
- Work well on desktop.
- Have a polished chat interface.
- Provide a persistent sidebar.
- Provide New Chat.
- Display conversation history.
- Provide recommendation results clearly.
- Support comparison actions.
- Support car details.
- Support favourites.
- Include EMI calculator.
- Include fuel-cost calculator.
- Provide loading states.
- Provide error states.
- Handle authentication cleanly.

The frontend may use React or Next.js.

---

## 45. UI Design Requirements

The design should feel:

- Modern.
- Clean.
- Professional.
- Automotive-inspired.
- Conversational.
- Minimal.
- Easy to understand.

Avoid:

- Excessive animations.
- Developer dashboards.
- Unnecessary technical terminology.
- Overly flashy AI effects.
- Clutter.
- Excessive cards.

The application should prioritise usability over visual gimmicks.

---

## 46. Loading and Error States

The UI should clearly handle:

### Loading

Examples:

- AI is thinking.
- Loading chat history.
- Loading car information.
- Saving favourite.
- Calculating.

### Errors

Examples:

- Invalid login.
- Registration failure.
- AI request failure.
- Database failure.
- Invalid calculator input.
- Missing vehicle information.

Errors should be user-friendly and should not expose internal stack traces or secrets.

---

## 47. Hallucination Mitigation

The assistant should minimise hallucination by:

- Using RAG for vehicle information.
- Retrieving relevant vehicle documents.
- Giving the model grounded context.
- Avoiding unsupported claims.
- Clearly indicating unavailable information.
- Using programmatic tools for calculations.
- Avoiding invented specifications.
- Including a pricing/specification disclaimer.

The assistant should never present fabricated vehicle specifications as facts.

---

## 48. Testing Requirements

Testing should cover the most important functionality.

### Unit Tests

Test:

- EMI calculation.
- Zero-interest EMI.
- Invalid EMI inputs.
- Fuel-cost calculation.
- Invalid fuel inputs.
- Validation logic.

### RAG Tests

Test:

- Vehicle document loading.
- Document ingestion.
- ChromaDB retrieval.
- Relevant vehicle retrieval.

### API Tests

Test:

- Health endpoint.
- Registration.
- Login.
- Authentication.
- Chat creation.
- Sending messages.
- Chat history.
- Favourites.
- EMI endpoint.
- Fuel-cost endpoint.

### Agent Tests

Test representative flows such as:

- Recommendation.
- Follow-up question.
- Comparison.
- EMI tool invocation.
- Fuel-cost tool invocation.

Tests should focus on reliable core behaviour rather than trying to test every possible LLM response.

---

## 49. CI/CD Requirements

GitHub Actions should be used.

The CI workflow should run on:

- Push.
- Pull request.

Suggested steps:

1. Checkout repository.
2. Set up Python.
3. Install backend dependencies.
4. Run linting/format checks where configured.
5. Run backend tests.
6. Install frontend dependencies.
7. Build frontend.
8. Fail the workflow if required checks fail.

Deployment is optional.

The primary goal is to demonstrate automated quality checks through CI/CD.

---

## 50. GitHub Copilot Usage

GitHub Copilot should be used throughout development.

Recommended usage:

- Use **Plan mode** for planning larger implementation phases.
- Use **Agent mode** for multi-file implementation tasks.
- Use **Ask mode** for questions and explanations.
- Give Copilot the relevant PRD/context.
- Break large features into smaller implementation tasks.
- Review generated code before accepting it.
- Run tests after meaningful changes.
- Ask Copilot to explain unfamiliar code.
- Avoid giving one enormous prompt that asks Copilot to build the entire application at once.

Copilot should accelerate development, not replace understanding of the architecture.

---

## 51. Development Phases

### Phase 1 — Project Setup

- Create repository.
- Create project folders.
- Configure Python environment.
- Configure frontend.
- Configure Git.
- Add `.gitignore`.
- Add `.env.example`.
- Add PRD.

### Phase 2 — Backend Foundation

- Create FastAPI application.
- Configure SQLite.
- Configure SQLAlchemy.
- Create health endpoint.
- Establish backend structure.

### Phase 3 — Authentication

- User model.
- Registration.
- Login.
- Password hashing.
- Authentication middleware/dependencies.
- Logout.
- User isolation.

### Phase 4 — Chat

- Conversation model.
- Message model.
- Create chat.
- Send messages.
- Persist history.
- Retrieve chats.

### Phase 5 — Vehicle Knowledge Base

- Create approximately 30 vehicle documents.
- Establish document format.
- Add vehicle metadata.

### Phase 6 — RAG

- Load vehicle documents.
- Chunk documents.
- Generate embeddings.
- Store embeddings in ChromaDB.
- Implement similarity retrieval.

### Phase 7 — Agent

- Integrate LangChain.
- Integrate Gemini.
- Connect RAG retrieval.
- Implement recommendation workflow.
- Implement follow-up behaviour.
- Implement comparison workflow.

### Phase 8 — MCP

- Create MCP server.
- Implement EMI tool.
- Implement fuel-cost tool.
- Connect tools to the agent.
- Add tool tests.

### Phase 9 — Car Features

- Car details.
- Recommendations.
- Comparison.
- Favourites.
- Filtering.
- EV/hybrid handling.

### Phase 10 — Dedicated Calculators

- EMI calculator UI/API.
- Fuel-cost calculator UI/API.

### Phase 11 — Frontend Polish

- ChatGPT-style sidebar.
- New Chat.
- Authentication screens.
- Recommendation UI.
- Comparison UI.
- Favourites.
- Calculators.
- Loading/error states.
- Responsive design.

### Phase 12 — Testing

- Unit tests.
- API tests.
- RAG tests.
- Agent/tool tests.
- Frontend checks.

### Phase 13 — CI/CD

- GitHub Actions.
- Automated tests.
- Frontend build.
- Quality checks.

### Phase 14 — Documentation

- README.
- Architecture documentation.
- Setup instructions.
- Environment configuration.
- Demo instructions.
- Screenshots where useful.

---

## 52. Performance Requirements

The application is designed for normal capstone workloads.

Requirements:

- Chat responses should show an appropriate loading state.
- ChromaDB should use local persistent storage.
- Chat history should load efficiently.
- API calls should avoid unnecessary repeated work.
- The frontend should remain responsive.
- Large prompts should be avoided where possible.
- Conversation context should be managed sensibly.

Production-scale optimisation is not required.

---

## 53. Data and Pricing Disclaimer

The application should clearly communicate that:

- Vehicle prices may change.
- Prices may vary by city and variant.
- Specifications may change.
- Availability may change.
- EMI estimates are illustrative.
- Fuel costs depend on actual mileage and fuel price.
- Users should verify final information with the manufacturer/dealer before purchasing.

No live pricing is required for the capstone.

---

## 54. UX Principles

The product should be:

- Helpful.
- Professional.
- Simple.
- Modern.
- Conversational.
- Trustworthy.

The product should not feel like:

- A developer dashboard.
- An AI research prototype.
- A technical RAG demo.
- An unnecessarily complicated enterprise system.
- A collection of disconnected AI features.

The user should feel like they are talking to a knowledgeable car-buying assistant.

---

## 55. Capstone Demo Flow

Recommended demonstration:

### Step 1 — Login

Show registration/login and authenticated application access.

### Step 2 — New Chat

Create a new conversation.

### Step 3 — Recommendation

Ask:

> “I need an automatic petrol car under ₹12 lakh for mostly city driving.”

Show the assistant asking a useful follow-up if needed.

### Step 4 — Recommendation

Show approximately three suitable cars and the “Why this car?” explanations.

### Step 5 — Comparison

Compare two recommended cars through chat and/or UI.

### Step 6 — EMI

Ask:

> “What would my EMI be for a ₹10 lakh loan at 9% for 5 years?”

Show the MCP EMI tool being used.

### Step 7 — Fuel Cost

Ask:

> “I drive 40 km every day. How much would fuel cost monthly?”

Show the MCP fuel-cost tool being used.

### Step 8 — Save

Save a preferred vehicle as a favourite.

### Step 9 — Chat History

Open another previous conversation from the sidebar.

### Step 10 — Technical Architecture

Briefly explain:

```text
React/Next.js
      ↓
FastAPI
      ↓
LangChain Agent
   ↙       ↘
RAG       MCP Tools
 ↓          ↓
ChromaDB   EMI/Fuel
 ↓
Gemini via Google AI Studio
```

### Step 11 — Engineering

Show:

- Tests.
- GitHub repository.
- GitHub Actions.
- README.

---

## 56. Capstone Presentation Story

The presentation should tell this story:

### Problem

Car buying is confusing because users must consider budget, fuel type, mileage, transmission, safety, usage, and financing.

### Solution

AI Car Advisor turns those requirements into a conversational recommendation experience.

### User Experience

The user talks naturally with the assistant instead of filling out a complicated form.

### RAG

Vehicle information is retrieved from a curated knowledge base using ChromaDB.

### Agent

A LangChain agent coordinates understanding, retrieval, recommendations, comparisons, and tool usage.

### MCP

MCP exposes deterministic EMI and fuel-cost tools.

### Gemini

Gemini accessed through Google AI Studio provides the natural-language intelligence.

### CI/CD

GitHub Actions automatically validates the project through tests and frontend builds.

### Result

A useful end-to-end AI product rather than a collection of disconnected demonstrations.

---

## 57. MVP Priority

### Must Work

- Registration.
- Login.
- Chat.
- New Chat.
- Persistent chat history.
- Gemini integration.
- Vehicle knowledge base.
- ChromaDB.
- RAG.
- LangChain agent.
- Car recommendations.
- Follow-up questions.
- Car comparison.
- EMI MCP tool.
- Fuel-cost MCP tool.
- Tests.
- GitHub Actions.

### Should Work

- Favourites.
- Dedicated EMI calculator.
- Dedicated fuel-cost calculator.
- Filtering.
- Loading states.
- Error states.
- User preferences.

### Nice to Have

- Streaming responses.
- Advanced UI animations.
- Advanced filtering.
- Additional vehicle capabilities.

---

## 58. Scope Protection

To ensure the capstone remains achievable:

Do not add:

- New external services unless necessary.
- Complex cloud infrastructure.
- Web scraping.
- Multiple agents.
- Another vector database.
- Another application database.
- Additional MCP servers unless essential.
- Unnecessary admin dashboards.
- Marketplace functionality.
- Real purchasing/payment functionality.

The guiding rule is:

> Complete and polished core functionality is more valuable than a large number of incomplete AI features.

---

## 59. Definition of Done

### Authentication

- [ ] User registration works.
- [ ] User login works.
- [ ] Passwords are securely hashed.
- [ ] Users can log out.
- [ ] User data is isolated.

### Chat

- [ ] New chat works.
- [ ] Messages are persisted.
- [ ] Chat history is persisted.
- [ ] Previous conversations can be reopened.
- [ ] Conversations can be deleted.

### AI

- [ ] Gemini works.
- [ ] Natural-language requirements are understood.
- [ ] Follow-up questions work.
- [ ] Recommendations work.
- [ ] Recommendation explanations work.
- [ ] Comparison works.

### RAG

- [ ] Vehicle documents exist.
- [ ] Documents are ingested.
- [ ] Embeddings are stored in ChromaDB.
- [ ] Relevant vehicle context is retrieved.
- [ ] Responses use grounded vehicle information.

### MCP

- [ ] EMI MCP tool works.
- [ ] Fuel-cost MCP tool works.
- [ ] Agent can invoke both tools.
- [ ] Tool calculations are programmatic.
- [ ] Tool tests pass.

### User Features

- [ ] Car details work.
- [ ] Favourites work.
- [ ] Filtering/retrieval works.
- [ ] EV support works.
- [ ] Hybrid support works.
- [ ] Dedicated EMI calculator works.
- [ ] Dedicated fuel calculator works.

### Engineering

- [ ] Environment variables are configured.
- [ ] Secrets are excluded from Git.
- [ ] Backend tests pass.
- [ ] Frontend builds successfully.
- [ ] GitHub Actions passes.
- [ ] README is complete.
- [ ] Architecture documentation is included.

### Presentation

- [ ] End-to-end demo works.
- [ ] RAG architecture can be explained.
- [ ] ChromaDB role can be explained.
- [ ] LangChain agent can be explained.
- [ ] MCP can be explained.
- [ ] Gemini/Google AI Studio integration can be explained.
- [ ] CI/CD can be demonstrated.

---

## 60. Technical Stack

### Frontend

- React or Next.js.
- Modern CSS/UI approach appropriate to the selected frontend.
- Responsive design.

### Backend

- Python.
- FastAPI.
- SQLAlchemy.
- SQLite.

### AI

- Gemini.
- Google AI Studio.
- LangChain.
- LangChain Agent.

### RAG

- ChromaDB.
- Embeddings.
- Curated Markdown vehicle documents.

### Tools

- MCP.
- EMI Calculator.
- Fuel Cost Calculator.

### Testing

- Python testing framework such as pytest.
- Appropriate frontend testing/build checks.

### DevOps

- GitHub.
- GitHub Actions.
- Git.
- CI/CD workflow.

### Development

- VS Code.
- GitHub Copilot.

---

## 61. Final Product Principle

The most important principle for the project is:

> **A working end-to-end product is more valuable than technical complexity.**

Priority order:

1. Working core functionality.
2. Reliable AI behaviour.
3. Grounded vehicle information.
4. Useful recommendations.
5. MCP tools that actually work.
6. Persistent user experience.
7. Polished UI.
8. Tests and CI/CD.
9. Technical sophistication only where it improves the product.

The final application should demonstrate that modern AI technologies can be combined into a practical product:

```text
User
 ↓
React / Next.js Frontend
 ↓
FastAPI Backend
 ↓
LangChain Agent
 ├───────────────┐
 ↓               ↓
RAG             MCP
 ↓               ├── EMI Calculator
ChromaDB         └── Fuel Cost Calculator
 ↓
Curated Vehicle Knowledge
 ↓
Gemini via Google AI Studio
```

The user should experience a simple car-buying assistant.

The technical architecture should demonstrate:

- LLM integration.
- RAG.
- Vector database.
- Agent.
- MCP.
- Tool calling.
- Application database.
- Authentication.
- Testing.
- CI/CD.
