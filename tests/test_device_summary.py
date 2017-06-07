from base_test import *
import pytest
from qversions.device_summary import DeviceSummary, DeviceSummaries
from qversions.qubit import Qubit
from qversions.gate import Gate

q = DeviceSummaries(engine)

def test_get():
    q.create_device(name1, desc)
    expected = DeviceSummary(name1, desc, list(), dict())
    assert q.get_device(name1) == expected

def test_save_qubit():
    q.create_device(name1, desc)
    q.save_qubit(qubit0)
    q.save_qubit(qubit1)
    expected = DeviceSummary(name1, desc, [qubit0, qubit1], dict())
    assert q.get_device(name1) == expected
    assert q.get_device(name1).get_qubit(0) == qubit0

def test_save_gate():
    q.create_device(name1, desc)
    q.save_qubit(qubit0)
    q.save_qubit(qubit1)
    q.save_gate(gate1X)
    q.save_gate(gate1Y)
    q.save_gate(gate0X)
    expected = DeviceSummary(name1, desc, [qubit0, qubit1], {
            0: set([gate0X]),
            1: set([gate1X, gate1Y])
        })
    assert q.get_device(name1) == expected
    assert q.get_device(name1).get_gates_by_qubit(1) == set([gate1X, gate1Y])
    q.qubits.delete_qubit(name1, 0)
    expected = DeviceSummary(name1, desc, [qubit1], {
            1: set([gate1X, gate1Y])
        })
    assert q.get_device(name1) == expected
    assert q.get_device(name1).get_gates_by_qubit(0) == None
    with pytest.raises(RuntimeError):
        q.save_gate(gate0X)
