from base_test import *
import pytest
from qversions.qubit import Qubit, Qubits

qubits = Qubits(engine)

def test_save():
    qubits.save_qubit(qubit0)
    assert qubits.get_qubit(name1, 0) == qubit0

def test_update():
    initial_timestamp = qubits.save_qubit(qubit0)
    qubit0.t1 = -1.0
    update_timestamp = qubits.save_qubit(qubit0)
    assert qubits.get_qubit(name1, 0).t1 == -1.0
    assert qubits.get_qubit(name1, 0, update_timestamp).t1 == 0.0
    assert qubits.get_qubit(name1, 0, initial_timestamp) == None

def test_get_qubits_by_device():
    qubit_on_different_device = Qubit("test-device-2", 1, resonance_frequency=5.0, t1=5.0, t2=5.0)
    save_qubits([qubit0, qubit1, qubit_on_different_device])
    qubits.save_qubit(qubit_on_different_device)
    assert set(qubits.get_qubits_by_device(name1)) == set([qubit0, qubit1])
    delete_timestamp = qubits.delete_qubit(name1, 0)
    assert set(qubits.get_qubits_by_device(name1)) == set([qubit1])
    assert set(qubits.get_qubits_by_device(name1, delete_timestamp)) == set([qubit0, qubit1])

def test_delete_qubit_nonexists():
    with pytest.raises(RuntimeError):
        qubits.delete_qubit(name1, 1)

def save_qubits(qubit_list):
    for qubit in qubit_list:
        qubits.save_qubit(qubit)
