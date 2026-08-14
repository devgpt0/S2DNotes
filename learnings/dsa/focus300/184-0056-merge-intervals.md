# Focus300 184: LeetCode 56 - Merge Intervals

**Source:** [LeetCode 56](https://leetcode.com/problems/merge-intervals/)  
**Difficulty:** Medium  
**Pattern:** sort and sweep closed intervals

## Exact contract

Given nonempty closed intervals `[start, end]`, merge every overlapping pair
and return disjoint intervals covering the same points in ascending start
order. Touching intervals overlap when one end equals the next start.

## First principles

After sorting by start, only the last merged interval can overlap the next
input. If it does, extend its end; otherwise the last interval is final because
all later starts are even larger.

## Cases that decide correctness

- Nested intervals do not shrink the enclosing end.
- Equal endpoints count as overlap for closed intervals.
- Input order is arbitrary.
- The implementation should not mutate caller-owned interval lists.
- Invalid intervals with start greater than end fail fast.

## Brute force: repeatedly merge any overlapping pair

```python
def merge_intervals_brute(intervals: list[list[int]]) -> list[list[int]]:
    if (
        type(intervals) is not list
        or not intervals
        or any(
            type(interval) is not list
            or len(interval) != 2
            or any(type(value) is not int for value in interval)
            for interval in intervals
        )
    ):
        raise TypeError("intervals must be a nonempty list of integer pairs")
    if any(start > end for start, end in intervals):
        raise ValueError("interval starts must not exceed ends")

    merged = [interval.copy() for interval in intervals]
    changed = True
    while changed:
        changed = False
        for first in range(len(merged)):
            for second in range(first + 1, len(merged)):
                if max(merged[first][0], merged[second][0]) <= min(
                    merged[first][1], merged[second][1]
                ):
                    merged[first] = [
                        min(merged[first][0], merged[second][0]),
                        max(merged[first][1], merged[second][1]),
                    ]
                    merged.pop(second)
                    changed = True
                    break
            if changed:
                break
    return sorted(merged)
```

At most `n - 1` merges each scan `O(n^2)` pairs, for `O(n^3)` time.

## Better approach: sweep ordered endpoint events

Counting active intervals across sorted starts and ends also constructs the
union, but closed-end tie ordering is easy to mishandle. Sorting whole
intervals makes the invariant direct.

## Expert solution: merge into the last output interval

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if (
        type(intervals) is not list
        or not intervals
        or any(
            type(interval) is not list
            or len(interval) != 2
            or any(type(value) is not int for value in interval)
            for interval in intervals
        )
    ):
        raise TypeError("intervals must be a nonempty list of integer pairs")
    if any(start > end for start, end in intervals):
        raise ValueError("interval starts must not exceed ends")

    ordered = sorted((start, end) for start, end in intervals)
    answer: list[list[int]] = []
    for start, end in ordered:
        if not answer or start > answer[-1][1]:
            answer.append([start, end])
        else:
            answer[-1][1] = max(answer[-1][1], end)
    return answer
```

Sorting ensures that any overlap involving the next interval must be with the
current output tail. Each interval is then processed exactly once.

**Complexity:** `O(n log n)` time and `O(n)` output space.
