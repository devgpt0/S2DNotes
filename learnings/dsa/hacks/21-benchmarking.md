# Benchmark Before Optimizing

## First principles

Optimization needs evidence. Benchmark the operation that dominates the real
solution, at realistic sizes, after a warm-up, and compare outputs as well as
time. A faster wrong program is not an improvement.

## Why it matters

Guessing about Python performance wastes contest time. A small benchmark can
confirm whether the intended complexity has enough margin.

## Technique

Use `perf_counter` around the computation, not input generation or printing.

```python
from time import perf_counter

values = build_worst_case()
start = perf_counter()
answer = solve_values(values)
elapsed = perf_counter() - start
print(f'{elapsed:.3f}s', file=sys.stderr)
```

For microbenchmarks outside a submission:

```python
from timeit import timeit

elapsed = timeit('sum(values)', globals={'values': list(range(100_000))}, number=100)
```

## Steps

1. Confirm asymptotic complexity first.
2. Build near-maximum and worst-shape input.
3. Warm up once if the environment benefits.
4. Run several times and use the slow result, not the lucky best.
5. Optimize the measured bottleneck only.

## Pattern recognition

Benchmark when Python is near the likely time limit, when choosing between two
same-complexity representations, or after profiling exposes a hot loop.

## Expert habit

Keep comfortable margin for judge hardware and interpreter differences. An
algorithm taking almost the full limit locally is not reliable.

## Visual worked example: isolate one decision

Question: list queue or deque for `200,000` removals?

```text
same generated items
        |
        +-> version A: list.pop(0)
        |
        +-> version B: deque.popleft()
        |
verify identical removal order
measure several complete runs
compare median, not one noisy sample
```

The complexity prediction already favors `deque`; the benchmark confirms the
constant factors in the actual environment.

## Traps

- Benchmarking tiny inputs dominated by startup overhead.
- Timing debug output or random generation with the algorithm.
- Micro-optimizing an `O(n^2)` solution that requires `O(n log n)`.
- Assuming CPython and PyPy perform every workload the same way.
