from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from schemas.entry_record import EntryRecord
from services.entry_record_service import EntryRecordService
from services.dependencies import get_entry_record_service
from datetime import date

router = APIRouter(prefix="/api", tags=["entry-records"])

@router.get("/entry-records", response_model=List[EntryRecord])
def get_all_entry_records(
    entry_record_service: EntryRecordService = Depends(get_entry_record_service),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None)
):
    return entry_record_service.get_all_entry_records(start_date=start_date, end_date=end_date)
