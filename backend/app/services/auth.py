from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.config import Settings
from backend.app.models import AuthSession, User
from backend.app.schemas.errors import AppError
from backend.app.security import hash_password, hash_session_token, new_session_token, normalize_email, session_expiry, verify_password


def public_user(user: User) -> dict:
    return {"id": user.id, "name": user.name, "email": user.email_normalized, "created_at": user.created_at}


def register(db: Session, name: str, email: str, password: str, settings: Settings) -> tuple[User, str]:
    normalized = normalize_email(email)
    if db.scalar(select(User).where(User.email_normalized == normalized)):
        raise AppError(409, "conflict", "An account with that email already exists.")
    user = User(name=name.strip(), email_normalized=normalized, password_hash=hash_password(password))
    db.add(user)
    db.flush()
    token = new_session_token()
    db.add(AuthSession(user_id=user.id, token_hash=hash_session_token(token), expires_at=session_expiry(settings.session_days)))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise AppError(409, "conflict", "An account with that email already exists.") from exc
    db.refresh(user)
    return user, token


def login(db: Session, email: str, password: str, settings: Settings) -> tuple[User, str]:
    user = db.scalar(select(User).where(User.email_normalized == normalize_email(email)))
    if user is None or not verify_password(user.password_hash, password):
        raise AppError(401, "invalid_credentials", "Email or password is incorrect.")
    token = new_session_token()
    db.add(AuthSession(user_id=user.id, token_hash=hash_session_token(token), expires_at=session_expiry(settings.session_days)))
    db.commit()
    return user, token


def logout(db: Session, token: str | None) -> None:
    if not token:
        return
    record = db.scalar(select(AuthSession).where(AuthSession.token_hash == hash_session_token(token)))
    if record:
        record.revoked_at = datetime.now(timezone.utc)
        db.commit()
