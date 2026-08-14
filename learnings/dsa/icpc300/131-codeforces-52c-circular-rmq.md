# 131. Circular RMQ — Codeforces 52C

**Source:** [Codeforces 52C - Circular RMQ](https://codeforces.com/problemset/problem/52/C)  
**Difficulty:** 2200

## 1. Problem in plain words

An array is indexed from `0` to `n - 1`. Each operation is either `left right delta`, which adds `delta` to a circular interval, or `left right`, which asks for that interval's minimum. If `left > right`, the interval wraps through index `n - 1` and index `0`. Print every query answer.

## 2. First principles

A wrapped interval is exactly two ordinary intervals: `[left, n - 1]` and `[0, right]`. The remaining problem is range addition plus range minimum. A lazy segment tree stores a minimum for every segment and postpones a full-segment addition in one lazy value.

## 3. Cases that define correctness

- `left == right` touches one element.
- `left > right` must update or query both pieces of the wrapped interval.
- Additions may be negative, so a minimum never changes monotonically.
- A full-array wrapped operation can touch both end pieces without overlap.

## 4. Brute force

Visit every index in the circular interval. This is useful as a small-instance oracle.

```python
def circular_rmq_brute_force(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    data = values.copy()
    answers: list[int] = []
    size = len(data)

    for operation in operations:
        if len(operation) not in (2, 3):
            raise ValueError("an operation must contain two or three integers")
        left, right = operation[:2]
        if not 0 <= left < size or not 0 <= right < size:
            raise ValueError("interval endpoint is outside the array")

        indices = (
            range(left, right + 1)
            if left <= right
            else list(range(left, size)) + list(range(right + 1))
        )
        if len(operation) == 3:
            delta = operation[2]
            for index in indices:
                data[index] += delta
        else:
            answers.append(min(data[index] for index in indices))

    return answers
```

For `q` operations this costs `O(nq)` time in the worst case and `O(n)` space.

## 5. Better approach: square-root decomposition

Split the array into blocks. Keep each block's minimum and a pending addition. A whole block is changed in `O(1)`; only the two boundary fragments are visited element by element.

```python
from math import isqrt


def circular_rmq_sqrt(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    size = len(values)
    block_size = isqrt(size) + 1
    block_count = (size + block_size - 1) // block_size
    data = values.copy()
    lazy = [0] * block_count
    block_min = [10**30] * block_count

    def rebuild(block: int) -> None:
        start = block * block_size
        end = min(size, start + block_size)
        block_min[block] = min(data[start:end])

    for block in range(block_count):
        rebuild(block)

    def add(left: int, right: int, delta: int) -> None:
        touched: set[int] = set()
        while left <= right and left % block_size:
            data[left] += delta
            touched.add(left // block_size)
            left += 1
        while left + block_size - 1 <= right:
            block = left // block_size
            lazy[block] += delta
            left += block_size
        while left <= right:
            data[left] += delta
            touched.add(left // block_size)
            left += 1
        for block in touched:
            rebuild(block)

    def minimum(left: int, right: int) -> int:
        answer = 10**30
        while left <= right and left % block_size:
            answer = min(answer, data[left] + lazy[left // block_size])
            left += 1
        while left + block_size - 1 <= right:
            block = left // block_size
            answer = min(answer, block_min[block] + lazy[block])
            left += block_size
        while left <= right:
            answer = min(answer, data[left] + lazy[left // block_size])
            left += 1
        return answer

    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (2, 3):
            raise ValueError("an operation must contain two or three integers")
        left, right = operation[:2]
        if not 0 <= left < size or not 0 <= right < size:
            raise ValueError("interval endpoint is outside the array")
        pieces = [(left, right)] if left <= right else [(left, size - 1), (0, right)]
        if len(operation) == 3:
            for start, end in pieces:
                add(start, end, operation[2])
        else:
            answers.append(min(minimum(start, end) for start, end in pieces))

    return answers
```

Each operation takes `O(sqrt(n))` time and the structure uses `O(n)` space.

## 6. Expert solution: lazy segment tree

For a fully covered node, increase both its stored minimum and its lazy tag. Push the tag only before descending into children. Split a circular interval before calling the ordinary range functions.

```python
def circular_rmq(values: list[int], operations: list[tuple[int, ...]]) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    size = len(values)
    tree = [0] * (4 * size)
    lazy = [0] * (4 * size)

    def build(node: int, left: int, right: int) -> None:
        if left == right:
            tree[node] = values[left]
            return
        middle = (left + right) // 2
        build(node * 2, left, middle)
        build(node * 2 + 1, middle + 1, right)
        tree[node] = min(tree[node * 2], tree[node * 2 + 1])

    def push(node: int) -> None:
        delta = lazy[node]
        if delta == 0:
            return
        for child in (node * 2, node * 2 + 1):
            tree[child] += delta
            lazy[child] += delta
        lazy[node] = 0

    def add(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        delta: int,
    ) -> None:
        if query_left <= left and right <= query_right:
            tree[node] += delta
            lazy[node] += delta
            return
        push(node)
        middle = (left + right) // 2
        if query_left <= middle:
            add(node * 2, left, middle, query_left, query_right, delta)
        if middle < query_right:
            add(node * 2 + 1, middle + 1, right, query_left, query_right, delta)
        tree[node] = min(tree[node * 2], tree[node * 2 + 1])

    def minimum(
        node: int, left: int, right: int, query_left: int, query_right: int
    ) -> int:
        if query_left <= left and right <= query_right:
            return tree[node]
        push(node)
        middle = (left + right) // 2
        answer = 10**30
        if query_left <= middle:
            answer = minimum(node * 2, left, middle, query_left, query_right)
        if middle < query_right:
            answer = min(
                answer,
                minimum(node * 2 + 1, middle + 1, right, query_left, query_right),
            )
        return answer

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation in operations:
        if len(operation) not in (2, 3):
            raise ValueError("an operation must contain two or three integers")
        left, right = operation[:2]
        if not 0 <= left < size or not 0 <= right < size:
            raise ValueError("interval endpoint is outside the array")
        pieces = [(left, right)] if left <= right else [(left, size - 1), (0, right)]
        if len(operation) == 3:
            for start, end in pieces:
                add(1, 0, size - 1, start, end, operation[2])
        else:
            answers.append(
                min(minimum(1, 0, size - 1, start, end) for start, end in pieces)
            )

    return answers
```

## 7. Why the expert solution is correct

Every circular operation is split into exactly its non-wrapping pieces. Each tree node stores the minimum after applying its own pending addition; pushing transfers that addition to both children without changing any represented value. Therefore range updates change exactly the requested elements, and a query combines minima from a disjoint cover of exactly the requested interval.

Time is `O((n + q) log n)` and space is `O(n)`.
