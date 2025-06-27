from sqlalchemy import Integer, String, Column, Enum
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


# class LicensePlate(Base):
#     __tablename__ = 'license_plates'
#     id = Column(Integer, primary_key=True)
#     plate_num = Column(String, nullable=False)
#     owner = Column(Integer, ForeignKey('users.id'))
