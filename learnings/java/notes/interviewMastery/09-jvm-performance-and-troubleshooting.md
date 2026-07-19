 # 09 - JVM Performance and Troubleshooting Interviews

## Evidence Sources

- metrics: rate, errors, latency percentiles, saturation
- logs: structured events with correlation
- traces: distributed critical path
- JFR: CPU, allocation, locks, I/O, GC, virtual-thread events
- thread dump: blocking, deadlock, pool starvation
- heap dump: retained objects and GC roots
- GC logs: allocation, live set, pauses, promotion
- database plans and pool metrics

## Scenario: High CPU

Confirm process/container CPU, profile hot methods, distinguish application loop from GC/JIT/serialization/regex, reproduce safely, fix algorithm or work, and compare before/after under the same load.

## Scenario: Growing Heap

Determine whether live set grows after full collections. Capture a heap dump, inspect dominators and GC-root paths, identify owner and missing eviction/release, then verify retention stabilizes.

## Scenario: Latency with Low CPU

Inspect thread states, connection pools, downstream latency, lock waits, queue depth, DNS/TLS, and timeouts. Low CPU often means waiting, not spare application capacity.

## Scenario: Database Pool Exhaustion

Look for slow queries, leaked/long transactions, remote calls inside transactions, excess concurrency, incorrect pool sizing, and missing deadlines. Increasing the pool may overload the database.

## Performance Answer Rule

Never propose tuning before naming the metric, evidence, bottleneck hypothesis, experiment, safety limit, and success criterion.
