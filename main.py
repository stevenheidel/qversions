from qversions._db import Base
from qversions.device_summary import DeviceSummaries
from sqlalchemy import create_engine

_engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(_engine)

q = DeviceSummaries(_engine)
