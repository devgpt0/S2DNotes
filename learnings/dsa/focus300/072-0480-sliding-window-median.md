# Focus300 072: LeetCode 480 - Sliding Window Median

**Source:** [LeetCode 480](https://leetcode.com/problems/sliding-window-median/)  
**Difficulty:** Hard  
**Pattern:** dual heaps with lazy deletion

## Exact contract

Given a nonempty integer array and `1 <= window_size <= len(numbers)`, return
the median of every consecutive window as floats. Odd windows use their middle
value; even windows use the mean of their two middle values.

## First principles

Maintain a max-heap for the lower half and a min-heap for the upper half. Their
valid sizes differ by at most one, with the lower half holding the extra value.
Python heaps cannot delete an arbitrary outgoing number efficiently, so record
it in a delayed-deletion counter and physically pop it only when it reaches a
heap root.


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

- `window_size = 1` returns every input as a float.
- Duplicate outgoing values require deletion counts, not a set.
- Stale heap entries do not count toward logical heap sizes.
- Even medians may end in `.5`.
- Negative values belong in the same ordering as positive values.

## Brute force: sort every window

```python
def sliding_window_median_brute(numbers: list[int], window_size: int) -> list[float]:
    if not numbers or not 1 <= window_size <= len(numbers):
        raise ValueError("invalid numbers or window size")

    answers: list[float] = []
    for start in range(len(numbers) - window_size + 1):
        ordered = sorted(numbers[start : start + window_size])
        middle = window_size // 2
        if window_size & 1:
            answers.append(float(ordered[middle]))
        else:
            answers.append((ordered[middle - 1] + ordered[middle]) / 2)
    return answers
```

This takes `O(n * k log k)` time and `O(k)` space.

## Better approach: maintain one sorted window

```python
from bisect import bisect_left, insort


def sliding_window_median_sorted(numbers: list[int], window_size: int) -> list[float]:
    if not numbers or not 1 <= window_size <= len(numbers):
        raise ValueError("invalid numbers or window size")

    ordered = sorted(numbers[:window_size])

    def median() -> float:
        middle = window_size // 2
        if window_size & 1:
            return float(ordered[middle])
        return (ordered[middle - 1] + ordered[middle]) / 2

    answers = [median()]
    for right in range(window_size, len(numbers)):
        outgoing = numbers[right - window_size]
        ordered.pop(bisect_left(ordered, outgoing))
        insort(ordered, numbers[right])
        answers.append(median())
    return answers
```

This avoids re-sorting but list insertion and deletion still cost `O(k)`.

## Expert solution: balanced heaps with delayed removals

```python
from collections import Counter
import heapq


def sliding_window_median(numbers: list[int], window_size: int) -> list[float]:
    if not numbers or not 1 <= window_size <= len(numbers):
        raise ValueError("invalid numbers or window size")

    lower: list[int] = []
    upper: list[int] = []
    delayed: Counter[int] = Counter()
    lower_size = 0
    upper_size = 0

    def prune(heap: list[int], is_lower: bool) -> None:
        while heap:
            value = -heap[0] if is_lower else heap[0]
            if delayed[value] == 0:
                return
            heapq.heappop(heap)
            delayed[value] -= 1
            if delayed[value] == 0:
                del delayed[value]

    def rebalance() -> None:
        nonlocal lower_size, upper_size
        if lower_size > upper_size + 1:
            heapq.heappush(upper, -heapq.heappop(lower))
            lower_size -= 1
            upper_size += 1
            prune(lower, True)
        elif lower_size < upper_size:
            heapq.heappush(lower, -heapq.heappop(upper))
            lower_size += 1
            upper_size -= 1
            prune(upper, False)

    def add(value: int) -> None:
        nonlocal lower_size, upper_size
        if not lower or value <= -lower[0]:
            heapq.heappush(lower, -value)
            lower_size += 1
        else:
            heapq.heappush(upper, value)
            upper_size += 1
        rebalance()

    def remove(value: int) -> None:
        nonlocal lower_size, upper_size
        delayed[value] += 1
        if value <= -lower[0]:
            lower_size -= 1
            if value == -lower[0]:
                prune(lower, True)
        else:
            upper_size -= 1
            if upper and value == upper[0]:
                prune(upper, False)
        rebalance()

    def median() -> float:
        if window_size & 1:
            return float(-lower[0])
        return (-lower[0] + upper[0]) / 2

    for value in numbers[:window_size]:
        add(value)
    answers = [median()]
    for right in range(window_size, len(numbers)):
        add(numbers[right])
        remove(numbers[right - window_size])
        answers.append(median())
    return answers
```

Logical sizes preserve the median split even while stale entries remain deeper
in a heap. Root pruning makes every observed boundary valid, and rebalancing
restores the size invariant after each update.

**Complexity:** `O(n log k)` amortized time and `O(k)` logical window space.
