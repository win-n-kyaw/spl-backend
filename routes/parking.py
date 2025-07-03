from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from db.models import ParkingSnapshot
from db.session import get_db
from schemas.parking import ParkingSnapshotResponse
from typing import List

router = APIRouter(tags=["Parking Status"])


@router.get("/parking", response_model=List[ParkingSnapshotResponse])
def get_parking_snapshots(db: Session = Depends(get_db)):
    try:
        snapshots = (
            db.query(ParkingSnapshot)
            .order_by(ParkingSnapshot.timestamp.desc())
            .all()
        )
        if not snapshots:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No parking snapshots found.",
            )
        return snapshots
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database query failed.",
        )


@router.get("/parking/latest", response_model=ParkingSnapshotResponse)
def get_latest_snapshot(db: Session = Depends(get_db)):
    try:
        latest_snapshot = (
            db.query(ParkingSnapshot)
            .order_by(ParkingSnapshot.timestamp.desc())
            .limit(1)
            .one_or_none()
        )
        if not latest_snapshot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No latest parking snapshot available.",
            )
        return latest_snapshot
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve the latest parking snapshot.",
        )
