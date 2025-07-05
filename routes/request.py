from fastapi import Depends, APIRouter, HTTPException
from db.models import LicensePlateRequest, Admin
from db.session import get_db
from schemas.request import LicensePlateRequestWithClient, RequestStatusUpdate
from enums import RequestStatus
from sqlalchemy.orm import Session, joinedload
from auth import jwt
from typing import List

router = APIRouter(tags=["Registeration requests"])

@router.get("/requests", response_model=List[LicensePlateRequestWithClient])
async def list_requests(db: Session = Depends(get_db), current_user: Admin = Depends(jwt.get_current_user)):
    if current_user.role not in ("admin", "operator"):
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    pending_requests = (
        db.query(LicensePlateRequest)
        .options(joinedload(LicensePlateRequest.user))
        .filter(LicensePlateRequest.status == RequestStatus.pending)
        .all()
    )

    if not pending_requests:
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
        for req in pending_requests
    ]

# request in context means license plate registration request
@router.put("/requests/{request_id}")
def update_request_status(
    request_id: int,
    payload: RequestStatusUpdate,
    db: Session = Depends(get_db),
    current_user: Admin = Depends(jwt.get_current_user)
):
    if current_user.role not in ("admin", "operator"):
        raise HTTPException(status_code=401, detail="You are not authorized to perform this action")
    
    request = db.query(LicensePlateRequest).filter_by(id=request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Registration request not found")

    if request.status != RequestStatus.pending:
        raise HTTPException(status_code=400, detail="Registration request already processed")

    request.status = payload.status
    db.commit()
    db.refresh(request)
    return request