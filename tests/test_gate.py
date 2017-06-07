from base_test import *
import pytest
from qversions.gate import Gate, Gates

gates = Gates(engine)

def test_save():
    gate = Gate("test-device-1", 0, "+X", amplitude=0.5, width=1.5, phase=2.5)
    gates.save_gate(gate)
    assert gates.get_gate("test-device-1", 0, "+X") == gate

def test_update():
    gate = Gate("test-device-1", 0, "+X", amplitude=1.0)
    initial_timestamp = gates.save_gate(gate)
    gate.amplitude = 2.0
    update_timestamp = gates.save_gate(gate)
    assert gates.get_gate("test-device-1", 0, "+X").amplitude == 2.0
    assert gates.get_gate("test-device-1", 0, "+X", update_timestamp).amplitude == 1.0
    assert gates.get_gate("test-device-1", 0, "+X", initial_timestamp) == None

def test_get_gates_by_qubit():
    gate1 = Gate("test-device-1", 0, "+X", amplitude=1.0)
    gate2 = Gate("test-device-1", 0, "-Y/2", width=1.0)
    gate_on_different_qubit = Gate("test-device-1", 1, "+X", amplitude=1.0)
    gate_on_different_device = Gate("test-device-2", 0, "+X", width=1.0)
    gates.save_gate(gate1)
    gates.save_gate(gate2)
    gates.save_gate(gate_on_different_qubit)
    gates.save_gate(gate_on_different_device)
    assert set(gates.get_gates_by_qubit("test-device-1", 0)) == set([gate1, gate2])
    delete_timestamp = gates.delete_gate("test-device-1", 0, "+X")
    assert set(gates.get_gates_by_qubit("test-device-1", 0)) == set([gate2])
    assert set(gates.get_gates_by_qubit("test-device-1", 0, delete_timestamp)) == set([gate1, gate2])

def test_get_gates_by_device():
    gate1 = Gate("test-device-1", 0, "+X", amplitude=1.0)
    gate2 = Gate("test-device-1", 0, "-Y/2", width=1.0)
    gate3 = Gate("test-device-1", 1, "+X", amplitude=1.0)
    gate_on_different_device = Gate("test-device-2", 0, "+X", width=1.0)
    gates.save_gate(gate1)
    gates.save_gate(gate2)
    gates.save_gate(gate3)
    gates.save_gate(gate_on_different_device)
    assert set(gates.get_gates_by_device("test-device-1")) == set([gate1, gate2, gate3])
    delete_timestamp = gates.delete_gate("test-device-1", 0, "+X")
    assert set(gates.get_gates_by_device("test-device-1")) == set([gate2, gate3])
    assert set(gates.get_gates_by_device("test-device-1", delete_timestamp)) == set([gate1, gate2, gate3])

def test_delete_gate_nonexistent():
    with pytest.raises(RuntimeError):
        gates.delete_gate("test-device-1", 1, "+X")
