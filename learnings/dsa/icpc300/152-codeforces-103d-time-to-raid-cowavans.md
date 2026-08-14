# ICPC300 152: Codeforces 103D - Time to Raid Cowavans

**Source:** [Codeforces 103D - Time to Raid Cowavans](https://codeforces.com/problemset/problem/103/D)  
**Rating:** 2200  
**Pattern:** square-root split on arithmetic-progression step  
**Goal:** For every zero-based query `(start, step)`, return
`values[start] + values[start + step] + ...` while indices remain in the array.
The source's one-based `start` is converted at the boundary.

## 1. First principles

For a fixed step,

```text
sum[start] = values[start] + sum[start + step]
```

A small step has many terms per query but only about `sqrt(n)` possible step
values, so precompute all of them. A large step has fewer than `sqrt(n)` terms,
so walking that query directly is already cheap.

## 2. Cases that decide correctness

- `step` must be positive; otherwise the progression never advances.
- `start` must name an existing element.
- A step larger than the array returns only `values[start]`.
- Negative array values are valid because this is an ordinary sum.
- Repeated queries must keep their original output order.

## 3. Brute force: walk every query

```python
def cowavan_sums_brute(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if not values:
        raise ValueError("values must be nonempty")
    answers: list[int] = []
    for start, step in queries:
        if not 0 <= start < len(values) or step <= 0:
            raise ValueError("invalid query")
        total = 0
        for index in range(start, len(values), step):
            total += values[index]
        answers.append(total)
    return answers
```

**Complexity:** `O(sum(n / step))` time and `O(q)` output space.

## 4. Better: one suffix DP per queried step

```python
def cowavan_sums_grouped(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must be nonempty")
    grouped: dict[int, list[tuple[int, int]]] = {}
    for query_index, (start, step) in enumerate(queries):
        if not 0 <= start < len(values) or step <= 0:
            raise ValueError("invalid query")
        grouped.setdefault(step, []).append((query_index, start))

    answers = [0] * len(queries)
    for step, requests in grouped.items():
        suffix = [0] * len(values)
        for index in range(len(values) - 1, -1, -1):
            suffix[index] = values[index]
            if index + step < len(values):
                suffix[index] += suffix[index + step]
        for query_index, start in requests:
            answers[query_index] = suffix[start]
    return answers
```

**Complexity:** `O(n * distinct_steps + q)` time and `O(n+q)` space.

## 5. Expert solution: small-step table, large-step walks

```python
from math import isqrt


def cowavan_sums_sqrt(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if not values:
        raise ValueError("values must be nonempty")
    for start, step in queries:
        if not 0 <= start < len(values) or step <= 0:
            raise ValueError("invalid query")

    threshold = isqrt(len(values)) + 1
    small = [[0] * len(values) for _ in range(threshold)]
    needed_steps = {step for _, step in queries if step < threshold}
    for step in needed_steps:
        for index in range(len(values) - 1, -1, -1):
            small[step][index] = values[index]
            if index + step < len(values):
                small[step][index] += small[step][index + step]

    answers: list[int] = []
    for start, step in queries:
        if step < threshold:
            answers.append(small[step][start])
            continue
        total = 0
        for index in range(start, len(values), step):
            total += values[index]
        answers.append(total)
    return answers
```

### Why the expert code is correct

The small-step recurrence contains exactly the same progression as a direct
walk, with its first term separated. Large-step queries are evaluated directly.
Every query enters exactly one branch, and both branches sum precisely its
requested indices.

**Complexity:** `O((n+q) sqrt(n))` time and `O(n sqrt(n) + q)` space.

## 6. What to remember

```text
small step -> expensive query, few possible steps -> precompute
large step -> many possible steps, few visited indices -> scan
split at sqrt(n) -> balanced total work
```
