# QVersion - Versioned quantum device calibration and performance parameters

## Assumptions

Throughput:
- Should be minimal throughput
- Read-biased
- Estimating less than 10 QPS (queries per second)

Data size:
- 10-100 devices, bits, gates
- Potentially many versions

## Special design goals

Primary goal should be to never delete information. These parameters may be difficult they should never be accidentally deleted.

## Design

Devices -> Qubits -> Gates will be associated using foreign keys

Qubits and Gates will use device id in their primary key so that data could be partitioned in the future (assuming a lot of measurements and versions)

No true "delete" operation, will set a tombstone/deleted flag to true instead. That data can be recovered later.

Qubits and Gates will have a timestamp as part of their primary key to allow versions at different points of time to be retrieved.
