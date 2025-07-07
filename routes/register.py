from fastapi import APIRouter, Depends
from helpers.registration_form_dependency import get_registration_form
from services.plate_request_service import PlateRequestService
from services.dependencies import get_plate_request_service


router = APIRouter(tags=["Plate registeration"])

@router.post("/register")
async def register(
    form_data: dict = Depends(get_registration_form),
    service: PlateRequestService = Depends(get_plate_request_service),
):
    request = service.create_plate_request(form_data)
    return {
        "request_id": request.id,
        "status": request.status,
        "submitted_at": request.submitted_at,
    }
