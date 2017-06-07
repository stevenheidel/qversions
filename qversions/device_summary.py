from .device import Device, Devices
from .gate import Gates
from .qubit import Qubits
from ._utils import validate_field, validate_param
from collections import defaultdict

"""
High level module for interacting with this versioning system.
"""

class DeviceSummary(object):
    def __init__(self, device_id, description, qubits, gates):
        self.device_id = device_id
        """Unique device id such as '7-qubit-prototype'"""
        self.description = description
        """Optional short description of the device"""
        self.qubits = qubits
        """List of qubits sorted by qubit id"""
        self.gates = gates
        """Map from qubit id to a set of gates for that qubit"""

    def __repr__(self):
        return ("Device id: {}\n"
                "Description: {}\n"
                "Qubits: {}\n"
                "Gates: {}"
                ).format(self.device_id, self.description, self.qubits, self.gates)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))

    def get_qubit(self, qubit_id):
        """
        Find a qubit with the corresponding id or None if it doesn't exist.

        :param int qubit_id: Qubit id
        :return: Qubit if it exists
        :rtype: Qubit
        """
        validate_param("qubit_id", qubit_id, int)

        for qubit in self.qubits:
            if qubit.qubit_id == qubit_id:
                return qubit
        return None

    def get_gates_by_qubit(self, qubit_id):
        """
        Find all gates that have been saved for a qubit or None if the qubit
        doesn't exist.

        :param int qubit_id: Qubit id
        :return: List of gates if the qubit exists
        :rtype: list
        """
        validate_param("qubit_id", qubit_id, int)

        return self.gates.get(qubit_id)

class DeviceSummaries(object):
    def __init__(self, engine):
        self.devices = Devices(engine)
        self.gates = Gates(engine)
        self.qubits = Qubits(engine)

    def create_device(self, device_id, description=None):
        """
        Create a new device. Device id must be unique even amongst devices that
        were previously deleted.

        :param string device_id: Unique device id such as '7-qubit-prototype'
        :param string description: Optional short description of the device
        """
        return self.devices.create_device(Device(device_id, description))

    def get_device(self, device_id):
        """
        Get device summary for this device_id or None if it doesn't exist.

        :param string device_id: Device id
        :return: Device summary if the device exists
        :rtype: DeviceSummary
        """
        device = self.devices.get_device(device_id)
        if device is None:
            raise RuntimeError("device_id {} does not exist".format(device_id))

        qubits = self.qubits.get_qubits_by_device(device_id)
        gates = self.gates.get_gates_by_device(device_id)

        return _make_summary(device, qubits, gates)

    def get_snapshot(self, device_id, timestamp):
        """
        Get the state of a device at a particular point in time.

        :param string device_id: Device id
        :return: Device summary if the device exists
        :rtype: DeviceSummary
        """
        device = self.devices.get_device(device_id)
        if device is None:
            raise RuntimeError("device_id {} does not exist".format(device_id))

        qubits = self.qubits.get_qubits_by_device(device_id, timestamp)
        gates = self.gates.get_gates_by_device(device_id, timestamp)

        return _make_summary(device, qubits, gates)

    def save_qubit(self, qubit):
        """
        Save new qubit measurements to the system.

        :param Qubit qubit: Qubit to save
        :return: timestamp of the system before saving qubit
        :rtype: int
        """
        if self.devices.get_device(qubit.device_id) is None:
            raise RuntimeError("device_id {} does not exist".format(qubit.device_id))

        return self.qubits.save_qubit(qubit)

    def save_gate(self, gate):
        """
        Save new gate measurements to the system.

        :param Gate gate: Gate to save
        :return: timestamp of the system before saving gate
        :rtype: int
        """
        if self.devices.get_device(gate.device_id) is None:
            raise RuntimeError("device_id {} does not exist".format(gate.device_id))

        if self.qubits.get_qubit(gate.device_id, gate.qubit_id) is None:
            raise RuntimeError("qubit with device_id {} and qubit_id {} does not exist"\
                    .format(gate.device_id, gate.qubit_id))

        return self.gates.save_gate(gate)

def _make_summary(device, qubits, gates):
    """
    Construct a summary object from the list results
    """
    qubit_ids = set(map(lambda qubit: qubit.qubit_id, qubits))
    sorted_qubits = sorted(qubits, key=lambda qubit: qubit.qubit_id)

    gate_dict = defaultdict(set)
    for gate in gates:
        if gate.qubit_id in qubit_ids:
            gate_dict[gate.qubit_id].add(gate)

    return DeviceSummary(device.device_id, device.description, sorted_qubits, gate_dict)
