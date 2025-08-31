from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from schemas.parking import ParkingSnapshotResponse
from services.dependencies import get_parking_service
from services.parking_service import ParkingService

router = APIRouter(prefix="/api/parking", tags=["parking"])


@router.get("/snapshot/latest", response_model=ParkingSnapshotResponse, status_code=status.HTTP_200_OK)
def get_latest_snapshot(
    parking_service: ParkingService = Depends(get_parking_service),
):
    return parking_service.get_latest_snapshot()


@router.get("/inference")
def get_parking1_inference(
    parking_service: ParkingService = Depends(get_parking_service),
):
    image_bytes = parking_service.infer_parking1_snapshot()
    return Response(content=image_bytes, media_type="image/jpeg")

@router.get("/open")
def get_open_gate(
    parking_service: ParkingService = Depends(get_parking_service),
):
    return parking_service.open_gate()