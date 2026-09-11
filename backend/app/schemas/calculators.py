from pydantic import BaseModel, Field


class EmiRequest(BaseModel):
    principal_inr: float = Field(gt=0)
    annual_interest_rate_percent: float = Field(ge=0)
    term_months: int = Field(gt=0, le=480)


class EmiResponse(BaseModel):
    kind: str
    inputs: EmiRequest
    monthly_payment_inr: float
    total_payment_inr: float
    total_interest_inr: float
    disclaimer: str


class FuelCostRequest(BaseModel):
    daily_distance_km: float = Field(gt=0)
    mileage_km_per_litre: float = Field(gt=0)
    fuel_price_inr_per_litre: float = Field(gt=0)
    monthly_driving_days: int = Field(gt=0, le=31)


class FuelCostResponse(BaseModel):
    kind: str
    inputs: FuelCostRequest
    daily_cost_inr: float
    monthly_consumption_litres: float
    monthly_cost_inr: float
    annual_cost_inr: float
    disclaimer: str
