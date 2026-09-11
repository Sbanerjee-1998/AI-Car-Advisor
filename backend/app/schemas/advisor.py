from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    vehicle_id: str = Field(min_length=1)
    vehicle_name: str
    fit_summary: str
    advantages: list[str]
    considerations: list[str]
    price_summary: str
    specifications: dict[str, str | int | float | None]
    match_reasons: list[str]


class AdvisorResult(BaseModel):
    kind: str
    answer: str
    recommendations: list[Recommendation] = Field(default_factory=list, max_length=3)
    follow_up_required: bool = False
    available_actions: list[str] = Field(default_factory=list)
