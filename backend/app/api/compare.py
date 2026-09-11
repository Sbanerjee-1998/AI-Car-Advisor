from fastapi import APIRouter, Depends, Request

from backend.app.api.dependencies import get_current_user
from backend.app.schemas.cars import CompareRequest, CompareResponse
from backend.app.services.comparison import compare

router = APIRouter(prefix="/api", tags=["compare"])


@router.post("/compare", response_model=CompareResponse)
def compare_cars(payload: CompareRequest, request: Request, _user=Depends(get_current_user)):
    return compare(request.app.state.catalog, payload.vehicle_ids)
