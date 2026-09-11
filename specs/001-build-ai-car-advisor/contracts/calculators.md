# Calculator Contract

Calculator endpoints are deterministic and share the same domain functions used by the MCP tools. Results are estimates, not financial or fuel guarantees.

## `POST /api/emi`

Request:

```json
{
  "principal_inr": 1000000,
  "annual_interest_rate_percent": 8.5,
  "term_months": 60
}
```

Response `200`:

```json
{
  "kind": "emi",
  "inputs": {
    "principal_inr": 1000000,
    "annual_interest_rate_percent": 8.5,
    "term_months": 60
  },
  "monthly_payment_inr": 20497.42,
  "total_payment_inr": 1229845.20,
  "total_interest_inr": 229845.20,
  "disclaimer": "This is an estimate. Confirm rates, fees, taxes, and terms with your lender."
}
```

A zero interest rate is valid and uses principal divided by term. Invalid, non-finite, non-positive, or out-of-bound inputs return `422` with field errors.

## `POST /api/fuel-cost`

Request:

```json
{
  "daily_distance_km": 40,
  "mileage_km_per_litre": 18,
  "fuel_price_inr_per_litre": 105,
  "monthly_driving_days": 22
}
```

Response `200`:

```json
{
  "kind": "fuel_cost",
  "inputs": {
    "daily_distance_km": 40,
    "mileage_km_per_litre": 18,
    "fuel_price_inr_per_litre": 105,
    "monthly_driving_days": 22
  },
  "daily_cost_inr": 233.33,
  "monthly_consumption_litres": 48.89,
  "monthly_cost_inr": 5133.33,
  "annual_cost_inr": 61600.00,
  "disclaimer": "This is an estimate. Actual cost varies with traffic, driving style, and fuel prices."
}
```

The endpoint rejects invalid or non-positive distance, mileage, price, and driving-day values.

## MCP Tools

The local MCP server exposes exactly these tools with equivalent validated inputs and numeric outputs:

- `calculate_emi(principal_inr, annual_interest_rate_percent, term_months)`
- `calculate_fuel_cost(daily_distance_km, mileage_km_per_litre, fuel_price_inr_per_litre, monthly_driving_days)`

MCP tool errors use the same field-level validation concepts, but transport formatting follows the selected MCP SDK.
