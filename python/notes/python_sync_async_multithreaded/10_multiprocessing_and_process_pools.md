# Multiprocessing and Process Pools Mastery

## 1) Why Multiprocessing

For CPU-bound workloads in standard CPython, multiprocessing enables true parallel execution by using separate processes.

## 2) Process vs Thread Model

- process: isolated memory, IPC required, higher startup/memory overhead.
- thread: shared memory, lighter but synchronization required.

## 3) `ProcessPoolExecutor` Basics

```python
from concurrent.futures import ProcessPoolExecutor


def cpu_task(x: int) -> int:
    return x * x


with ProcessPoolExecutor(max_workers=4) as pool:
    out = list(pool.map(cpu_task, range(10)))
print(out)
```

## 4) Pickle Boundary Rules

Process pools serialize callables/args/results.

Implications:
- functions should be top-level importable callables.
- avoid non-picklable closures/lambdas in pool tasks.

## 5) `if __name__ == "__main__"` Guard

Required especially on Windows for safe process spawning.

## 6) Inter-Process Communication Patterns

Options:
- queues/pipes
- manager objects (with caution)
- explicit files/DB/message brokers for larger systems

## 7) Process Pool Pitfalls

- high serialization overhead for tiny tasks
- spawning too many workers causing context-switch pressure
- passing huge payloads repeatedly across process boundary

## 8) When Not to Use Multiprocessing

- mostly I/O-bound workloads
- tiny tasks where pool overhead dominates
- environments with strict memory constraints

## 9) Interview Questions

1. Why CPU-bound work often prefers processes?
2. Why pickle-ability matters?
3. Why `__main__` guard is important on Windows?
4. How do you choose process count?

## 10) Production Checklist

1. task function is pure/minimal side effects.
2. data payload across processes is compact.
3. timeout/cancellation policy exists for pool tasks.
4. worker count tuned from benchmark, not guess.
