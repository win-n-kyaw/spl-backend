from abc import ABC, abstractmethod
from typing import List, Optional
from db.models import EntryRecord
from datetime import date

class IEntryRecordRepository(ABC):
    @abstractmethod
    def get_all_entry_records(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[EntryRecord]:
        pass
