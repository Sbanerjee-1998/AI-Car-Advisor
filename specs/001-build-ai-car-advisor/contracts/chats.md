# Chat Contract

All chat endpoints require the current authenticated session. Conversation IDs are opaque identifiers. The server resolves ownership from the session, never from a client-supplied user ID.

## `GET /api/chats`

Return the current user's conversations ordered by most recently updated.

Response `200`:

```json
{
  "items": [
    {
      "id": "conversation-id",
      "title": "Family automatic SUV",
      "created_at": "2026-09-10T09:00:00Z",
      "updated_at": "2026-09-10T09:05:00Z"
    }
  ]
}
```

## `POST /api/chats`

Create an empty conversation.

Request:

```json
{
  "title": null
}
```

Response `201` returns the conversation summary.

## `GET /api/chats/{chat_id}`

Return an owned conversation, its visible messages, and current structured preferences. Response `200`:

```json
{
  "id": "conversation-id",
  "title": "Family automatic SUV",
  "messages": [
    {
      "id": "message-id",
      "role": "user",
      "content": "I need an automatic car for a family of five.",
      "created_at": "2026-09-10T09:01:00Z"
    }
  ],
  "preferences": {
    "fuel_type": null,
    "transmission": "automatic",
    "seating_capacity": 5
  }
}
```

An unowned or missing conversation returns `404`.

## `DELETE /api/chats/{chat_id}`

Delete an owned conversation and its messages/preferences. Response `204`. Missing or unowned conversations return `404`.

## `POST /api/chats/{chat_id}/messages`

Accept a user turn, run the bounded-context advisor flow, persist the visible user and assistant messages, and return structured UI data.

Request:

```json
{
  "content": "My budget is about 12 lakh and I drive 40 km daily."
}
```

Response `200`:

```json
{
  "conversation_id": "conversation-id",
  "user_message": {
    "id": "user-message-id",
    "role": "user",
    "content": "My budget is about 12 lakh and I drive 40 km daily.",
    "created_at": "2026-09-10T09:05:00Z"
  },
  "assistant_message": {
    "id": "assistant-message-id",
    "role": "assistant",
    "content": "A few details will help me narrow this down.",
    "created_at": "2026-09-10T09:05:01Z"
  },
  "recommendations": [],
  "follow_up_required": true,
  "available_actions": [],
  "disclaimer": "Prices and specifications are approximate and should be verified with an authorized dealer."
}
```

For a completed recommendation, `recommendations` contains at most three canonical vehicle items. `available_actions` may include `compare`, `view_details`, `save_favourite`, `calculate_emi`, or `calculate_fuel_cost`. Internal prompts, hidden reasoning, raw tool traces, and credentials are never returned.
