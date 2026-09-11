from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from backend.app.agents.context import pack_context
from backend.app.agents.provider import GeminiProvider
from backend.app.config import settings
from backend.app.services.catalog import CatalogService, Vehicle
from backend.app.services.preferences import extract_preferences, merge_preferences, preference_dict

logger = logging.getLogger(__name__)


@dataclass
class AdvisorResult:
    content: str
    recommendations: list[dict]
    follow_up_required: bool
    available_actions: list[str]


class AdvisorService:
    """Single orchestration boundary with a grounded Gemini path and local fallback."""

    def __init__(self, catalog: CatalogService, provider: GeminiProvider | None = None):
        self.catalog = catalog
        self.provider = provider or GeminiProvider(settings)

    def respond(self, db, conversation, text: str) -> AdvisorResult:
        updates = extract_preferences(text)
        preference = merge_preferences(db, conversation, updates)
        active = preference_dict(preference)
        enough_context = bool(
            active.get("budget_max_inr")
            or active.get("fuel_type")
            or active.get("daily_distance_km")
            or active.get("body_type")
        )
        filters = {
            key: active.get(key)
            for key in (
                "fuel_type",
                "transmission",
                "body_type",
                "seating_capacity",
                "budget_max_inr",
            )
        }
        vehicles = self.catalog.search(text, filters, limit=6)
        if not vehicles:
            filters.pop("fuel_type", None)
            vehicles = self.catalog.search(text, filters, limit=6)
        if self.provider.configured:
            ai_result = self._respond_with_ai(db, conversation, text, active, vehicles)
            if ai_result is not None:
                preference.unresolved_question = (
                    None if not ai_result.follow_up_required else ai_result.content
                )
                return ai_result
        if not enough_context:
            preference.unresolved_question = "What budget and fuel type should I use?"
            return AdvisorResult(
                (
                    "I can narrow this down quickly. What is your approximate budget "
                    "and preferred fuel type?"
                ),
                [],
                True,
                [],
            )
        recommendations = [self._recommendation(vehicle, active) for vehicle in vehicles]
        if recommendations:
            content = (
                "Here is a shortlist grounded in the curated catalog. "
                "I have called out the trade-offs so you can decide what matters most."
            )
            actions = [
                "compare",
                "view_details",
                "save_favourite",
                "calculate_emi",
                "calculate_fuel_cost",
            ]
        else:
            content = (
                "I could not find a close match in the curated catalog. "
                "Try broadening the budget, fuel type, or body-style preference."
            )
            actions = []
        preference.unresolved_question = None
        return AdvisorResult(content, recommendations, False, actions)

    def _respond_with_ai(
        self, db, conversation, text: str, active: dict[str, Any], vehicles: list[Vehicle]
    ) -> AdvisorResult | None:
        del db
        messages = [
            {"role": message.role, "content": message.content}
            for message in sorted(conversation.messages, key=lambda item: item.created_at)
        ]
        candidates = [self._candidate_context(vehicle) for vehicle in vehicles]
        try:
            response = self.provider.generate(
                user_message=text,
                conversation_context=pack_context(
                    messages, text, budget=settings.context_token_budget
                ),
                preferences=active,
                candidates=candidates,
            )
        except Exception as exc:
            logger.warning(
                "Gemini advisor request failed: %s",
                type(exc).__name__,
            )
            return None

        by_id = {vehicle.id: vehicle for vehicle in vehicles}
        selected = []
        for vehicle_id in response.recommendation_ids:
            vehicle = by_id.get(vehicle_id)
            if vehicle is not None and vehicle not in selected:
                selected.append(vehicle)
        recommendations = [self._recommendation(vehicle, active) for vehicle in selected[:3]]
        answer = response.answer.strip()
        if response.follow_up_required and response.follow_up_question:
            question = response.follow_up_question.strip()
            if question and question not in answer:
                answer = f"{answer}\n\n{question}"
        actions = (
            [
                "compare",
                "view_details",
                "save_favourite",
                "calculate_emi",
                "calculate_fuel_cost",
            ]
            if recommendations
            else []
        )
        return AdvisorResult(answer, recommendations, response.follow_up_required, actions)

    @staticmethod
    def _candidate_context(vehicle: Vehicle) -> dict[str, Any]:
        return {
            "id": vehicle.id,
            "name": vehicle.name,
            "manufacturer": vehicle.manufacturer,
            "fuel_type": vehicle.fuel_type,
            "transmission": vehicle.transmission,
            "body_type": vehicle.body_type,
            "seating_capacity": vehicle.seating_capacity,
            "price_min_inr": vehicle.price_min_inr,
            "price_max_inr": vehicle.price_max_inr,
            "specifications": vehicle.specifications,
            "features": vehicle.features,
            "use_cases": vehicle.use_cases,
            "advantages": vehicle.advantages,
            "considerations": vehicle.considerations,
        }

    @staticmethod
    def _recommendation(vehicle: Vehicle, active: dict) -> dict:
        matches = []
        for key, label in (
            ("fuel_type", "powertrain"),
            ("transmission", "transmission"),
            ("body_type", "body style"),
        ):
            if active.get(key) == getattr(vehicle, key):
                matches.append(f"matches your {label} preference")
        if (
            active.get("budget_max_inr")
            and vehicle.price_min_inr
            and vehicle.price_min_inr <= active["budget_max_inr"]
        ):
            matches.append("fits within the stated budget range")
        price = "Approximate pricing unavailable"
        if vehicle.price_min_inr is not None and vehicle.price_max_inr is not None:
            price = f"₹{vehicle.price_min_inr:,.0f}–₹{vehicle.price_max_inr:,.0f} (approx.)"
        return {
            "vehicle_id": vehicle.id,
            "vehicle_name": vehicle.name,
            "fit_summary": "; ".join(matches) or "a relevant option from the curated catalog",
            "advantages": vehicle.advantages[:3] or ["Supported by the curated vehicle catalog."],
            "considerations": vehicle.considerations[:3]
            or ["Verify the exact variant and on-road price."],
            "price_summary": price,
            "specifications": vehicle.specifications,
            "match_reasons": matches,
        }
