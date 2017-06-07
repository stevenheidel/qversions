from base_test import *
import pytest
from qversions.device import Device, Devices

devices = Devices(engine)

def test_create():
    device = Device("test-device-1")
    devices.create_device(device)
    assert devices.get_device("test-device-1") == device

def test_create_conflict():
    device = Device("test-device-1")
    devices.create_device(device)
    with pytest.raises(RuntimeError):
        devices.create_device(device)

def test_get_nonexistent():
    assert devices.get_device("test-device-1") == None

def test_get_all_devices():
    device1 = Device("test-device-1")
    device2 = Device("test-device-2", description="desc")
    devices.create_device(device1)
    devices.create_device(device2)
    assert set(devices.get_all_devices()) == set([device1, device2])
    devices.delete_device("test-device-1")
    assert set(devices.get_all_devices()) == set([device2])

def test_update_device():
    device = Device("test-device-1", description="old")
    devices.create_device(device)
    device = Device("test-device-1", description="new")
    devices.update_device(device)
    assert devices.get_device("test-device-1").description == "new"

def test_update_nonexistent():
    device = Device("test-device-1", description="old")
    with pytest.raises(RuntimeError):
        devices.update_device(device)

def test_delete_device():
    device = Device("test-device-1")
    devices.create_device(device)
    assert devices.get_device("test-device-1") == device
    devices.delete_device("test-device-1")
    assert devices.get_device("test-device-1") == None

def test_delete_device_nonexistent():
    with pytest.raises(RuntimeError):
        devices.delete_device("test-device-1")

def test_get_archived_devices():
    device1 = Device("test-device-1")
    device2 = Device("test-device-2", description="desc")
    device3 = Device("test-device-3")
    devices.create_device(device1)
    devices.create_device(device2)
    devices.delete_device("test-device-1")
    devices.delete_device("test-device-2")
    assert set(devices.get_archived_devices()) == set([device1, device2])

def test_restore_device():
    device = Device("test-device-1")
    devices.create_device(device)
    devices.delete_device("test-device-1")
    assert devices.get_device("test-device-1") == None
    devices.restore_device("test-device-1")
    assert devices.get_device("test-device-1") == device
