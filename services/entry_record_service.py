from typing import List, Optional
from repository.ientry_record_repository import IEntryRecordRepository
from schemas.entry_record import EntryRecord
from datetime import date

class EntryRecordService:
    def __init__(self, entry_record_repository: IEntryRecordRepository):
        self.entry_record_repository = entry_record_repository

    def get_all_entry_records(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[EntryRecord]:
        db_entry_records = self.entry_record_repository.get_all_entry_records(start_date=start_date, end_date=end_date)
        return [EntryRecord.from_orm(rec) for rec in db_entry_records]
