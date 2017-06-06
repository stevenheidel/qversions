
"""
Module for interacting with Quantum devices.
"""

class Device:
    def __init__(self, device_id, description):
        self.device_id = device_id
        """Unique device id such as '7-qubit-prototype'"""
        self.description = description
        """Short description of the device"""

def create_device(device):
    """
    Create a new device. Device id must be unique even amongst devices that were
    previously deleted.

    :param Device device: Device to create
    """
    pass

def get_device(device_id):
    """
    Get a device by its id.

    :param string device_id: Device id
    :return: Either a device or None if not found or device was deleted
    :rtype: Device
    """
    pass

def get_all_devices():
    """
    Return a list of all saved devices.

    :return: List of devices
    :rtype: list
    """
    pass

def update_device(device):
    """
    Update the description of a device. Will raise exception if device does not
    exist.

    :param Device device: Device to update
    """
    pass

def delete_device(device_id):
    """
    Archive a device. Will raise exception if device does not exist.

    Also archives all the Qubits for this device as well as the Gates for
    those Qubits.

    :param string device_id: Device id
    """
    pass

def get_all_archived_devices():
    """
    Return a list of all devices that have been deleted.

    :return: List of deleted devices
    :rtype: list
    """
    pass

def restore_device(device_id):
    """
    Un-archive a device. Will raise exception if device was never created.

    Also un-archives all the Qubits for this device as well as the Gates for
    those Qubits.

    :param string device_id: Device id
    :return: The un-archived device
    :rtype: Device
    """
    pass
