from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.models import Favourite
from backend.app.schemas.errors import AppError


def list_favourites(db: Session, user_id: int) -> list[Favourite]:
    return list(db.scalars(select(Favourite).where(Favourite.user_id == user_id).order_by(Favourite.created_at.desc())))


def add_favourite(db: Session, user_id: int, vehicle_id: str) -> Favourite:
    existing = db.scalar(select(Favourite).where(Favourite.user_id == user_id, Favourite.vehicle_id == vehicle_id))
    if existing:
        raise AppError(409, "conflict", "That vehicle is already in your favourites.")
    favourite = Favourite(user_id=user_id, vehicle_id=vehicle_id)
    db.add(favourite)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AppError(409, "conflict", "That vehicle is already in your favourites.") from exc
    db.refresh(favourite)
    return favourite


def remove_favourite(db: Session, user_id: int, vehicle_id: str) -> None:
    favourite = db.scalar(select(Favourite).where(Favourite.user_id == user_id, Favourite.vehicle_id == vehicle_id))
    if favourite is None:
        raise AppError(404, "not_found", "Favourite was not found.")
    db.delete(favourite)
    db.commit()
