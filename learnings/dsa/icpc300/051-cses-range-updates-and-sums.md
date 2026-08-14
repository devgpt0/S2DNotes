# ICPC300 051: CSES - Range Updates and Sums

**Source:** [CSES - Range Updates and Sums](https://cses.fi/problemset/task/1735/)  
**Pattern:** lazy segment tree with assignment and addition  
**Goal:** Support range addition, range assignment, and range-sum queries.

The implementations use zero-based inclusive ranges. Operations are
`(1, left, right, value)` for addition, `(2, left, right, value)` for
assignment, and `(3, left, right)` for a sum.

## 1. First principles

A full segment update should change one stored segment total instead of every
leaf. A **lazy tag** records the update that descendants must receive later.

Assignment and addition compose differently:

```text
old pending work, then assign x -> discard old work; pending value is x
pending assignment x, then add y -> pending assignment becomes x + y
pending addition x, then add y   -> pending addition becomes x + y
```

Push a tag before descending into only part of its segment.

## 2. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Assign after add | Assignment replaces the earlier values and pending add. |
| Add after assign | Increase the pending assigned value. |
| Partial update after full update | Push the parent tag before visiting children. |
| Negative update | Segment sums may decrease. |
| One-element range | Behave like a point operation. |

## 3. Brute force: update every element

```python
def range_updates_and_sums_brute(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    current = values.copy()
    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, left, right, value = operation
            for index in range(left, right + 1):
                current[index] += value
        elif operation_type == 2:
            _, left, right, value = operation
            for index in range(left, right + 1):
                current[index] = value
        elif operation_type == 3:
            _, left, right = operation
            answers.append(sum(current[left : right + 1]))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(n)` per operation in the worst case and `O(n)` space.

## 4. Better: square-root decomposition

Split the array into blocks. Full blocks keep a sum plus lazy assignment/add
tags; only boundary blocks are materialized element by element.

```python
from math import isqrt


def range_updates_and_sums_sqrt(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    current = values.copy()
    block_size = isqrt(len(values)) + 1
    block_count = (len(values) + block_size - 1) // block_size
    block_sum = [0] * block_count
    pending_add = [0] * block_count
    pending_set: list[int | None] = [None] * block_count

    def bounds(block: int) -> tuple[int, int]:
        start = block * block_size
        return start, min(start + block_size, len(current))

    def rebuild(block: int) -> None:
        start, end = bounds(block)
        block_sum[block] = sum(current[start:end])

    def push(block: int) -> None:
        start, end = bounds(block)
        assigned_value = pending_set[block]
        if assigned_value is not None:
            for index in range(start, end):
                current[index] = assigned_value
            pending_set[block] = None
        added_value = pending_add[block]
        if added_value != 0:
            for index in range(start, end):
                current[index] += added_value
            pending_add[block] = 0

    def apply_full(block: int, operation_type: int, value: int) -> None:
        start, end = bounds(block)
        if operation_type == 1:
            pending_add[block] += value
            block_sum[block] += value * (end - start)
        else:
            pending_set[block] = value
            pending_add[block] = 0
            block_sum[block] = value * (end - start)

    def update(operation_type: int, left: int, right: int, value: int) -> None:
        first_block = left // block_size
        last_block = right // block_size
        if first_block == last_block:
            push(first_block)
            for index in range(left, right + 1):
                if operation_type == 1:
                    current[index] += value
                else:
                    current[index] = value
            rebuild(first_block)
            return

        push(first_block)
        _, first_end = bounds(first_block)
        for index in range(left, first_end):
            if operation_type == 1:
                current[index] += value
            else:
                current[index] = value
        rebuild(first_block)

        for block in range(first_block + 1, last_block):
            apply_full(block, operation_type, value)

        push(last_block)
        last_start, _ = bounds(last_block)
        for index in range(last_start, right + 1):
            if operation_type == 1:
                current[index] += value
            else:
                current[index] = value
        rebuild(last_block)

    def range_sum(left: int, right: int) -> int:
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
    for operation in operations:
        operation_type = operation[0]
        if operation_type in (1, 2):
            _, left, right, value = operation
            update(operation_type, left, right, value)
        elif operation_type == 3:
            _, left, right = operation
            answers.append(range_sum(left, right))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(sqrt(n))` per operation and `O(n)` space.

## 5. Expert solution: lazy segment tree

Each node stores its segment sum. A pending assignment is applied before a
pending addition; this implementation absorbs a later addition directly into
the assigned value.

```python
def range_updates_and_sums_lazy(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values:
        raise ValueError("values must not be empty")

    size = len(values)
    tree = [0] * (4 * size)
    pending_add = [0] * (4 * size)
    pending_set: list[int | None] = [None] * (4 * size)

    def build(node: int, low: int, high: int) -> None:
        if low == high:
            tree[node] = values[low]
            return
        middle = (low + high) // 2
        build(2 * node, low, middle)
        build(2 * node + 1, middle + 1, high)
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    def apply_set(node: int, low: int, high: int, value: int) -> None:
        tree[node] = value * (high - low + 1)
        pending_set[node] = value
        pending_add[node] = 0

    def apply_add(node: int, low: int, high: int, value: int) -> None:
        tree[node] += value * (high - low + 1)
        assigned_value = pending_set[node]
        if assigned_value is not None:
            pending_set[node] = assigned_value + value
        else:
            pending_add[node] += value

    def push(node: int, low: int, high: int) -> None:
        if low == high:
            pending_set[node] = None
            pending_add[node] = 0
            return
        middle = (low + high) // 2
        assigned_value = pending_set[node]
        if assigned_value is not None:
            apply_set(2 * node, low, middle, assigned_value)
            apply_set(2 * node + 1, middle + 1, high, assigned_value)
            pending_set[node] = None
        added_value = pending_add[node]
        if added_value != 0:
            apply_add(2 * node, low, middle, added_value)
            apply_add(2 * node + 1, middle + 1, high, added_value)
            pending_add[node] = 0

    def update(
        node: int,
        low: int,
        high: int,
        query_left: int,
        query_right: int,
        value: int,
        is_assignment: bool,
    ) -> None:
        if query_left <= low and high <= query_right:
            if is_assignment:
                apply_set(node, low, high, value)
            else:
                apply_add(node, low, high, value)
            return
        push(node, low, high)
        middle = (low + high) // 2
        if query_left <= middle:
            update(
                2 * node,
                low,
                middle,
                query_left,
                query_right,
                value,
                is_assignment,
            )
        if query_right > middle:
            update(
                2 * node + 1,
                middle + 1,
                high,
                query_left,
                query_right,
                value,
                is_assignment,
            )
        tree[node] = tree[2 * node] + tree[2 * node + 1]

    def query(
        node: int,
        low: int,
        high: int,
        query_left: int,
        query_right: int,
    ) -> int:
        if query_left <= low and high <= query_right:
            return tree[node]
        push(node, low, high)
        middle = (low + high) // 2
        total = 0
        if query_left <= middle:
            total += query(2 * node, low, middle, query_left, query_right)
        if query_right > middle:
            total += query(
                2 * node + 1,
                middle + 1,
                high,
                query_left,
                query_right,
            )
        return total

    build(1, 0, size - 1)
    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type in (1, 2):
            _, left, right, value = operation
            update(
                1,
                0,
                size - 1,
                left,
                right,
                value,
                operation_type == 2,
            )
        elif operation_type == 3:
            _, left, right = operation
            answers.append(query(1, 0, size - 1, left, right))
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

### Why the expert code is correct

- Every node sum includes its own pending tag, so a fully covered query can
  return immediately.
- `push` gives both children the parent's operations in their original order.
- Partial updates recurse only after pushing, then rebuild the parent from the
  exact child sums.

**Complexity:** `O(log n)` per operation and `O(n)` space.

## 6. What to remember

```text
assignment overrides older tags
addition composes with either assignment or addition
push before partial descent; keep the node sum already updated
```
