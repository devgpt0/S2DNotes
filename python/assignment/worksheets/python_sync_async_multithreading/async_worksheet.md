# Worksheet: Async Programming (Interview Level 3-5 Years)

Question mix:
- Print the Output: 20
- MCQ (Single Correct): 40
- MCQ (Multiple Correct): 40
- Total: 100

Coverage map:
- Coroutine, task, awaitable, and event-loop fundamentals
- create_task, gather, timeout, and failure behaviors
- Structured concurrency with TaskGroup
- Cancellation, cleanup, and graceful shutdown
- Semaphore, queue backpressure, and async locks
- Blocking integration via to_thread/run_in_executor
- Debugging, observability, and production pitfalls

---

## Section A: Print the Output (1-20)

1. What will be printed?
```python
import asyncio

async def a():
    print("A:start")
    await asyncio.sleep(0.01)
    print("A:end")

async def b():
    print("B:start")
    await asyncio.sleep(0.01)
    print("B:end")

async def main():
    await a()
    await b()

asyncio.run(main())
```

2. Predict the output.
```python
import asyncio

async def work(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    t1 = asyncio.create_task(work("A", 0.02))
    t2 = asyncio.create_task(work("B", 0.01))
    print(await t1, await t2)

asyncio.run(main())
```

3. What is printed?
```python
import asyncio

async def work(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    res = await asyncio.gather(
        work("X", 0.03),
        work("Y", 0.01),
        work("Z", 0.02),
    )
    print(res)

asyncio.run(main())
```

4. Predict the output.
```python
import asyncio

async def ok():
    await asyncio.sleep(0.01)
    return "ok"

async def bad():
    await asyncio.sleep(0.01)
    raise RuntimeError("boom")

async def main():
    try:
        await asyncio.gather(ok(), bad())
    except RuntimeError as exc:
        print(f"caught:{exc}")

asyncio.run(main())
```

5. What will be printed?
```python
import asyncio

async def ok():
    return "ok"

async def bad():
    raise ValueError("x")

async def main():
    res = await asyncio.gather(ok(), bad(), return_exceptions=True)
    print(res[0], isinstance(res[1], ValueError))

asyncio.run(main())
```

6. Predict the output.
```python
import asyncio

async def slow():
    await asyncio.sleep(0.1)
    return "done"

async def main():
    try:
        print(await asyncio.wait_for(slow(), timeout=0.01))
    except TimeoutError:
        print("timed-out")

asyncio.run(main())
```

7. What is printed?
```python
import asyncio

async def slow():
    await asyncio.sleep(0.1)
    return "done"

async def main():
    try:
        async with asyncio.timeout(0.01):
            print(await slow())
    except TimeoutError:
        print("timeout-context")

asyncio.run(main())
```

8. Predict the output.
```python
import asyncio
import time

def blocking():
    time.sleep(0.01)
    return "file"

async def main():
    print(await asyncio.to_thread(blocking))

asyncio.run(main())
```

9. What will be printed?
```python
import asyncio

async def main():
    loop = asyncio.get_running_loop()
    fut = loop.run_in_executor(None, lambda: 6 * 7)
    print(await fut)

asyncio.run(main())
```

10. Predict cancellation output.
```python
import asyncio

async def long_job():
    try:
        while True:
            await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        print("cleanup")
        raise

async def main():
    task = asyncio.create_task(long_job())
    await asyncio.sleep(0.03)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled")

asyncio.run(main())
```

11. What is printed?
```python
import asyncio

async def worker(name, delay):
    await asyncio.sleep(delay)
    print(name)

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker("A", 0.02))
        tg.create_task(worker("B", 0.01))
    print("group-done")

asyncio.run(main())
```

12. Predict semaphore result.
```python
import asyncio

active = 0
max_active = 0
sem = asyncio.Semaphore(2)

async def worker():
    global active, max_active
    async with sem:
        active += 1
        max_active = max(max_active, active)
        await asyncio.sleep(0.01)
        active -= 1

async def main():
    await asyncio.gather(*(worker() for _ in range(6)))
    print(max_active)

asyncio.run(main())
```

13. What will be printed?
```python
import asyncio

async def producer(q):
    for i in range(3):
        await q.put(i)
    await q.put(None)

async def consumer(q, out):
    while True:
        item = await q.get()
        if item is None:
            q.task_done()
            break
        out.append(item * 10)
        q.task_done()

async def main():
    q = asyncio.Queue(maxsize=1)
    out = []
    p = asyncio.create_task(producer(q))
    c = asyncio.create_task(consumer(q, out))
    await p
    await q.join()
    await c
    print(out)

asyncio.run(main())
```

14. Predict lock-protected counter output.
```python
import asyncio

counter = 0
lock = asyncio.Lock()

async def inc():
    global counter
    for _ in range(100):
        async with lock:
            counter += 1
        await asyncio.sleep(0)

async def main():
    await asyncio.gather(inc(), inc(), inc())
    print(counter)

asyncio.run(main())
```

15. What is printed with shield?
```python
import asyncio

async def commit():
    await asyncio.sleep(0.05)
    return "committed"

async def main():
    task = asyncio.create_task(commit())
    try:
        async with asyncio.timeout(0.01):
            await asyncio.shield(task)
    except TimeoutError:
        print("caller-timeout")
    print(await task)

asyncio.run(main())
```

16. Predict the output.
```python
import asyncio

async def sample():
    return 5

obj = sample()
print(type(obj).__name__)
obj.close()
```

17. What will be printed?
```python
import asyncio

async def work():
    await asyncio.sleep(0.01)
    return 9

async def main():
    task = asyncio.create_task(work(), name="fetch-9")
    print(task.get_name())
    print(await task)

asyncio.run(main())
```

18. Predict the output.
```python
import asyncio

async def main():
    print("start")
    await asyncio.sleep(0)
    print("end")

asyncio.run(main())
```

19. What is printed?
```python
import asyncio

async def call(delay):
    await asyncio.sleep(delay)
    return "ok"

async def main():
    try:
        async with asyncio.timeout(0.01):
            print(await call(0.02))
    except TimeoutError:
        print("fallback")

asyncio.run(main())
```

20. Predict queue size outputs.
```python
import asyncio

async def main():
    q = asyncio.Queue(maxsize=2)
    await q.put("a")
    await q.put("b")
    print(q.qsize())
    print(await q.get())
    print(q.qsize())

asyncio.run(main())
```

---

## Section B: MCQ (Single Correct) (21-60)

21. Which statement is correct about coroutines and awaitables?
- A. Async automatically makes CPU-heavy loops scale across cores.
- B. Using await is optional when calling coroutines from async code.
- C. A coroutine is created by calling an async function, and it runs when awaited or scheduled.
- D. time.sleep is recommended in coroutines for better precision.

22. Which statement is correct about event loop scheduling?
- A. The event loop schedules coroutines, tasks, callbacks, and I/O readiness.
- B. Cancellation can be ignored safely in production services.
- C. TaskGroup is mainly for running OS threads.
- D. time.sleep is recommended in coroutines for better precision.

23. Which statement is correct about create_task and gather behavior?
- A. Cancellation can be ignored safely in production services.
- B. await yields control cooperatively to the event loop.
- C. gather always returns results in completion order.
- D. Semaphores control queue size only and not active concurrency.

24. Which statement is correct about timeouts and failure handling?
- A. create_task schedules coroutine execution concurrently and returns a Task handle.
- B. Backpressure is unnecessary when downstream service is overloaded.
- C. Async code never needs locks because it is single-threaded.
- D. Semaphores control queue size only and not active concurrency.

25. Which statement is correct about event-loop blocking risks?
- A. Async code never needs locks because it is single-threaded.
- B. shield should be wrapped around every await by default.
- C. Timeouts are less important in async because event loop keeps running.
- D. gather collects results in input order.

26. Which statement is correct about structured concurrency with TaskGroup?
- A. return_exceptions=True allows gather to return exceptions as values.
- B. to_thread converts blocking libraries into native async libraries.
- C. Timeouts are less important in async because event loop keeps running.
- D. return_exceptions=True causes gather to crash immediately on first error.

27. Which statement is correct about cancellation semantics?
- A. wait_for can enforce per-operation timeouts.
- B. to_thread converts blocking libraries into native async libraries.
- C. Event loop can continue normally even if a coroutine calls time.sleep.
- D. Orphan tasks are harmless in production.

28. Which statement is correct about semaphore and backpressure controls?
- A. asyncio.timeout context is a modern timeout pattern.
- B. Orphan tasks are harmless in production.
- C. Retries should be infinite in async systems.
- D. Observability is optional for debugging async incidents.

29. Which statement is correct about async queues and pipelines?
- A. Task naming makes no practical difference.
- B. Async code review should ignore cancellation paths.
- C. Retries should be infinite in async systems.
- D. Blocking calls in coroutine code can stall unrelated async tasks.

30. Which statement is correct about async lock and shared state?
- A. run_in_executor cannot be awaited.
- B. Async code review should ignore cancellation paths.
- C. Structured concurrency is slower and always unnecessary.
- D. time.sleep inside async code blocks the event loop thread.

31. Which statement is correct about shield usage?
- A. Structured concurrency is slower and always unnecessary.
- B. Timeout contexts should never be used with external APIs.
- C. Async queue maxsize has no effect on producers.
- D. asyncio.sleep is the cooperative non-blocking sleep primitive.

32. Which statement is correct about blocking-library integration?
- A. Timeout contexts should never be used with external APIs.
- B. Graceful shutdown means cancelling everything without cleanup.
- C. If code works once, async failure handling is complete.
- D. asyncio.to_thread helps integrate blocking sync code.

33. Which statement is correct about debugging and observability?
- A. Graceful shutdown means cancelling everything without cleanup.
- B. Async gather cannot run multiple awaitables concurrently.
- C. run_in_executor is another bridge for blocking work.
- D. Await points are unrelated to cooperative task switching.

34. Which statement is correct about interview tradeoff reasoning?
- A. TaskGroup provides structured concurrency and scoped child lifecycle.
- B. Blocking DB drivers should run directly in event loop.
- C. Async is always better than sync regardless of workload.
- D. Async gather cannot run multiple awaitables concurrently.

35. Which statement is correct about production reliability patterns?
- A. Cancellation raises CancelledError at await points.
- B. Semaphores are only useful for CPU parallelism.
- C. Async automatically makes CPU-heavy loops scale across cores.
- D. Async is always better than sync regardless of workload.

36. Which statement is correct about coroutines and awaitables?
- A. time.sleep is recommended in coroutines for better precision.
- B. Async automatically makes CPU-heavy loops scale across cores.
- C. Using await is optional when calling coroutines from async code.
- D. Cleanup on cancellation should be explicit for reliability.

37. Which statement is correct about event loop scheduling?
- A. time.sleep is recommended in coroutines for better precision.
- B. TaskGroup is mainly for running OS threads.
- C. Cancellation can be ignored safely in production services.
- D. Semaphores cap in-flight concurrency against downstream services.

38. Which statement is correct about create_task and gather behavior?
- A. Cancellation can be ignored safely in production services.
- B. Bounded queues provide backpressure to producers.
- C. gather always returns results in completion order.
- D. Semaphores control queue size only and not active concurrency.

39. Which statement is correct about timeouts and failure handling?
- A. Semaphores control queue size only and not active concurrency.
- B. Async locks can protect shared mutable state across await points.
- C. Backpressure is unnecessary when downstream service is overloaded.
- D. Async code never needs locks because it is single-threaded.

40. Which statement is correct about event-loop blocking risks?
- A. Async code never needs locks because it is single-threaded.
- B. shield can prevent outer cancellation from cancelling inner critical operation.
- C. shield should be wrapped around every await by default.
- D. Timeouts are less important in async because event loop keeps running.

41. Which statement is correct about structured concurrency with TaskGroup?
- A. Timeouts are less important in async because event loop keeps running.
- B. Overusing shield can make cancellation semantics harder to reason about.
- C. return_exceptions=True causes gather to crash immediately on first error.
- D. to_thread converts blocking libraries into native async libraries.

42. Which statement is correct about cancellation semantics?
- A. Event loop can continue normally even if a coroutine calls time.sleep.
- B. to_thread converts blocking libraries into native async libraries.
- C. Orphan tasks are harmless in production.
- D. Async is strongest for high-concurrency I/O-bound workloads.

43. Which statement is correct about semaphore and backpressure controls?
- A. Retries should be infinite in async systems.
- B. Observability is optional for debugging async incidents.
- C. Orphan tasks are harmless in production.
- D. Async is not automatic CPU parallelism.

44. Which statement is correct about async queues and pipelines?
- A. Async code review should ignore cancellation paths.
- B. Retries should be infinite in async systems.
- C. Task supervision is important to avoid orphaned fire-and-forget tasks.
- D. Task naming makes no practical difference.

45. Which statement is correct about async lock and shared state?
- A. Async code review should ignore cancellation paths.
- B. run_in_executor cannot be awaited.
- C. Structured concurrency is slower and always unnecessary.
- D. Timeout + retry + concurrency limit is a common production trio.

46. Which statement is correct about shield usage?
- A. Task naming can improve observability during debugging.
- B. Structured concurrency is slower and always unnecessary.
- C. Timeout contexts should never be used with external APIs.
- D. Async queue maxsize has no effect on producers.

47. Which statement is correct about blocking-library integration?
- A. PYTHONASYNCIODEBUG can help spot async misuse.
- B. If code works once, async failure handling is complete.
- C. Graceful shutdown means cancelling everything without cleanup.
- D. Timeout contexts should never be used with external APIs.

48. Which statement is correct about debugging and observability?
- A. Async gather cannot run multiple awaitables concurrently.
- B. Graceful shutdown means cancelling everything without cleanup.
- C. Await points are unrelated to cooperative task switching.
- D. Missing await or missing task supervision is a common async code review issue.

49. Which statement is correct about interview tradeoff reasoning?
- A. Async is always better than sync regardless of workload.
- B. Blocking DB drivers should run directly in event loop.
- C. Async queue producer-consumer pipelines can smooth bursty workloads.
- D. Async gather cannot run multiple awaitables concurrently.

50. Which statement is correct about production reliability patterns?
- A. Backpressure mechanisms prevent uncontrolled fan-out.
- B. Async is always better than sync regardless of workload.
- C. Async automatically makes CPU-heavy loops scale across cores.
- D. Semaphores are only useful for CPU parallelism.

51. Which statement is correct about coroutines and awaitables?
- A. time.sleep is recommended in coroutines for better precision.
- B. Graceful async shutdown should await pending task cleanup.
- C. Async automatically makes CPU-heavy loops scale across cores.
- D. Using await is optional when calling coroutines from async code.

52. Which statement is correct about event loop scheduling?
- A. Structured concurrency improves lifecycle clarity compared to loose tasks.
- B. Cancellation can be ignored safely in production services.
- C. time.sleep is recommended in coroutines for better precision.
- D. TaskGroup is mainly for running OS threads.

53. Which statement is correct about create_task and gather behavior?
- A. Cancellation can be ignored safely in production services.
- B. Semaphores control queue size only and not active concurrency.
- C. gather always returns results in completion order.
- D. One stuck blocking call in event loop can hurt whole service latency.

54. Which statement is correct about timeouts and failure handling?
- A. Async code never needs locks because it is single-threaded.
- B. Async design interviews expect failure-propagation reasoning, not only syntax.
- C. Backpressure is unnecessary when downstream service is overloaded.
- D. Semaphores control queue size only and not active concurrency.

55. Which statement is correct about event-loop blocking risks?
- A. Cancellation behavior should be tested, not assumed.
- B. Async code never needs locks because it is single-threaded.
- C. shield should be wrapped around every await by default.
- D. Timeouts are less important in async because event loop keeps running.

56. Which statement is correct about structured concurrency with TaskGroup?
- A. return_exceptions=True causes gather to crash immediately on first error.
- B. to_thread converts blocking libraries into native async libraries.
- C. Semaphore limits in-flight concurrency, not total queue size.
- D. Timeouts are less important in async because event loop keeps running.

57. Which statement is correct about cancellation semantics?
- A. Gather and TaskGroup solve different lifecycle needs.
- B. to_thread converts blocking libraries into native async libraries.
- C. Event loop can continue normally even if a coroutine calls time.sleep.
- D. Orphan tasks are harmless in production.

58. Which statement is correct about semaphore and backpressure controls?
- A. Orphan tasks are harmless in production.
- B. Retries should be infinite in async systems.
- C. Observability is optional for debugging async incidents.
- D. Using async without real concurrency needs can increase complexity.

59. Which statement is correct about async queues and pipelines?
- A. Async code review should ignore cancellation paths.
- B. Retries should be infinite in async systems.
- C. Task naming makes no practical difference.
- D. Retries in async workflows should still be bounded with backoff/jitter.

60. Which statement is correct about async lock and shared state?
- A. run_in_executor cannot be awaited.
- B. Async systems benefit from queue depth, latency, and timeout metrics.
- C. Async code review should ignore cancellation paths.
- D. Structured concurrency is slower and always unnecessary.

---

## Section C: MCQ (Multiple Correct) (61-100)

61. Select all correct statements about coroutines and awaitables.
Select all that apply.
- A. The event loop schedules coroutines, tasks, callbacks, and I/O readiness.
- B. Using await is optional when calling coroutines from async code.
- C. Async automatically makes CPU-heavy loops scale across cores.
- D. A coroutine is created by calling an async function, and it runs when awaited or scheduled.

62. Select all correct statements about event loop scheduling.
Select all that apply.
- A. TaskGroup is mainly for running OS threads.
- B. await yields control cooperatively to the event loop.
- C. create_task schedules coroutine execution concurrently and returns a Task handle.
- D. time.sleep is recommended in coroutines for better precision.

63. Select all correct statements about create_task and gather behavior.
Select all that apply.
- A. gather always returns results in completion order.
- B. return_exceptions=True allows gather to return exceptions as values.
- C. Cancellation can be ignored safely in production services.
- D. gather collects results in input order.

64. Select all correct statements about timeouts and failure handling.
Select all that apply.
- A. Semaphores control queue size only and not active concurrency.
- B. Backpressure is unnecessary when downstream service is overloaded.
- C. wait_for can enforce per-operation timeouts.
- D. asyncio.timeout context is a modern timeout pattern.

65. Select all correct statements about event-loop blocking risks.
Select all that apply.
- A. shield should be wrapped around every await by default.
- B. Async code never needs locks because it is single-threaded.
- C. time.sleep inside async code blocks the event loop thread.
- D. Blocking calls in coroutine code can stall unrelated async tasks.

66. Select all correct statements about structured concurrency with TaskGroup.
Select all that apply.
- A. Timeouts are less important in async because event loop keeps running.
- B. asyncio.sleep is the cooperative non-blocking sleep primitive.
- C. asyncio.to_thread helps integrate blocking sync code.
- D. return_exceptions=True causes gather to crash immediately on first error.

67. Select all correct statements about cancellation semantics.
Select all that apply.
- A. run_in_executor is another bridge for blocking work.
- B. TaskGroup provides structured concurrency and scoped child lifecycle.
- C. to_thread converts blocking libraries into native async libraries.
- D. Event loop can continue normally even if a coroutine calls time.sleep.

68. Select all correct statements about semaphore and backpressure controls.
Select all that apply.
- A. Observability is optional for debugging async incidents.
- B. Cleanup on cancellation should be explicit for reliability.
- C. Orphan tasks are harmless in production.
- D. Cancellation raises CancelledError at await points.

69. Select all correct statements about async queues and pipelines.
Select all that apply.
- A. Retries should be infinite in async systems.
- B. Semaphores cap in-flight concurrency against downstream services.
- C. Task naming makes no practical difference.
- D. Bounded queues provide backpressure to producers.

70. Select all correct statements about async lock and shared state.
Select all that apply.
- A. Async code review should ignore cancellation paths.
- B. run_in_executor cannot be awaited.
- C. Async locks can protect shared mutable state across await points.
- D. shield can prevent outer cancellation from cancelling inner critical operation.

71. Select all correct statements about shield usage.
Select all that apply.
- A. Structured concurrency is slower and always unnecessary.
- B. Async is strongest for high-concurrency I/O-bound workloads.
- C. Async queue maxsize has no effect on producers.
- D. Overusing shield can make cancellation semantics harder to reason about.

72. Select all correct statements about blocking-library integration.
Select all that apply.
- A. Task supervision is important to avoid orphaned fire-and-forget tasks.
- B. If code works once, async failure handling is complete.
- C. Timeout contexts should never be used with external APIs.
- D. Async is not automatic CPU parallelism.

73. Select all correct statements about debugging and observability.
Select all that apply.
- A. Timeout + retry + concurrency limit is a common production trio.
- B. Await points are unrelated to cooperative task switching.
- C. Task naming can improve observability during debugging.
- D. Graceful shutdown means cancelling everything without cleanup.

74. Select all correct statements about interview tradeoff reasoning.
Select all that apply.
- A. Blocking DB drivers should run directly in event loop.
- B. PYTHONASYNCIODEBUG can help spot async misuse.
- C. Async gather cannot run multiple awaitables concurrently.
- D. Missing await or missing task supervision is a common async code review issue.

75. Select all correct statements about production reliability patterns.
Select all that apply.
- A. Semaphores are only useful for CPU parallelism.
- B. Async is always better than sync regardless of workload.
- C. Backpressure mechanisms prevent uncontrolled fan-out.
- D. Async queue producer-consumer pipelines can smooth bursty workloads.

76. Select all correct statements about coroutines and awaitables.
Select all that apply.
- A. Graceful async shutdown should await pending task cleanup.
- B. Using await is optional when calling coroutines from async code.
- C. Async automatically makes CPU-heavy loops scale across cores.
- D. Structured concurrency improves lifecycle clarity compared to loose tasks.

77. Select all correct statements about event loop scheduling.
Select all that apply.
- A. Async design interviews expect failure-propagation reasoning, not only syntax.
- B. One stuck blocking call in event loop can hurt whole service latency.
- C. time.sleep is recommended in coroutines for better precision.
- D. TaskGroup is mainly for running OS threads.

78. Select all correct statements about create_task and gather behavior.
Select all that apply.
- A. Cancellation behavior should be tested, not assumed.
- B. Semaphore limits in-flight concurrency, not total queue size.
- C. Cancellation can be ignored safely in production services.
- D. gather always returns results in completion order.

79. Select all correct statements about timeouts and failure handling.
Select all that apply.
- A. Using async without real concurrency needs can increase complexity.
- B. Semaphores control queue size only and not active concurrency.
- C. Backpressure is unnecessary when downstream service is overloaded.
- D. Gather and TaskGroup solve different lifecycle needs.

80. Select all correct statements about event-loop blocking risks.
Select all that apply.
- A. shield should be wrapped around every await by default.
- B. Async code never needs locks because it is single-threaded.
- C. Retries in async workflows should still be bounded with backoff/jitter.
- D. Async systems benefit from queue depth, latency, and timeout metrics.

81. Select all correct statements about structured concurrency with TaskGroup.
Select all that apply.
- A. Timeouts are less important in async because event loop keeps running.
- B. The event loop schedules coroutines, tasks, callbacks, and I/O readiness.
- C. return_exceptions=True causes gather to crash immediately on first error.
- D. A coroutine is created by calling an async function, and it runs when awaited or scheduled.

82. Select all correct statements about cancellation semantics.
Select all that apply.
- A. await yields control cooperatively to the event loop.
- B. to_thread converts blocking libraries into native async libraries.
- C. Event loop can continue normally even if a coroutine calls time.sleep.
- D. create_task schedules coroutine execution concurrently and returns a Task handle.

83. Select all correct statements about semaphore and backpressure controls.
Select all that apply.
- A. Orphan tasks are harmless in production.
- B. return_exceptions=True allows gather to return exceptions as values.
- C. gather collects results in input order.
- D. Observability is optional for debugging async incidents.

84. Select all correct statements about async queues and pipelines.
Select all that apply.
- A. asyncio.timeout context is a modern timeout pattern.
- B. wait_for can enforce per-operation timeouts.
- C. Task naming makes no practical difference.
- D. Retries should be infinite in async systems.

85. Select all correct statements about async lock and shared state.
Select all that apply.
- A. Async code review should ignore cancellation paths.
- B. time.sleep inside async code blocks the event loop thread.
- C. Blocking calls in coroutine code can stall unrelated async tasks.
- D. run_in_executor cannot be awaited.

86. Select all correct statements about shield usage.
Select all that apply.
- A. asyncio.sleep is the cooperative non-blocking sleep primitive.
- B. Structured concurrency is slower and always unnecessary.
- C. Async queue maxsize has no effect on producers.
- D. asyncio.to_thread helps integrate blocking sync code.

87. Select all correct statements about blocking-library integration.
Select all that apply.
- A. Timeout contexts should never be used with external APIs.
- B. run_in_executor is another bridge for blocking work.
- C. TaskGroup provides structured concurrency and scoped child lifecycle.
- D. If code works once, async failure handling is complete.

88. Select all correct statements about debugging and observability.
Select all that apply.
- A. Cleanup on cancellation should be explicit for reliability.
- B. Graceful shutdown means cancelling everything without cleanup.
- C. Await points are unrelated to cooperative task switching.
- D. Cancellation raises CancelledError at await points.

89. Select all correct statements about interview tradeoff reasoning.
Select all that apply.
- A. Bounded queues provide backpressure to producers.
- B. Semaphores cap in-flight concurrency against downstream services.
- C. Async gather cannot run multiple awaitables concurrently.
- D. Blocking DB drivers should run directly in event loop.

90. Select all correct statements about production reliability patterns.
Select all that apply.
- A. Semaphores are only useful for CPU parallelism.
- B. Async locks can protect shared mutable state across await points.
- C. shield can prevent outer cancellation from cancelling inner critical operation.
- D. Async is always better than sync regardless of workload.

91. Select all correct statements about coroutines and awaitables.
Select all that apply.
- A. Overusing shield can make cancellation semantics harder to reason about.
- B. Async automatically makes CPU-heavy loops scale across cores.
- C. Async is strongest for high-concurrency I/O-bound workloads.
- D. Using await is optional when calling coroutines from async code.

92. Select all correct statements about event loop scheduling.
Select all that apply.
- A. TaskGroup is mainly for running OS threads.
- B. Async is not automatic CPU parallelism.
- C. Task supervision is important to avoid orphaned fire-and-forget tasks.
- D. time.sleep is recommended in coroutines for better precision.

93. Select all correct statements about create_task and gather behavior.
Select all that apply.
- A. gather always returns results in completion order.
- B. Timeout + retry + concurrency limit is a common production trio.
- C. Cancellation can be ignored safely in production services.
- D. Task naming can improve observability during debugging.

94. Select all correct statements about timeouts and failure handling.
Select all that apply.
- A. PYTHONASYNCIODEBUG can help spot async misuse.
- B. Backpressure is unnecessary when downstream service is overloaded.
- C. Missing await or missing task supervision is a common async code review issue.
- D. Semaphores control queue size only and not active concurrency.

95. Select all correct statements about event-loop blocking risks.
Select all that apply.
- A. Async code never needs locks because it is single-threaded.
- B. Async queue producer-consumer pipelines can smooth bursty workloads.
- C. Backpressure mechanisms prevent uncontrolled fan-out.
- D. shield should be wrapped around every await by default.

96. Select all correct statements about structured concurrency with TaskGroup.
Select all that apply.
- A. Graceful async shutdown should await pending task cleanup.
- B. return_exceptions=True causes gather to crash immediately on first error.
- C. Structured concurrency improves lifecycle clarity compared to loose tasks.
- D. Timeouts are less important in async because event loop keeps running.

97. Select all correct statements about cancellation semantics.
Select all that apply.
- A. Async design interviews expect failure-propagation reasoning, not only syntax.
- B. Event loop can continue normally even if a coroutine calls time.sleep.
- C. One stuck blocking call in event loop can hurt whole service latency.
- D. to_thread converts blocking libraries into native async libraries.

98. Select all correct statements about semaphore and backpressure controls.
Select all that apply.
- A. Orphan tasks are harmless in production.
- B. Semaphore limits in-flight concurrency, not total queue size.
- C. Cancellation behavior should be tested, not assumed.
- D. Observability is optional for debugging async incidents.

99. Select all correct statements about async queues and pipelines.
Select all that apply.
- A. Retries should be infinite in async systems.
- B. Task naming makes no practical difference.
- C. Using async without real concurrency needs can increase complexity.
- D. Gather and TaskGroup solve different lifecycle needs.

100. Select all correct statements about async lock and shared state.
Select all that apply.
- A. Retries in async workflows should still be bounded with backoff/jitter.
- B. Async code review should ignore cancellation paths.
- C. Async systems benefit from queue depth, latency, and timeout metrics.
- D. run_in_executor cannot be awaited.
