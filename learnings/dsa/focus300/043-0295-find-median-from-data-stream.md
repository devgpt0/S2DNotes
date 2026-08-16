# Focus300 043: LeetCode 295 - Find Median from Data Stream

**Source:** [LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/)  
**Difficulty:** Hard  
**Pattern:** balanced max-heap and min-heap

## Exact contract

Implement a stateful `MedianFinder`. `add_num(value)` inserts one integer.
`find_median()` returns the middle value as `float` after an odd number of
insertions or the mean of the two middle values after an even number. LeetCode
calls `find_median` only after at least one insertion; the code fails explicitly
if that precondition is violated.

## First principles

Split the stream into a lower half and upper half. Keep every lower value no
greater than every upper value, and keep the lower half the same size as the
upper half or one element larger. The median is then exposed at the heap roots.


## Classroom board: keep only the useful unfinished work

```text
a stack stores the part of the state that can still matter after the next step.
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

- Duplicate and negative values are retained.
- The first inserted value is the median.
- Even stream length averages two roots.
- Rebalancing may move one value between heaps after every insertion.
- Integer sums are converted to a floating-point median.

## Brute force: keep the entire stream sorted

```python
from bisect import insort


class MedianFinderSorted:
    def __init__(self) -> None:
        self.values: list[int] = []

    def add_num(self, value: int) -> None:
        insort(self.values, value)

    def find_median(self) -> float:
        if not self.values:
            raise ValueError("at least one value is required")
        middle = len(self.values) // 2
        if len(self.values) & 1:
            return float(self.values[middle])
        return (self.values[middle - 1] + self.values[middle]) / 2
```

Insertion costs `O(n)` because list elements shift; median lookup is `O(1)`.

## Better transition: expose only the two middle boundaries

Values below the median need not be internally sorted beyond their maximum;
values above it need only expose their minimum. Two heaps maintain exactly
those boundaries and rebalance in logarithmic time.

## Expert solution: two balanced heaps

```python
import heapq


class MedianFinder:
    def __init__(self) -> None:
        self.lower: list[int] = []
        self.upper: list[int] = []

    def add_num(self, value: int) -> None:
        heapq.heappush(self.lower, -value)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def find_median(self) -> float:
        if not self.lower:
            raise ValueError("at least one value is required")
        if len(self.lower) > len(self.upper):
            return float(-self.lower[0])
        return (-self.lower[0] + self.upper[0]) / 2
```

Moving the largest lower candidate through the upper heap establishes ordering.
The final rebalance preserves the size invariant, so the one or two median
values are always the heap roots.

**Complexity:** `O(log n)` per insertion, `O(1)` per median query, and `O(n)`
space.
