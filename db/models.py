from sqlalchemy import Integer, String, Column, Enum, DateTime, func, ForeignKey, Text , Float
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from schemas.user import RoleEnum
from enums import RequestStatus
from datetime import datetime

class Base(DeclarativeBase):
    pass


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.operator)


class ParkingSnapshot(Base):
    __tablename__ = "parking_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(String, default="CAMT_01", nullable=False)
    timestamp = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    available_spaces = Column(Integer, nullable=False)
    total_spaces = Column(Integer, default=30, nullable=False)
    occupied_spaces = Column(Integer, nullable=False)
    occupacy_rate = Column(Float, nullable=False)
    confidence= Column(Float, nullable=False)
    processing_time_seconds = Column(Float, nullable=False)

# User table
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relationship
    requests: Mapped[list["LicensePlateRequest"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


# License Plate Request table
class LicensePlateRequest(Base):
    __tablename__ = "license_plate_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    plate_number: Mapped[str] = mapped_column(String(20), nullable=False)
    plate_image_url: Mapped[str] = mapped_column(String, nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[RequestStatus] = mapped_column(default=RequestStatus.pending)

    # Relationship
    user: Mapped["User"] = relationship(back_populates="requests")

