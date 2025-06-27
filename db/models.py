from sqlalchemy import Integer, String, Column, Enum, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from schemas.user import RoleEnum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

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
    available_spots = Column(Integer, nullable=False)
    total_spots = Column(Integer, default=30, nullable=False)


# class LicensePlate(Base):
#     __tablename__ = 'license_plates'
#     id = Column(Integer, primary_key=True)
#     plate_num = Column(String, nullable=False)
#     owner = Column(Integer, ForeignKey('users.id'))
