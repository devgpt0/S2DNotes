# Multithreading in Python: Advanced and ThreadPoolExecutor

## 1. Why Advanced Threading Matters

Interviews at mid/senior level focus on:
- safe concurrency design
- deadlock avoidance
- correct shutdown and failure handling
- choosing `ThreadPoolExecutor` over manual thread management

---

## 2. `ThreadPoolExecutor` Basics

`ThreadPoolExecutor` manages reusable worker threads.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time


def fetch(item_id: int) -> str:
    time.sleep(1)
    return f"item-{item_id}"


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(fetch, i) for i in range(1, 7)]
        for future in as_completed(futures):
            print(future.result())


if __name__ == "__main__":
    main()
```

---

## 3. `submit` vs `map`

`submit`:
- returns `Future` per task
- flexible per-task control

`map`:
- simple batch mapping
- preserves input order in output iteration

Use `submit` when you need timeouts, selective cancellation, or custom error handling.

---

## 4. Understanding `Future`

`Future` represents result of async execution in thread pool.

Key methods:
- `result(timeout=...)`
- `exception()`
- `done()`
- `cancel()`

Interview point:
- cancellation succeeds only if task has not started.

---

## 5. Error Handling Pattern With Futures

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import random


def risky_task(i: int) -> int:
    if random.random() < 0.3:
        raise ValueError(f"task {i} failed")
    return i * 10


def main():
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = [pool.submit(risky_task, i) for i in range(10)]
        for f in as_completed(futures):
            try:
                print(f.result())
            except ValueError as exc:
                print(f"Handled error: {exc}")


if __name__ == "__main__":
    main()
```

---

## 6. Deadlock Patterns and Avoidance

### Deadlock causes
1. Thread A holds lock1 waiting for lock2.
2. Thread B holds lock2 waiting for lock1.

### Prevention checklist
1. Use consistent lock acquisition order.
2. Keep critical sections short.
3. Avoid nested locks when possible.
4. Prefer queue/message passing.

---

## 7. `RLock`, `Event`, `Condition`, `Semaphore`

### `RLock`
Re-entrant lock, same thread can acquire multiple times.

### `Event`
One thread signals others (`set`, `clear`, `wait`).

### `Condition`
Wait/notify with lock coordination.

### `Semaphore`
Limit concurrent access to finite resource pool.

---

## 8. `Event` Example

```python
import threading
import time

ready = threading.Event()


def worker():
    print("Worker waiting for signal...")
    ready.wait()
    print("Worker started after signal")


t = threading.Thread(target=worker)
t.start()
time.sleep(1)
ready.set()
t.join()
```

---

## 9. Bounded Resource Access With `Semaphore`

```python
import threading
import time

pool = threading.Semaphore(2)


def use_db_connection(name: str):
    with pool:
        print(f"{name} acquired connection")
        time.sleep(1)
        print(f"{name} released connection")


threads = [threading.Thread(target=use_db_connection, args=(f"T{i}",)) for i in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

Only 2 threads run inside critical resource at same time.

---

## 10. Graceful Shutdown Pattern

For long-running worker threads:
- use stop signal (`Event` or sentinel in queue)
- avoid abrupt termination
- flush pending work if required

```python
import queue
import threading

STOP = object()


def worker(q: queue.Queue):
    for item in iter(q.get, STOP):
        print(f"processed {item}")
        q.task_done()
    q.task_done()


q = queue.Queue()
t = threading.Thread(target=worker, args=(q,))
t.start()
for i in range(3):
    q.put(i)
q.put(STOP)
q.join()
t.join()
```

---

## 11. Mixing Async and Thread Pool

Common production pattern:
- async web app
- offload blocking library calls to thread pool

Example:
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time


def blocking_call(x: int) -> int:
    time.sleep(1)
    return x * x


async def main():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor(max_workers=4) as pool:
        tasks = [loop.run_in_executor(pool, blocking_call, i) for i in range(5)]
        results = await asyncio.gather(*tasks)
        print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 12. Observability for Threaded Systems

Add:
- thread names (`threading.current_thread().name`)
- request/job ids in logs
- queue depth metrics
- task success/failure counts

Interview point:
- concurrency bugs are often observability bugs first.

---

## 13. Advanced Interview Questions

1. How do you detect and prevent deadlocks?
2. Why prefer thread pool over creating thread per task?
3. How do you cancel or time out thread work?
4. How would you design graceful shutdown?
5. How do you bound concurrency against external dependencies?

---

## 14. One-Page Summary

- `ThreadPoolExecutor` is preferred for many short I/O tasks.
- `Future` gives result/error control.
- Use synchronization primitives intentionally.
- Deadlock prevention is mostly design discipline.
- Shutdown and observability are first-class requirements.

---

## 15. Practice Assignment

Build threaded file ingestion service:
- use `ThreadPoolExecutor(max_workers=8)`
- submit parse tasks per file
- add per-task timeout handling
- collect failures and retry once
- expose summary counts: processed/failed/retried

