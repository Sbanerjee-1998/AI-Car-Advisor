from __future__ import annotations

from collections.abc import Generator

from fastapi import Cookie, Depends, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import AuthSession, User
from backend.app.security import hash_session_token, is_expired
from backend.app.schemas.errors import AppError


def get_db(request: Request) -> Generator[Session, None, None]:
    session = request.app.state.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(
    request: Request,
    session_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    cookie_name = request.app.state.settings.session_cookie_name
    if not session_token:
        session_token = request.cookies.get(cookie_name)
    if not session_token:
        raise AppError(401, "authentication_required", "Please sign in to continue.")
    record = db.scalar(
        select(AuthSession).where(
            AuthSession.token_hash == hash_session_token(session_token),
            AuthSession.revoked_at.is_(None),
        )
    )
    if record is None or is_expired(record.expires_at):
        raise AppError(401, "authentication_required", "Please sign in to continue.")
    return db.get(User, record.user_id)
