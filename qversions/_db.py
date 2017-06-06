from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DeviceModel(Base):
    __tablename__ = 'devices'

    device_id = Column(String, primary_key=True)
    description = Column(String)
    archived = Column(Boolean, default=False)
