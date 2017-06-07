from ._db import QubitModel
from ._utils import validate_field, validate_param
from contextlib import contextmanager
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import make_transient
from sqlalchemy.sql import func
import time

"""
Module for interacting with Quantum Bits (Qubits).
"""

class Qubit(object):
    def __init__(self, device_id, qubit_id, resonance_frequency, t1, t2):
        self.device_id = device_id
        """Device that this qubit is associated with"""
        self.qubit_id = qubit_id
        """Positive integer uniquely identifying this qubit"""
        self.resonance_frequency = resonance_frequency
        """Resonance frequency in GHz (optional)"""
        self.t1 = t1
        """Coherence time constant 1 in microseconds (optional)"""
        self.t2 = t2
        """Coherence time constant 2 in microseconds (optional)"""

    def __repr__(self):
        return "<Qubit(device_id={}, qubit_id={}, resonance_frequency={}, t1={}, t2={})>"\
                .format(self.device_id, self.qubit_id, self.resonance_frequency,
                        self.t1, self.t2)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(frozenset(self.__dict__.items()))

class Qubits(object):
    def __init__(self, engine):
        self.sessionmaker = sessionmaker(bind=engine)

    def save_qubit(self, qubit):
        """
        Save new parameters for this qubit. Will overwrite any previous data saved
        for this device's qubit with the same qubit id.

        :param Qubit qubit: Qubit to save
        :return: Timestamp of the old qubit version
        :rtype: int
        """
        validate_param("qubit", qubit, Qubit)
        qubit = _validate(qubit)
        with self._session() as session:
            timestamp = _current_timestamp()
            qubit.timestamp = timestamp
            session.add(qubit)
        return timestamp

    def get_qubit(self, device_id, qubit_id, timestamp=None):
        """
        Get a qubit by its id.

        :param string device_id: Device id
        :param int qubit_id: Qubit id
        :param long timestamp: If specified, will return the qubit's measurements
                from that particular time. Otherwise, will return latest info.
        :return: Either a qubit or None if not found or qubit was deleted
        :rtype: Qubit
        """
        validate_param("device_id", device_id, str)
        validate_param("qubit_id", qubit_id, int)

        session = self.sessionmaker()
        return _wrap(self._get_qubit(session, device_id, qubit_id, timestamp))

    def get_qubits_by_device(self, device_id, timestamp=None):
        """
        Find all the qubits that have been saved for a device.

        :param string device_id: Device id
        :param long timestamp: If specified, will return the qubits that existed at
                that particular time. Otherwise, will return latest info.
        :return: List of qubits
        :rtype: list
        """
        validate_param("device_id", device_id, str)

        def query(query_builder):
            query = query_builder.filter_by(device_id=device_id)
            if timestamp:
                return query.filter(QubitModel.timestamp < timestamp)
            return query

        session = self.sessionmaker()
        return _wrap(self._query(session, query).all())

    def delete_qubit(self, device_id, qubit_id):
        """
        Archive a qubit. Will raise exception if qubit does not exist.

        :param string device_id: Device id
        :param int qubit_id: Qubit id
        :return: timestamp of the state before qubit was archived
        :rtype: int
        """
        validate_param("device_id", device_id, str)
        validate_param("qubit_id", qubit_id, int)

        with self._session() as session:
            qubit = self._get_qubit(session, device_id, qubit_id, timestamp=None)
            if qubit is None:
                raise RuntimeError("qubit with device_id {} and qubit_id {} does not exist"\
                        .format(device_id, qubit_id))
            # Don't track any more modifications to qubit
            session.expunge(qubit)
            make_transient(qubit)
            # Create a new entry with a new timestamp that is archived
            timestamp = _current_timestamp()
            qubit.timestamp = timestamp
            qubit.archived = True
            session.add(qubit)
            return timestamp

    def _get_qubit(self, session, device_id, qubit_id, timestamp):
        """
        Return a QubitModel for this point in time
        """
        def query(query_builder):
            query_builder = query_builder\
                    .filter_by(device_id=device_id, qubit_id=qubit_id)

            if timestamp:
                return query_builder.filter(QubitModel.timestamp < timestamp)
            return query_builder

        return self._query(session, query).one_or_none()

    def _query(self, session, f):
        """
        Perform a query on only the latest version of the qubits.
        Takes a method f which adds filter operations to the query.
        """
        # Find the max for each qubit
        query_builder = session.query(QubitModel.device_id, QubitModel.qubit_id,
                func.max(QubitModel.timestamp).label("latest_timestamp"))\
                        .group_by(QubitModel.device_id, QubitModel.qubit_id)
        # Add custom filters
        latest = f(query_builder).subquery()
        # Join with whole table to get original information
        query = session.query(QubitModel).join((latest, and_(
                QubitModel.device_id == latest.c.device_id,
                QubitModel.qubit_id == latest.c.qubit_id,
                QubitModel.timestamp == latest.c.latest_timestamp)))
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

def _validate(qubit):
    """
    Validate the public Qubit API and then convert to internal model.
    """
    validate_field(qubit, "device_id", str)
    validate_field(qubit, "qubit_id", int)
    validate_field(qubit, "resonance_frequency", float)
    validate_field(qubit, "t1", float)
    validate_field(qubit, "t2", float)

    return QubitModel(device_id=qubit.device_id, qubit_id=qubit.qubit_id,
            resonance_frequency=qubit.resonance_frequency, t1=qubit.t1,
            t2=qubit.t2)

def _wrap(model):
    """
    Converts the internal model into the public qubit API. Also filters out
    archived and None qubits.
    """
    if model is None:
        return None
    elif isinstance(model, list):
        return list(filter(lambda q: q is not None, map(_wrap, model)))
    elif model.archived:
        return None
    else:
        return Qubit(device_id=model.device_id, qubit_id=model.qubit_id,
                resonance_frequency = model.resonance_frequency, t1=model.t1,
                t2=model.t2)
