# Multithreading in Python: Fundamentals

## 1. What Is Multithreading

Multithreading runs multiple threads inside one process.

Thread facts:
- threads share same process memory
- each thread has its own stack
- scheduler switches between threads

---

## 2. Why Use Threads in Python

Threads are useful mainly for I/O-bound concurrency in CPython.

Examples:
- many HTTP calls
- file I/O
- waiting on sockets

---

## 3. GIL Basics + Python 3.14 Update (Very Important Interview Topic)

### Default CPython behavior (GIL-enabled build)
CPython has a GIL (Global Interpreter Lock):
- only one thread executes Python bytecode at a time
- reduces race issues in interpreter internals
- limits CPU-bound parallelism with threads

### Python 3.13 and 3.14 update
- Python 3.13 introduced a free-threaded build where GIL can be disabled.
- Python 3.14 improved and officially supported free-threaded mode.
- Important: this is still not the default interpreter build.

### How this changes things in practice
1. CPU-bound thread workloads can scale better on free-threaded builds.
2. Code that accidentally relied on GIL behavior can show races now.
3. Lock discipline (`Lock`, `RLock`, `Queue`) becomes even more important.
4. Some third-party extension modules may not be ready and can force GIL behavior.

### Interview-safe statement
- on default CPython, threads mainly help I/O concurrency
- on free-threaded CPython, threads can also help CPU parallelism
- multiprocessing remains a strong portable choice for CPU-heavy work

Check runtime/build quickly:
```python
import sys
import sysconfig

is_free_thread_build = sysconfig.get_config_var("Py_GIL_DISABLED") == 1
gil_enabled_now = sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else True

print(f"Free-threaded build: {is_free_thread_build}")
print(f"GIL currently enabled: {gil_enabled_now}")
```

---

## 4. First Thread Example

```python
import threading
import time


def worker(name: str):
    print(f"{name} started")
    time.sleep(1)
    print(f"{name} finished")


def main():
    t1 = threading.Thread(target=worker, args=("Thread-1",))
    t2 = threading.Thread(target=worker, args=("Thread-2",))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All done")


if __name__ == "__main__":
    main()
```

---

## 5. `start()` vs `run()` (Interview Trap)

- `start()` creates new thread and then calls `run()` internally
- calling `run()` directly does not start a new thread

---

## 6. Daemon vs Non-Daemon Threads

Daemon thread:
- killed when main program exits
- use for background helper tasks

Non-daemon thread:
- program waits for it to finish
- use for important work

```python
import threading
import time


def background():
    while True:
        print("heartbeat")
        time.sleep(0.5)


t = threading.Thread(target=background, daemon=True)
t.start()
time.sleep(1.2)
print("main exiting")
```

---

## 7. Race Condition Basics

Race condition occurs when result depends on unpredictable execution ordering.

Unsafe example:
```python
import threading

counter = 0


def increment():
    global counter
    for _ in range(100000):
        counter += 1


t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start()
t2.start()
t1.join()
t2.join()
print(counter)
```

Expected ideal value is `200000`, but unsafe shared updates can break correctness.

---

## 8. Fix Race With `Lock`

```python
import threading

counter = 0
lock = threading.Lock()


def increment():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1


t1 = threading.Thread(target=increment)
t2 = threading.Thread(target=increment)
t1.start()
t2.start()
t1.join()
t2.join()
print(counter)
```

`Lock` ensures one thread enters critical section at a time.

---

## 9. Thread-Safe Communication With `queue.Queue`

Prefer message passing over shared mutable state.

```python
import queue
import threading
import time


def producer(q: queue.Queue):
    for i in range(5):
        q.put(i)
    q.put(None)


def consumer(q: queue.Queue):
    while True:
        item = q.get()
        if item is None:
            q.task_done()
            break
        print(f"Processed {item}")
        time.sleep(0.2)
        q.task_done()


q = queue.Queue()
t1 = threading.Thread(target=producer, args=(q,))
t2 = threading.Thread(target=consumer, args=(q,))
t1.start()
t2.start()
t1.join()
q.join()
t2.join()
```

---

## 10. Common Threading Mistakes

1. Forgetting `join()`, causing early program exit.
2. Holding lock longer than needed.
3. Nested locks without order (deadlock risk).
4. Busy wait loops instead of events/queues.
5. Using threads for CPU-heavy math expecting speedup.

---

## 11. Interview Questions From This Level

1. What is a thread?
2. Why do Python threads not speed CPU-bound tasks much?
3. What is GIL?
4. What is race condition?
5. How does lock fix race?
6. Why is queue safer than shared globals?

---

## 12. One-Page Summary

- Threads share memory and can run concurrently.
- In default CPython builds, GIL limits CPU-parallel bytecode execution.
- In free-threaded builds (3.13+), threads can run Python code in parallel.
- Threads are strong for I/O-bound workloads.
- Use `Lock` and `Queue` for correctness.
- Correctness first, then performance tuning.

---

## 13. Practice Assignment

Implement threaded log processor:
- producer reads mock log lines
- 3 consumer threads parse lines
- shared result dict protected by lock
- then refactor to queue-based message passing with less shared state
