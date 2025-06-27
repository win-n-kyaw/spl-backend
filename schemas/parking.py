from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ParkingPayload(BaseModel):
    lot_id: str = "CAMT_01"
    available_spots: int
    total_spots: int = 30
    timestamp: Optional[datetime] = None  # fallback to server time if None


class ParkingSnapshotResponse(BaseModel):
    id: int
    lot_id: str
    timestamp: datetime
    available_spots: int
    total_spots: int

    class Config:
        orm_mode = True
