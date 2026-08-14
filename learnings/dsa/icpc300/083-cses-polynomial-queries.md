# ICPC300 083: CSES - Polynomial Queries

**Source:** [CSES - Polynomial Queries](https://cses.fi/problemset/task/1736/)  
**Pattern:** lazy segment tree with affine updates  
**Goal:** Update `[left, right]` by adding `1, 2, ..., right-left+1`, and answer
range sums.

Operations are zero-based `(1, left, right)` updates and `(2, left, right)`
queries.

## 1. First principles

At global index `i`, an update beginning at `left` adds:

```text
i - left + 1 = 1 * i + (1 - left)
```

It is an affine function `slope*i + intercept`. A segment can apply it from
only its length and index sum. Lazy tags add their slopes and intercepts.

## 2. Cases that decide correctness

- Every update restarts at `1` at its own left endpoint.
- Overlapping updates add their affine functions.
- A full segment needs the inclusive index sum.
- Negative intercepts are normal when `left > 1`.
- A one-element update adds exactly `1`.

## 3. Brute force: update each element

```python
def polynomial_queries_brute(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    current = values.copy()
    answers: list[int] = []
    for operation_type, left, right in operations:
        if operation_type == 1:
            for index in range(left, right + 1):
                current[index] += index - left + 1
        elif operation_type == 2:
            answers.append(sum(current[left : right + 1]))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(n)` per operation and `O(n)` space.

## 4. Better: square-root affine tags

Full blocks keep pending slope/intercept tags. Only boundary blocks are pushed
and updated element by element.

```python
from math import isqrt


def polynomial_queries_sqrt(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    current = values.copy()
    block_size = isqrt(len(values)) + 1
    block_count = (len(values) + block_size - 1) // block_size
    block_sum = [0] * block_count
    pending_slope = [0] * block_count
    pending_intercept = [0] * block_count

    def bounds(block: int) -> tuple[int, int]:
        start = block * block_size
        return start, min(start + block_size, len(current))

    def rebuild(block: int) -> None:
        start, end = bounds(block)
        block_sum[block] = sum(current[start:end])

    def push(block: int) -> None:
        slope = pending_slope[block]
        intercept = pending_intercept[block]
        if slope == 0 and intercept == 0:
            return
        start, end = bounds(block)
        for index in range(start, end):
            current[index] += slope * index + intercept
        pending_slope[block] = 0
        pending_intercept[block] = 0

    def apply_full(block: int, slope: int, intercept: int) -> None:
        start, end = bounds(block)
        length = end - start
        index_sum = (start + end - 1) * length // 2
        block_sum[block] += slope * index_sum + intercept * length
        pending_slope[block] += slope
        pending_intercept[block] += intercept

    def update(left: int, right: int) -> None:
        first_block = left // block_size
        last_block = right // block_size
        intercept = 1 - left
        if first_block == last_block:
            push(first_block)
            for index in range(left, right + 1):
                current[index] += index + intercept
            rebuild(first_block)
            return

        push(first_block)
        _, first_end = bounds(first_block)
        for index in range(left, first_end):
            current[index] += index + intercept
        rebuild(first_block)

        for block in range(first_block + 1, last_block):
            apply_full(block, 1, intercept)

        push(last_block)
        last_start, _ = bounds(last_block)
        for index in range(last_start, right + 1):
            current[index] += index + intercept
        rebuild(last_block)

    def query(left: int, right: int) -> int:
        first_block = left // block_size
        last_block = right // block_size
        if first_block == last_block:
            push(first_block)
            return sum(current[left : right + 1])
        push(first_block)
        _, first_end = bounds(first_block)
        total = sum(current[left:first_end])
        total += sum(block_sum[first_block + 1 : last_block])
        push(last_block)
        last_start, _ = bounds(last_block)
        return total + sum(current[last_start : right + 1])

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for operation_type, left, right in operations:
        if operation_type == 1:
            update(left, right)
        elif operation_type == 2:
            answers.append(query(left, right))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(sqrt(n))` per operation and `O(n)` space.

## 5. Expert solution: affine lazy segment tree

```python
def polynomial_queries_lazy_segment_tree(
    values: list[int], operations: list[tuple[int, int, int]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    size = len(values)
    tree = [0] * (4 * size)
    pending_slope = [0] * (4 * size)
    pending_intercept = [0] * (4 * size)

    def build(node: int, low: int, high: int) -> None:
        if low == high:
            tree[node] = values[low]
            return
        middle = (low + high) // 2
        build(2 * node, low, middle)
        build(2 * node + 1, middle + 1, high)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    def apply(node: int, low: int, high: int, slope: int, intercept: int) -> None:
        length = high - low + 1
        index_sum = (low + high) * length // 2
        tree[node] += slope * index_sum + intercept * length
        pending_slope[node] += slope
        pending_intercept[node] += intercept

    def push(node: int, low: int, high: int) -> None:
        if low == high:
            pending_slope[node] = 0
            pending_intercept[node] = 0
            return
        slope = pending_slope[node]
        intercept = pending_intercept[node]
        if slope == 0 and intercept == 0:
            return
        middle = (low + high) // 2
        apply(2 * node, low, middle, slope, intercept)
        apply(2 * node + 1, middle + 1, high, slope, intercept)
        pending_slope[node] = 0
        pending_intercept[node] = 0

    def update(
        node: int, low: int, high: int, left: int, right: int, intercept: int
    ) -> None:
        if left <= low and high <= right:
            apply(node, low, high, 1, intercept)
            return
        push(node, low, high)
        middle = (low + high) // 2
        if left <= middle:
            update(2 * node, low, middle, left, right, intercept)
        if right > middle:
            update(2 * node + 1, middle + 1, high, left, right, intercept)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    def query(node: int, low: int, high: int, left: int, right: int) -> int:
        if left <= low and high <= right:
            return tree[node]
        push(node, low, high)
        middle = (low + high) // 2
        total = 0
        if left <= middle:
            total += query(2 * node, low, middle, left, right)
        if right > middle:
            total += query(2 * node + 1, middle + 1, high, left, right)
        return total

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation_type, left, right in operations:
        if operation_type == 1:
            update(1, 0, size - 1, left, right, 1 - left)
        elif operation_type == 2:
            answers.append(query(1, 0, size - 1, left, right))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

### Why the expert code is correct

Every source update is the same global affine function on its covered range.
Node sums apply that function exactly using the segment's index sum, and lazy
tags preserve the sum of all deferred affine updates.

**Complexity:** `O(log n)` per operation and `O(n)` space.

## 6. What to remember

```text
local sequence 1,2,3,... -> global affine function i + (1-left)
affine range addition composes by adding coefficients
segment increment = slope * index_sum + intercept * length
```
