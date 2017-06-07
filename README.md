# QVersion - Versioned quantum device calibration and performance parameters

## Setup

1. Install sqlalchemy v1.1

## Run tests

1. Install pytest v3.1
2. In root dir, run `pytest tests`

## Assumptions

Throughput:
- Should be minimal throughput
- Read-biased, measurements will be updated very infrequently
- Estimating less than 10 QPS (queries per second)

Data size:
- 10-100 devices, bits, gates
- Potentially many versions

## Special design goals

Primary goal should be to never delete information. These parameters may be difficult to obtain so they should never be accidentally deleted.

Design should be as simple as possible to avoid problems with bugs or any
needed maintenance.

## Design

Devices -> Qubits -> Gates will be associated using compound keys. There's no reason to use auto-generated ids / foreign keys given that the problem has well-defined ids for each entity already.

Qubits and Gates will use device id in their primary key so that data could be partitioned in the future (assuming a lot of measurements and versions)

No true "delete" operation, will set a tombstone/deleted flag to true instead. That data can be recovered later.

Qubits and Gates will have a timestamp as part of their primary key to allow versions at different points of time to be retrieved.

## Drawbacks

Referential integrity is not enforced at the database layer. Most access will be through the DeviceSummary interface which can check for integrity at that time.

Timestamp as part of the key could mean writes could fail if they happen at the exact same time. This should be very rare though: timestamps are stored in microseconds.
