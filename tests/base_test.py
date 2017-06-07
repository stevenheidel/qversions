import pytest
from qversions._db import Base, DeviceModel, GateModel, QubitModel
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
    session.commit()
    yield
