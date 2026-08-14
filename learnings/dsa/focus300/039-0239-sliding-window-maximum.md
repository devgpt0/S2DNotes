# Focus300 039: LeetCode 239 - Sliding Window Maximum

**Source:** [LeetCode 239 - Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/)  
**Difficulty:** Hard  
**Pattern:** monotone deque of undominated indices  

## Exact contract

For every contiguous window of exactly `window_size` integers, return its
maximum from left to right.

## First principles

When a new value is at least an older value, the older one can never become a
future maximum: it expires earlier and is no larger. Keep only undominated
indices in decreasing-value order. The front is the current maximum.

## Cases that decide correctness

- Window size one returns the input values.
- Window size equal to the input length returns one maximum.
- Equal values may discard the older index safely.
- Expired indices leave from the deque front.
- Invalid or oversized windows fail immediately.

## Brute force: scan every window

```python
def sliding_window_maximum_brute(values: list[int], window_size: int) -> list[int]:
    if (
        any(type(value) is not int for value in values)
        or type(window_size) is not int
        or not 1 <= window_size <= len(values)
    ):
        raise ValueError("invalid values or window_size")
    return [
        max(values[left : left + window_size])
        for left in range(len(values) - window_size + 1)
    ]
```

**Complexity:** `O(n * window_size)` time and `O(window_size)` slice space.

## Better approach: lazy max-heap

```python
from heapq import heappop, heappush


def sliding_window_maximum_heap(values: list[int], window_size: int) -> list[int]:
    if (
        any(type(value) is not int for value in values)
        or type(window_size) is not int
        or not 1 <= window_size <= len(values)
    ):
        raise ValueError("invalid values or window_size")
    heap: list[tuple[int, int]] = []
    result = []
    for index, value in enumerate(values):
        heappush(heap, (-value, index))
        if index + 1 < window_size:
            continue
        window_left = index - window_size + 1
        while heap[0][1] < window_left:
            heappop(heap)
        result.append(-heap[0][0])
    return result
```

Lazy expiration gives `O(n log n)` time and `O(n)` worst-case space.

## Expert solution: decreasing monotone deque

```python
from collections import deque


def sliding_window_maximum(values: list[int], window_size: int) -> list[int]:
    if (
        any(type(value) is not int for value in values)
        or type(window_size) is not int
        or not 1 <= window_size <= len(values)
    ):
        raise ValueError("invalid values or window_size")
    candidates: deque[int] = deque()
    result = []
    for index, value in enumerate(values):
        while candidates and candidates[0] <= index - window_size:
            candidates.popleft()
        while candidates and values[candidates[-1]] <= value:
            candidates.pop()
        candidates.append(index)
        if index + 1 >= window_size:
            result.append(values[candidates[0]])
    return result
```

Deque values decrease from front to back and all indices remain inside the
window. Each index enters and leaves once, making the front exactly the maximum
with linear total work.

**Complexity:** `O(n)` time and `O(window_size)` space.

