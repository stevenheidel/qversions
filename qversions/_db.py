from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DeviceModel(Base):
    __tablename__ = 'devices'

    device_id = Column(String, primary_key=True)
    description = Column(String, nullable=False)
    archived = Column(Boolean, default=False, index=True)

class QubitModel(Base):
    __tablename__ = 'qubits'

    device_id = Column(String, primary_key=True)
    qubit_id = Column(Integer, primary_key=True)
    timestamp = Column(BigInteger, primary_key=True)
    resonance_frequency = Column(Float, nullable=False)
    t1 = Column(Float, nullable=False)
    t2 = Column(Float, nullable=False)
    archived = Column(Boolean, default=False, index=True)

class GateModel(Base):
    __tablename__ = 'gates'

    device_id = Column(String, primary_key=True)
    qubit_id = Column(Integer, primary_key=True)
    gate_id = Column(String, primary_key=True)
    timestamp = Column(BigInteger, primary_key=True)
    amplitude = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    phase = Column(Float, nullable=False)
    archived = Column(Boolean, default=False, index=True)
