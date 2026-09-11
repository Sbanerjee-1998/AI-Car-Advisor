from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user, get_db
from backend.app.schemas.auth import LoginRequest, RegisterRequest, UserResponse
from backend.app.schemas.errors import AppError
from backend.app.services.auth import login, logout, public_user, register

router = APIRouter(prefix="/api/auth", tags=["auth"])


def set_session_cookie(response: Response, request: Request, token: str) -> None:
    settings = request.app.state.settings
    response.set_cookie(
        settings.session_cookie_name,
        token,
        max_age=settings.session_days * 86400,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
    )


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(payload: RegisterRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    if not payload.passwords_match():
        raise AppError(422, "validation_error", "Please check the highlighted fields.", {"password_confirmation": "Passwords do not match."})
    user, token = register(db, payload.name, str(payload.email), payload.password, request.app.state.settings)
    set_session_cookie(response, request, token)
    return public_user(user)


@router.post("/login", response_model=UserResponse)
def login_user(payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)):
    user, token = login(db, str(payload.email), payload.password, request.app.state.settings)
    set_session_cookie(response, request, token)
    return public_user(user)


@router.post("/logout", status_code=204)
def logout_user(request: Request, response: Response, db: Session = Depends(get_db)):
    logout(db, request.cookies.get(request.app.state.settings.session_cookie_name))
    response.delete_cookie(request.app.state.settings.session_cookie_name)


@router.get("/me", response_model=UserResponse)
def current_user(user=Depends(get_current_user)):
    return public_user(user)
