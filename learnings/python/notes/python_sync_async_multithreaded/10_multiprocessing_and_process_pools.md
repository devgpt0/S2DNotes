# Multiprocessing and Process Pools - Beginner to Expert

Multiprocessing runs work in separate operating-system processes. It provides memory isolation and CPU parallelism at the cost of startup, serialization, coordination, and higher memory use.

## 1. Process Versus Thread

| Property | Process | Thread |
|---|---|---|
| Python runtime | normally separate | shared process runtime |
| memory | isolated by default | shared objects |
| communication | IPC/serialization/shared memory | queues, locks, shared objects |
| startup | heavier | lighter |
| failure isolation | stronger, not complete | one process failure domain |
| CPU-bound Python | parallel across processes | limited by GIL on traditional builds |

Use processes for sufficiently large independent CPU tasks, isolation, or native-library constraints. Do not use them automatically for small work.

## 2. First Process

Save as `first_process.py`:

```python
from multiprocessing import Process, current_process


def teach(topic: str) -> None:
    print(f"{current_process().name}: {topic}")


def main() -> None:
    process = Process(target=teach, args=("multiprocessing",))
    process.start()
    process.join()

    if process.exitcode != 0:
        raise RuntimeError(f"child failed with exit code {process.exitcode}")


if __name__ == "__main__":
    main()
```

Example output:

```text
Process-1: multiprocessing
```

The main guard prevents spawn-based children from starting the complete program again while importing the main module.

## 3. Start Methods

Python supports platform-dependent start methods:

- `spawn`: starts a fresh interpreter and imports required code;
- `fork`: child begins from a copy-on-write snapshot of the parent process on supported POSIX systems;
- `forkserver`: a server process forks children on supported POSIX systems.

Use an explicit context when behavior must be consistent:

```python
import multiprocessing as mp


def square(value: int) -> int:
    return value * value


def main() -> None:
    context = mp.get_context("spawn")
    process = context.Process(target=square, args=(4,))
    process.start()
    process.join()


if __name__ == "__main__":
    main()
```

Do not change the global start method in an imported library. Accept or create a context at the application boundary.

Forking a multi-threaded parent can inherit locks and native-library state in unsafe conditions. Follow the current platform/runtime guidance and test the exact deployment environment.

## 4. Process Pool for CPU Work

Save as `pool_example.py`:

```python
from concurrent.futures import ProcessPoolExecutor


def square(value: int) -> int:
    return value * value


def main() -> None:
    values = [1, 2, 3, 4]
    with ProcessPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(square, values))

    print(results)


if __name__ == "__main__":
    main()
```

Output:

```text
[1, 4, 9, 16]
```

`map` preserves input order even if tasks finish in another order.

## 5. Pickle Boundary

Process-pool tasks, arguments, and results normally cross a serialization boundary.

Prefer:

- top-level importable worker functions;
- small immutable arguments;
- small explicit results;
- stable versioned message shapes.

Avoid assuming these are portable pool tasks:

- lambdas;
- nested functions and closures;
- open files, sockets, locks, and database connections;
- objects tied to one process;
- huge object graphs sent for every task.

Never unpickle data from an untrusted source. Pickle can execute arbitrary code during loading.

## 6. Submit and Observe Failures

```python
from concurrent.futures import ProcessPoolExecutor, as_completed


def reciprocal(value: int) -> float:
    if value == 0:
        raise ValueError("value must not be zero")
    return 1 / value


def main() -> None:
    with ProcessPoolExecutor(max_workers=2) as executor:
        futures = {
            executor.submit(reciprocal, value): value
            for value in [2, 0, 4]
        }

        for future in as_completed(futures):
            value = futures[future]
            try:
                print(value, future.result())
            except ValueError as error:
                print(value, type(error).__name__)


if __name__ == "__main__":
    main()
```

Possible output order:

```text
2 0.5
0 ValueError
4 0.25
```

Calling `result()` re-raises the worker exception in the parent. Always observe submitted futures.

## 7. Broken Worker Process

If a worker exits abruptly, pending work can raise `BrokenProcessPool`. Treat this differently from a normal domain exception:

- stop accepting dependent work;
- report the operational failure;
- decide whether the complete operation must fail;
- rebuild the pool only under an explicit bounded recovery policy;
- investigate native crashes, out-of-memory kills, or forced termination.

Do not retry forever on a repeatedly crashing input.

## 8. Task Granularity and `chunksize`

Tiny tasks can spend more time serializing and scheduling than computing.

```python
from concurrent.futures import ProcessPoolExecutor


def transform(value: int) -> int:
    return value * value


def main() -> None:
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(transform, range(10_000), chunksize=100))

    print(len(results))


if __name__ == "__main__":
    main()
```

Output:

```text
10000
```

Larger chunks reduce scheduling overhead but can worsen load balance and cancellation responsiveness. Benchmark representative task distributions.

## 9. Worker Count

Start from CPU availability for CPU-heavy tasks, then measure. Fewer workers may be better when:

- each task uses large memory;
- native libraries create their own threads;
- the container has a smaller CPU quota than the host;
- tasks compete for disk, memory bandwidth, or a database;
- serialization becomes the bottleneck.

Avoid multiplying process workers by native-library thread pools accidentally.

## 10. Initializer

Initialize process-local read-only resources once per worker:

```python
from concurrent.futures import ProcessPoolExecutor

lookup: tuple[int, ...] = ()


def initialize_worker() -> None:
    global lookup
    lookup = tuple(range(100))


def lookup_value(index: int) -> int:
    return lookup[index]


def main() -> None:
    with ProcessPoolExecutor(
        max_workers=2,
        initializer=initialize_worker,
    ) as executor:
        print(list(executor.map(lookup_value, [1, 2, 3])))


if __name__ == "__main__":
    main()
```

Output:

```text
[1, 2, 3]
```

If initialization fails, the pool becomes unusable. Do not initialize inherited network connections and assume they are safe in each child; create process-owned connections according to the client library's contract.

## 11. Queues for Explicit Processes

```python
import multiprocessing as mp
from dataclasses import dataclass
from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


class ReadQueue(Protocol[T_co]):
    def get(self) -> T_co: ...


class WriteQueue(Protocol[T_contra]):
    def put(self, value: T_contra) -> None: ...


@dataclass(frozen=True, slots=True)
class Job:
    value: int


def worker(
    jobs: ReadQueue[Job | None],
    results: WriteQueue[int],
) -> None:
    while True:
        job = jobs.get()
        if job is None:
            return
        results.put(job.value * job.value)


def main() -> None:
    context = mp.get_context("spawn")
    jobs = context.Queue()
    results = context.Queue()
    process = context.Process(target=worker, args=(jobs, results))
    process.start()

    jobs.put(Job(6))
    jobs.put(Job(7))
    jobs.put(None)

    print(results.get())
    print(results.get())

    process.join()
    if process.exitcode != 0:
        raise RuntimeError(f"worker failed with exit code {process.exitcode}")


if __name__ == "__main__":
    main()
```

Output:

```text
36
49
```

For production, bound queue sizes and define how the producer reacts when the queue is full. A sentinel must be sent once per consumer.

The worker depends on the two queue operations it consumes instead of a concrete multiprocessing implementation. Static stub support for `multiprocessing.Queue` varies by checker and version.

## 12. Pipes

A pipe is useful for a direct point-to-point connection. Clearly assign which endpoint each process owns and which direction messages travel. Close unused endpoints so end-of-stream detection works.

Queues are usually simpler for multiple producers or consumers.

## 13. Shared Memory

Shared memory avoids serializing a large byte/numeric buffer, but synchronization and lifetime become your responsibility.

```python
from multiprocessing import shared_memory

memory = shared_memory.SharedMemory(create=True, size=4)
try:
    memory.buf[:] = b"data"
    print(bytes(memory.buf))
finally:
    memory.close()
    memory.unlink()
```

Output:

```text
b'data'
```

- `close()` releases this process's handle;
- `unlink()` requests destruction of the shared segment;
- other processes need a safe way to receive its name, shape, dtype, and ownership contract;
- concurrent writes require synchronization.

Use higher-level data transfer unless profiling proves serialization is the bottleneck.

## 14. Manager Proxies

A `multiprocessing.Manager` exposes proxy objects managed by a server process. Operations involve IPC and are not equivalent to local list/dict access.

Use a manager for small coordination state when simplicity matters more than throughput. Prefer queues or partitioned ownership for high-volume work.

## 15. Cancellation and Timeouts

```python
from concurrent.futures import ProcessPoolExecutor, TimeoutError
from time import sleep


def slow_square(value: int) -> int:
    sleep(0.05)
    return value * value


def main() -> None:
    with ProcessPoolExecutor(max_workers=1) as executor:
        future = executor.submit(slow_square, 6)
        try:
            print(future.result(timeout=0.001))
        except TimeoutError:
            print("timed out waiting")


if __name__ == "__main__":
    main()
```

Output:

```text
timed out waiting
```

A timeout stops the parent from waiting; it does not automatically stop running process work. `Future.cancel()` normally cancels only work that has not started.

For cooperative cancellation, split work into bounded chunks and check process-safe cancellation state between chunks. Forced process termination can leave files, locks, shared memory, and transactions inconsistent.

## 16. Shutdown

`with ProcessPoolExecutor(...)` calls shutdown and waits for submitted work by default.

A service shutdown policy should define:

1. stop accepting new tasks;
2. cancel tasks that have not started when appropriate;
3. wait for running tasks up to a deadline;
4. terminate only under an explicit force policy;
5. close queues/pipes and release shared memory;
6. report incomplete work and non-zero failure.

## 17. Recycling Workers

Long-lived workers that call native libraries can accumulate fragmented memory or process-local state. A configured maximum tasks per child can recycle workers in supported APIs and Python versions.

Recycling is a containment tool, not a substitute for fixing a leak. Measure startup cost and verify compatibility with the selected start method.

## 18. Testing Multiprocessing Code

- keep worker logic in an ordinary directly testable function;
- integration-test process wiring under the deployment start method;
- use small deterministic inputs;
- set timeouts so tests cannot hang forever;
- verify exception propagation and non-zero child exits;
- verify queues and shared memory are cleaned up;
- run platform CI because process behavior differs;
- avoid asserting completion order unless the API guarantees it.

## 19. Security

- never unpickle untrusted messages;
- validate paths and command arguments in workers;
- do not pass secrets unless the worker genuinely needs them;
- apply least privilege to every process;
- parameterize database queries;
- bound payload size, result size, and queue depth;
- avoid shell command construction from job data.

Process isolation is not a security sandbox by itself.

## 20. Decision Guide

Use multiprocessing when:

- tasks are CPU-heavy and large enough to amortize overhead;
- tasks can be partitioned with compact inputs/results;
- process isolation is useful;
- dependencies are safe in child processes.

Avoid or reconsider when:

- work is primarily I/O waiting;
- each task is tiny;
- a huge object graph must cross for every task;
- memory is severely constrained;
- native code already uses all available cores;
- deployment forbids child processes.

## Final Rules

- protect the entry point with the main guard;
- choose and test a start method deliberately;
- keep worker functions importable and inputs compact;
- observe every future and child exit code;
- benchmark task granularity, chunks, and worker count;
- prefer message passing and partitioned ownership;
- use shared memory only with explicit lifetime and synchronization;
- understand that waiting timeout is not execution cancellation;
- design bounded shutdown and cleanup;
- never treat pickle or processes as a security boundary.
