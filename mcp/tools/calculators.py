from backend.app.services.calculators import calculate_emi as _calculate_emi
from backend.app.services.calculators import calculate_fuel_cost as _calculate_fuel_cost


def calculate_emi(principal_inr: float, annual_interest_rate_percent: float, term_months: int) -> dict[str, float | str]:
    return {"kind": "emi", **_calculate_emi(principal_inr, annual_interest_rate_percent, term_months)}


def calculate_fuel_cost(daily_distance_km: float, mileage_km_per_litre: float, fuel_price_inr_per_litre: float, monthly_driving_days: int) -> dict[str, float | str]:
    return {"kind": "fuel_cost", **_calculate_fuel_cost(daily_distance_km, mileage_km_per_litre, fuel_price_inr_per_litre, monthly_driving_days)}
