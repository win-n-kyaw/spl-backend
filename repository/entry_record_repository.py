from typing import List, Optional
from sqlalchemy.orm import Session
from db.models import EntryRecord
from repository.ientry_record_repository import IEntryRecordRepository
from datetime import date, time, datetime

class EntryRecordRepository(IEntryRecordRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all_entry_records(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[EntryRecord]:
        query = self.db.query(EntryRecord).order_by(EntryRecord.timestamp.desc())
        if start_date:
            start_datetime = datetime.combine(start_date, time.min)
            query = query.filter(EntryRecord.timestamp >= start_datetime)
        if end_date:
            end_datetime = datetime.combine(end_date, time.max)
            query = query.filter(EntryRecord.timestamp <= end_datetime)
        return query.all()

    def get_entry_record_by_id(self, entry_id: int) -> Optional[EntryRecord]:
        return self.db.query(EntryRecord).filter(EntryRecord.id == entry_id).first()

    def update_entry_record(self, entry_record: EntryRecord) -> EntryRecord:
        self.db.add(entry_record)
        self.db.commit()
        self.db.refresh(entry_record)
        return entry_record

    def delete_entry_record(self, entry_id: int) -> None:
        entry_record = self.get_entry_record_by_id(entry_id)
        if entry_record:
            self.db.delete(entry_record)
            self.db.commit()
