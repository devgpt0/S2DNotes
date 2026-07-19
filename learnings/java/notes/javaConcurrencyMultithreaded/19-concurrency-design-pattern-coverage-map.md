# 19 - Concurrency Design Pattern Coverage Map

This map groups the major Java concurrency patterns by the problem they solve. Several names describe the same underlying structure.

## Thread Safety and State Ownership

- Single Threaded Execution / Mutex: one thread at a time enters a critical section; see [synchronization](04-synchronization-and-monitors.md).
- Monitor Object: an object owns protected state and synchronized operations; see [synchronization](04-synchronization-and-monitors.md).
- Immutable Object: share values without synchronization; see [thread-safe design](06-thread-safety-immutability-and-confinement.md).
- Thread Confinement: mutable state belongs to one task or thread; see [thread-safe design](06-thread-safety-immutability-and-confinement.md).
- Thread-Specific Storage: associate context with one thread; see [thread-local pattern](15-read-write-copy-on-write-cache-and-thread-local.md).
- Read-Write Lock: concurrent reads and exclusive writes; see [read/write pattern](15-read-write-copy-on-write-cache-and-thread-local.md).
- Copy-on-Write: publish immutable snapshots after each write; see [copy-on-write pattern](15-read-write-copy-on-write-cache-and-thread-local.md).
- Lock Striping / Partitioning: protect independent keys with independent lanes or locks; see [keyed serial execution](11-worker-thread-thread-per-task-and-serial-executor.md).
- Optimistic Concurrency / CAS: retry an atomic state transition when the expected value changes; see [atomics](05-locks-atomics-and-synchronizers.md).
- Lazy Initialization Holder: rely on class initialization for safe publication; see [initialization](12-guarded-suspension-balking-and-termination.md).

## Task Creation and Execution

- Thread-Per-Task / Thread-Per-Message: give each independent blocking task its own virtual thread; see [virtual threads](09-virtual-threads.md).
- Worker Thread / Thread Pool: fixed workers pull tasks from a queue; see [worker pattern](11-worker-thread-thread-per-task-and-serial-executor.md).
- Serial Executor: order operations and confine state to one executor; see [serial pattern](11-worker-thread-thread-per-task-and-serial-executor.md).
- Active Object: queue method requests behind an asynchronous object boundary; see [Active Object](14-active-object-event-loop-and-reactive-streams.md).
- Future / Promise: represent a result that will complete later; see [CompletableFuture](08-future-and-completable-future.md).
- Scheduler: execute tasks after a delay or on a cadence; see [resilience and scheduling](16-timeout-retry-backpressure-bulkhead-and-rate-limit.md).
- Leader-Followers: one pool member receives an event and promotes the next leader; see [worker patterns](11-worker-thread-thread-per-task-and-serial-executor.md).

## Handoff and Coordination

- Producer-Consumer / Bounded Buffer: hand off work through a capacity-limited queue; see [producer-consumer](10-producer-consumer-and-bounded-buffer.md).
- Guarded Suspension: wait until a protected condition is true; see [guarded suspension](12-guarded-suspension-balking-and-termination.md).
- Balking: reject or skip an operation when its state precondition is false; see [balking](12-guarded-suspension-balking-and-termination.md).
- Two-Phase Termination: request shutdown, then clean up cooperatively; see [termination](12-guarded-suspension-balking-and-termination.md).
- Latch, Barrier, Phaser, and Semaphore: coordinate phases or permits; see [synchronizers](05-locks-atomics-and-synchronizers.md).
- Poison Pill: place a shutdown sentinel in a work queue; see [producer-consumer](10-producer-consumer-and-bounded-buffer.md).

## Parallel Decomposition

- Pipeline: connect bounded transformation stages; see [pipeline](13-pipeline-fanout-fanin-and-forkjoin.md).
- Fan-Out/Fan-In or Scatter-Gather: run independent branches and combine their results; see [fan-out/fan-in](13-pipeline-fanout-fanin-and-forkjoin.md).
- Master-Worker: a coordinator distributes independent tasks to workers; see [worker and fan-out patterns](11-worker-thread-thread-per-task-and-serial-executor.md).
- Divide-and-Conquer / Fork-Join / Work Stealing: recursively split CPU work; see [fork/join](13-pipeline-fanout-fanin-and-forkjoin.md).
- Map-Reduce: transform independent inputs and reduce associatively; see [map-reduce](13-pipeline-fanout-fanin-and-forkjoin.md).

## Event-Driven and Asynchronous I/O

- Event Loop: serialize callbacks on an event-owned thread; see [event loop](14-active-object-event-loop-and-reactive-streams.md).
- Reactor: dispatch handlers when channels become ready; see [reactor and proactor](14-active-object-event-loop-and-reactive-streams.md).
- Proactor: dispatch completion handlers after asynchronous operations finish; see [reactor and proactor](14-active-object-event-loop-and-reactive-streams.md).
- Reactive Streams: exchange data according to downstream demand; see [Flow API](14-active-object-event-loop-and-reactive-streams.md).

## Resilience and Overload Control

- Timeout / Deadline: bound total waiting time.
- Retry with Backoff and Jitter: repeat safe transient failures within a deadline.
- Backpressure: slow or reject producers when consumers cannot keep up.
- Bulkhead: isolate concurrency capacity by dependency or workload.
- Rate Limiter: bound accepted work over time.
- Circuit Breaker: stop calls to a persistently failing dependency and probe recovery.

All resilience patterns are covered in [timeouts, retries, and flow control](16-timeout-retry-backpressure-bulkhead-and-rate-limit.md).

## Selection Rule

Prefer the Java library abstraction that directly expresses the required guarantee. Custom low-level concurrency protocols require formal invariants, cancellation behavior, stress testing, operational metrics, and strong evidence that a standard utility is insufficient.
