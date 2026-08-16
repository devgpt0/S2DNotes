# Focus300 109: LeetCode 757 - Set Intersection Size At Least Two

**Source:** [LeetCode 757](https://leetcode.com/problems/set-intersection-size-at-least-two/)  
**Difficulty:** Hard  
**Pattern:** interval-end greedy with two retained points

## Exact contract

Given integer intervals `[start, end]` with `start < end`, find the minimum size
of an integer set such that every interval contains at least two set elements.
Intervals are closed and endpoints lie between `0` and `10^8`.

## First principles

Process intervals by increasing right endpoint. When an interval needs new
points, choosing the largest available values leaves them usable for the most
future intervals. For equal right endpoints, process the interval with the
larger left endpoint first because it is more restrictive.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- Intervals are closed, so both endpoints belong to an interval.
- Every source interval contains at least two distinct integers.
- Two already selected points inside an interval require no addition.
- Exactly one selected point requires adding the current right endpoint.
- Equal ends must be ordered by decreasing starts.

## Brute force: enumerate candidate subsets

```python
from itertools import combinations


def intersection_size_two_brute(intervals: list[list[int]]) -> int:
    if not intervals or any(
        len(interval) != 2 or not 0 <= interval[0] < interval[1] <= 100_000_000
        for interval in intervals
    ):
        raise ValueError("intervals must satisfy 0 <= start < end <= 1e8")

    first = min(interval[0] for interval in intervals)
    last = max(interval[1] for interval in intervals)
    candidates = range(first, last + 1)
    for size in range(2, last - first + 2):
        for selected in combinations(candidates, size):
            if all(
                sum(start <= value <= end for value in selected) >= 2
                for start, end in intervals
            ):
                return size
    raise RuntimeError("source constraints guarantee a solution")
```

This is exact but explores exponentially many subsets of the covered integer
range.

## Better solution: store the complete selected set

```python
def intersection_size_two_set(intervals: list[list[int]]) -> int:
    if not intervals or any(
        len(interval) != 2 or not 0 <= interval[0] < interval[1] <= 100_000_000
        for interval in intervals
    ):
        raise ValueError("intervals must satisfy 0 <= start < end <= 1e8")

    selected: set[int] = set()
    for start, end in sorted(
        ((interval[0], interval[1]) for interval in intervals),
        key=lambda interval: (interval[1], -interval[0]),
    ):
        covered = sum(start <= value <= end for value in selected)
        candidate = end
        while covered < 2:
            if candidate not in selected:
                selected.add(candidate)
                covered += 1
            candidate -= 1
    return len(selected)
```

The greedy choices are correct, but recounting the full selected set makes this
`O(n^2)` after sorting.

## Expert solution: retain only the two largest selected points

```python
def intersection_size_two(intervals: list[list[int]]) -> int:
    if not intervals or any(
        len(interval) != 2 or not 0 <= interval[0] < interval[1] <= 100_000_000
        for interval in intervals
    ):
        raise ValueError("intervals must satisfy 0 <= start < end <= 1e8")

    second_last = -2
    last = -1
    answer = 0
    for start, end in sorted(
        ((interval[0], interval[1]) for interval in intervals),
        key=lambda interval: (interval[1], -interval[0]),
    ):
        if start > last:
            second_last = end - 1
            last = end
            answer += 2
        elif start > second_last:
            second_last = last
            last = end
            answer += 1
    return answer
```

Because right endpoints never decrease, `second_last` and `last` are the two
largest selected points. If either lies left of the current interval, every
earlier selected point does too. Adding `end - 1, end` or just `end` is therefore
both necessary now and optimal for all remaining intervals.

**Complexity:** `O(n log n)` time for sorting and `O(n)` space for the sorted
intervals (`O(1)` additional state after sorting).
