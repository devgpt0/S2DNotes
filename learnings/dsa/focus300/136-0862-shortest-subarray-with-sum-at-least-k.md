# Focus300 136: LeetCode 862 - Shortest Subarray with Sum at Least K

**Source:** [LeetCode 862](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/)  
**Difficulty:** Hard  
**Pattern:** monotonic deque of prefix sums

## Exact contract

Given a nonempty integer array and positive `k`, return the minimum length of a
nonempty contiguous subarray whose sum is at least `k`, or `-1` if none exists.
The source length is at most 100,000 and values may be negative.

## First principles

Subarray sum `[i, j)` is `prefix[j] - prefix[i]`. For a fixed `j`, an earlier
index with a larger prefix is never better than a later index with a smaller
prefix: it gives a no-larger sum and a longer subarray. A deque retains only
undominated prefix indices in increasing prefix-sum order.


## Classroom board: turn a range into two prefixes

```text
a subarray sum becomes prefix[right] - prefix[left], so one prefix table
replaces many repeated range scans.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- Negative values invalidate ordinary shrinking-window logic.
- The empty prefix at index zero is a valid left boundary.
- Pop every feasible front because later ends can only make it longer.
- Pop larger or equal prefix sums from the back as dominated.
- Return `-1` when the target is never reached.

## Brute force: sum every starting interval

```python
def shortest_subarray_brute(numbers: list[int], target: int) -> int:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 100_000:
        raise ValueError("numbers length must be between 1 and 100000")
    if type(target) is not int or target <= 0:
        raise ValueError("target must be a positive integer")

    answer = len(numbers) + 1
    for left in range(len(numbers)):
        total = 0
        for right in range(left, len(numbers)):
            total += numbers[right]
            if total >= target:
                answer = min(answer, right - left + 1)
                break
    return -1 if answer > len(numbers) else answer
```

This takes `O(n^2)` time and `O(1)` auxiliary space.

## Better approach: query prefix sums in an ordered structure

Coordinate compression plus a tree can find a qualifying earlier prefix in
`O(log n)` per endpoint. The deque is linear because both required orderings
can be maintained as prefixes arrive.

## Expert solution: discard dominated prefix boundaries

```python
from collections import deque


def shortest_subarray(numbers: list[int], target: int) -> int:
    if type(numbers) is not list or any(type(value) is not int for value in numbers):
        raise TypeError("numbers must be a list of integers")
    if not 1 <= len(numbers) <= 100_000:
        raise ValueError("numbers length must be between 1 and 100000")
    if type(target) is not int or target <= 0:
        raise ValueError("target must be a positive integer")

    prefix = [0]
    for value in numbers:
        prefix.append(prefix[-1] + value)

    candidates: deque[int] = deque()
    answer = len(numbers) + 1
    for right, current in enumerate(prefix):
        while candidates and current - prefix[candidates[0]] >= target:
            answer = min(answer, right - candidates.popleft())
        while candidates and prefix[candidates[-1]] >= current:
            candidates.pop()
        candidates.append(right)
    return -1 if answer > len(numbers) else answer
```

Each prefix index enters and leaves the deque at most once. Front removals
produce feasible shortest candidates; back removals eliminate prefixes that
can never beat the current one.

**Complexity:** `O(n)` time and `O(n)` space.
