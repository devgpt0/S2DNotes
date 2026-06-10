# Sync vs Async vs Multithreading: Interview Decision Guide

## 1. Why This Comparison Is Asked Often

Interviewers test architecture thinking, not only syntax.

Typical question:
"You need to process many network calls and some CPU-heavy transforms. Which model do you choose and why?"

---

## 2. Quick Definitions

- Sync: one operation at a time, straightforward flow.
- Async: cooperative concurrency on event loop, best for many waiting tasks.
- Multithreading: multiple threads in one process, shared memory.
- Multiprocessing: multiple processes, true CPU parallelism in CPython.

---

## 3. Decision Matrix

### Workload Type
- mostly simple, low concurrency: sync
- high I/O concurrency: async or threads
- CPU-heavy: multiprocessing (or native extensions)

### Team/Codebase Constraints
- team new to concurrency: start sync + safe boundaries
- async-native framework already used: async
- blocking legacy libraries: threads or async + thread offload

### Correctness Needs
- complex shared state: async with clear ownership or queue-based threads
- heavy mutable shared state in threads: high bug risk, redesign preferred

---

## 4. GIL and Decision Making

CPython has two realities now:

### GIL-enabled build (default)
- threads do not give true CPU parallel bytecode execution
- threads are still valuable for I/O wait overlap
- CPU-bound work often goes to multiprocessing or native/vectorized code

### Free-threaded build (introduced in 3.13, improved/supported in 3.14)
- GIL can be disabled
- CPU-bound threaded code can use multiple cores more effectively
- thread safety bugs become more visible if code relied on implicit GIL behavior
- dependency compatibility must be validated in your environment

Interview-safe one-liner:
"On default CPython, threads/async are great for I/O; for CPU-heavy work, multiprocessing is usually safer. On free-threaded CPython, threads can also be a CPU option if your code and dependencies are thread-safe."

---

## 5. Example Scenarios and Recommended Model

### Scenario A: 2000 outbound HTTP calls per minute
Recommended: async (`aiohttp`/async client), semaphore limits, timeout and retries.

### Scenario B: Image resizing pipeline
Recommended: multiprocessing or external worker service.

### Scenario C: Django app with legacy blocking SDK
Recommended: sync or thread pool around blocking SDK.

### Scenario D: FastAPI with mixed async handlers and blocking DB driver
Recommended: use async driver if possible; otherwise offload blocking calls using thread pool.

---

## 6. Latency, Throughput, and Complexity Tradeoff

Sync:
- lowest cognitive complexity
- lower concurrency scalability

Async:
- high I/O throughput
- medium/high complexity (cancellation, loop rules)

Threads:
- easier incremental adoption with blocking libs
- risk of races/deadlocks and shared-state bugs

Multiprocessing:
- CPU scaling
- higher deployment/memory overhead

---

## 7. Reliability Checklist by Model

### Sync
1. Always set timeouts.
2. Add retries with cap.
3. Keep request path small.

### Async
1. No blocking calls in loop.
2. Handle cancellations.
3. Add concurrency limits.
4. Supervise tasks (TaskGroup).

### Threads
1. Minimize shared mutable state.
2. Use lock/queue correctly.
3. Prevent deadlocks via lock order.
4. Implement graceful shutdown.

---

## 8. Common Wrong Answers in Interviews

1. "Async is always faster."
2. "Threads solve CPU-heavy work in Python."
3. "GIL means threads are useless."
4. "Concurrency and parallelism are the same."
5. "If code works locally, locking is fine."

Correct framing:
- speed depends on workload shape
- correctness and maintainability matter as much as raw speed

---

## 9. How to Give a Strong Interview Answer

Use this structure:
1. Identify workload type (I/O vs CPU).
2. Pick model with reason.
3. Mention failure handling (timeouts, retries, cancellation).
4. Mention observability (metrics/logging).
5. Mention scaling path if load grows.

---

## 10. Sample Interview Answer Template

```text
This workload is primarily I/O-bound because most time is spent waiting on remote APIs.
I would choose async to support high concurrency with controlled resource usage.
I will enforce timeout per request, semaphore-limited concurrency, retry with jitter, and
structured task lifecycle using TaskGroup. For any blocking SDK dependency, I will offload
to a thread pool. If CPU-heavy transformation grows, I will move that stage to multiprocessing.
```

---

## 11. One-Page Summary

- Choose model by workload, not trend.
- Async and threads help I/O concurrency.
- Multiprocessing helps CPU parallelism in all standard CPython deployments.
- Free-threaded CPython (3.13+) can make threaded CPU parallelism viable.
- Include reliability and observability in every design answer.
- Best interview answers explain tradeoffs and failure behavior.

---

## 12. Practice Assignment

Take one feature (for example "download and process 500 URLs"):
1. write sync design
2. write async design
3. write thread-pool design
4. compare complexity, runtime, and failure handling
5. present final recommendation with reasons
