from fastapi import HTTPException, status
from repository.iparking_repository import IParkingRepository
from schemas.parking import ParkingSnapshotCreate, ParkingSnapshotResponse


class ParkingService:
    def __init__(self, parking_repo: IParkingRepository):
        self.parking_repo = parking_repo

    def get_latest_snapshot(self) -> ParkingSnapshotResponse:
        snapshot = self.parking_repo.get_latest_snapshot()
        if not snapshot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No parking snapshot found",
            )
        return ParkingSnapshotResponse.from_orm(snapshot)

    def create_snapshot(self, snapshot_data: ParkingSnapshotCreate) -> ParkingSnapshotResponse:
        snapshot = self.parking_repo.create_snapshot(snapshot_data)
        return ParkingSnapshotResponse.from_orm(snapshot)
