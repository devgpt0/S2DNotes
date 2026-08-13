# Profiling and Performance Optimization

## 1. Define the performance requirement

Optimize a metric, not a feeling. Common targets are latency percentiles,
throughput, CPU time, peak memory, allocation count, and startup time.

```python
def unique_count(values: list[int]) -> int:
    return len(set(values))


print(unique_count([1, 1, 2, 3, 3]))
```

Output:

```text
3
```

Correctness must be fixed before speed is compared.

## 2. Wall time and CPU time answer different questions

`time.perf_counter()` measures elapsed wall time. `time.process_time()` measures
CPU time used by the current process. Their numeric results depend on the
machine and workload, so do not document an exact universal duration.

```python
from time import perf_counter

started = perf_counter()
result = sum(range(10_000))
elapsed = perf_counter() - started

print(result)
print(elapsed >= 0.0)
```

Output:

```text
49995000
True
```

The Boolean is stable; the duration is intentionally not printed.

## 3. Use `timeit` for small repeatable operations

`timeit` repeats code and reduces common timer mistakes. Run it from the same
environment used for both candidates.

```bash
python -m timeit -s "values = list(range(1000))" "999 in values"
```

The command prints platform-dependent timing statistics. Record the command,
Python version, input, repeat count, and full result in benchmark evidence.

Do not use `timeit` for an end-to-end service request that depends on networks,
databases, or caches.

## 4. Use `cProfile` to locate CPU hot paths

```bash
python -m cProfile -s cumulative app.py
```

The report includes call counts and measured times. Start with high cumulative
time, then inspect whether that function is doing necessary work.

For a reusable report:

```bash
python -m cProfile -o profile.pstats app.py
python -m pstats profile.pstats
```

These are contextual commands: the exact report depends on `app.py`.

## 5. Use `tracemalloc` for Python allocation evidence

Start tracing before the workload, take snapshots around the operation, and
compare them. Traced sizes vary, so print stable facts in teaching examples.

```python
import tracemalloc

tracemalloc.start()
before = tracemalloc.take_snapshot()
values = [value for value in range(1_000)]
after = tracemalloc.take_snapshot()

print(len(values))
print(isinstance(after.compare_to(before, "lineno"), list))
tracemalloc.stop()
```

Output:

```text
1000
True
```

`tracemalloc` observes Python allocations, not every allocation made by native
libraries or the operating system.

## 6. Prefer algorithmic improvements

Choose a data structure that matches the operation.

```python
allowed_ids = {10, 20, 30}
requested_ids = [20, 40]

print([item for item in requested_ids if item in allowed_ids])
```

Output:

```text
[20]
```

Set membership is average-case O(1); scanning a list is O(n). This matters more
than small syntax changes when membership is repeated over large data.

## 7. Build trustworthy benchmarks

- Use representative inputs and include cold-start behavior when it matters.
- Compare multiple runs and report distribution, not only the fastest run.
- Isolate unrelated background work when possible.
- Warm caches only if production uses warm caches.
- Keep outputs and side effects equivalent.
- Change one factor at a time.
- Reject a faster change that violates correctness, memory, or maintainability.

Microbenchmarks can explain a mechanism; they do not predict whole-system
performance by themselves.

## 8. Optimization order

| Order | Action |
| ---: | --- |
| 1 | remove unnecessary work |
| 2 | improve the algorithm or data structure |
| 3 | batch I/O and reduce serialization or copying |
| 4 | use optimized built-ins or libraries |
| 5 | apply appropriate concurrency |
| 6 | compile only the remaining measured hot path |

## 9. Mental model

```text
requirement -> baseline -> profile -> smallest change -> tests -> new baseline
```

A performance claim without its workload and measurement method is not
reproducible evidence.

## 10. Benchmark process-level noise

For important microbenchmarks, the third-party `pyperf` project can run worker
processes, calibrate iterations, retain metadata, and compare result files. It
does not make an unrepresentative workload meaningful.

Record CPU model, operating system, Python build, dependency versions, affinity
or container limits, and whether the system was thermally or operationally
stable. Keep raw benchmark artifacts so later comparisons use the same statistic
instead of selected console lines.

## 11. Profile production with the least intrusive tool

Deterministic profilers observe every selected event and are useful in controlled
runs. Sampling profilers perturb hot code less and are often better for live
systems. `sys.monitoring` enables lower-impact event instrumentation for tooling
on Python 3.12+.

Always measure profiler overhead, protect captured arguments and stack data, and
remove diagnostic hooks after the investigation.
