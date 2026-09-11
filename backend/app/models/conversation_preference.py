from datetime import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.base import Base
from backend.app.models.user import utc_now


class ConversationPreference(Base):
    __tablename__ = "conversation_preferences"

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), unique=True)
    budget_min_inr: Mapped[float] = mapped_column(Numeric(14, 2), nullable=True)
    budget_max_inr: Mapped[float] = mapped_column(Numeric(14, 2), nullable=True)
    fuel_type: Mapped[str] = mapped_column(String(24), nullable=True)
    body_type: Mapped[str] = mapped_column(String(32), nullable=True)
    seating_capacity: Mapped[int] = mapped_column(Integer, nullable=True)
    transmission: Mapped[str] = mapped_column(String(24), nullable=True)
    daily_distance_km: Mapped[float] = mapped_column(Numeric(12, 2), nullable=True)
    usage_notes: Mapped[str] = mapped_column(String(500), nullable=True)
    unresolved_question: Mapped[str] = mapped_column(String(500), nullable=True)
    recent_vehicle_ids: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    conversation = relationship("Conversation", back_populates="preference")
