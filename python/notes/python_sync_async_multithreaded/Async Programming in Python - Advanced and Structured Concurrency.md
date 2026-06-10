# Async Programming in Python: Advanced and Structured Concurrency

## 1. What "Advanced Async" Means

At interview level, async knowledge is not just syntax.  
You must explain:
- cancellation
- failure propagation
- resource limits
- backpressure
- graceful shutdown

---

## 2. Structured Concurrency With `TaskGroup` (Python 3.11+)

`TaskGroup` keeps child task lifetime tied to parent scope.

```python
import asyncio


async def worker(name: str, delay: float):
    await asyncio.sleep(delay)
    print(f"{name} completed")


async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker("A", 1.0))
        tg.create_task(worker("B", 0.5))
        tg.create_task(worker("C", 1.5))


if __name__ == "__main__":
    asyncio.run(main())
```

Why interviewers like it:
- no orphan tasks
- clearer lifecycle
- safer error propagation than loose `create_task` usage

---

## 3. Cancellation Basics

Cancellation raises `asyncio.CancelledError` at await points.

```python
import asyncio


async def long_job():
    try:
        while True:
            print("working...")
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        print("cleanup before exit")
        raise


async def main():
    task = asyncio.create_task(long_job())
    await asyncio.sleep(1.2)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("task cancelled")


if __name__ == "__main__":
    asyncio.run(main())
```

Interview expected answer:
- always release resources on cancellation
- re-raise `CancelledError` unless you intentionally transform flow

---

## 4. Timeout Contexts

Python 3.11+:
```python
import asyncio


async def maybe_slow():
    await asyncio.sleep(2)
    return "ok"


async def main():
    try:
        async with asyncio.timeout(1.0):
            print(await maybe_slow())
    except TimeoutError:
        print("operation timed out")


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. Concurrency Limiting With `Semaphore`

Avoid flooding APIs/databases.

```python
import asyncio
import random

semaphore = asyncio.Semaphore(3)


async def fetch(item_id: int):
    async with semaphore:
        delay = random.uniform(0.3, 1.0)
        await asyncio.sleep(delay)
        return f"item-{item_id}"


async def main():
    tasks = [fetch(i) for i in range(1, 11)]
    results = await asyncio.gather(*tasks)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

Interview line:
- semaphore controls in-flight concurrency, not queue size.

---

## 6. Producer-Consumer With `asyncio.Queue`

```python
import asyncio


async def producer(queue: asyncio.Queue):
    for i in range(5):
        await queue.put(i)
    await queue.put(None)  # sentinel


async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        print(f"processed {item}")
        queue.task_done()


async def main():
    queue = asyncio.Queue(maxsize=2)
    p = asyncio.create_task(producer(queue))
    c = asyncio.create_task(consumer(queue))
    await asyncio.gather(p)
    await queue.join()
    await c


if __name__ == "__main__":
    asyncio.run(main())
```

Important interview point:
- `maxsize` applies backpressure to producer.

---

## 7. Async Locks for Shared Mutable State

Even single-threaded async code can have logical races between await points.

```python
import asyncio

counter = 0
lock = asyncio.Lock()


async def increment_many():
    global counter
    for _ in range(1000):
        async with lock:
            counter += 1
        await asyncio.sleep(0)


async def main():
    await asyncio.gather(increment_many(), increment_many(), increment_many())
    print(counter)


if __name__ == "__main__":
    asyncio.run(main())
```

Without lock, output may be inconsistent with expected value.

---

## 8. `asyncio.shield` (Advanced)

Use shield when outer cancellation should not cancel critical inner operation.

```python
import asyncio


async def commit():
    await asyncio.sleep(1)
    return "committed"


async def main():
    task = asyncio.create_task(commit())
    try:
        async with asyncio.timeout(0.2):
            await asyncio.shield(task)
    except TimeoutError:
        print("caller timed out")
    print(await task)


if __name__ == "__main__":
    asyncio.run(main())
```

Use carefully. Overuse makes cancellation behavior confusing.

---

## 9. Integrating Blocking Libraries

If library has no async support:
- run in thread with `asyncio.to_thread`
- or `loop.run_in_executor`

Interview tradeoff:
- easier migration
- but still uses threads for that part

---

## 10. Common Production Pitfalls

1. Fire-and-forget tasks without supervision.
2. Infinite retries with no jitter/backoff.
3. Missing cancellation handling in long loops.
4. No concurrency cap against external APIs.
5. Closing app without waiting task cleanup.

---

## 11. Debugging Async

Useful techniques:
- enable debug mode (`PYTHONASYNCIODEBUG=1`)
- task naming (`asyncio.create_task(coro, name="fetch-42")`)
- structured logs with request id/task id
- inspect pending tasks on shutdown

---

## 12. Async Design Checklist (Interview Gold)

1. What is max concurrency?
2. What is timeout per remote dependency?
3. What retries are allowed?
4. How do cancellations propagate?
5. How do we guarantee cleanup?
6. What metrics prove this improved throughput?

---

## 13. One-Page Summary

- Use `TaskGroup` for structured task lifecycle.
- Handle cancellation explicitly.
- Enforce timeouts and semaphore limits.
- Use queues for backpressure.
- Protect critical shared state with async locks.

---

## 14. Practice Assignment

Build async crawling pipeline:
- producer: enqueue URLs
- workers: fetch/process (mock with sleep)
- queue with `maxsize`
- semaphore limit 5 outbound requests
- timeout each fetch
- cancellation-safe shutdown on keyboard interrupt

