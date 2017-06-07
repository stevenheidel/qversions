from base_test import *
import pytest
from qversions.gate import Gate, Gates

gates = Gates(engine)

def test_save():
    gates.save_gate(gate0X)
    assert gates.get_gate(name1, 0, "+X") == gate0X

def test_update():
    initial_timestamp = gates.save_gate(gate0X)
    gate0X.amplitude = -1.0
    update_timestamp = gates.save_gate(gate0X)
    assert gates.get_gate(name1, 0, "+X").amplitude == -1.0
    assert gates.get_gate(name1, 0, "+X", update_timestamp).amplitude == 0.0
    assert gates.get_gate(name1, 0, "+X", initial_timestamp) == None

def test_get_gates_by_qubit():
    gate_on_different_device = Gate(name2, 0, "+X", amplitude=5.0, width=5.0, phase=5.0)
    save_gates([gate1X, gate1Y, gate0X, gate_on_different_device])
    assert set(gates.get_gates_by_qubit(name1, 1)) == set([gate1X, gate1Y])
    delete_timestamp = gates.delete_gate(name1, 1, "+X")
    assert set(gates.get_gates_by_qubit(name1, 1)) == set([gate1Y])
    assert set(gates.get_gates_by_qubit(name1, 1, delete_timestamp)) == set([gate1X, gate1Y])

def test_get_gates_by_device():
    gate_on_different_device = Gate(name2, 0, "+X", amplitude=5.0, width=5.0, phase=5.0)
    save_gates([gate1X, gate1Y, gate0X, gate_on_different_device])
    assert set(gates.get_gates_by_device(name1)) == set([gate1X, gate1Y, gate0X])
    delete_timestamp = gates.delete_gate(name1, 0, "+X")
    assert set(gates.get_gates_by_device(name1)) == set([gate1X, gate1Y])
    assert set(gates.get_gates_by_device(name1, delete_timestamp)) == set([gate1X, gate1Y, gate0X])

def test_delete_gate_nonexistent():
    with pytest.raises(RuntimeError):
        gates.delete_gate(name1, 1, "+X")

def save_gates(gate_list):
    for gate in gate_list:
        gates.save_gate(gate)
