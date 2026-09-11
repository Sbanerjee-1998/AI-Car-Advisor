from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


MONEY = Decimal("0.01")
EMI_DISCLAIMER = "This is an estimate. Confirm rates, fees, taxes, and terms with your lender."
FUEL_DISCLAIMER = "This is an estimate. Actual cost varies with traffic, driving style, and fuel prices."


def _decimal(value: float | int | str, field: str, positive: bool = True, allow_zero: bool = False) -> Decimal:
    try:
        number = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field} must be a finite number.") from exc
    if not number.is_finite() or (positive and number < 0) or (positive and not allow_zero and number == 0):
        comparator = "greater than zero" if positive and not allow_zero else "zero or greater"
        raise ValueError(f"{field} must be {comparator}.")
    return number


def _money(value: Decimal) -> float:
    return float(value.quantize(MONEY, rounding=ROUND_HALF_UP))


def calculate_emi(principal_inr: float, annual_interest_rate_percent: float, term_months: int) -> dict[str, float]:
    principal = _decimal(principal_inr, "principal_inr")
    annual_rate = _decimal(annual_interest_rate_percent, "annual_interest_rate_percent", allow_zero=True)
    if term_months <= 0:
        raise ValueError("term_months must be greater than zero.")
    months = Decimal(str(term_months))
    monthly_rate = annual_rate / Decimal("1200")
    if monthly_rate == 0:
        monthly = principal / months
    else:
        factor = (Decimal("1") + monthly_rate) ** int(term_months)
        monthly = principal * monthly_rate * factor / (factor - Decimal("1"))
    total = monthly * months
    return {
        "monthly_payment_inr": _money(monthly),
        "total_payment_inr": _money(total),
        "total_interest_inr": _money(total - principal),
    }


def calculate_fuel_cost(
    daily_distance_km: float,
    mileage_km_per_litre: float,
    fuel_price_inr_per_litre: float,
    monthly_driving_days: int,
) -> dict[str, float]:
    distance = _decimal(daily_distance_km, "daily_distance_km")
    mileage = _decimal(mileage_km_per_litre, "mileage_km_per_litre")
    price = _decimal(fuel_price_inr_per_litre, "fuel_price_inr_per_litre")
    if monthly_driving_days <= 0:
        raise ValueError("monthly_driving_days must be greater than zero.")
    daily_litres = distance / mileage
    daily_cost = daily_litres * price
    monthly_litres = daily_litres * Decimal(str(monthly_driving_days))
    monthly_cost = daily_cost * Decimal(str(monthly_driving_days))
    return {
        "daily_cost_inr": _money(daily_cost),
        "monthly_consumption_litres": _money(monthly_litres),
        "monthly_cost_inr": _money(monthly_cost),
        "annual_cost_inr": _money(monthly_cost * Decimal("12")),
    }
