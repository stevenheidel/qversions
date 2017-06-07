from sqlalchemy.orm import sessionmaker

"""
Module for interacting with Quantum Gates.
"""

class Gate(object):
    def __init__(self, device_id, qubit_id, gate_id, amplitude, width, phase):
        self.device_id = device_id
        """Device that this gate is associated with"""
        self.qubit_id = qubit_id
        """Qubit that this gate is associated with"""
        self.gate_id = gate_id
        """Short name string like '+X' to uniquely identify the gate"""
        self.amplitude = amplitude
        """Amplitude of control pulse in mV (optional)"""
        self.width = width
        """Width of control pulse in ns (optional)"""
        self.phase = phase
        """Phase of control pulse (optional)"""

class Gates(object):
    def __init__(self, engine):
        self.sessionmaker = sessionmaker(bind=engine)

def save_gate(gate):
    """
    Save new parameters for this gate. Will overwrite any previous data saved
    for this qubit's gate with the same id.

    :param Gate qubit: Gate to save
    """
    pass

def get_gate(device_id, qubit_id, gate_id, timestamp=None):
    """
    Get a gate by its id.

    :param string device_id: Device id
    :param int qubit_id: Qubit id
    :param string gate_id: Gate id
    :param long timestamp: If specified, will return the gate's measurements
            from that particular time. Otherwise, will return latest info.
    :return: Either a gate or None if not found or gate was deleted
    :rtype: Gate
    """
    pass

def get_gates_by_qubit(device_id, qubit_id, timestamp=None):
    """
    Find all gates that have been saved for a qubit.

    :param string device_id: Device id
    :param int qubit_id: Qubit id
    :return: List of gates
    :rtype: list
    """
    pass

def get_gates_by_device(device_id, timestamp=None):
    """
    Find all gates that have been saved for all qubits on a device.

    :param string device_id: Device id
    :param long timestamp: If specified, will return the gates that existed at
            that particular time. Otherwise, will return latest info.
    :return: List of gates
    :rtype: list
    """
    pass

def delete_qubit(device_id, qubit_id):
    """
    Archive a qubit. Will raise exception if qubit does not exist.

    :param string device_id: Device id
    :param int qubit_id: Qubit id
    """
    pass
