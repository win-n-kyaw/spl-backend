from fastapi import APIRouter, Depends
from helpers.registration_form_dependency import get_registration_form
from helpers.google_drive import upload_file_to_drive
from helpers.s3_cloudfront import upload_to_s3
from db.models import Client, LicensePlateRequest
from db.session import get_db


router = APIRouter(tags=["Plate registeration"])

@router.post("/register")
async def register(form_data: dict = Depends(get_registration_form), db=Depends(get_db)):
    name = form_data["name"]
    email = form_data["email"]
    plate_number = form_data["plate_number"]
    plate_photo = form_data["plate_photo"]
    # save to gdrive
    # image_url = upload_file_to_drive(plate_photo)

    #save to s3
    image_url = upload_to_s3(plate_photo)

    # Check if client exists
    client = db.query(Client).filter(Client.email == email).first()
    if not client:
        client = Client(name=name, email=email)
        db.add(client)
        db.commit()
        db.refresh(client)

    # Create license plate request
    request = LicensePlateRequest(
        client_id=client.id,
        plate_number=plate_number,
        plate_image_url=image_url,
    )
    db.add(request)
    db.commit()
    db.refresh(request)

    return {
        "request_id": request.id,
        "status": request.status,
        "submitted_at": request.submitted_at,
    }