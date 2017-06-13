from qversions._db import Base
from qversions.device_summary import DeviceSummaries
from qversions.qubit import Qubit
from qversions.gate import Gate
from sqlalchemy import create_engine

_engine = create_engine("sqlite:///:memory:")
# _engine = create_engine("postgres://postgres@localhost:5432/qversions")
# _engine = create_engine("mysql+mysqldb://root@localhost/qversions")
Base.metadata.create_all(_engine)

q = DeviceSummaries(_engine)

sample = "sample"
try:
    q.get_device(sample)
except:
    q.create_device(sample, "Sample device")
    q.save_qubit(Qubit(sample, 0, resonance_frequency=0.0, t1=0.0, t2=0.0))
    q.save_qubit(Qubit(sample, 1, resonance_frequency=1.0, t1=1.0, t2=1.0))
    q.save_gate(Gate(sample, 0, "+X", amplitude=0.0, width=0.0, phase=0.0))
