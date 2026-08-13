# Timeouts, Retries, and Backpressure

## 1. Bound every wait

A timeout limits how long the caller waits for an operation. It does not prove
that underlying remote, thread, or process work has stopped.

```python
import asyncio


async def slow_operation() -> str:
    await asyncio.sleep(1)
    return "done"


async def main() -> None:
    try:
        async with asyncio.timeout(0.01):
            await slow_operation()
    except TimeoutError:
        print("timed out")


asyncio.run(main())
```

Output:

```text
timed out
```

Use the dependency's own connection, read, write, and pool-acquisition timeouts
when available; an outer deadline alone may leave resources occupied.

## 2. Propagate a deadline across calls

Independent full timeouts let nested work exceed the request budget. Compute a
monotonic deadline once and pass the remaining budget to each boundary.

Never use wall-clock timestamps for elapsed-time decisions because system time
can move.

## 3. Retry only transient, safe operations

A retry repeats the operation. Restrict it by exception, attempt count, total
deadline, and idempotency.

```python
def fetch_with_retry() -> str:
    outcomes = iter([ConnectionError("temporary"), "ok"])

    for attempt in range(1, 4):
        outcome = next(outcomes)
        if isinstance(outcome, ConnectionError):
            print(f"attempt {attempt} failed")
            continue
        return outcome

    raise RuntimeError("retry budget exhausted")


print(fetch_with_retry())
```

Output:

```text
attempt 1 failed
ok
```

The example is deterministic and omits sleeping. Production retries normally
use capped exponential backoff with jitter to avoid synchronized retry storms.

## 4. Idempotency prevents duplicated effects

An idempotent operation has the same intended effect when repeated with the
same key. Payments, messages, and order creation need an idempotency design
before automatic retry.

```python
processed: dict[str, str] = {}


def create_order(key: str) -> str:
    if key not in processed:
        processed[key] = f"ORDER-{len(processed) + 1}"
    return processed[key]


print(create_order("request-7"))
print(create_order("request-7"))
```

Output:

```text
ORDER-1
ORDER-1
```

Real idempotency storage must use an atomic database or service operation; the
in-memory teaching example is not safe across workers.

## 5. Backpressure bounds admitted work

Backpressure slows or rejects producers when consumers are saturated. Use
bounded queues, semaphores, rate limits, or explicit rejection.

```python
import asyncio


async def main() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue(maxsize=1)
    await queue.put("first")

    try:
        queue.put_nowait("second")
    except asyncio.QueueFull:
        print("queue full")

    print(await queue.get())
    queue.task_done()


asyncio.run(main())
```

Output:

```text
queue full
first
```

An unbounded queue converts overload into memory growth and extreme latency.

## 6. Limit active concurrency

A semaphore bounds work already admitted for execution; a queue bounds work
waiting to execute. Many systems need both.

Keep the limit in configuration with a strictly validated positive integer.
Choose it from dependency capacity and measurements, not an arbitrary large
number.

## 7. Avoid retry amplification

If every service layer retries three times, one request can multiply into many
downstream calls. Assign retry ownership to one layer, keep a total deadline,
and expose attempt and rejection metrics.

Do not retry:

- validation or authentication failures;
- deterministic business-rule failures;
- permanent not-found results unless the contract says they are transient;
- non-idempotent effects without an idempotency mechanism.

## 8. Reliability decision table

| Failure | Control |
| --- | --- |
| operation may wait forever | timeout or deadline |
| transient dependency failure | bounded conditional retry |
| producer outruns consumer | bounded queue and rejection |
| too many active calls | semaphore or worker limit |
| repeated dependency failure | circuit breaker after measurement and clear policy |
| duplicate side effect | idempotency key and atomic storage |

## 9. Mental model

```text
admission bound -> execution bound -> deadline -> selective retry -> observable result
```
