from fastapi import Depends, APIRouter
from db.models import Admin
from schemas.request import LicensePlateRequestWithClient, RequestStatusUpdate
from auth import dependencies
from typing import List
from services.plate_request_service import PlateRequestService
from services.dependencies import get_plate_request_service

request_router: APIRouter = APIRouter(tags=["Registeration requests"])

@request_router.get("/requests", response_model=List[LicensePlateRequestWithClient])
async def list_requests(
    service: PlateRequestService = Depends(get_plate_request_service),
    current_user: Admin = Depends(dependencies.get_current_user),
):
    return service.get_all_plate_requests(current_user)

# request in context means license plate registration request
@request_router.put("/requests/{request_id}")
def update_request_status(
    request_id: int,
    payload: RequestStatusUpdate,
    service: PlateRequestService = Depends(get_plate_request_service),
    current_user: Admin = Depends(dependencies.get_current_user),
):
    return service.update_plate_status(request_id, payload, current_user)
