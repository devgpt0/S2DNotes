# Async Programming in Python: asyncio Fundamentals

## 1. Why Async Exists

Async programming is designed to improve throughput for I/O-heavy workloads.

Core idea:
- do not block while waiting for I/O
- switch to another task during wait time

---

## 2. Key Terms (Must Know for Interviews)

### Coroutine
Function declared with `async def`.  
It returns a coroutine object and runs when awaited/scheduled.

### Event loop
Scheduler that runs coroutines and switches between them.

### Awaitable
Object usable with `await` (coroutine, task, future).

### Task
Coroutine wrapped for concurrent scheduling by event loop.

---

## 3. First Async Example

```python
import asyncio


async def fetch_user():
    print("Fetching user...")
    await asyncio.sleep(2)
    print("User fetched")


async def fetch_orders():
    print("Fetching orders...")
    await asyncio.sleep(2)
    print("Orders fetched")


async def main():
    await fetch_user()
    await fetch_orders()


if __name__ == "__main__":
    asyncio.run(main())
```

This is still sequential because calls are awaited one by one.

---

## 4. True Async Concurrency With `create_task`

```python
import asyncio
import time


async def fetch_user():
    await asyncio.sleep(2)
    return {"id": 1, "name": "Asha"}


async def fetch_orders():
    await asyncio.sleep(2)
    return [{"order_id": 101}, {"order_id": 102}]


async def main():
    start = time.perf_counter()

    user_task = asyncio.create_task(fetch_user())
    orders_task = asyncio.create_task(fetch_orders())

    user = await user_task
    orders = await orders_task

    elapsed = time.perf_counter() - start
    print(user)
    print(orders)
    print(f"Total time: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

Expected output:
```text
{'id': 1, 'name': 'Asha'}
[{'order_id': 101}, {'order_id': 102}]
Total time: 2.00s
```

---

## 5. `await` Rule (Very Important)

`await` pauses current coroutine and gives control back to event loop.

Interview phrasing:
- async is cooperative multitasking
- task switches happen at await points

No `await` means no cooperative yielding.

---

## 6. `asyncio.gather`

`gather` runs awaitables concurrently and returns results in input order.

```python
import asyncio


async def work(name: str, seconds: int):
    await asyncio.sleep(seconds)
    return f"{name} done"


async def main():
    results = await asyncio.gather(
        work("A", 2),
        work("B", 1),
        work("C", 3),
    )
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

Expected output:
```text
['A done', 'B done', 'C done']
```

---

## 7. Exception Behavior in Async

If one awaited task fails, exception propagates like sync code.

```python
import asyncio


async def ok():
    await asyncio.sleep(0.2)
    return "ok"


async def fail():
    await asyncio.sleep(0.1)
    raise RuntimeError("network error")


async def main():
    try:
        await asyncio.gather(ok(), fail())
    except RuntimeError as exc:
        print(f"Caught: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
```

Interview follow-up:
- mention `return_exceptions=True` when collecting errors as values

---

## 8. Timeouts With `asyncio.wait_for`

```python
import asyncio


async def slow_call():
    await asyncio.sleep(3)
    return "done"


async def main():
    try:
        result = await asyncio.wait_for(slow_call(), timeout=1.0)
        print(result)
    except TimeoutError:
        print("Timed out")


if __name__ == "__main__":
    asyncio.run(main())
```

Expected output:
```text
Timed out
```

---

## 9. Important Rule: Never Block Event Loop

Bad:
```python
import time

async def bad():
    time.sleep(2)  # blocks entire event loop
```

Good:
```python
import asyncio

async def good():
    await asyncio.sleep(2)
```

Interview trap:
- `time.sleep` in async code is a common rejection point.

---

## 10. Running Blocking Work in Async Apps

Use `asyncio.to_thread` for blocking sync functions:

```python
import asyncio
import time


def blocking_io():
    time.sleep(2)
    return "file content"


async def main():
    content = await asyncio.to_thread(blocking_io)
    print(content)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 11. Async Interview Pitfalls

1. Calling coroutine without `await` or scheduling task.
2. Mixing blocking I/O inside async functions.
3. Assuming async gives CPU parallelism.
4. Ignoring cancellation and timeout handling.
5. Creating tasks and never awaiting/monitoring them.

---

## 12. When Async Is a Good Fit

Use async when:
- high concurrency
- many network/database calls
- mostly waiting on I/O
- framework is async-native (FastAPI async endpoints, aiohttp, etc.)

Avoid async when:
- mostly CPU-heavy
- team unfamiliar and no real concurrency need

---

## 13. One-Page Summary

- `async def` defines coroutine.
- event loop schedules tasks.
- `await` yields control cooperatively.
- `create_task` and `gather` enable concurrency.
- never block loop with sync sleeps/network calls.

---

## 14. Practice Assignment

Build async product aggregator:
- concurrently call 3 mock APIs (`price`, `inventory`, `reviews`)
- use `asyncio.gather`
- add timeout (`wait_for`)
- if one API fails, return fallback value
- measure total runtime

