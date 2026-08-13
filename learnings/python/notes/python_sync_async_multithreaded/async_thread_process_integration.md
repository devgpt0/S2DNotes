# Integrating Async, Threads, and Processes

## 1. Keep one orchestration model

Use the event loop as the owner in an async application. Cross into a thread
only for blocking I/O and into a process only for substantial CPU work.

```text
async owner -> blocking I/O adapter -> thread
            -> CPU adapter          -> process
```

The bridge should be narrow and explicit.

## 2. Call blocking I/O with `asyncio.to_thread()`

`to_thread()` runs a synchronous callable in the event loop's default thread
pool without blocking the loop.

```python
import asyncio


def blocking_double(value: int) -> int:
    return value * 2


async def main() -> None:
    results = await asyncio.gather(
        *(asyncio.to_thread(blocking_double, value) for value in [1, 2, 3])
    )
    print(results)


asyncio.run(main())
```

Output:

```text
[2, 4, 6]
```

The callable must still be thread-safe. Bound callers when the dependency has a
smaller connection or request capacity than the default executor.

## 3. Call CPU work with a process executor

`loop.run_in_executor()` can submit an importable top-level function to an
explicit process pool.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor


def square(value: int) -> int:
    return value * value


async def run(pool: ProcessPoolExecutor) -> None:
    loop = asyncio.get_running_loop()
    results = await asyncio.gather(
        *(loop.run_in_executor(pool, square, value) for value in [1, 2, 3])
    )
    print(results)


def main() -> None:
    with ProcessPoolExecutor(max_workers=2) as pool:
        asyncio.run(run(pool))


if __name__ == "__main__":
    main()
```

Output:

```text
[1, 4, 9]
```

Create and close the pool at the application boundary, not per request.

## 4. Cancellation does not stop executor work

Cancelling the asyncio future stops the async wait. A thread or process function
already running may continue and still consume its resource.

Design blocking adapters with their own timeout and cancellation mechanism when
the underlying library supports one. Otherwise keep work bounded and account
for late completion during shutdown.

## 5. Preserve context deliberately

`asyncio.to_thread()` propagates the current `contextvars.Context`. Process
workers do not share Python memory or live context. Pass only the explicit,
non-sensitive data the worker needs.

Never place passwords, tokens, or unnecessary personal data in work items,
exception strings, or logs.

## 6. Avoid nested pools

An async server with a process pool whose workers create thread pools can
multiply resource use unexpectedly. Count the maximum tasks, threads, processes,
connections, and queued items across the whole path.

Keep one owner for each executor and configure explicit limits.

## 7. Failure and shutdown rules

- Await every submitted future or deliberately record its terminal result.
- Let unexpected executor failures propagate to the request or owning task.
- Stop accepting new work before closing executors.
- Cancel queued async work, then wait according to the shutdown deadline.
- Expect already-running executor calls to outlive an async cancellation.
- Test worker crashes and application shutdown, not only successful results.

## 8. Decision guide

| Boundary | API | Use |
| --- | --- | --- |
| async to blocking I/O | `asyncio.to_thread()` | small synchronous adapter |
| async to explicit thread pool | `run_in_executor(thread_pool, ...)` | owned pool or custom capacity |
| async to CPU work | `run_in_executor(process_pool, ...)` | substantial serializable work |
| async to native code | direct call only if non-blocking or GIL-releasing | measure event-loop impact |

## 9. Mental model

```text
async owner -> explicit bridge -> bounded executor -> awaited result -> owned shutdown
```
