from backend.app.services.calculators import calculate_emi, calculate_fuel_cost
from backend.app.services.catalog import CatalogService


def test_health_contract(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "ai-car-advisor"}


def test_calculators_support_zero_interest_and_period_outputs(client):
    emi = client.post("/api/emi", json={"principal_inr": 100000, "annual_interest_rate_percent": 0, "term_months": 10})
    assert emi.status_code == 200
    assert emi.json()["monthly_payment_inr"] == 10000.0
    fuel = client.post("/api/fuel-cost", json={"daily_distance_km": 30, "mileage_km_per_litre": 15, "fuel_price_inr_per_litre": 100, "monthly_driving_days": 20})
    assert fuel.status_code == 200
    assert fuel.json()["daily_cost_inr"] == 200.0
    assert fuel.json()["monthly_cost_inr"] == 4000.0
    assert fuel.json()["annual_cost_inr"] == 48000.0


def test_catalog_has_thirty_grounded_vehicles():
    catalog = CatalogService("backend/data/cars")
    assert len(catalog.vehicles) == 30
    assert {vehicle.fuel_type for vehicle in catalog.vehicles.values()} == {"petrol", "diesel", "electric", "hybrid"}
