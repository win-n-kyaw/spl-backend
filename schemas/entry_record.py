from pydantic import BaseModel
from datetime import datetime

class EntryRecordBase(BaseModel):
    plate_number: str
    plate_image_url: str
    timestamp: datetime

class EntryRecordCreate(EntryRecordBase):
    pass

class EntryRecord(EntryRecordBase):
    id: int

    class Config:
        from_attributes = True
