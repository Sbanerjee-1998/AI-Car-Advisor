from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ConversationCreate(BaseModel):
    title: str | None = Field(default=None, max_length=160)


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    content: str
    created_at: datetime


class PreferenceResponse(BaseModel):
    budget_min_inr: float | None = None
    budget_max_inr: float | None = None
    fuel_type: str | None = None
    body_type: str | None = None
    seating_capacity: int | None = None
    transmission: str | None = None
    daily_distance_km: float | None = None
    usage_notes: str | None = None
    unresolved_question: str | None = None


class ConversationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime


class ConversationDetail(ConversationSummary):
    messages: list[MessageResponse]
    preferences: PreferenceResponse | None = None


class ChatMessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class RecommendationResponse(BaseModel):
    vehicle_id: str
    vehicle_name: str
    fit_summary: str
    advantages: list[str]
    considerations: list[str]
    price_summary: str
    specifications: dict[str, str | int | float | None]
    match_reasons: list[str]


class ChatMessageResponse(BaseModel):
    conversation_id: int
    user_message: MessageResponse
    assistant_message: MessageResponse
    recommendations: list[RecommendationResponse]
    follow_up_required: bool
    available_actions: list[str]
    disclaimer: str
