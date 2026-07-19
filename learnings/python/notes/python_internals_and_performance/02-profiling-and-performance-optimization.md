# Profiling and Performance Optimization

Performance work starts with a user-visible target and measurement. It does not start by rewriting clear code into clever code.

## 1. Optimization Loop

```text
define target -> reproduce workload -> measure -> find bottleneck
              -> make one change -> measure again -> keep or revert
```

Examples of useful targets:

- p95 request latency below 200 ms;
- batch completes within 10 minutes;
- peak memory remains below 512 MiB;
- throughput exceeds 2,000 records per second;
- startup remains below 500 ms.

## 2. Classify the Bottleneck

| Bottleneck | Evidence | Common direction |
|---|---|---|
| CPU | cores busy; hot Python/native stacks | algorithm, built-ins, vectorization, processes, native code |
| allocation | many short-lived objects; GC pressure | stream, reuse representation, remove copies |
| memory retention | live objects keep growing | ownership, cache bounds, reference chains |
| disk/network I/O | tasks wait on external operations | batching, concurrency, caching, protocol changes |
| lock/contention | threads wait on locks or queues | smaller critical section, ownership redesign |
| database | slow queries, pool saturation | query plan, indexes, batching, transaction scope |

Do not apply CPU optimization to a database bottleneck.

## 3. Use `perf_counter` for Elapsed Time

```python
from time import perf_counter, sleep

started = perf_counter()
sleep(0.02)
elapsed = perf_counter() - started

print(elapsed >= 0.02)
```

Output:

```text
True
```

`perf_counter` is monotonic and intended for duration measurement. Do not use wall-clock timestamps to benchmark elapsed work.

## 4. Microbenchmark with `timeit`

```python
from timeit import repeat

samples = repeat(
    stmt="sum(range(1_000))",
    repeat=5,
    number=10_000,
)

print(len(samples))
print(min(samples) > 0)
```

Output:

```text
5
True
```

Use multiple samples and report the environment. A microbenchmark answers a narrow question; it does not predict complete service latency.

From the command line:

```powershell
python -m timeit -s "values=list(range(1000))" "sum(values)"
```

## 5. Deterministic CPU Profiling with `cProfile`

Create `workload.py`:

```python
def count_even(limit: int) -> int:
    return sum(1 for value in range(limit) if value % 2 == 0)


def main() -> None:
    print(count_even(1_000_000))


if __name__ == "__main__":
    main()
```

Run:

```powershell
python -m cProfile -o profile.prof workload.py
python -m pstats profile.prof
```

Inside `pstats`:

```text
sort cumulative
stats 20
callers count_even
```

Important columns:

- `ncalls`: number of calls;
- `tottime`: time in the function excluding callees;
- `cumtime`: time in the function including callees;
- `percall`: derived cost per call.

Start with cumulative time to find expensive call paths. Use total time to find expensive function bodies.

## 6. Read Profiles Programmatically

```python
import pstats

statistics = pstats.Stats("profile.prof")
statistics.strip_dirs().sort_stats("cumulative").print_stats(10)
```

This helps produce repeatable CI artifacts, but do not make a noisy wall-clock benchmark a flaky unit-test gate.

## 7. Sampling Profilers

Sampling profilers periodically inspect stacks and usually perturb the process less than deterministic tracing. They are useful for long-running or production-like workloads.

Common options include:

- `py-spy` for external sampling of Python processes;
- Scalene for CPU, memory, and Python-versus-native attribution;
- platform profilers for complete process and system evidence.

Choose tools according to operating-system support and security policy. Attaching to a process may require elevated diagnostic permissions.

## 8. Find Python Allocations with `tracemalloc`

```python
import tracemalloc

tracemalloc.start(10)

values = [str(number) for number in range(10_000)]
snapshot = tracemalloc.take_snapshot()
largest = snapshot.statistics("lineno")[:3]

print(len(values))
print(len(largest) > 0)
```

Output:

```text
10000
True
```

Compare snapshots around one operation:

```python
before = tracemalloc.take_snapshot()
values = [str(number) for number in range(10_000)]
after = tracemalloc.take_snapshot()

for statistic in after.compare_to(before, "lineno")[:5]:
    print(statistic)
```

`tracemalloc` traces Python-managed allocations. It does not account for every native library allocation or the full process RSS.

## 9. Measure Object Size Carefully

```python
import sys

values = [1, 2, 3]
print(sys.getsizeof(values) > 0)
```

Output:

```text
True
```

`getsizeof(values)` measures the list object, not every referenced integer recursively. Deep-size tools make assumptions about shared references; document those assumptions.

## 10. Inspect Garbage Collection

```python
import gc

print(gc.isenabled())
print(len(gc.get_count()) == 3)
```

Typical output:

```text
True
True
```

Do not call `gc.collect()` repeatedly as a default optimization. First prove cyclic garbage collection is responsible for the measured latency or memory behavior.

## 11. Algorithm Before Syntax

Membership in a list is linear; membership in a set is expected constant time.

```python
allowed_list = list(range(100_000))
allowed_set = set(allowed_list)

print(99_999 in allowed_list)
print(99_999 in allowed_set)
```

Output:

```text
True
True
```

The behavior matches, but the data structures express different performance contracts. Consider construction cost, memory, ordering, duplicates, and required operations—not only one lookup.

## 12. Prefer Built-ins for Tight Work

Built-ins commonly execute their inner loops in optimized native code.

```python
values = range(1_000)

manual = 0
for value in values:
    manual += value

built_in = sum(values)
print(manual == built_in)
```

Output:

```text
True
```

Prefer the built-in because it is clearer. Verify speed with the real input before treating it as a performance claim.

## 13. Avoid Accidental Quadratic Concatenation

```python
parts = ["python", "profiling", "optimization"]
message = " ".join(parts)
print(message)
```

Output:

```text
python profiling optimization
```

Repeated string concatenation inside a large loop can copy growing intermediate strings. `str.join` states the intent and performs one coordinated construction.

## 14. Stream Instead of Materializing

```python
from collections.abc import Iterator


def squares(limit: int) -> Iterator[int]:
    for value in range(limit):
        yield value * value


print(sum(squares(5)))
```

Output:

```text
30
```

A generator reduces peak memory when the consumer can process one item at a time. It may not be faster, and it is one-pass.

## 15. Reduce Copies at Boundaries

Use borrowed read-only views where the API supports them:

- `memoryview` for binary buffers;
- iterators for streams;
- paths instead of reading entire files prematurely;
- database cursors or pages instead of unbounded result lists.

```python
payload = b"HEADER:content"
view = memoryview(payload)
print(bytes(view[:6]))
```

Output:

```text
b'HEADER'
```

The slice of a memory view does not copy the underlying bytes. Converting it with `bytes` does copy, as shown for printing.

## 16. Cache Only with an Ownership Policy

```python
from functools import lru_cache


@lru_cache(maxsize=256)
def parse_course_id(raw: str) -> tuple[str, ...]:
    return tuple(raw.split("-"))


print(parse_course_id("python-performance"))
print(parse_course_id.cache_info().maxsize)
```

Output:

```text
('python', 'performance')
256
```

A bounded cache still retains keys and values. Include invalidation, staleness, memory, sensitive-data, and multi-process behavior in the design.

## 17. CPU Parallelism Choices

For CPU-bound Python work:

1. improve the algorithm;
2. use optimized built-ins or a proven vectorized library;
3. consider processes for independent coarse tasks;
4. consider a free-threaded build only with compatible code and dependencies;
5. move a measured stable kernel to Cython, C, C++, or Rust when justified.

Serialization and inter-process transfer can erase multiprocessing gains for small tasks.

## 18. I/O Concurrency Choices

- synchronous code for simple low-concurrency flows;
- threads for blocking libraries and moderate I/O concurrency;
- asyncio for high concurrency when the complete dependency path is async;
- batching when the remote system benefits from fewer larger operations.

Concurrency does not make one operation faster. It overlaps waiting and must be bounded.

## 19. Benchmark Correctness

Before trusting a comparison:

- confirm both implementations produce the same result;
- use representative data sizes and distributions;
- include warm-up when relevant;
- use multiple samples;
- isolate unrelated system load where practical;
- record Python version, implementation, CPU, OS, dependencies, and configuration;
- measure release/native builds with their production flags;
- include allocation and peak memory when relevant.

## 20. Performance Regression Tests

Keep ordinary unit tests deterministic. Run benchmarks in a controlled performance job, store historical results, and alert on a meaningful sustained regression rather than one noisy sample.

## Final Rules

- optimize a measured user-facing objective;
- profile a representative workload;
- fix algorithms and I/O patterns before micro-optimizing syntax;
- distinguish allocation traces from process RSS;
- bound caches, queues, result sets, and concurrency;
- keep correctness tests beside every optimized implementation;
- add native code only after simpler Python improvements are exhausted;
- measure again after every change.
