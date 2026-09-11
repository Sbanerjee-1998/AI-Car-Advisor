from __future__ import annotations

from dataclasses import dataclass

from backend.app.services.catalog import CatalogService, Vehicle
from backend.app.services.preferences import extract_preferences, merge_preferences, preference_dict


@dataclass
class AdvisorResult:
    content: str
    recommendations: list[dict]
    follow_up_required: bool
    available_actions: list[str]


class AdvisorService:
    """Single orchestration boundary with deterministic fallback for credential-free demos."""

    def __init__(self, catalog: CatalogService):
        self.catalog = catalog

    def respond(self, db, conversation, text: str) -> AdvisorResult:
        updates = extract_preferences(text)
        preference = merge_preferences(db, conversation, updates)
        active = preference_dict(preference)
        enough_context = bool(active.get("budget_max_inr") or active.get("fuel_type") or active.get("daily_distance_km") or active.get("body_type"))
        if not enough_context:
            preference.unresolved_question = "What budget and fuel type should I use?"
            return AdvisorResult(
                "I can narrow this down quickly. What is your approximate budget and preferred fuel type?",
                [], True, [],
            )
        filters = {key: active.get(key) for key in ("fuel_type", "transmission", "body_type", "seating_capacity", "budget_max_inr")}
        vehicles = self.catalog.search(text, filters, limit=3)
        if not vehicles:
            filters.pop("fuel_type", None)
            vehicles = self.catalog.search(text, filters, limit=3)
        recommendations = [self._recommendation(vehicle, active) for vehicle in vehicles]
        if recommendations:
            content = "Here is a shortlist grounded in the curated catalog. I have called out the trade-offs so you can decide what matters most."
            actions = ["compare", "view_details", "save_favourite", "calculate_emi", "calculate_fuel_cost"]
        else:
            content = "I could not find a close match in the curated catalog. Try broadening the budget, fuel type, or body-style preference."
            actions = []
        preference.unresolved_question = None
        return AdvisorResult(content, recommendations, False, actions)

    @staticmethod
    def _recommendation(vehicle: Vehicle, active: dict) -> dict:
        matches = []
        for key, label in (("fuel_type", "powertrain"), ("transmission", "transmission"), ("body_type", "body style")):
            if active.get(key) == getattr(vehicle, key):
                matches.append(f"matches your {label} preference")
        if active.get("budget_max_inr") and vehicle.price_min_inr and vehicle.price_min_inr <= active["budget_max_inr"]:
            matches.append("fits within the stated budget range")
        price = "Approximate pricing unavailable"
        if vehicle.price_min_inr is not None and vehicle.price_max_inr is not None:
            price = f"₹{vehicle.price_min_inr:,.0f}–₹{vehicle.price_max_inr:,.0f} (approx.)"
        return {
            "vehicle_id": vehicle.id,
            "vehicle_name": vehicle.name,
            "fit_summary": "; ".join(matches) or "a relevant option from the curated catalog",
            "advantages": vehicle.advantages[:3] or ["Supported by the curated vehicle catalog."],
            "considerations": vehicle.considerations[:3] or ["Verify the exact variant and on-road price."],
            "price_summary": price,
            "specifications": vehicle.specifications,
            "match_reasons": matches,
        }
