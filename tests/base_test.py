import pytest
from qversions._db import Base, DeviceModel, GateModel, QubitModel
from qversions.device import Device
from qversions.qubit import Qubit
from qversions.gate import Gate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

@pytest.yield_fixture(autouse=True)
def setup():
    session = sessionmaker(bind=engine)()
    session.query(DeviceModel).delete()
    session.query(GateModel).delete()
    session.query(QubitModel).delete()
    yield

name1 = "test-device-1"
name2 = "test-device-2"
name3 = "test-device-3"
desc = "This is a test device"

qubit0 = Qubit(name1, 0, resonance_frequency=0.0, t1=0.0, t2=0.0)
qubit1 = Qubit(name1, 1, resonance_frequency=1.0, t1=1.0, t2=1.0)

gate1X = Gate(name1, 1, "+X", amplitude=1.0, width=1.0, phase=1.0)
gate1Y = Gate(name1, 1, "-Y/2", amplitude=1.2, width=1.2, phase=1.2)
gate0X = Gate(name1, 0, "+X", amplitude=0.0, width=0.0, phase=0.0)
