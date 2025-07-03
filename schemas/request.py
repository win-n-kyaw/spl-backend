from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from schemas.enums import RequestStatus

class LicensePlateRequestOut(BaseModel):
    id: int
    plate_number: str
    plate_image_url: str
    status: RequestStatus
    submitted_at: datetime

    class Config:
        orm_mode = True

class LicensePlateRequestWithClient(BaseModel):
    id: int
    plate_number: str
    plate_image_url: str
    status: RequestStatus

    client_name: str
    client_email: EmailStr

    class Config:
        orm_mode = True

class RequestStatusUpdate(BaseModel):
    status: RequestStatus  # "approved" or "declined"

class LicensePlateUpdate(BaseModel):
    status: Optional[RequestStatus]
    client_email: Optional[EmailStr]
    plate_number: Optional[str] = None
    plate_image_url: Optional[str] = None

