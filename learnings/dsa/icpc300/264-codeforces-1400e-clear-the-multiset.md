# ICPC300 264: Codeforces 1400E - Clear the Multiset

**Source:** [Codeforces 1400E - Clear the Multiset](https://codeforces.com/problemset/problem/1400/E)  
**Rating:** 2200  
**Pattern:** divide at a range minimum  
**Goal:** Turn every nonnegative array value into zero. One operation either
sets one position to zero or subtracts one from every value in a positive
contiguous segment. Minimize the operations.

## 1. First principles

For an interval currently reduced to a common baseline, there are two complete
choices:

1. clear every position separately, costing the interval length;
2. lower the whole interval to its minimum, then solve the positive pieces
   separated by minimum positions.

Choosing one minimum position as the split is enough. Other equal minima are
handled by zero-cost descendant levels.

## 2. Cases that decide correctness

- An all-zero interval costs zero.
- Equal minima may create empty child intervals.
- The horizontal cost is `minimum - baseline`, not the absolute minimum.
- Clearing positions separately remains available at every recursive interval.
- An iterative traversal avoids recursion failure on monotone arrays.

## 3. Brute force: breadth-first search over arrays

```python
from collections import deque


def clear_multiset_brute(values: list[int]) -> int:
    if not values or any(type(value) is not int or value < 0 for value in values):
        raise ValueError("values must be nonnegative integers")
    start = tuple(values)
    target = (0,) * len(values)
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        state, distance = queue.popleft()
        if state == target:
            return distance
        for index, value in enumerate(state):
            if value:
                changed = list(state)
                changed[index] = 0
                next_state = tuple(changed)
                if next_state not in seen:
                    seen.add(next_state)
                    queue.append((next_state, distance + 1))
        for left in range(len(state)):
            if state[left] == 0:
                continue
            for right in range(left, len(state)):
                if state[right] == 0:
                    break
                changed = list(state)
                for index in range(left, right + 1):
                    changed[index] -= 1
                next_state = tuple(changed)
                if next_state not in seen:
                    seen.add(next_state)
                    queue.append((next_state, distance + 1))
    raise RuntimeError("zero state must be reachable")
```

**Complexity:** exponential in the array length and total height.

## 4. Better approach: scan for every recursive minimum

The recurrence can scan each interval to find its minimum. It uses only linear
extra stack space but takes `O(n^2)` time on a monotone array.

## 5. Expert solution: range-minimum tree and iterative recurrence

```python
def minimum_clear_operations(values: list[int]) -> int:
    if not values or any(type(value) is not int or value < 0 for value in values):
        raise ValueError("values must be nonnegative integers")

    leaf_count = 1
    while leaf_count < len(values):
        leaf_count *= 2
    tree = [(10**30, -1)] * (2 * leaf_count)
    for index, value in enumerate(values):
        tree[leaf_count + index] = (value, index)
    for index in range(leaf_count - 1, 0, -1):
        tree[index] = min(tree[2 * index], tree[2 * index + 1])

    def range_minimum(left: int, right: int) -> tuple[int, int]:
        left += leaf_count
        right += leaf_count
        answer = (10**30, -1)
        while left < right:
            if left & 1:
                answer = min(answer, tree[left])
                left += 1
            if right & 1:
                right -= 1
                answer = min(answer, tree[right])
            left //= 2
            right //= 2
        return answer

    results: dict[tuple[int, int, int], int] = {}
    stack = [(0, len(values), 0, False, -1)]
    while stack:
        left, right, baseline, expanded, minimum_index = stack.pop()
        key = (left, right, baseline)
        if left >= right:
            results[key] = 0
            continue
        if not expanded:
            minimum, minimum_index = range_minimum(left, right)
            stack.append((left, right, baseline, True, minimum_index))
            stack.append((minimum_index + 1, right, minimum, False, -1))
            stack.append((left, minimum_index, minimum, False, -1))
            continue

        minimum = values[minimum_index]
        horizontal = minimum - baseline
        horizontal += results[(left, minimum_index, minimum)]
        horizontal += results[(minimum_index + 1, right, minimum)]
        results[key] = min(right - left, horizontal)
    return results[(0, len(values), 0)]
```

### Why the expert code is correct

Any solution either clears every surviving position individually or performs
enough whole-interval decrements to reach its minimum before treating the
separated positive parts. These exhaustive choices are exactly the recurrence;
the range-minimum tree changes only how its split is found.

**Complexity:** `O(n log n)` time and `O(n)` space.

## 6. What to remember

```text
vertical choice -> interval length
horizontal choice -> minimum minus baseline plus child pieces
take the smaller choice at every minimum split
```
