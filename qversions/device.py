from ._db import DeviceModel
from ._utils import validate_field, validate_param
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

"""
Module for interacting with Quantum devices.
"""

class Device(object):
    def __init__(self, device_id, description=None):
        self.device_id = device_id
        """Unique device id such as '7-qubit-prototype'"""
        self.description = description
        """Short description of the device (optional)"""

    def __repr__(self):
        return "<Device(device_id={}, description={})>".format(self.device_id,
                self.description)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))

class Devices(object):
    def __init__(self, engine):
        self.sessionmaker = sessionmaker(bind=engine)

    def create_device(self, device):
        """
        Create a new device. Device id must be unique even amongst devices that were
        previously deleted.

        :param Device device: Device to create
        """
        validate_param("device", device, Device)
        try:
            with self._session() as session:
                session.add(_validate(device))
        except IntegrityError:
            raise RuntimeError("Device already exists")

    def get_device(self, device_id):
        """
        Get a device by its id.

        :param string device_id: Device id
        :return: Either a device or None if not found or device was deleted
        :rtype: Device
        """
        validate_param("device_id", device_id, str)
        result = self._query().filter_by(archived=False, device_id=device_id)\
                .one_or_none()
        return _wrap(result)

    def get_all_devices(self):
        """
        Return a list of all saved devices.

        :return: List of devices
        :rtype: list
        """
        result = self._query().filter_by(archived=False).all()
        return _wrap(result)

    def update_device(self, device):
        """
        Update the description of a device. Will raise exception if device does not
        exist.

        :param Device device: Device to update
        """
        validate_param("device", device, Device)
        _validate(device)
        with self._session() as session:
            old_device = session.query(DeviceModel).get(device.device_id)
            if old_device is None:
                raise RuntimeError("device_id {} does not exist".format(device.device_id))
            old_device.description = device.description

    def delete_device(self, device_id):
        """
        Archive a device. Will raise exception if device does not exist.

        :param string device_id: Device id
        """
        validate_param("device_id", device_id, str)
        with self._session() as session:
            deleted_device = session.query(DeviceModel).get(device_id)
            if deleted_device is None:
                raise RuntimeError("device_id {} does not exist".format(device_id))
            deleted_device.archived = True

    def get_archived_devices(self):
        """
        Return a list of all devices that have been deleted.

        :return: List of deleted devices
        :rtype: list
        """
        result = self._query().filter_by(archived=True).all()
        return _wrap(result)

    def restore_device(self, device_id):
        """
        Un-archive a device. Will raise exception if device was never created.

        :param string device_id: Device id
        :return: The un-archived device
        :rtype: Device
        """
        validate_param("device_id", device_id, str)
        with self._session() as session:
            deleted_device = session.query(DeviceModel).get(device_id)
            deleted_device.archived = False

    def _query(self):
        session = self.sessionmaker()
        return session.query(DeviceModel)

    @contextmanager
    def _session(self):
        session = self.sessionmaker()
        yield session
        session.commit()

def _validate(device):
    """
    Validate the public Device API and then convert to internal model.
    """
    validate_field(device, "device_id", str)
    validate_field(device, "description", str, optional=True)

    return DeviceModel(device_id=device.device_id,
            description=device.description)

def _wrap(model):
    """
    Converts the internal model into the public device API.
    """
    if model is None:
        return None
    elif isinstance(model, list):
        return list(map(_wrap, model))
    else:
        return Device(device_id=model.device_id,
                description=model.description)
