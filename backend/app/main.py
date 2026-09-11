from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.agents.advisor import AdvisorService
from backend.app.api import auth, calculators, cars, chats, compare, errors, favourites, health
from backend.app.config import ROOT_DIR, Settings, settings
from backend.app.database.base import Base
from backend.app.database.session import create_database
from backend.app.services.catalog import CatalogService
from backend.app.schemas.errors import AppError
from fastapi.exceptions import RequestValidationError


def create_app(database_url: str | None = None, catalog_dir: str | None = None) -> FastAPI:
    app = FastAPI(title="AI Car Advisor", version="1.0.0")
    app_settings = settings
    app_settings.ensure_runtime_dirs()
    engine, session_local = create_database(database_url)
    Base.metadata.create_all(engine)
    source_dir = Path(catalog_dir) if catalog_dir else ROOT_DIR / "backend" / "data" / "cars"
    catalog = CatalogService(source_dir)
    app.state.engine = engine
    app.state.SessionLocal = session_local
    app.state.settings = app_settings
    app.state.catalog = catalog
    app.state.advisor = AdvisorService(catalog)
    app.add_middleware(CORSMiddleware, allow_origins=[app_settings.frontend_origin], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.add_exception_handler(AppError, errors.app_error_handler)
    app.add_exception_handler(RequestValidationError, errors.validation_error_handler)
    app.add_exception_handler(Exception, errors.unexpected_error_handler)
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(chats.router)
    app.include_router(cars.router)
    app.include_router(compare.router)
    app.include_router(favourites.router)
    app.include_router(calculators.router)
    return app


app = create_app()
