# Focus300 135: LeetCode 857 - Minimum Cost to Hire K Workers

**Source:** [LeetCode 857](https://leetcode.com/problems/minimum-cost-to-hire-k-workers/)  
**Difficulty:** Hard  
**Pattern:** ratio sweep with a bounded max-heap

## Exact contract

Choose exactly `k` workers. Worker `i` has positive quality `quality[i]` and
requires at least `wage[i]`; all chosen workers must be paid at one common rate
per quality unit. Return the minimum total cost. The arrays have equal length
at most 10,000 and `1 <= k <= n`.

## First principles

For a chosen group, the smallest legal common rate is the maximum
`wage[i] / quality[i]` in that group. If workers are processed by increasing
required ratio, the current worker supplies that maximum. The cheapest group
at that ratio uses the `k` smallest qualities seen so far.

## Cases that decide correctness

- Paying below any selected worker's ratio is invalid.
- Exactly `k` workers are chosen, not at most `k`.
- Equal ratios remain valid in any processing order.
- A max-heap removes the largest quality when more than `k` are available.
- Exact rational comparisons avoid ratio-ordering errors.

## Brute force: evaluate every k-worker group

```python
from fractions import Fraction
from itertools import combinations


def minimum_hiring_cost_brute(
    quality: list[int], wage: list[int], worker_count: int
) -> float:
    if (
        type(quality) is not list
        or type(wage) is not list
        or any(type(value) is not int for value in quality + wage)
    ):
        raise TypeError("quality and wage must be lists of integers")
    if (
        len(quality) != len(wage)
        or not 1 <= len(quality) <= 10_000
        or type(worker_count) is not int
        or not 1 <= worker_count <= len(quality)
    ):
        raise ValueError("arrays and worker_count violate source bounds")
    if any(value <= 0 for value in quality + wage):
        raise ValueError("qualities and wages must be positive")

    best: Fraction | None = None
    for group in combinations(range(len(quality)), worker_count):
        rate = max(Fraction(wage[index], quality[index]) for index in group)
        cost = rate * sum(quality[index] for index in group)
        if best is None or cost < best:
            best = cost
    if best is None:
        raise RuntimeError("a valid group must exist")
    return float(best)
```

This checks `C(n, k)` groups and spends `O(k)` time on each.

## Better approach: rescan earlier qualities for each ratio

After sorting ratios, select the `k - 1` smallest prior qualities for every
possible maximum-ratio worker. Sorting or scanning that prefix repeatedly is
quadratic; a heap maintains the same selection incrementally.

## Expert solution: keep the k smallest qualities seen

```python
from fractions import Fraction
from heapq import heappop, heappush


def minimum_hiring_cost(
    quality: list[int], wage: list[int], worker_count: int
) -> float:
    if (
        type(quality) is not list
        or type(wage) is not list
        or any(type(value) is not int for value in quality + wage)
    ):
        raise TypeError("quality and wage must be lists of integers")
    if (
        len(quality) != len(wage)
        or not 1 <= len(quality) <= 10_000
        or type(worker_count) is not int
        or not 1 <= worker_count <= len(quality)
    ):
        raise ValueError("arrays and worker_count violate source bounds")
    if any(value <= 0 for value in quality + wage):
        raise ValueError("qualities and wages must be positive")

    workers = sorted(
        (Fraction(required, worker_quality), worker_quality)
        for worker_quality, required in zip(quality, wage, strict=True)
    )
    largest_quality: list[int] = []
    quality_sum = 0
    best: Fraction | None = None
    for rate, worker_quality in workers:
        quality_sum += worker_quality
        heappush(largest_quality, -worker_quality)
        if len(largest_quality) > worker_count:
            quality_sum += heappop(largest_quality)
        if len(largest_quality) == worker_count:
            cost = rate * quality_sum
            if best is None or cost < best:
                best = cost
    if best is None:
        raise RuntimeError("a valid group must exist")
    return float(best)
```

At each candidate maximum ratio, the heap contains the lowest possible total
quality among processed workers. Multiplying those two values gives the best
group whose limiting ratio is at most the current one.

**Complexity:** `O(n log n)` time and `O(k)` heap space.
