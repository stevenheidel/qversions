from .device import Devices
from .gate import Gates
from .qubit import Qubits

"""
High level module for interacting with this versioning system.
"""

class DeviceSummary:
    def __init__(self, device_id, summary, qubits, gates):
        self.device_id = device_id
        """Unique device id such as '7-qubit-prototype'"""
        self.summary = summary
        """Optional short description of the device"""
        self.qubits = qubits
        """List of qubits sorted by qubit id"""
        self.gates = gates
        """Map from qubit id to a list of gates for that qubit"""

    def get_qubit(qubit_id):
        """
        Find a qubit with the corresponding id or None if it doesn't exist.

        :param int qubit_id: Qubit id
        :return: Qubit if it exists
        :rtype: Qubit
        """
        for qubit in qubits:
            if qubit.qubit_id == qubit_id:
                return qubit
        return None

    def get_gates_by_qubit(qubit_id):
        """
        Find all gates that have been saved for a qubit or None if the qubit
        doesn't exist.

        :param int qubit_id: Qubit id
        :return: List of gates if the qubit exists
        :rtype: list
        """
        return gates.get(qubit_id)

class DeviceSummaries:
    def __self__(engine):
        self.devices = Devices(engine)
        self.gates = Gates(engine)
        self.qubits = Qubits(engine)

    def create_device(device_id, description):
        """
        Create a new device. Device id must be unique even amongst devices that
        were previously deleted.

        :param string device_id: Unique device id such as '7-qubit-prototype'
        :param string description: Optional short description of the device
        """
        return devices.create_device(Device(device_id, description))

    def get_device(device_id):
        """
        Get device summary for this device_id or None if it doesn't exist.

        :param string device_id: Device id
        :return: Device summary if the device exists
        :rtype: DeviceSummary
        """
        pass

    def get_snapshot(device_id, timestamp):
        """
        Get the state of a device at a particular point in time.

        :param string device_id: Device id
        :return: Device summary if the device exists
        :rtype: DeviceSummary
        """
        pass

    def save_qubit(qubit):
        return qubits.save_qubit(qubit)

    def save_gate(gate):
        return gates.save_gate(gate)
