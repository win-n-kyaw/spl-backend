from fastapi import APIRouter, Depends, status
from schemas.parking import ParkingSnapshotResponse
from services.dependencies import get_parking_service
from services.parking_service import ParkingService

router = APIRouter(prefix="/parking", tags=["parking"])


@router.get("/snapshot/latest", response_model=ParkingSnapshotResponse, status_code=status.HTTP_200_OK)
def get_latest_snapshot(
    parking_service: ParkingService = Depends(get_parking_service),
):
    return parking_service.get_latest_snapshot()
