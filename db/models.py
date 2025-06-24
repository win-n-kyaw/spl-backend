import datetime as _dt
from sqlalchemy import Integer, String, Float, Column, ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


# class LicensePlate(Base):
#     __tablename__ = 'license_plates'
#     id = Column(Integer, primary_key=True)
#     plate_num = Column(String, nullable=False)
#     owner = Column(Integer, ForeignKey('users.id'))
