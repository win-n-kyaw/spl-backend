from abc import ABC, abstractmethod
from typing import Optional
from db.models import ParkingSnapshot
from schemas.parking import ParkingSnapshotCreate


class IParkingRepository(ABC):
    @abstractmethod
    def get_latest_snapshot(self) -> Optional[ParkingSnapshot]:
        pass

    @abstractmethod
    def create_snapshot(self, snapshot: ParkingSnapshotCreate) -> ParkingSnapshot:
        pass
