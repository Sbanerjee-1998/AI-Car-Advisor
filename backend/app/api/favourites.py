from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.models import User
from backend.app.schemas.cars import FavouriteCreate, FavouriteResponse
from backend.app.schemas.errors import AppError
from backend.app.services.favourites import add_favourite, list_favourites, remove_favourite

router = APIRouter(prefix="/api/favourites", tags=["favourites"])


@router.get("", response_model=dict)
def get_favourites(request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = []
    for favourite in list_favourites(db, user.id):
        vehicle = request.app.state.catalog.get(favourite.vehicle_id)
        if vehicle:
            items.append({"vehicle_id": favourite.vehicle_id, "created_at": favourite.created_at.isoformat(), "vehicle": vehicle.summary()})
    return {"items": items}


@router.post("", response_model=FavouriteResponse, status_code=201)
def save_favourite(payload: FavouriteCreate, request: Request, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    vehicle = request.app.state.catalog.get(payload.vehicle_id)
    if vehicle is None:
        raise AppError(404, "not_found", "Vehicle was not found.")
    favourite = add_favourite(db, user.id, vehicle.id)
    return {"vehicle_id": favourite.vehicle_id, "created_at": favourite.created_at.isoformat(), "vehicle": vehicle.summary()}


@router.delete("/{car_id}", status_code=204)
def delete_favourite(car_id: str, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    remove_favourite(db, user.id, car_id)
