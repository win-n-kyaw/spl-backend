from typing import List, Optional
from sqlalchemy.orm import Session
from db.models import EntryRecord
from repository.ientry_record_repository import IEntryRecordRepository
from datetime import date, time, datetime

class EntryRecordRepository(IEntryRecordRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_entry_records(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[EntryRecord]:
        query = self.db.query(EntryRecord)
        if start_date:
            start_datetime = datetime.combine(start_date, time.min)
            query = query.filter(EntryRecord.timestamp >= start_datetime)
        if end_date:
            end_datetime = datetime.combine(end_date, time.max)
            query = query.filter(EntryRecord.timestamp <= end_datetime)
        return query.all()
