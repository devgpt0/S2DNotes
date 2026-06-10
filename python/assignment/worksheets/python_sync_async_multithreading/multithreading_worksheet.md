# Worksheet: Multithreading in Python (Interview Level 3-5 Years)

Question mix:
- Print the Output: 20
- MCQ (Single Correct): 40
- MCQ (Multiple Correct): 40
- Total: 100

Coverage map:
- Thread model, start/run, daemon behavior
- GIL vs free-threaded CPython interview nuance
- Race conditions, locks, and safe shared-state access
- queue.Queue pipelines and graceful stop patterns
- ThreadPoolExecutor, Future, submit/map, and errors
- Deadlock prevention and synchronization primitives
- Operational observability and reliability tradeoffs

---

## Section A: Print the Output (1-20)

1. What will be printed?
```python
import threading

out = []

def worker():
    out.append("run")

t = threading.Thread(target=worker)
t.run()
print(out)
```

2. Predict the output.
```python
import threading

def worker(name):
    print(f"{name}:start")
    print(f"{name}:end")

t1 = threading.Thread(target=worker, args=("T1",))
t2 = threading.Thread(target=worker, args=("T2",))
t1.start()
t1.join()
t2.start()
t2.join()
print("done")
```

3. What is printed?
```python
import threading

counter = 0
lock = threading.Lock()

def inc():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1

t1 = threading.Thread(target=inc)
t2 = threading.Thread(target=inc)
t1.start()
t2.start()
t1.join()
t2.join()
print(counter)
```

4. Predict the output.
```python
import queue
import threading

q = queue.Queue()
out = []

def producer():
    for i in [1, 2, 3]:
        q.put(i)
    q.put(None)

def consumer():
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        out.append(item * 2)
        q.task_done()

t1 = threading.Thread(target=producer)
t2 = threading.Thread(target=consumer)
t1.start()
t2.start()
t1.join()
q.join()
t2.join()
print(out)
```

5. What will be printed?
```python
from concurrent.futures import ThreadPoolExecutor

def square(x):
    return x * x

with ThreadPoolExecutor(max_workers=3) as pool:
    print(list(pool.map(square, [1, 2, 3, 4])))
```

6. Predict the output.
```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=2) as pool:
    f = pool.submit(lambda x: x + 10, 5)
    print(f.result())
```

7. What is printed?
```python
from concurrent.futures import ThreadPoolExecutor

def risky(x):
    if x == 2:
        raise ValueError("bad")
    return x

with ThreadPoolExecutor(max_workers=2) as pool:
    f = pool.submit(risky, 2)
    try:
        print(f.result())
    except ValueError as exc:
        print(f"handled:{exc}")
```

8. Predict the output.
```python
import threading
import time

ready = threading.Event()

def worker():
    ready.wait()
    print("started")

t = threading.Thread(target=worker)
t.start()
time.sleep(0.01)
ready.set()
t.join()
print("done")
```

9. What will be printed?
```python
import threading
import time

sem = threading.Semaphore(2)
lock = threading.Lock()
active = 0
max_active = 0

def worker():
    global active, max_active
    with sem:
        with lock:
            active += 1
            max_active = max(max_active, active)
        time.sleep(0.01)
        with lock:
            active -= 1

threads = [threading.Thread(target=worker) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(max_active)
```

10. Predict RLock behavior.
```python
import threading

lock = threading.RLock()
count = 0

def nested():
    global count
    with lock:
        count += 1
        with lock:
            count += 1

nested()
print(count)
```

11. What is printed?
```python
from concurrent.futures import ThreadPoolExecutor
import time

def slow():
    time.sleep(0.05)
    return "slow"

def fast():
    return "fast"

with ThreadPoolExecutor(max_workers=1) as pool:
    f1 = pool.submit(slow)
    f2 = pool.submit(fast)
    print(f2.cancel())
    print(f1.result())
```

12. Predict the output.
```python
import threading

def show():
    print(threading.current_thread().name)

t = threading.Thread(target=show, name="ingest-worker")
t.start()
t.join()
```

13. What will be printed?
```python
import threading

out = []

def worker():
    out.append("worker")

t = threading.Thread(target=worker, daemon=False)
t.start()
t.join()
out.append("main")
print(out)
```

14. Predict queue join output.
```python
import queue
import threading

q = queue.Queue()
count = 0
lock = threading.Lock()

def worker():
    global count
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        with lock:
            count += item
        q.task_done()

t = threading.Thread(target=worker)
t.start()
for i in [1, 2, 3]:
    q.put(i)
q.put(None)
q.join()
t.join()
print(count)
```

15. What is printed?
```python
import threading

condition = threading.Condition()
state = {"ready": False}

def worker():
    with condition:
        while not state["ready"]:
            condition.wait()
        print("go")

t = threading.Thread(target=worker)
t.start()
with condition:
    state["ready"] = True
    condition.notify()
t.join()
print("done")
```

16. Predict the output.
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def job(x):
    time.sleep(0.01 * x)
    return x

with ThreadPoolExecutor(max_workers=3) as pool:
    futures = [pool.submit(job, x) for x in [1, 2, 3]]
    out = [f.result() for f in as_completed(futures)]
    print(out)
```

17. What will be printed?
```python
import queue
import threading

STOP = object()
q = queue.Queue()
out = []

def worker():
    for item in iter(q.get, STOP):
        out.append(item)
        q.task_done()
    q.task_done()

t = threading.Thread(target=worker)
t.start()
for x in [10, 20]:
    q.put(x)
q.put(STOP)
q.join()
t.join()
print(out)
```

18. Predict Event state output.
```python
import threading

ev = threading.Event()
print(ev.is_set())
ev.set()
print(ev.is_set())
```

19. What is printed?
```python
import threading

sem = threading.Semaphore(1)
print(sem.acquire(blocking=False))
print(sem.acquire(blocking=False))
sem.release()
print(sem.acquire(blocking=False))
```

20. Predict graceful-stop output.
```python
import queue
import threading

STOP = object()
q = queue.Queue()
processed = []

def worker():
    while True:
        item = q.get()
        if item is STOP:
            q.task_done()
            break
        processed.append(item * 10)
        q.task_done()

t = threading.Thread(target=worker)
t.start()
for i in [1, 2, 3]:
    q.put(i)
q.put(STOP)
q.join()
t.join()
print(processed)
```

---

## Section B: MCQ (Single Correct) (21-60)

21. Which statement is correct about thread model fundamentals?
- A. Calling run() directly always creates a new OS thread.
- B. GIL means threads are useless for all workloads.
- C. Threads in Python always guarantee CPU parallel speedup on default builds.
- D. Threads share process memory while each thread has its own stack.

22. Which statement is correct about GIL and free-threaded CPython?
- A. In default CPython builds, GIL allows one thread at a time to execute Python bytecode.
- B. Daemon threads are best for must-not-lose critical financial writes.
- C. Calling run() directly always creates a new OS thread.
- D. Race conditions are impossible when using lists and dicts.

23. Which statement is correct about start/run semantics?
- A. Threads are commonly useful for I/O-bound concurrency.
- B. Queue is mainly for sorting elements, not coordination.
- C. Race conditions are impossible when using lists and dicts.
- D. Locks should be held as long as possible for safety.

24. Which statement is correct about daemon vs non-daemon behavior?
- A. ThreadPoolExecutor removes all need for error handling.
- B. Free-threaded CPython builds can allow parallel Python bytecode execution.
- C. Queue is mainly for sorting elements, not coordination.
- D. Future.cancel() always cancels running tasks immediately.

25. Which statement is correct about race conditions and locks?
- A. start() launches a new thread; direct run() does not.
- B. Lock acquisition order has no impact on deadlock risk.
- C. Deadlocks happen only in async code, not threads.
- D. Future.cancel() always cancels running tasks immediately.

26. Which statement is correct about queue-based communication?
- A. Event can only wake one waiter and cannot be reused.
- B. Lock acquisition order has no impact on deadlock risk.
- C. RLock and Lock are completely identical in behavior.
- D. Daemon threads may stop when main program exits.

27. Which statement is correct about ThreadPoolExecutor and Future APIs?
- A. Condition is unnecessary in producer-consumer designs.
- B. Semaphore increases available resource count automatically.
- C. Event can only wake one waiter and cannot be reused.
- D. Non-daemon threads keep process alive until they finish.

28. Which statement is correct about deadlock prevention?
- A. Race conditions arise from unsafely shared mutable state timing.
- B. Graceful shutdown means killing threads without signaling.
- C. Semaphore increases available resource count automatically.
- D. Thread names add no value in logs.

29. Which statement is correct about thread synchronization primitives?
- A. Threading primitives are interchangeable with no tradeoffs.
- B. Queue depth metrics are not useful for tuning thread pools.
- C. Lock protects critical sections against concurrent access.
- D. Thread names add no value in logs.

30. Which statement is correct about graceful shutdown patterns?
- A. Free-threaded CPython is the default everywhere now.
- B. Join is optional even when correctness depends on completion.
- C. Threading primitives are interchangeable with no tradeoffs.
- D. Queue-based message passing can reduce shared-state bugs.

31. Which statement is correct about observability and debugging?
- A. Shared mutable state is always easier than message passing.
- B. Free-threaded CPython is the default everywhere now.
- C. ThreadPoolExecutor reuses worker threads and simplifies lifecycle.
- D. Long critical sections improve throughput.

32. Which statement is correct about interview architecture tradeoffs?
- A. submit returns Future handles for per-task control.
- B. Long critical sections improve throughput.
- C. Busy waiting is the recommended waiting strategy.
- D. Multiprocessing and threading are the same model.

33. Which statement is correct about thread model fundamentals?
- A. map provides ordered output iteration for mapped inputs.
- B. Multiprocessing and threading are the same model.
- C. Error handling should be avoided in concurrent code for speed.
- D. Worker count should always be unlimited for best latency.

34. Which statement is correct about GIL and free-threaded CPython?
- A. Worker count should always be unlimited for best latency.
- B. Future.result() can surface task exceptions.
- C. Observability is unnecessary if tests are green.
- D. Default GIL build never benefits from thread-based I/O overlap.

35. Which statement is correct about start/run semantics?
- A. Future.cancel() typically succeeds only before task start.
- B. Sentinel shutdown patterns are an anti-pattern in worker queues.
- C. Threads in Python always guarantee CPU parallel speedup on default builds.
- D. Observability is unnecessary if tests are green.

36. Which statement is correct about daemon vs non-daemon behavior?
- A. Threads in Python always guarantee CPU parallel speedup on default builds.
- B. Calling run() directly always creates a new OS thread.
- C. GIL means threads are useless for all workloads.
- D. Deadlocks often involve circular waits on locks/resources.

37. Which statement is correct about race conditions and locks?
- A. Daemon threads are best for must-not-lose critical financial writes.
- B. Calling run() directly always creates a new OS thread.
- C. Race conditions are impossible when using lists and dicts.
- D. Consistent lock acquisition order helps avoid deadlocks.

38. Which statement is correct about queue-based communication?
- A. Queue is mainly for sorting elements, not coordination.
- B. RLock supports re-entrant acquisition by same thread.
- C. Race conditions are impossible when using lists and dicts.
- D. Locks should be held as long as possible for safety.

39. Which statement is correct about ThreadPoolExecutor and Future APIs?
- A. Future.cancel() always cancels running tasks immediately.
- B. Event supports signaling between threads.
- C. ThreadPoolExecutor removes all need for error handling.
- D. Queue is mainly for sorting elements, not coordination.

40. Which statement is correct about deadlock prevention?
- A. Deadlocks happen only in async code, not threads.
- B. Lock acquisition order has no impact on deadlock risk.
- C. Future.cancel() always cancels running tasks immediately.
- D. Condition supports wait/notify coordination with lock.

41. Which statement is correct about thread synchronization primitives?
- A. Semaphore caps concurrent access to limited resources.
- B. Event can only wake one waiter and cannot be reused.
- C. Lock acquisition order has no impact on deadlock risk.
- D. RLock and Lock are completely identical in behavior.

42. Which statement is correct about graceful shutdown patterns?
- A. Graceful shutdown usually uses stop signals/events/sentinels.
- B. Event can only wake one waiter and cannot be reused.
- C. Condition is unnecessary in producer-consumer designs.
- D. Semaphore increases available resource count automatically.

43. Which statement is correct about observability and debugging?
- A. Thread names add no value in logs.
- B. Queue depth and success/failure metrics aid threaded observability.
- C. Graceful shutdown means killing threads without signaling.
- D. Semaphore increases available resource count automatically.

44. Which statement is correct about interview architecture tradeoffs?
- A. Thread names can improve log readability during incidents.
- B. Thread names add no value in logs.
- C. Threading primitives are interchangeable with no tradeoffs.
- D. Queue depth metrics are not useful for tuning thread pools.

45. Which statement is correct about thread model fundamentals?
- A. Long lock hold times increase contention and latency.
- B. Join is optional even when correctness depends on completion.
- C. Free-threaded CPython is the default everywhere now.
- D. Threading primitives are interchangeable with no tradeoffs.

46. Which statement is correct about GIL and free-threaded CPython?
- A. Long critical sections improve throughput.
- B. Shared mutable state is always easier than message passing.
- C. Minimizing shared mutable state improves correctness.
- D. Free-threaded CPython is the default everywhere now.

47. Which statement is correct about start/run semantics?
- A. For CPU-heavy workloads on default CPython, multiprocessing is often stronger.
- B. Busy waiting is the recommended waiting strategy.
- C. Multiprocessing and threading are the same model.
- D. Long critical sections improve throughput.

48. Which statement is correct about daemon vs non-daemon behavior?
- A. Worker count should always be unlimited for best latency.
- B. Multiprocessing and threading are the same model.
- C. Thread pools are often safer than thread-per-task creation at scale.
- D. Error handling should be avoided in concurrent code for speed.

49. Which statement is correct about race conditions and locks?
- A. Default GIL build never benefits from thread-based I/O overlap.
- B. Worker count should always be unlimited for best latency.
- C. Observability is unnecessary if tests are green.
- D. Error handling should happen around future.result() calls.

50. Which statement is correct about queue-based communication?
- A. Bounded worker counts protect downstream systems from overload.
- B. Observability is unnecessary if tests are green.
- C. Threads in Python always guarantee CPU parallel speedup on default builds.
- D. Sentinel shutdown patterns are an anti-pattern in worker queues.

51. Which statement is correct about ThreadPoolExecutor and Future APIs?
- A. GIL means threads are useless for all workloads.
- B. Threads in Python always guarantee CPU parallel speedup on default builds.
- C. Calling run() directly always creates a new OS thread.
- D. Threading and parallelism are related but not identical concepts.

52. Which statement is correct about deadlock prevention?
- A. Join helps ensure threads finish before process exit.
- B. Daemon threads are best for must-not-lose critical financial writes.
- C. Race conditions are impossible when using lists and dicts.
- D. Calling run() directly always creates a new OS thread.

53. Which statement is correct about thread synchronization primitives?
- A. Race conditions are impossible when using lists and dicts.
- B. Locks should be held as long as possible for safety.
- C. Without proper synchronization, outputs may depend on timing.
- D. Queue is mainly for sorting elements, not coordination.

54. Which statement is correct about graceful shutdown patterns?
- A. Future.cancel() always cancels running tasks immediately.
- B. Structured shutdown should drain or account for in-flight work.
- C. ThreadPoolExecutor removes all need for error handling.
- D. Queue is mainly for sorting elements, not coordination.

55. Which statement is correct about observability and debugging?
- A. Lock acquisition order has no impact on deadlock risk.
- B. Deadlocks happen only in async code, not threads.
- C. Thread primitives should be chosen by coordination need, not habit.
- D. Future.cancel() always cancels running tasks immediately.

56. Which statement is correct about interview architecture tradeoffs?
- A. Default GIL build still benefits from threads for overlapping I/O waits.
- B. Lock acquisition order has no impact on deadlock risk.
- C. Event can only wake one waiter and cannot be reused.
- D. RLock and Lock are completely identical in behavior.

57. Which statement is correct about thread model fundamentals?
- A. Condition is unnecessary in producer-consumer designs.
- B. Event can only wake one waiter and cannot be reused.
- C. Semaphore increases available resource count automatically.
- D. Free-threaded mode increases need for careful thread-safety discipline.

58. Which statement is correct about GIL and free-threaded CPython?
- A. Thread names add no value in logs.
- B. Graceful shutdown means killing threads without signaling.
- C. Semaphore increases available resource count automatically.
- D. Busy-wait loops are often worse than events or conditions.

59. Which statement is correct about start/run semantics?
- A. Thread names add no value in logs.
- B. Threading primitives are interchangeable with no tradeoffs.
- C. Queue depth metrics are not useful for tuning thread pools.
- D. Queue with sentinel is a common worker-stop pattern.

60. Which statement is correct about daemon vs non-daemon behavior?
- A. Threading primitives are interchangeable with no tradeoffs.
- B. Free-threaded CPython is the default everywhere now.
- C. Concurrency bugs are easier to fix when observability is strong.
- D. Join is optional even when correctness depends on completion.

---

## Section C: MCQ (Multiple Correct) (61-100)

61. Select all correct statements about thread model fundamentals.
Select all that apply.
- A. GIL means threads are useless for all workloads.
- B. In default CPython builds, GIL allows one thread at a time to execute Python bytecode.
- C. Threads share process memory while each thread has its own stack.
- D. Threads in Python always guarantee CPU parallel speedup on default builds.

62. Select all correct statements about GIL and free-threaded CPython.
Select all that apply.
- A. Daemon threads are best for must-not-lose critical financial writes.
- B. Calling run() directly always creates a new OS thread.
- C. Free-threaded CPython builds can allow parallel Python bytecode execution.
- D. Threads are commonly useful for I/O-bound concurrency.

63. Select all correct statements about start/run semantics.
Select all that apply.
- A. Daemon threads may stop when main program exits.
- B. start() launches a new thread; direct run() does not.
- C. Race conditions are impossible when using lists and dicts.
- D. Locks should be held as long as possible for safety.

64. Select all correct statements about daemon vs non-daemon behavior.
Select all that apply.
- A. ThreadPoolExecutor removes all need for error handling.
- B. Non-daemon threads keep process alive until they finish.
- C. Queue is mainly for sorting elements, not coordination.
- D. Race conditions arise from unsafely shared mutable state timing.

65. Select all correct statements about race conditions and locks.
Select all that apply.
- A. Future.cancel() always cancels running tasks immediately.
- B. Queue-based message passing can reduce shared-state bugs.
- C. Lock protects critical sections against concurrent access.
- D. Deadlocks happen only in async code, not threads.

66. Select all correct statements about queue-based communication.
Select all that apply.
- A. RLock and Lock are completely identical in behavior.
- B. Lock acquisition order has no impact on deadlock risk.
- C. ThreadPoolExecutor reuses worker threads and simplifies lifecycle.
- D. submit returns Future handles for per-task control.

67. Select all correct statements about ThreadPoolExecutor and Future APIs.
Select all that apply.
- A. Future.result() can surface task exceptions.
- B. map provides ordered output iteration for mapped inputs.
- C. Condition is unnecessary in producer-consumer designs.
- D. Event can only wake one waiter and cannot be reused.

68. Select all correct statements about deadlock prevention.
Select all that apply.
- A. Semaphore increases available resource count automatically.
- B. Graceful shutdown means killing threads without signaling.
- C. Future.cancel() typically succeeds only before task start.
- D. Deadlocks often involve circular waits on locks/resources.

69. Select all correct statements about thread synchronization primitives.
Select all that apply.
- A. Queue depth metrics are not useful for tuning thread pools.
- B. RLock supports re-entrant acquisition by same thread.
- C. Consistent lock acquisition order helps avoid deadlocks.
- D. Thread names add no value in logs.

70. Select all correct statements about graceful shutdown patterns.
Select all that apply.
- A. Threading primitives are interchangeable with no tradeoffs.
- B. Join is optional even when correctness depends on completion.
- C. Condition supports wait/notify coordination with lock.
- D. Event supports signaling between threads.

71. Select all correct statements about observability and debugging.
Select all that apply.
- A. Shared mutable state is always easier than message passing.
- B. Graceful shutdown usually uses stop signals/events/sentinels.
- C. Free-threaded CPython is the default everywhere now.
- D. Semaphore caps concurrent access to limited resources.

72. Select all correct statements about interview architecture tradeoffs.
Select all that apply.
- A. Busy waiting is the recommended waiting strategy.
- B. Queue depth and success/failure metrics aid threaded observability.
- C. Thread names can improve log readability during incidents.
- D. Long critical sections improve throughput.

73. Select all correct statements about thread model fundamentals.
Select all that apply.
- A. Error handling should be avoided in concurrent code for speed.
- B. Minimizing shared mutable state improves correctness.
- C. Multiprocessing and threading are the same model.
- D. Long lock hold times increase contention and latency.

74. Select all correct statements about GIL and free-threaded CPython.
Select all that apply.
- A. Worker count should always be unlimited for best latency.
- B. Default GIL build never benefits from thread-based I/O overlap.
- C. For CPU-heavy workloads on default CPython, multiprocessing is often stronger.
- D. Thread pools are often safer than thread-per-task creation at scale.

75. Select all correct statements about start/run semantics.
Select all that apply.
- A. Error handling should happen around future.result() calls.
- B. Observability is unnecessary if tests are green.
- C. Bounded worker counts protect downstream systems from overload.
- D. Sentinel shutdown patterns are an anti-pattern in worker queues.

76. Select all correct statements about daemon vs non-daemon behavior.
Select all that apply.
- A. GIL means threads are useless for all workloads.
- B. Join helps ensure threads finish before process exit.
- C. Threads in Python always guarantee CPU parallel speedup on default builds.
- D. Threading and parallelism are related but not identical concepts.

77. Select all correct statements about race conditions and locks.
Select all that apply.
- A. Daemon threads are best for must-not-lose critical financial writes.
- B. Structured shutdown should drain or account for in-flight work.
- C. Without proper synchronization, outputs may depend on timing.
- D. Calling run() directly always creates a new OS thread.

78. Select all correct statements about queue-based communication.
Select all that apply.
- A. Default GIL build still benefits from threads for overlapping I/O waits.
- B. Race conditions are impossible when using lists and dicts.
- C. Locks should be held as long as possible for safety.
- D. Thread primitives should be chosen by coordination need, not habit.

79. Select all correct statements about ThreadPoolExecutor and Future APIs.
Select all that apply.
- A. Busy-wait loops are often worse than events or conditions.
- B. Queue is mainly for sorting elements, not coordination.
- C. Free-threaded mode increases need for careful thread-safety discipline.
- D. ThreadPoolExecutor removes all need for error handling.

80. Select all correct statements about deadlock prevention.
Select all that apply.
- A. Deadlocks happen only in async code, not threads.
- B. Concurrency bugs are easier to fix when observability is strong.
- C. Queue with sentinel is a common worker-stop pattern.
- D. Future.cancel() always cancels running tasks immediately.

81. Select all correct statements about thread synchronization primitives.
Select all that apply.
- A. Lock acquisition order has no impact on deadlock risk.
- B. In default CPython builds, GIL allows one thread at a time to execute Python bytecode.
- C. Threads share process memory while each thread has its own stack.
- D. RLock and Lock are completely identical in behavior.

82. Select all correct statements about graceful shutdown patterns.
Select all that apply.
- A. Free-threaded CPython builds can allow parallel Python bytecode execution.
- B. Condition is unnecessary in producer-consumer designs.
- C. Event can only wake one waiter and cannot be reused.
- D. Threads are commonly useful for I/O-bound concurrency.

83. Select all correct statements about observability and debugging.
Select all that apply.
- A. Graceful shutdown means killing threads without signaling.
- B. Semaphore increases available resource count automatically.
- C. Daemon threads may stop when main program exits.
- D. start() launches a new thread; direct run() does not.

84. Select all correct statements about interview architecture tradeoffs.
Select all that apply.
- A. Queue depth metrics are not useful for tuning thread pools.
- B. Race conditions arise from unsafely shared mutable state timing.
- C. Non-daemon threads keep process alive until they finish.
- D. Thread names add no value in logs.

85. Select all correct statements about thread model fundamentals.
Select all that apply.
- A. Queue-based message passing can reduce shared-state bugs.
- B. Join is optional even when correctness depends on completion.
- C. Lock protects critical sections against concurrent access.
- D. Threading primitives are interchangeable with no tradeoffs.

86. Select all correct statements about GIL and free-threaded CPython.
Select all that apply.
- A. submit returns Future handles for per-task control.
- B. Shared mutable state is always easier than message passing.
- C. ThreadPoolExecutor reuses worker threads and simplifies lifecycle.
- D. Free-threaded CPython is the default everywhere now.

87. Select all correct statements about start/run semantics.
Select all that apply.
- A. map provides ordered output iteration for mapped inputs.
- B. Long critical sections improve throughput.
- C. Busy waiting is the recommended waiting strategy.
- D. Future.result() can surface task exceptions.

88. Select all correct statements about daemon vs non-daemon behavior.
Select all that apply.
- A. Error handling should be avoided in concurrent code for speed.
- B. Deadlocks often involve circular waits on locks/resources.
- C. Future.cancel() typically succeeds only before task start.
- D. Multiprocessing and threading are the same model.

89. Select all correct statements about race conditions and locks.
Select all that apply.
- A. RLock supports re-entrant acquisition by same thread.
- B. Worker count should always be unlimited for best latency.
- C. Consistent lock acquisition order helps avoid deadlocks.
- D. Default GIL build never benefits from thread-based I/O overlap.

90. Select all correct statements about queue-based communication.
Select all that apply.
- A. Condition supports wait/notify coordination with lock.
- B. Event supports signaling between threads.
- C. Observability is unnecessary if tests are green.
- D. Sentinel shutdown patterns are an anti-pattern in worker queues.

91. Select all correct statements about ThreadPoolExecutor and Future APIs.
Select all that apply.
- A. Semaphore caps concurrent access to limited resources.
- B. Threads in Python always guarantee CPU parallel speedup on default builds.
- C. GIL means threads are useless for all workloads.
- D. Graceful shutdown usually uses stop signals/events/sentinels.

92. Select all correct statements about deadlock prevention.
Select all that apply.
- A. Thread names can improve log readability during incidents.
- B. Daemon threads are best for must-not-lose critical financial writes.
- C. Calling run() directly always creates a new OS thread.
- D. Queue depth and success/failure metrics aid threaded observability.

93. Select all correct statements about thread synchronization primitives.
Select all that apply.
- A. Locks should be held as long as possible for safety.
- B. Race conditions are impossible when using lists and dicts.
- C. Long lock hold times increase contention and latency.
- D. Minimizing shared mutable state improves correctness.

94. Select all correct statements about graceful shutdown patterns.
Select all that apply.
- A. ThreadPoolExecutor removes all need for error handling.
- B. For CPU-heavy workloads on default CPython, multiprocessing is often stronger.
- C. Queue is mainly for sorting elements, not coordination.
- D. Thread pools are often safer than thread-per-task creation at scale.

95. Select all correct statements about observability and debugging.
Select all that apply.
- A. Bounded worker counts protect downstream systems from overload.
- B. Future.cancel() always cancels running tasks immediately.
- C. Deadlocks happen only in async code, not threads.
- D. Error handling should happen around future.result() calls.

96. Select all correct statements about interview architecture tradeoffs.
Select all that apply.
- A. Lock acquisition order has no impact on deadlock risk.
- B. Threading and parallelism are related but not identical concepts.
- C. Join helps ensure threads finish before process exit.
- D. RLock and Lock are completely identical in behavior.

97. Select all correct statements about thread model fundamentals.
Select all that apply.
- A. Structured shutdown should drain or account for in-flight work.
- B. Condition is unnecessary in producer-consumer designs.
- C. Without proper synchronization, outputs may depend on timing.
- D. Event can only wake one waiter and cannot be reused.

98. Select all correct statements about GIL and free-threaded CPython.
Select all that apply.
- A. Default GIL build still benefits from threads for overlapping I/O waits.
- B. Semaphore increases available resource count automatically.
- C. Graceful shutdown means killing threads without signaling.
- D. Thread primitives should be chosen by coordination need, not habit.

99. Select all correct statements about start/run semantics.
Select all that apply.
- A. Thread names add no value in logs.
- B. Queue depth metrics are not useful for tuning thread pools.
- C. Busy-wait loops are often worse than events or conditions.
- D. Free-threaded mode increases need for careful thread-safety discipline.

100. Select all correct statements about daemon vs non-daemon behavior.
Select all that apply.
- A. Concurrency bugs are easier to fix when observability is strong.
- B. Queue with sentinel is a common worker-stop pattern.
- C. Join is optional even when correctness depends on completion.
- D. Threading primitives are interchangeable with no tradeoffs.
