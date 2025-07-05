from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from enums import RequestStatus
from schemas.request import LicensePlateRequestWithClient, LicensePlateUpdate
from db.models import Admin, LicensePlateRequest, User
from auth import jwt
from db.session import get_db

router = APIRouter(tags=["License Plates"])

@router.get("/plates")
async def approved_plates(db: Session = Depends(get_db), current_user: Admin = Depends(jwt.get_current_user)):
    if current_user.role not in ("admin", "operator"):
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")

    approve_requests = (
        db.query(LicensePlateRequest)
        .options(joinedload(LicensePlateRequest.user))
        .filter(LicensePlateRequest.status == RequestStatus.approved)
        .all()
    )

    if not approve_requests:
        return []

    return [
        LicensePlateRequestWithClient(
            id=req.id,
            plate_number=req.plate_number,
            plate_image_url=req.plate_image_url,
            status=req.status,
            username=req.user.name,
            user_email=req.user.email
        )
        for req in approve_requests
    ]


@router.put("/plates/{plate_id}")
async def update_plate(
    plate_id: int,
    payload: LicensePlateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(jwt.get_current_user)
):
    if current_user.role not in ("admin", "operator"):
        raise HTTPException(status_code=401, detail="Not authorized")

    plate = db.query(LicensePlateRequest).filter(LicensePlateRequest.id == plate_id).first()
    if not plate:
        raise HTTPException(status_code=404, detail="License plate not found")

    # Update plate_number
    if payload.plate_number is not None:
        plate.plate_number = payload.plate_number

    # Update plate_image_url
    if payload.plate_image_url is not None:
        plate.plate_image_url = payload.plate_image_url

    # Update status
    if payload.status is not None:
        if payload.status not in RequestStatus.__members__:
            raise HTTPException(status_code=400, detail="Invalid status value")
        plate.status = payload.status

    # Update client_email (via FK relationship)
    if payload.client_email:
        user = db.query(User).filter(User.email == payload.client_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Client with that email not found")
        plate.user_id = user.id

    db.commit()
    db.refresh(plate)

    return {"detail": "Plate updated successfully"}
