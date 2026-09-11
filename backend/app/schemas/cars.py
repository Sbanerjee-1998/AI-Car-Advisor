from pydantic import BaseModel, Field


class VehicleSummary(BaseModel):
    id: str
    name: str
    manufacturer: str
    fuel_type: str
    transmission: str
    body_type: str
    seating_capacity: int
    price_min_inr: float | None
    price_max_inr: float | None


class VehicleDetail(VehicleSummary):
    model_year: int | None = None
    specifications: dict[str, str | int | float | None]
    features: list[str]
    use_cases: list[str]
    advantages: list[str]
    considerations: list[str]
    source: str
    disclaimer: str


class VehicleListResponse(BaseModel):
    items: list[VehicleSummary]
    total: int


class CompareRequest(BaseModel):
    vehicle_ids: list[str] = Field(min_length=2, max_length=3)


class CompareResponse(BaseModel):
    vehicles: list[VehicleDetail]
    fields: list[str]
    trade_offs: list[str]
    conclusion: str
    disclaimer: str


class FavouriteCreate(BaseModel):
    vehicle_id: str = Field(min_length=1, max_length=120)


class FavouriteResponse(BaseModel):
    vehicle_id: str
    created_at: str
    vehicle: VehicleSummary
