from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from backend.app.schemas.errors import AppError


def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message, "fields": exc.fields}},
    )


def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    fields = {}
    for item in exc.errors():
        location = item.get("loc", [])
        field = str(location[-1]) if location else "request"
        fields[field] = "Please provide a valid value."
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "message": "Please check the highlighted fields.", "fields": fields}},
    )


def unexpected_error_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "internal_error", "message": "Something went wrong. Please try again.", "fields": None}},
    )
