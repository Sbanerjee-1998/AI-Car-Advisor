from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]


def _bool_env(name: str, default: bool) -> bool:
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./.local/app.db")
    chroma_path: str = os.getenv("CHROMA_PATH", ".local/chroma")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.2"))
    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    session_cookie_name: str = os.getenv("SESSION_COOKIE_NAME", "ai_car_advisor_session")
    session_cookie_secure: bool = _bool_env("SESSION_COOKIE_SECURE", False)
    session_days: int = int(os.getenv("SESSION_DAYS", "14"))
    max_message_length: int = int(os.getenv("MAX_MESSAGE_LENGTH", "4000"))
    context_message_limit: int = int(os.getenv("CONTEXT_MESSAGE_LIMIT", "12"))
    context_token_budget: int = int(os.getenv("CONTEXT_TOKEN_BUDGET", "8000"))

    def ensure_runtime_dirs(self) -> None:
        if self.database_url.startswith("sqlite:///./"):
            (ROOT_DIR / ".local").mkdir(parents=True, exist_ok=True)
        chroma = Path(self.chroma_path)
        if not chroma.is_absolute():
            chroma = ROOT_DIR / chroma
        chroma.mkdir(parents=True, exist_ok=True)


settings = Settings()
