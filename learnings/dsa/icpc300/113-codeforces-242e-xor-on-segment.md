# ICPC300 113: Codeforces 242E - XOR on Segment

**Source:** [Codeforces 242E - XOR on Segment](https://codeforces.com/problemset/problem/242/E)  
**Pattern:** lazy segment tree with per-bit counts  
**Goal:** Support range XOR updates and range-sum queries.

Operations use zero-based inclusive ranges: `(1, left, right)` queries and
`(2, left, right, mask)` updates. Values and masks are nonnegative.

## 1. First principles

Sum is not directly stable under XOR. Store how many values have each bit set.
If an XOR mask contains bit `b`, every value flips that bit:

```text
new_ones[b] = segment_length - old_ones[b]
```

XOR lazy tags compose with XOR, so repeated pending masks combine exactly.

## 2. Cases that decide correctness

- Applying the same mask twice cancels it.
- Only set bits in the mask flip counts.
- Partial updates must push the parent mask first.
- A zero mask changes nothing.
- The bit width must include every initial value and update mask.

## 3. Brute force: update every value

```python
def xor_on_segment_brute(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonempty and nonnegative")

    current = values.copy()
    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        if operation_type == 1:
            _, left, right = operation
            answers.append(sum(current[left : right + 1]))
        elif operation_type == 2:
            _, left, right, mask = operation
            if mask < 0:
                raise ValueError("XOR masks must be nonnegative")
            for index in range(left, right + 1):
                current[index] ^= mask
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(n)` per operation and `O(n)` space.

## 4. Better: square-root blocks with XOR tags

Each block stores per-bit counts and one pending XOR mask. Boundary blocks are
materialized; full blocks flip counts directly.

```python
from math import isqrt


def xor_on_segment_sqrt(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonempty and nonnegative")

    maximum = max(values)
    for operation in operations:
        if operation[0] == 2:
            maximum = max(maximum, operation[3])
    bit_count = max(1, maximum.bit_length())
    current = values.copy()
    block_size = isqrt(len(values)) + 1
    block_count = (len(values) + block_size - 1) // block_size
    ones = [[0] * bit_count for _ in range(block_count)]
    pending_xor = [0] * block_count

    def bounds(block: int) -> tuple[int, int]:
        start = block * block_size
        return start, min(start + block_size, len(current))

    def rebuild(block: int) -> None:
        ones[block] = [0] * bit_count
        start, end = bounds(block)
        for index in range(start, end):
            for bit in range(bit_count):
                ones[block][bit] += (current[index] >> bit) & 1

    def push(block: int) -> None:
        mask = pending_xor[block]
        if mask == 0:
            return
        start, end = bounds(block)
        for index in range(start, end):
            current[index] ^= mask
        pending_xor[block] = 0
        rebuild(block)

    def apply_full(block: int, mask: int) -> None:
        start, end = bounds(block)
        for bit in range(bit_count):
            if mask & (1 << bit):
                ones[block][bit] = end - start - ones[block][bit]
        pending_xor[block] ^= mask

    def block_sum(block: int) -> int:
        return sum(count << bit for bit, count in enumerate(ones[block]))

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for operation in operations:
        operation_type = operation[0]
        left = operation[1]
        right = operation[2]
        first_block = left // block_size
        last_block = right // block_size
        if operation_type == 1:
            if first_block == last_block:
                push(first_block)
                answers.append(sum(current[left : right + 1]))
                continue
            push(first_block)
            _, first_end = bounds(first_block)
            total = sum(current[left:first_end])
            total += sum(
                block_sum(block) for block in range(first_block + 1, last_block)
            )
            push(last_block)
            last_start, _ = bounds(last_block)
            answers.append(total + sum(current[last_start : right + 1]))
        elif operation_type == 2:
            mask = operation[3]
            if mask < 0:
                raise ValueError("XOR masks must be nonnegative")
            if first_block == last_block:
                push(first_block)
                for index in range(left, right + 1):
                    current[index] ^= mask
                rebuild(first_block)
                continue
            push(first_block)
            _, first_end = bounds(first_block)
            for index in range(left, first_end):
                current[index] ^= mask
            rebuild(first_block)
            for block in range(first_block + 1, last_block):
                apply_full(block, mask)
            push(last_block)
            last_start, _ = bounds(last_block)
            for index in range(last_start, right + 1):
                current[index] ^= mask
            rebuild(last_block)
        else:
            raise ValueError(f"unknown operation type: {operation_type}")
    return answers
```

**Complexity:** `O(sqrt(n) * bits)` per operation and `O(n + sqrt(n)*bits)`
space.

## 5. Expert solution: per-bit lazy segment tree

```python
def xor_on_segment_lazy(
    values: list[int], operations: list[tuple[int, ...]]
) -> list[int]:
    if not values or any(value < 0 for value in values):
        raise ValueError("values must be nonempty and nonnegative")

    maximum = max(values)
    for operation in operations:
        if operation[0] == 2:
            maximum = max(maximum, operation[3])
    bit_count = max(1, maximum.bit_length())
    size = len(values)
    ones = [[0] * (4 * size) for _ in range(bit_count)]
    pending_xor = [0] * (4 * size)

    def build(node: int, low: int, high: int) -> None:
        if low == high:
            for bit in range(bit_count):
                ones[bit][node] = (values[low] >> bit) & 1
            return
        middle = (low + high) // 2
        build(2 * node, low, middle)
        build(2 * node + 1, middle + 1, high)
        for bit in range(bit_count):
            ones[bit][node] = ones[bit][2 * node] + ones[bit][2 * node + 1]

    def apply(node: int, low: int, high: int, mask: int) -> None:
        for bit in range(bit_count):
            if mask & (1 << bit):
                ones[bit][node] = high - low + 1 - ones[bit][node]
        pending_xor[node] ^= mask

    def push(node: int, low: int, high: int) -> None:
        mask = pending_xor[node]
        if mask == 0 or low == high:
            return
        middle = (low + high) // 2
        apply(2 * node, low, middle, mask)
        apply(2 * node + 1, middle + 1, high, mask)
        pending_xor[node] = 0

    def update(
        node: int, low: int, high: int, left: int, right: int, mask: int
    ) -> None:
        if left <= low and high <= right:
            apply(node, low, high, mask)
            return
        push(node, low, high)
        middle = (low + high) // 2
        if left <= middle:
            update(2 * node, low, middle, left, right, mask)
        if right > middle:
            update(2 * node + 1, middle + 1, high, left, right, mask)
        for bit in range(bit_count):
            ones[bit][node] = ones[bit][2 * node] + ones[bit][2 * node + 1]

    def query(node: int, low: int, high: int, left: int, right: int) -> int:
        if left <= low and high <= right:
            return sum(ones[bit][node] << bit for bit in range(bit_count))
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
    for operation in operations:
        if operation[0] == 1:
            _, left, right = operation
            answers.append(query(1, 0, size - 1, left, right))
        elif operation[0] == 2:
            _, left, right, mask = operation
            if mask < 0:
                raise ValueError("XOR masks must be nonnegative")
            update(1, 0, size - 1, left, right, mask)
        else:
            raise ValueError(f"unknown operation type: {operation[0]}")
    return answers
```

### Why the expert code is correct

Each node's bit counts exactly reconstruct its segment sum. Applying XOR flips
precisely the selected bit counts, and XOR-composed lazy tags preserve the
effect of every deferred update.

**Complexity:** `O(bits * log n)` per operation and `O(bits * n)` space.

## 6. What to remember

```text
range XOR does not update sums uniformly
store count of ones per bit
XOR bit set -> ones becomes segment_length - ones
```
