from __future__ import annotations

from backend.app.config import Settings


class GeminiProvider:
    """Optional Gemini adapter seam; local tests use AdvisorService's deterministic path."""

    def __init__(self, settings: Settings):
        self.settings = settings

    @property
    def configured(self) -> bool:
        return bool(self.settings.gemini_api_key)
