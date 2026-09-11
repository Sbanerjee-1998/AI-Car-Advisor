# Vehicle Catalog Contract

Vehicle endpoints expose the curated catalog and do not trigger live scraping.

## `GET /api/cars`

List catalog vehicles with optional filters. Supported filters include `fuel_type`, `transmission`, `body_type`, `seating_capacity`, `price_min_inr`, `price_max_inr`, and a bounded text `q` search.

Response `200`:

```json
{
  "items": [
    {
      "id": "tata-nexon-2025",
      "name": "Tata Nexon",
      "manufacturer": "Tata",
      "fuel_type": "petrol",
      "transmission": "automatic",
      "body_type": "suv",
      "seating_capacity": 5,
      "price_min_inr": 800000,
      "price_max_inr": 1500000
    }
  ],
  "total": 1
}
```

Prices are informational ranges from curated data and carry the standard verification disclaimer in user-facing contexts.

## `GET /api/cars/{car_id}`

Return the full curated profile for a stable vehicle slug, including known specifications, features, use cases, advantages, considerations, and unavailable markers for missing fields. Missing slugs return `404`.

## `POST /api/compare`

Compare two or three distinct vehicle IDs from the curated catalog.

Request:

```json
{
  "vehicle_ids": ["tata-nexon-2025", "hyundai-creta-2025"]
}
```

Response `200` contains canonical profiles or comparison fields, trade-offs, and a concise contextual recommendation. Unsupported fields are marked unavailable rather than inferred. Invalid counts or unknown IDs return a validation error.
