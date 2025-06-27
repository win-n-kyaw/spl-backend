from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.models import ParkingSnapshot
from db.session import get_db
from schemas.parking import ParkingSnapshotResponse
from typing import List

router = APIRouter(tags=["Parking Status"])


@router.get("/parking", response_model=List[ParkingSnapshotResponse])
def get_parking_snapshots(db: Session = Depends(get_db)):
    return db.query(ParkingSnapshot).order_by(ParkingSnapshot.timestamp.desc()).all()


@router.get("/parking/latest", response_model=ParkingSnapshotResponse)
def get_latest_snapshot(db: Session = Depends(get_db)):
    return (
        db.query(ParkingSnapshot)
        .order_by(ParkingSnapshot.timestamp.desc())
        .limit(1)
        .one_or_none()
    )
