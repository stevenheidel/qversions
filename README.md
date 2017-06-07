# QVersion - Versioned quantum device calibration and performance parameters

## Setup

1. Install sqlalchemy v1.1
2. Open up a `python3` prompt
3. Run `>>> from main import *`

By default uses sqlite in memory, to use a real database modify main.py to either the sample mysql or postgresql strings. You may be required to install drivers such as 'mysqlclient' for mysql or 'psycopg2' for postgresql

## Example session

```
>>> from main import *
>>> from qversions.gate import Gate

# Sample device: qubit 0 has 1 gates, qubit 1 has no gates
>>> q.get_device(sample)
Device id: sample
Description: Sample device
Qubits: [<Qubit(device_id=sample, qubit_id=0, resonance_frequency=0.0, t1=0.0, t2=0.0)>, <Qubit(device_id=sample, qubit_id=1, resonance_frequency=1.0, t1=1.0, t2=1.0)>]
Gates: {0: {<Gate(device_id=sample, qubit_id=0, gate_id=+X, amplitude=0.0, width=0.0, phase=0.0)>}}

# Add new measurements for a gate.
# This returns a version number to restore values before these ones.
>>> prev_version = q.save_gate(Gate(sample, 0, "+X", 7.7, -9.1, 42.42))
>>> q.get_device(sample)
Device id: sample
Description: Sample device
Qubits: [<Qubit(device_id=sample, qubit_id=0, resonance_frequency=0.0, t1=0.0, t2=0.0)>, <Qubit(device_id=sample, qubit_id=1, resonance_frequency=1.0, t1=1.0, t2=1.0)>]
Gates: {0: {<Gate(device_id=sample, qubit_id=0, gate_id=+X, amplitude=7.7, width=-9.1, phase=42.42)>}}

# Get the previous version and recover the original values.
>>> q.get_snapshot(sample, prev_version)
Device id: sample
Description: Sample device
Qubits: [<Qubit(device_id=sample, qubit_id=0, resonance_frequency=0.0, t1=0.0, t2=0.0)>, <Qubit(device_id=sample, qubit_id=1, resonance_frequency=1.0, t1=1.0, t2=1.0)>]
Gates: {0: {<Gate(device_id=sample, qubit_id=0, gate_id=+X, amplitude=0.0, width=0.0, phase=0.0)>}}
```

## Run tests

1. Install pytest v3.1
2. In root dir, run `python3 -m pytest tests`

## Public API

Most interactions will take place with the DeviceSummaries object which returns all the information about a device, its qubits, and its gates.

There's also classes (Devices, Qubits, Gates) to perform less common operations such as deletion.

# QVersion design

## Assumptions

Throughput:
- Should be minimal throughput
- Read-biased, measurements will be updated very infrequently
- Estimating less than 10 QPS (queries per second)

Data size:
- 10-100 devices, bits, gates
- Potentially many versions

Interface:
- Assuming this might eventually get put in front of a REST API or similar

## Special design goals

Primary goal should be to never delete information. These parameters may be difficult to obtain so they should never be accidentally deleted.

Design should be as simple as possible to avoid problems with bugs or any
needed maintenance.

## Design

Devices -> Qubits -> Gates will be associated using compound keys. There's no reason to use auto-generated ids / foreign keys given that the problem has well-defined ids for each entity already. Compound keys also easily extend to a REST API.

Qubits and Gates will use device id in their primary key so that data could be partitioned in the future (assuming a lot of measurements and versions)

No true "delete" operation, will set a tombstone/deleted flag to true instead. That data can be recovered later.

Qubits and Gates will have a timestamp as part of their primary key to allow versions at different points of time to be retrieved.

## Drawbacks

Referential integrity is not enforced at the database layer. Most access will be through the DeviceSummary interface which can check for integrity at that time.

Timestamp as part of the key could mean writes could fail if they happen at the exact same time. This should be very rare though: timestamps are stored in microseconds.
