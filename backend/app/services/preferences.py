from __future__ import annotations

import re
from typing import Any

from sqlalchemy.orm import Session

from backend.app.models import Conversation, ConversationPreference


def extract_preferences(text: str) -> dict[str, Any]:
    lower = text.casefold()
    result: dict[str, Any] = {}
    powertrains = {"electric": "electric", "ev": "electric", "petrol": "petrol", "diesel": "diesel", "hybrid": "hybrid"}
    for marker, value in powertrains.items():
        if re.search(rf"\b{re.escape(marker)}\b", lower):
            result["fuel_type"] = value
            break
    if "automatic" in lower or "amt" in lower or "cvt" in lower:
        result["transmission"] = "automatic"
    elif "manual" in lower:
        result["transmission"] = "manual"
    for body in ("suv", "sedan", "hatchback", "muv", "mpv"):
        if body in lower:
            result["body_type"] = body
            break
    seat = re.search(r"(?:seat|seater|people|family of)\s*(?:is|are|of)?\s*(\d+)", lower)
    if seat:
        result["seating_capacity"] = int(seat.group(1))
    distance = re.search(r"(\d+(?:\.\d+)?)\s*(?:km|kilomet(?:er|re)s?)\s*(?:daily|a day|per day)?", lower)
    if distance:
        result["daily_distance_km"] = float(distance.group(1))
    lakh = re.search(r"(?:under|below|around|budget(?: is)?|of)\s*(?:₹|inr\s*)?(\d+(?:\.\d+)?)\s*(lakh|lac|crore|cr)", lower)
    if lakh:
        value = float(lakh.group(1)) * (100000 if lakh.group(2) in {"lakh", "lac"} else 10000000)
        result["budget_max_inr"] = value
    return result


def merge_preferences(db: Session, conversation: Conversation, updates: dict[str, Any]) -> ConversationPreference:
    preference = conversation.preference
    if preference is None:
        preference = ConversationPreference(conversation_id=conversation.id, recent_vehicle_ids=[])
        db.add(preference)
        db.flush()
    for key, value in updates.items():
        if value is not None and hasattr(preference, key):
            setattr(preference, key, value)
    return preference


def preference_dict(preference: ConversationPreference | None) -> dict[str, Any]:
    if preference is None:
        return {}
    return {
        "budget_min_inr": preference.budget_min_inr,
        "budget_max_inr": preference.budget_max_inr,
        "fuel_type": preference.fuel_type,
        "body_type": preference.body_type,
        "seating_capacity": preference.seating_capacity,
        "transmission": preference.transmission,
        "daily_distance_km": preference.daily_distance_km,
        "usage_notes": preference.usage_notes,
        "unresolved_question": preference.unresolved_question,
    }
