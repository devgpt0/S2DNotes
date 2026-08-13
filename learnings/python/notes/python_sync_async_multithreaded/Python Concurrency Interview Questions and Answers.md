# Python Concurrency Interview Questions and Answers

## 1. Fundamentals

### Q1. What is the difference between concurrency and parallelism?
Concurrency is about handling many tasks in overlapping time.
Parallelism is about executing tasks at the same instant on multiple cores.

### Q2. Is async parallel?
Not by default. Async is usually concurrent on one thread with cooperative scheduling.

### Q3. Is multithreading parallel in Python?
On default CPython builds, GIL limits Python-bytecode parallel execution.
On free-threaded CPython builds (3.13+, improved/supported in 3.14), threads can run Python code in parallel.
For I/O waiting, threading improves throughput in both cases.

### Q4. What is a blocking call?
A call that prevents current thread/event loop progress until it finishes.

### Q5. What does `await` do?
It pauses current coroutine and returns control to event loop until awaited object is ready.

---

## 2. Asyncio Core Questions

### Q6. Difference between coroutine and task?
Coroutine is an awaitable function result.
Task is a scheduled wrapper around coroutine managed by event loop.

### Q7. `asyncio.create_task` vs direct `await`?
`await` runs and waits immediately.
`create_task` schedules work concurrently and returns task handle.

### Q8. What is event loop?
Core scheduler running async tasks, callbacks, and I/O events.

### Q9. Why is `time.sleep` bad in async code?
It blocks event loop thread and stops all other tasks.

### Q10. How do you enforce timeout in async?
Use `asyncio.wait_for` or `asyncio.timeout`.

### Q11. What is `asyncio.gather`?
Runs multiple awaitables concurrently and collects results in input order.

### Q12. How does cancellation work?
`task.cancel()` requests cancellation; `CancelledError` is raised at await points.

### Q13. Why use `TaskGroup`?
Structured concurrency: child task lifecycle and error propagation are scoped and safer.

### Q14. How do you limit async concurrency?
Use `asyncio.Semaphore` and bounded queues.

### Q15. Can async improve CPU-heavy work?
Not significantly by itself; CPU-heavy tasks need multiprocessing/native optimizations.

---

## 3. Threading Questions

### Q16. What is GIL?
Global Interpreter Lock in CPython that allows one thread at a time to execute Python bytecode (in GIL-enabled builds).

### Q16A. Did Python 3.14 remove GIL completely?
No. Python 3.14 improved and officially supported free-threaded CPython, but the normal/default build still uses the GIL.

### Q17. When are threads useful in Python?
Always useful for I/O-bound tasks and integration with blocking libraries.
On free-threaded builds, they can also be useful for CPU-bound workloads.

### Q18. What is race condition?
Incorrect behavior caused by uncontrolled shared-state access timing.

### Q19. How to prevent race conditions?
Locks, immutable data, queue-based message passing, or ownership boundaries.

### Q20. Difference between `Lock` and `RLock`?
`RLock` allows same thread to acquire lock multiple times; `Lock` does not.

### Q21. What is deadlock?
Two or more threads waiting forever on each other's held resources.

### Q22. How to avoid deadlocks?
Consistent lock order, short critical sections, fewer nested locks, queue-based designs.

### Q23. Thread vs process?
Thread: shared memory, lower overhead.
Process: separate memory, higher overhead, true CPU parallelism in CPython (including default GIL builds).

### Q24. Why use `ThreadPoolExecutor`?
Simpler lifecycle and bounded reusable workers compared to manual thread creation.

### Q25. What is a `Future`?
Represents ongoing/completed async result with result/error/cancel APIs.

---

## 4. Design and Architecture Questions

### Q26. How do you choose sync vs async vs threads?
Decide by workload (I/O vs CPU), framework constraints, team expertise, and reliability requirements.

### Q27. How to handle mixed async and blocking code?
Offload blocking calls with `asyncio.to_thread` or executors.

### Q28. How to implement graceful shutdown?
Stop accepting new work, signal workers, drain queue, await task/thread completion, close resources.

### Q29. What metrics matter in concurrency systems?
Latency percentiles, throughput, queue depth, timeout rate, retry rate, error rate.

### Q30. How do retries affect system stability?
Unbounded retries can amplify outages. Use capped retries with backoff and jitter.

### Q31. What is backpressure?
Mechanism to slow producers when consumers or downstream systems are overloaded.

### Q32. How do you enforce backpressure?
Bounded queue size, semaphores, rate limits, reject/slowdown strategy.

### Q33. Where should timeout be configured?
At all unstable boundaries: outbound HTTP, DB, cache, message broker operations.

### Q34. Why not share too much mutable state across threads?
It increases coupling and race/deadlock risk; debugging becomes difficult.

### Q35. What is structured concurrency in one sentence?
Child concurrent tasks must finish or fail within the parent's scope and lifecycle.

---

## 5. Code Review and Debugging Questions

### Q36. Common red flags in async code review?
Blocking calls in coroutine, un-awaited tasks, missing cancellation handling, no timeout.

### Q37. Common red flags in threaded code review?
Unsafe shared globals, no lock strategy, inconsistent lock order, no shutdown signal.

### Q38. How to debug "task was destroyed but pending"?
Track created tasks, await them on shutdown, or use `TaskGroup` for managed lifetime.

### Q39. Why can a lock hurt performance?
Long lock hold times serialize work and increase contention.

### Q40. How to improve thread pool performance safely?
Profile first, size workers by workload and external limits, reduce blocking critical sections.

---

## 6. Rapid Fire (One-Liners)

1. Async is best for many waiting operations.
2. In default CPython, threads mainly help I/O; in free-threaded CPython they can also scale CPU work.
3. Multiprocessing gives CPU parallelism.
4. Use timeout everywhere external dependency is called.
5. Bounded queues and semaphores protect downstream systems.
6. `TaskGroup` improves async reliability and readability.
7. Prefer message passing over shared mutable state.
8. Correctness before optimization.

---

## 8. Final Revision Checklist

Before interview, make sure you can:
1. Explain GIL and free-threaded CPython distinction in simple words.
2. Write `asyncio.gather` and timeout examples from memory.
3. Explain race condition and lock fix clearly.
4. Choose between sync/async/thread/process for scenario questions.
5. Discuss failure handling (timeout, retries, cancellation, shutdown).
