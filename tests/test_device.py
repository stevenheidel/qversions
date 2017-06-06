from base_test import *
import pytest
from qversions._db import DeviceModel
from qversions.device import Device, Devices
from sqlalchemy.orm import sessionmaker

@pytest.yield_fixture(autouse=True)
def setup():
    session = sessionmaker(bind=engine)()
    session.query(DeviceModel).delete()
    yield

devices = Devices(engine)

def test_create():
    device = Device(device_id="abc")
    devices.create_device(device)
    assert devices.get_device("abc") == device

def test_create_conflict():
    device = Device(device_id="abc")
    devices.create_device(device)
    with pytest.raises(RuntimeError):
        devices.create_device(device)

def test_get_nonexistent():
    assert devices.get_device("abc") == None

def test_get_all_devices():
    device1 = Device(device_id="abc")
    device2 = Device(device_id="def", description="desc")
    devices.create_device(device1)
    devices.create_device(device2)
    assert set(devices.get_all_devices()) == set([device1, device2])
    devices.delete_device("abc")
    assert set(devices.get_all_devices()) == set([device2])

def test_update_device():
    device = Device(device_id="abc", description="old")
    devices.create_device(device)
    device = Device(device_id="abc", description="new")
    devices.update_device(device)
    assert devices.get_device("abc").description == "new"

def test_update_nonexistent():
    device = Device(device_id="abc", description="old")
    with pytest.raises(RuntimeError):
        devices.update_device(device)

def test_delete_device():
    device = Device(device_id="abc")
    devices.create_device(device)
    assert devices.get_device("abc") == device
    devices.delete_device("abc")
    assert devices.get_device("abc") == None

def test_delete_device_nonexistent():
    with pytest.raises(RuntimeError):
        devices.delete_device("abc")

def test_get_archived_devices():
    device1 = Device(device_id="abc")
    device2 = Device(device_id="def", description="desc")
    device3 = Device(device_id="ghi")
    devices.create_device(device1)
    devices.create_device(device2)
    devices.delete_device("abc")
    devices.delete_device("def")
    assert set(devices.get_archived_devices()) == set([device1, device2])

def test_restore_device():
    device = Device(device_id="abc")
    devices.create_device(device)
    devices.delete_device("abc")
    assert devices.get_device("abc") == None
    devices.restore_device("abc")
    assert devices.get_device("abc") == device
