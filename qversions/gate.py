from ._db import GateModel
from ._utils import validate_field, validate_param
from contextlib import contextmanager
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import make_transient
from sqlalchemy.sql import func
import time

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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))

class Gates(object):
    def __init__(self, engine):
        self.sessionmaker = sessionmaker(bind=engine)

    def save_gate(self, gate):
        """
        Save new parameters for this gate. Will overwrite any previous data saved
        for this qubit's gate with the same id.

        :param Gate qubit: Gate to save
        :return: Timestamp of the old gate version
        :rtype: int
        """
        validate_param("gate", gate, Gate)
        gate = _validate(gate)
        with self._session() as session:
            timestamp = _current_timestamp()
            gate.timestamp = timestamp
            session.add(gate)
        return timestamp

    def get_gate(self, device_id, qubit_id, gate_id, timestamp=None):
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
        validate_param("device_id", device_id, str)
        validate_param("qubit_id", qubit_id, int)
        validate_param("gate_id", gate_id, str)

        session = self.sessionmaker()
        return _wrap(self._get_gate(session, device_id, qubit_id, gate_id, timestamp))

    def get_gates_by_qubit(self, device_id, qubit_id, timestamp=None):
        """
        Find all gates that have been saved for a qubit.

        :param string device_id: Device id
        :param int qubit_id: Qubit id
        :return: List of gates
        :rtype: list
        """
        validate_param("device_id", device_id, str)
        validate_param("qubit_id", qubit_id, int)

        def query(query_builder):
            query = query_builder.filter_by(device_id=device_id, qubit_id=qubit_id)
            if timestamp:
                return query.filter(GateModel.timestamp < timestamp)
            return query

        session = self.sessionmaker()
        return _wrap(self._query(session, query).all())

    def get_gates_by_device(self, device_id, timestamp=None):
        """
        Find all gates that have been saved for all qubits on a device.

        :param string device_id: Device id
        :param long timestamp: If specified, will return the gates that existed at
                that particular time. Otherwise, will return latest info.
        :return: List of gates
        :rtype: list
        """
        validate_param("device_id", device_id, str)

        def query(query_builder):
            query = query_builder.filter_by(device_id=device_id)
            if timestamp:
                return query.filter(GateModel.timestamp < timestamp)
            return query

        session = self.sessionmaker()
        return _wrap(self._query(session, query).all())

    def delete_gate(self, device_id, qubit_id, gate_id):
        """
        Archive a gate. Will raise exception if gate does not exist.

        :param string device_id: Device id
        :param int qubit_id: Qubit id
        :param string gate_id: Gate id
        :return: timestamp of the state before gate was archived
        :rtype: int
        """
        validate_param("device_id", device_id, str)
        validate_param("qubit_id", qubit_id, int)
        validate_param("gate_id", gate_id, str)

        with self._session() as session:
            gate = self._get_gate(session, device_id, qubit_id, gate_id, timestamp=None)
            if gate is None:
                raise RuntimeError("gate with device_id {} and qubit_id {} and gate_id {} does not exist"\
                        .format(device_id, qubit_id, gate_id))
            # Don't track any more modifications to gate
            session.expunge(gate)
            make_transient(gate)
            # Create a new entry with a new timestamp that is archived
            timestamp = _current_timestamp()
            gate.timestamp = timestamp
            gate.archived = True
            session.add(gate)
            return timestamp

    def _get_gate(self, session, device_id, qubit_id, gate_id, timestamp):
        """
        Return a GateModel for this point in time.
        """
        def query(query_builder):
            query_builder = query_builder\
                .filter_by(device_id=device_id, qubit_id=qubit_id, gate_id=gate_id)

            if timestamp:
                return query_builder.filter(GateModel.timestamp < timestamp)
            return query_builder

        return self._query(session, query).one_or_none()

    def _query(self, session, f):
        """
        Perform a query on only the latest version of the gates.
        Takes a method f which adds filter operations to the query.
        """
        # Find the max for each gate
        query_builder = session.query(GateModel.device_id, GateModel.qubit_id, GateModel.gate_id,
                func.max(GateModel.timestamp).label("latest_timestamp"))\
                        .group_by(GateModel.device_id, GateModel.qubit_id, GateModel.gate_id)
        # Add custom filters
        latest = f(query_builder).subquery()
        # Join with whole table to get original information
        query = session.query(GateModel).join((latest, and_(
                GateModel.device_id == latest.c.device_id,
                GateModel.qubit_id == latest.c.qubit_id,
                GateModel.gate_id == latest.c.gate_id,
                GateModel.timestamp == latest.c.latest_timestamp)))
        return query

    @contextmanager
    def _session(self):
        session = self.sessionmaker()
        yield session
        session.commit()

def _current_timestamp():
    """
    Return microseconds since epoch.
    """
    return int(time.time() * 1000000)

def _validate(gate):
    """
    Validate the public Gate API and then convert to internal model.
    """
    validate_field(gate, "device_id", str)
    validate_field(gate, "qubit_id", int)
    validate_field(gate, "gate_id", str)
    validate_field(gate, "amplitude", float)
    validate_field(gate, "width", float)
    validate_field(gate, "phase", float)

    return GateModel(device_id=gate.device_id, qubit_id=gate.qubit_id,
            gate_id=gate.gate_id, amplitude=gate.amplitude, width=gate.width,
            phase=gate.phase)

def _wrap(model):
    """
    Converts the internal model into the public gate API. Also filters out
    archived and None gates.
    """
    if model is None:
        return None
    elif isinstance(model, list):
        return list(filter(lambda q: q is not None, map(_wrap, model)))
    elif model.archived:
        return None
    else:
        return Gate(device_id=model.device_id, qubit_id=model.qubit_id,
                gate_id=model.gate_id, amplitude=model.amplitude,
                width=model.width, phase=model.phase)
