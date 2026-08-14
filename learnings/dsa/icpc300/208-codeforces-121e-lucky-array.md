# ICPC300 208: Codeforces 121E - Lucky Array

**Source:** [Codeforces 121E - Lucky Array](https://codeforces.com/problemset/problem/121/E)  
**Difficulty:** 2400  
**Pattern:** lazy range addition with distance-to-next-special repair

## Exact contract

A positive integer is lucky when every decimal digit is `4` or `7`. Maintain a
positive array under zero-based half-open operations:

- `("add", left, right, delta)` adds a nonnegative integer to the interval;
- `("count", left, right, 0)` counts lucky values in the interval.

Return all count answers.

## First principles

For each value store `next_lucky(value) - value`. Adding `delta` subtracts it
from every stored distance, so ordinary range-add lazy propagation applies.
A zero distance means the value is lucky. A negative distance means an update
crossed the recorded lucky number; descend only through negative-minimum nodes
and recompute those leaves against their next lucky number.

## Cases that decide correctness

- Landing exactly on a lucky value leaves distance zero and increments counts.
- One update may skip several lucky values; leaf repair uses the actual value.
- Pending additions must reach a repaired leaf exactly once.
- Count queries never need to repair because every update repairs negatives.
- Only nonnegative additions preserve the next-lucky distance invariant.

## Brute force: update values directly

```python
def lucky_array_brute(
    values: list[int], operations: list[tuple[str, int, int, int]]
) -> list[int]:
    if not values or any(type(value) is not int or value < 1 for value in values):
        raise ValueError("values must be positive integers")

    def is_lucky(value: int) -> bool:
        return all(digit in "47" for digit in str(value))

    current = values.copy()
    answers: list[int] = []
    for action, left, right, argument in operations:
        if (
            type(left) is not int
            or type(right) is not int
            or not 0 <= left < right <= len(current)
        ):
            raise ValueError("invalid interval")
        if action == "add":
            if type(argument) is not int or argument < 0:
                raise ValueError("delta must be nonnegative")
            for index in range(left, right):
                current[index] += argument
        elif action == "count":
            if type(argument) is not int or argument != 0:
                raise ValueError("count uses zero as its unused argument")
            answers.append(sum(is_lucky(value) for value in current[left:right]))
        else:
            raise ValueError("unknown operation")
    return answers
```

Every operation can touch the complete array.

## Better approach: no separate intermediate

Square-root blocks can defer full-block additions, but counting exact lucky
targets still needs per-block ordered-value maintenance. The segment tree below
uses the stronger distance invariant and repairs only leaves that cross a
target.

## Expert solution: minimum distance and selective leaf repair

```python
from bisect import bisect_left


def lucky_array(
    values: list[int], operations: list[tuple[str, int, int, int]]
) -> list[int]:
    if not values or any(type(value) is not int or value < 1 for value in values):
        raise ValueError("values must be positive integers")
    maximum_possible = max(values)
    for action, left, right, argument in operations:
        if (
            type(left) is not int
            or type(right) is not int
            or not 0 <= left < right <= len(values)
        ):
            raise ValueError("invalid interval")
        if action == "add":
            if type(argument) is not int or argument < 0:
                raise ValueError("delta must be nonnegative")
            maximum_possible += argument
        elif action == "count":
            if type(argument) is not int or argument != 0:
                raise ValueError("count uses zero as its unused argument")
        else:
            raise ValueError("unknown operation")
    if maximum_possible > 10**18:
        raise ValueError("values exceed the supported source bound")

    digit_count = len(str(maximum_possible)) + 1
    generation_limit = 10**digit_count
    lucky: list[int] = []
    stack = [4, 7]
    while stack:
        value = stack.pop()
        if value >= generation_limit:
            continue
        lucky.append(value)
        stack.append(value * 10 + 4)
        stack.append(value * 10 + 7)
    lucky.sort()

    size = len(values)
    materialized = values.copy()
    minimum = [0] * (4 * size)
    minimum_count = [0] * (4 * size)
    lazy = [0] * (4 * size)

    def next_distance(value: int) -> int:
        index = bisect_left(lucky, value)
        if index == len(lucky):
            raise RuntimeError("lucky generation limit is too small")
        return lucky[index] - value

    def pull(node: int) -> None:
        minimum[node] = min(minimum[node * 2], minimum[node * 2 + 1])
        minimum_count[node] = 0
        if minimum[node * 2] == minimum[node]:
            minimum_count[node] += minimum_count[node * 2]
        if minimum[node * 2 + 1] == minimum[node]:
            minimum_count[node] += minimum_count[node * 2 + 1]

    def apply(node: int, addition: int) -> None:
        minimum[node] -= addition
        lazy[node] += addition

    def build(node: int, left: int, right: int) -> None:
        if right - left == 1:
            minimum[node] = next_distance(materialized[left])
            minimum_count[node] = 1
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle, right)
        pull(node)

    def push(node: int) -> None:
        if lazy[node]:
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = 0

    def add(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        addition: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            apply(node, addition)
            return
        push(node)
        middle = (left + right) // 2
        add(node * 2, left, middle, query_left, query_right, addition)
        add(node * 2 + 1, middle, right, query_left, query_right, addition)
        pull(node)

    def repair(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> None:
        if query_right <= left or right <= query_left or minimum[node] >= 0:
            return
        if right - left == 1:
            materialized[left] += lazy[node]
            lazy[node] = 0
            minimum[node] = next_distance(materialized[left])
            minimum_count[node] = 1
            return
        push(node)
        middle = (left + right) // 2
        repair(node * 2, left, middle, query_left, query_right)
        repair(node * 2 + 1, middle, right, query_left, query_right)
        pull(node)

    def count(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> int:
        if query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return minimum_count[node] if minimum[node] == 0 else 0
        push(node)
        middle = (left + right) // 2
        return count(node * 2, left, middle, query_left, query_right) + count(
            node * 2 + 1, middle, right, query_left, query_right
        )

    build(1, 0, size)
    answers: list[int] = []
    for action, left, right, argument in operations:
        if action == "add":
            add(1, 0, size, left, right, argument)
            repair(1, 0, size, left, right)
        else:
            answers.append(count(1, 0, size, left, right))
    return answers
```

Every stored minimum is the least nonnegative distance to a recorded next lucky
value after repair. Range addition preserves distances algebraically; negative
nodes identify exactly the leaves whose target was crossed.

**Complexity:** `O((n+q) log n + R log n)` time, where `R` is the total number
of crossed lucky targets, and `O(n)` segment-tree space.
