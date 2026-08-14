# ICPC300 231: Codeforces 487B - Strip

**Source:** [Codeforces 487B - Strip](https://codeforces.com/problemset/problem/487/B)  
**Difficulty:** 2300  
**Pattern:** monotone validity window plus range-minimum partition DP

## Exact contract

Partition an integer array into the fewest contiguous segments. Every segment
must have length at least `minimum_length` and `max(segment)-min(segment) <=
maximum_difference`. Return `-1` when no partition exists.

## First principles

For each right endpoint, monotone max/min deques find the smallest start whose
window satisfies the difference bound. Every later start is also valid. If a
segment ends at `right`, its start must lie in
`[smallest_valid, right-minimum_length+1]`; minimize the prefix DP on that
interval.

## Cases that decide correctness

- Length exactly `minimum_length` is allowed.
- Equal values remain in both monotone deques by index.
- Expired prefix-DP candidates must leave when the validity boundary advances.
- An unreachable prefix never becomes a heap candidate.
- The complete prefix may remain unreachable even when some windows are valid.

## Brute force: try every next segment

```python
from functools import cache


def strip_brute(values: list[int], maximum_difference: int, minimum_length: int) -> int:
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be a nonempty integer list")
    if type(maximum_difference) is not int or maximum_difference < 0:
        raise ValueError("maximum_difference must be nonnegative")
    if type(minimum_length) is not int or minimum_length < 1:
        raise ValueError("minimum_length must be positive")

    @cache
    def solve(start: int) -> int:
        if start == len(values):
            return 0
        best = len(values) + 1
        minimum = maximum = values[start]
        for end in range(start, len(values)):
            minimum = min(minimum, values[end])
            maximum = max(maximum, values[end])
            if (
                end - start + 1 >= minimum_length
                and maximum - minimum <= maximum_difference
            ):
                suffix = solve(end + 1)
                if suffix <= len(values):
                    best = min(best, suffix + 1)
        return best

    answer = solve(0)
    return -1 if answer > len(values) else answer
```

The number of partitions is exponential before memoization and `O(n^2)` after
memoization.

## Better approach: quadratic prefix DP

Testing every segment start for every endpoint gives `O(n^2)` DP. The expert
method makes both the valid-start interval and its minimum incremental.

## Expert solution: two deques and a candidate heap

```python
from collections import deque
from heapq import heappop, heappush


def minimum_strip_segments(
    values: list[int], maximum_difference: int, minimum_length: int
) -> int:
    if not values or any(type(value) is not int for value in values):
        raise ValueError("values must be a nonempty integer list")
    if type(maximum_difference) is not int or maximum_difference < 0:
        raise ValueError("maximum_difference must be nonnegative")
    if type(minimum_length) is not int or minimum_length < 1:
        raise ValueError("minimum_length must be positive")

    size = len(values)
    infinity = size + 1
    partitions = [infinity] * (size + 1)
    partitions[0] = 0
    increasing: deque[int] = deque()
    decreasing: deque[int] = deque()
    candidates: list[tuple[int, int]] = []
    smallest_valid = 0

    for right, value in enumerate(values):
        while increasing and values[increasing[-1]] >= value:
            increasing.pop()
        increasing.append(right)
        while decreasing and values[decreasing[-1]] <= value:
            decreasing.pop()
        decreasing.append(right)

        while values[decreasing[0]] - values[increasing[0]] > maximum_difference:
            if increasing[0] == smallest_valid:
                increasing.popleft()
            if decreasing[0] == smallest_valid:
                decreasing.popleft()
            smallest_valid += 1

        newest_start = right - minimum_length + 1
        if newest_start >= 0 and partitions[newest_start] < infinity:
            heappush(candidates, (partitions[newest_start], newest_start))
        while candidates and candidates[0][1] < smallest_valid:
            heappop(candidates)
        if newest_start >= smallest_valid and candidates:
            partitions[right + 1] = candidates[0][0] + 1

    return -1 if partitions[size] == infinity else partitions[size]
```

The deques maintain the exact earliest valid start. The heap contains precisely
reachable starts old enough to meet the length bound and discards starts once
they become invalid.

**Complexity:** `O(n log n)` time and `O(n)` space.
