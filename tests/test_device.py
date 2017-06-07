from base_test import *
import pytest
from qversions.device import Device, Devices

devices = Devices(engine)

name1 = "test-device-1"
name2 = "test-device-2"
name3 = "test-device-3"

def test_create():
    device = Device(name1, desc)
    devices.create_device(device)
    assert devices.get_device(name1) == device

def test_create_conflict():
    device = Device(name1, desc)
    devices.create_device(device)
    with pytest.raises(RuntimeError):
        devices.create_device(device)

def test_get_nonexistent():
    assert devices.get_device(name1) == None

def test_get_all_devices():
    device1 = Device(name1, desc)
    device2 = Device(name2, desc)
    devices.create_device(device1)
    devices.create_device(device2)
    assert set(devices.get_all_devices()) == set([device1, device2])
    devices.delete_device(name1)
    assert set(devices.get_all_devices()) == set([device2])

def test_update_device():
    device = Device(name1, "old")
    devices.create_device(device)
    device = Device(name1, "new")
    devices.update_device(device)
    assert devices.get_device(name1).description == "new"

def test_update_nonexistent():
    device = Device(name1, "old")
    with pytest.raises(RuntimeError):
        devices.update_device(device)

def test_delete_device():
    device = Device(name1, desc)
    devices.create_device(device)
    assert devices.get_device(name1) == device
    devices.delete_device(name1)
    assert devices.get_device(name1) == None

def test_delete_device_nonexistent():
    with pytest.raises(RuntimeError):
        devices.delete_device(name1)

def test_get_archived_devices():
    device1 = Device(name1, desc)
    device2 = Device(name2, desc)
    device3 = Device(name3, desc)
    devices.create_device(device1)
    devices.create_device(device2)
    devices.delete_device(name1)
    devices.delete_device(name2)
    assert set(devices.get_archived_devices()) == set([device1, device2])

def test_restore_device():
    device = Device(name1, desc)
    devices.create_device(device)
    devices.delete_device(name1)
    assert devices.get_device(name1) == None
    devices.restore_device(name1)
    assert devices.get_device(name1) == device
