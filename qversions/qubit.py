
"""
Module for interacting with Quantum Bits (Qubits).
"""

class Qubit:
    def __init__(self, device_id, qubit_id, resonance_frequency, t1, t2):
        self.device_id = device_id
        """Device that this qubit is associated with"""
        self.qubit_id = qubit_id
        """Positive integer uniquely identifying this qubit"""
        self.resonance_frequency = resonance_frequency
        """Resonance frequency in GHz"""
        self.t1 = t1
        """Coherence time constant 1 in microseconds"""
        self.t2 = t2
        """Coherence time constant 2 in microseconds"""

def save_qubit(qubit):
    """
    Save new parameters for this qubit. Will overwrite any previous data saved
    for this device's qubit with the same qubit id.

    :param Qubit qubit: Qubit to save
    """
    pass

def get_qubit(device_id, qubit_id, timestamp=None):
    """
    Get a qubit by its id.

    :param string device_id: Device id
    :param int qubit_id: Qubit id
    :param long timestamp: If specified, will return the qubit's measurements
            from that particular time. Otherwise, will return latest info.
    :return: Either a qubit or None if not found or qubit was deleted
    :rtype: Qubit
    """
    pass

def get_qubits_by_device(device_id, timestamp=None):
    """
    Find all the qubits that have been saved for a device.

    :param string device_id: Device id
    :param long timestamp: If specified, will return the qubits that existed at
            that particular time. Otherwise, will return latest info.
    :return: List of qubits
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
