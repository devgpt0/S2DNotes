# Concurrency Design Patterns

## 1. Producer-consumer

Producers create work; consumers own processing. A bounded queue defines the
handoff and provides backpressure.

```python
import asyncio


async def producer(queue: asyncio.Queue[int | None]) -> None:
    for value in [3, 1, 2]:
        await queue.put(value)
    await queue.put(None)


async def consumer(
    queue: asyncio.Queue[int | None], results: list[int]
) -> None:
    while True:
        value = await queue.get()
        try:
            if value is None:
                return
            results.append(value * value)
        finally:
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=2)
    results: list[int] = []

    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue, results))
    await producer_task
    await queue.join()
    await consumer_task

    print(results)


asyncio.run(main())
```

Output:

```text
[9, 1, 4]
```

One sentinel stops one consumer. With multiple consumers, send one sentinel per
consumer or use an explicit cancellation and shutdown protocol.

## 2. Worker pool

A worker pool caps active concurrency and reuses workers. It does not bound
submitted work unless admission is separately limited.

```python
from concurrent.futures import ThreadPoolExecutor


def normalize(value: str) -> str:
    return value.strip().lower()


with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(normalize, [" A ", " B ", " C "]))

print(results)
```

Output:

```text
['a', 'b', 'c']
```

Use a thread pool for blocking I/O. Use a process pool for sufficiently large
CPU-bound Python work.

## 3. Fan-out and fan-in

Fan-out starts independent operations; fan-in combines their results. Structured
concurrency keeps child tasks owned by one scope.

```python
import asyncio


async def double(value: int) -> int:
    await asyncio.sleep(0)
    return value * 2


async def main() -> None:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(double(value)) for value in [1, 2, 3]]

    print([task.result() for task in tasks])


asyncio.run(main())
```

Output:

```text
[2, 4, 6]
```

`TaskGroup` waits for all children and groups concurrent failures. Retain task
handles when results are needed in a defined order.

## 4. Pipeline

A pipeline assigns each stage one transformation. Separate queues let stages
run concurrently but add buffering, failure propagation, and shutdown work.

Use a normal function chain when stages do not benefit from overlap.

```python
def parse(raw: str) -> int:
    return int(raw)


def transform(value: int) -> int:
    return value * 10


def run_pipeline(raw_values: list[str]) -> list[int]:
    return [transform(parse(raw)) for raw in raw_values]


print(run_pipeline(["1", "2", "3"]))
```

Output:

```text
[10, 20, 30]
```

This synchronous pipeline is the correct baseline before adding concurrent
queues.

## 5. Ownership and shutdown

Every pattern must define:

- who creates and closes workers;
- who owns queued work and results;
- how the first failure affects siblings;
- how cancellation crosses each boundary;
- whether queued work is drained, rejected, or discarded on shutdown;
- which bounds prevent overload.

## 6. Decision guide

| Need | Pattern |
| --- | --- |
| decouple production and consumption | producer-consumer |
| cap reusable executors | worker pool |
| run independent subtasks then combine | fan-out/fan-in |
| transform through meaningful stages | pipeline |
| no demonstrated overlap or capacity need | synchronous loop |

## 7. Mental model

```text
owner -> bounded admission -> bounded workers -> result/error -> deterministic shutdown
```
