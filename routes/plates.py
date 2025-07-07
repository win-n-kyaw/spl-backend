from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import EmailStr
from schemas.request import LicensePlateUpdate, LicensePlateCreate
from db.models import Admin
from auth import dependencies
from services.plate_service import PlateService
from services.dependencies import get_plate_service
from helpers.s3_cloudfront import upload_to_s3

router = APIRouter(tags=["License Plates"])

@router.get("/plates")
async def get_plates(
    plate_service: PlateService = Depends(get_plate_service),
    current_user: Admin = Depends(dependencies.get_current_user),
):
    return plate_service.get_all_plates(current_user)

@router.post("/plates")
def create_plate(
    email: EmailStr = Form(...),
    name: str = Form(...),
    plateNumber: str = Form(...),
    photo: UploadFile = File(...),
    plate_service: PlateService = Depends(get_plate_service),
    current_user: Admin = Depends(dependencies.get_current_user),
):
    photo_url = upload_to_s3(photo)
    payload = LicensePlateCreate(
        user_email=email,
        username=name,
        plate_number=plateNumber,
        plate_image_url=photo_url,
    )
    return plate_service.create_plate(current_user, payload)

@router.put("/plates/{plate_id}")
async def update_plate(
    plate_id: int,
    payload: LicensePlateUpdate,
    plate_service: PlateService = Depends(get_plate_service),
    current_user: Admin = Depends(dependencies.get_current_user),
):
    return plate_service.update_plate(plate_id, payload, current_user)
