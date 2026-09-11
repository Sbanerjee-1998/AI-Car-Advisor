from fastapi import APIRouter

from backend.app.schemas.calculators import EmiRequest, EmiResponse, FuelCostRequest, FuelCostResponse
from backend.app.schemas.errors import AppError
from backend.app.services.calculators import EMI_DISCLAIMER, FUEL_DISCLAIMER, calculate_emi, calculate_fuel_cost

router = APIRouter(prefix="/api", tags=["calculators"])


@router.post("/emi", response_model=EmiResponse)
def emi(payload: EmiRequest):
    try:
        values = calculate_emi(payload.principal_inr, payload.annual_interest_rate_percent, payload.term_months)
    except ValueError as exc:
        raise AppError(422, "validation_error", "Please check the highlighted fields.", {"calculator": str(exc)}) from exc
    return {"kind": "emi", "inputs": payload, **values, "disclaimer": EMI_DISCLAIMER}


@router.post("/fuel-cost", response_model=FuelCostResponse)
def fuel_cost(payload: FuelCostRequest):
    try:
        values = calculate_fuel_cost(payload.daily_distance_km, payload.mileage_km_per_litre, payload.fuel_price_inr_per_litre, payload.monthly_driving_days)
    except ValueError as exc:
        raise AppError(422, "validation_error", "Please check the highlighted fields.", {"calculator": str(exc)}) from exc
    return {"kind": "fuel_cost", "inputs": payload, **values, "disclaimer": FUEL_DISCLAIMER}
