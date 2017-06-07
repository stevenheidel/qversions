from base_test import *
import pytest
from qversions.qubit import Qubit, Qubits

qubits = Qubits(engine)

def test_save():
    qubit = Qubit(device_id="abc", qubit_id=0, resonance_frequency=0.5, t1=1.5, t2=2.5)
    qubits.save_qubit(qubit)
    assert qubits.get_qubit("abc", 0) == qubit

def test_update():
    qubit = Qubit(device_id="abc", qubit_id=0, t1=1.0)
    initial_timestamp = qubits.save_qubit(qubit)
    qubit.t1 = 2.0
    update_timestamp = qubits.save_qubit(qubit)
    assert qubits.get_qubit("abc", 0).t1 == 2.0
    assert qubits.get_qubit("abc", 0, update_timestamp).t1 == 1.0
    assert qubits.get_qubit("abc", 0, initial_timestamp) == None

def test_get_qubits_by_device():
    qubit1 = Qubit(device_id="abc", qubit_id=1, t1=1.0)
    qubit2 = Qubit(device_id="abc", qubit_id=2, t2=1.0)
    qubits.save_qubit(qubit1)
    qubits.save_qubit(qubit2)
    assert set(qubits.get_qubits_by_device("abc")) == set([qubit1, qubit2])
    delete_timestamp = qubits.delete_qubit("abc", 1)
    assert set(qubits.get_qubits_by_device("abc")) == set([qubit2])
    assert set(qubits.get_qubits_by_device("abc", delete_timestamp)) == set([qubit1, qubit2])

def test_delete_qubit_nonexists():
    with pytest.raises(RuntimeError):
        qubits.delete_qubit("abc", 1)
