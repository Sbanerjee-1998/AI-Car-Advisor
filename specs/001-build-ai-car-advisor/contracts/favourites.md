# Favourites Contract

All favourite endpoints require an authenticated session and scope records to the current user.

## `GET /api/favourites`

Response `200`:

```json
{
  "items": [
    {
      "vehicle_id": "tata-nexon-2025",
      "created_at": "2026-09-10T09:10:00Z",
      "vehicle": {
        "id": "tata-nexon-2025",
        "name": "Tata Nexon",
        "fuel_type": "petrol"
      }
    }
  ]
}
```

## `POST /api/favourites`

Request:

```json
{
  "vehicle_id": "tata-nexon-2025"
}
```

Response `201` returns the favourite and canonical vehicle summary. Unknown vehicle IDs return `404`; an existing user/vehicle pair returns `409` or an idempotent `200`, chosen consistently by implementation.

## `DELETE /api/favourites/{car_id}`

Delete the current user's favourite for the stable vehicle slug. Response `204`. Missing records return `404` without revealing another user's favourite.
