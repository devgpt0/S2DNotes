# Focus300 144: LeetCode 895 - Maximum Frequency Stack

**Source:** [LeetCode 895](https://leetcode.com/problems/maximum-frequency-stack/)  
**Difficulty:** Hard  
**Pattern:** frequency buckets with recency stacks

## Exact contract

Implement `FreqStack`. `push(value)` adds an integer. `pop()` removes and
returns a value with maximum current frequency; when several values share that
frequency, return the one pushed most recently among them. Source operations
never pop an empty stack.

## First principles

When a value's frequency becomes `f`, append it to the stack for frequency `f`.
The top of the highest non-empty frequency stack is exactly the most recent
value among those tied at maximum frequency. Popping it lowers that value's
frequency and may empty the highest bucket.


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

- Frequency is based only on currently active pushes.
- Recency breaks ties after frequency, not before it.
- Repeated pops expose earlier occurrences in their original order.
- The maximum frequency decreases only when its bucket becomes empty.
- A value may appear in several frequency buckets, one record per attained level.

## Brute force: recount and scan backward on every pop

```python
from collections import Counter


class FreqStackBrute:
    def __init__(self) -> None:
        self._values: list[int] = []

    def push(self, value: int) -> None:
        self._values.append(value)

    def pop(self) -> int:
        if not self._values:
            raise IndexError("pop from empty frequency stack")
        frequencies = Counter(self._values)
        maximum = max(frequencies.values())
        for index in range(len(self._values) - 1, -1, -1):
            if frequencies[self._values[index]] == maximum:
                return self._values.pop(index)
        raise RuntimeError("a non-empty stack must have a maximum")
```

`pop` takes `O(n)` time and the active pushes use `O(n)` space.

## Better solution: heap ordered by frequency and time

```python
import heapq


class FreqStackHeap:
    def __init__(self) -> None:
        self._frequency: dict[int, int] = {}
        self._heap: list[tuple[int, int, int]] = []
        self._sequence = 0

    def push(self, value: int) -> None:
        frequency = self._frequency.get(value, 0) + 1
        self._frequency[value] = frequency
        heapq.heappush(self._heap, (-frequency, -self._sequence, value))
        self._sequence += 1

    def pop(self) -> int:
        if not self._heap:
            raise IndexError("pop from empty frequency stack")
        _, _, value = heapq.heappop(self._heap)
        self._frequency[value] -= 1
        return value
```

Each occurrence's heap record captures the frequency it attained and its push
time, giving `O(log n)` operations.

## Expert solution: one recency stack per frequency

```python
class FreqStack:
    def __init__(self) -> None:
        self._frequency: dict[int, int] = {}
        self._groups: dict[int, list[int]] = {}
        self._maximum = 0

    def push(self, value: int) -> None:
        frequency = self._frequency.get(value, 0) + 1
        self._frequency[value] = frequency
        self._groups.setdefault(frequency, []).append(value)
        self._maximum = max(self._maximum, frequency)

    def pop(self) -> int:
        if self._maximum == 0:
            raise IndexError("pop from empty frequency stack")
        value = self._groups[self._maximum].pop()
        self._frequency[value] -= 1
        if not self._groups[self._maximum]:
            del self._groups[self._maximum]
            self._maximum -= 1
        return value
```

The maximum-frequency bucket resolves frequency and recency with one list pop;
no search or reordering remains.

**Complexity:** `O(1)` average time per operation and `O(n)` space.
