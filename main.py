from qversions.device import Device, Devices

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
