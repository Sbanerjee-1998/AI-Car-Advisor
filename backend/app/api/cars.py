from fastapi import APIRouter, Depends, Query, Request

from backend.app.api.dependencies import get_current_user
from backend.app.schemas.cars import VehicleDetail, VehicleListResponse
from backend.app.schemas.errors import AppError

router = APIRouter(prefix="/api/cars", tags=["cars"])


@router.get("", response_model=VehicleListResponse)
def list_cars(
    request: Request,
    fuel_type: str | None = Query(default=None),
    transmission: str | None = Query(default=None),
    body_type: str | None = Query(default=None),
    seating_capacity: int | None = Query(default=None, gt=0),
    price_min_inr: float | None = Query(default=None, ge=0),
    price_max_inr: float | None = Query(default=None, ge=0),
    q: str | None = Query(default=None, max_length=100),
    _user=Depends(get_current_user),
):
    vehicles = request.app.state.catalog.list({"fuel_type": fuel_type, "transmission": transmission, "body_type": body_type, "seating_capacity": seating_capacity, "price_min_inr": price_min_inr, "price_max_inr": price_max_inr, "q": q})
    return {"items": [vehicle.summary() for vehicle in vehicles], "total": len(vehicles)}


@router.get("/{car_id}", response_model=VehicleDetail)
def get_car(car_id: str, request: Request, _user=Depends(get_current_user)):
    vehicle = request.app.state.catalog.get(car_id)
    if vehicle is None:
        raise AppError(404, "not_found", "Vehicle was not found.")
    return vehicle.detail()
