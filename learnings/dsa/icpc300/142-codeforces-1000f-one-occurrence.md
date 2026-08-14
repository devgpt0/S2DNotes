# 142. One Occurrence — Codeforces 1000F

**Source:** [Codeforces 1000F - One Occurrence](https://codeforces.com/problemset/problem/1000/F)  
**Difficulty:** 2200

## 1. Problem in plain words

For every subarray query `[left, right]`, print any value occurring exactly once in that subarray. Print `0` if no such value exists.

The functions below use zero-based inclusive endpoints.

## 2. First principles

Process queries by increasing right endpoint. At that moment, keep only the latest occurrence position of every value. At latest position `i`, store that value's previous occurrence `previous[i]`.

For query `[l, r]`, a latest position `i` in the interval represents a unique value exactly when `previous[i] < l`. A range-minimum tree over stored previous positions can find such a candidate.

## 3. Cases that define correctness

- Returning any unique value is accepted; answers need not be deterministic across methods.
- A value repeated inside the query has its latest previous occurrence at least `left`.
- Occurrences before `left` do not prevent uniqueness inside the query.
- `0` is the required failure output and source values are positive.

## 4. Brute force

Count the subarray and return its first value with frequency one.

```python
from collections import Counter


def one_occurrence_brute_force(
    values: list[int], queries: list[tuple[int, int]]
) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    answers: list[int] = []
    for left, right in queries:
        if not 0 <= left <= right < len(values):
            raise ValueError("invalid query")
        counts = Counter(values[left : right + 1])
        answers.append(
            next((value for value in values[left : right + 1] if counts[value] == 1), 0)
        )
    return answers
```

Worst-case time is `O(nq)` and temporary space is `O(n)`.

## 5. Better approach: Mo's algorithm

Order queries so adjacent windows differ little. Maintain value frequencies and a set containing exactly the frequency-one values.

```python
from math import isqrt


def one_occurrence_mo(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    size = len(values)
    block_size = isqrt(size) + 1
    ordered: list[tuple[int, int, int]] = []
    for index, (left, right) in enumerate(queries):
        if not 0 <= left <= right < size:
            raise ValueError("invalid query")
        ordered.append((left, right, index))
    ordered.sort(
        key=lambda item: (
            item[0] // block_size,
            item[1] if item[0] // block_size % 2 == 0 else -item[1],
        )
    )

    frequency: dict[int, int] = {}
    singletons: set[int] = set()

    def change(position: int, delta: int) -> None:
        value = values[position]
        old = frequency.get(value, 0)
        if old == 1:
            singletons.remove(value)
        new = old + delta
        if new < 0:
            raise RuntimeError("negative frequency")
        if new == 0:
            frequency.pop(value)
        else:
            frequency[value] = new
        if new == 1:
            singletons.add(value)

    answers = [0] * len(queries)
    current_left = 0
    current_right = -1
    for left, right, query_index in ordered:
        while current_left > left:
            current_left -= 1
            change(current_left, 1)
        while current_right < right:
            current_right += 1
            change(current_right, 1)
        while current_left < left:
            change(current_left, -1)
            current_left += 1
        while current_right > right:
            change(current_right, -1)
            current_right -= 1
        answers[query_index] = next(iter(singletons), 0)
    return answers
```

The standard bound is `O((n + q) sqrt(n))` window changes and `O(n + q)` space.

## 6. Expert solution: offline previous-occurrence minimum

Sort queries by `right`. On a new occurrence, disable the old latest position and store the old position at the new latest position. Query the minimum stored previous occurrence in `[left, right]`.

```python
def one_occurrence(values: list[int], queries: list[tuple[int, int]]) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    size = len(values)
    ordered: list[tuple[int, int, int]] = []
    for index, (left, right) in enumerate(queries):
        if not 0 <= left <= right < size:
            raise ValueError("invalid query")
        ordered.append((right, left, index))
    ordered.sort()

    leaf_count = 1
    while leaf_count < size:
        leaf_count *= 2
    infinity = size + 1
    tree = [(infinity, -1)] * (2 * leaf_count)

    def update(position: int, previous: int) -> None:
        node = position + leaf_count
        tree[node] = (previous, position)
        node //= 2
        while node:
            tree[node] = min(tree[node * 2], tree[node * 2 + 1])
            node //= 2

    def range_minimum(left: int, right: int) -> tuple[int, int]:
        left += leaf_count
        right += leaf_count + 1
        answer = (infinity, -1)
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

    answers = [0] * len(queries)
    last_position: dict[int, int] = {}
    query_pointer = 0
    for right, value in enumerate(values):
        previous = last_position.get(value, -1)
        if previous != -1:
            update(previous, infinity)
        update(right, previous)
        last_position[value] = right

        while query_pointer < len(ordered) and ordered[query_pointer][0] == right:
            _, left, query_index = ordered[query_pointer]
            previous_occurrence, position = range_minimum(left, right)
            if previous_occurrence < left:
                answers[query_index] = values[position]
            query_pointer += 1
    return answers
```

## 7. Why the expert solution is correct

At each processed right endpoint, exactly the latest position of every seen value remains enabled. If that position lies in the query, the value occurs exactly once there precisely when its preceding occurrence lies before `left`. The range minimum is below `left` iff at least one such value exists, and its stored position identifies a valid answer.

Time is `O((n + q) log n)` and space is `O(n + q)`.
