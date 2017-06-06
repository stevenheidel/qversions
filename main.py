from qversions.device import Device, Devices
from qversions.qubit import Qubit, Qubits

from sqlalchemy import create_engine
engine = create_engine("sqlite:///:memory:")

from qversions._db import Base
Base.metadata.create_all(engine)

devices = Devices(engine)
devices.create_device(Device(device_id="abc"))
devices.create_device(Device(device_id="def"))
print(devices.get_device("abc"))
print(devices.get_device("def"))
print(devices.get_all_devices())
devices.update_device(Device(device_id="abc", description="hello"))
print(devices.get_all_devices())
devices.delete_device("abc")
print(devices.get_device("abc"))
print(devices.get_all_devices())
print(devices.get_archived_devices())

qubits = Qubits(engine)
qubits.save_qubit(Qubit(device_id="abc", qubit_id=0, t1=0.5))
print(qubits.get_qubit("abc", 0))
timestamp_before_delete = qubits.save_qubit(Qubit(device_id="abc", qubit_id=0, t1=0.3))
print(qubits.get_qubit("abc", 0))
print(qubits.get_qubits_by_device("abc"))
qubits.delete_qubit("abc", 0)
print(qubits.get_qubit("abc", 0))
print(qubits.get_qubits_by_device("abc"))
qubits.save_qubit(Qubit(device_id="abc", qubit_id=0, t1=0.2))
print(qubits.get_qubit("abc", 0))
timestamp = qubits.save_qubit(Qubit(device_id="abc", qubit_id=0, t1=0.1))
print(timestamp)
print(qubits.get_qubit("abc", 0, timestamp-1))
print(qubits.get_qubits_by_device("abc", timestamp_before_delete))
