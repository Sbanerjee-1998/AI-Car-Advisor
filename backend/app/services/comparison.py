from backend.app.schemas.errors import AppError
from backend.app.services.catalog import DISCLAIMER, CatalogService


def compare(catalog: CatalogService, vehicle_ids: list[str], priorities: str = "") -> dict:
    if len(vehicle_ids) not in (2, 3) or len(set(vehicle_ids)) != len(vehicle_ids):
        raise AppError(422, "validation_error", "Choose two or three different vehicles.", {"vehicle_ids": "Select 2 or 3 vehicles."})
    vehicles = [catalog.get(vehicle_id) for vehicle_id in vehicle_ids]
    if any(vehicle is None for vehicle in vehicles):
        raise AppError(404, "not_found", "One or more selected vehicles were not found.")
    resolved = [vehicle for vehicle in vehicles if vehicle is not None]
    fields = ["price", "fuel_type", "transmission", "seating_capacity", "engine_or_battery", "mileage_or_range", "boot_space", "safety"]
    trade_offs = [f"{vehicle.name}: " + (vehicle.considerations[0] if vehicle.considerations else "verify the exact variant details") for vehicle in resolved]
    conclusion = f"Choose {resolved[0].name} if its strengths match your priorities; compare the listed trade-offs rather than treating one vehicle as a universal winner."
    return {"vehicles": [vehicle.detail() for vehicle in resolved], "fields": fields, "trade_offs": trade_offs, "conclusion": conclusion, "disclaimer": DISCLAIMER}
