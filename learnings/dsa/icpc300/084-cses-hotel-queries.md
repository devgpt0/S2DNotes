# ICPC300 084: CSES - Hotel Queries

**Source:** [CSES - Hotel Queries](https://cses.fi/problemset/task/1143/)  
**Pattern:** segment-tree first feasible position  
**Goal:** For each group, choose the first hotel with enough free rooms, reduce
that hotel's capacity, and report its index.

These functions return zero-based indices and `-1` when no hotel fits. The
source prints one-based indices and `0` for failure.

## 1. First principles

A segment stores the maximum remaining capacity in its range. If that maximum
is below the group size, the whole segment is impossible. Otherwise descend
left first; only try the right child when the left maximum is too small.

## 2. Cases that decide correctness

- Selection is first fit, not the smallest sufficient capacity.
- A hotel with capacity exactly equal to the group is valid.
- Failed groups change no capacity.
- Repeated assignments see earlier capacity reductions.
- Left-child feasibility must take priority over every right index.

## 3. Brute force: scan hotels from the start

```python
def hotel_queries_brute(capacities: list[int], groups: list[int]) -> list[int]:
    if any(capacity < 0 for capacity in capacities) or any(
        group <= 0 for group in groups
    ):
        raise ValueError("capacities must be nonnegative and groups positive")

    remaining = capacities.copy()
    answers: list[int] = []
    for group in groups:
        assigned = -1
        for hotel, capacity in enumerate(remaining):
            if capacity >= group:
                remaining[hotel] -= group
                assigned = hotel
                break
        answers.append(assigned)
    return answers
```

**Complexity:** `O(nm)` time for `m` groups and `O(n)` space.

## 4. Better: square-root block maxima

Skip blocks whose maximum is too small, then scan the first feasible block.

```python
from math import isqrt


def hotel_queries_sqrt(capacities: list[int], groups: list[int]) -> list[int]:
    if any(capacity < 0 for capacity in capacities) or any(
        group <= 0 for group in groups
    ):
        raise ValueError("capacities must be nonnegative and groups positive")
    if not capacities:
        return [-1] * len(groups)

    remaining = capacities.copy()
    block_size = isqrt(len(remaining)) + 1
    block_count = (len(remaining) + block_size - 1) // block_size
    block_maximum = [0] * block_count

    def rebuild(block: int) -> None:
        start = block * block_size
        end = min(start + block_size, len(remaining))
        block_maximum[block] = max(remaining[start:end])

    for block in range(block_count):
        rebuild(block)

    answers: list[int] = []
    for group in groups:
        assigned = -1
        for block in range(block_count):
            if block_maximum[block] < group:
                continue
            start = block * block_size
            end = min(start + block_size, len(remaining))
            for hotel in range(start, end):
                if remaining[hotel] >= group:
                    remaining[hotel] -= group
                    assigned = hotel
                    rebuild(block)
                    break
            break
        answers.append(assigned)
    return answers
```

**Complexity:** `O((n + m) sqrt(n))` time and `O(n)` space.

## 5. Expert solution: maximum segment tree

```python
def hotel_queries_segment_tree(capacities: list[int], groups: list[int]) -> list[int]:
    if any(capacity < 0 for capacity in capacities) or any(
        group <= 0 for group in groups
    ):
        raise ValueError("capacities must be nonnegative and groups positive")
    if not capacities:
        return [-1] * len(groups)

    size = 1
    while size < len(capacities):
        size *= 2
    tree = [0] * (2 * size)
    tree[size : size + len(capacities)] = capacities
    for node in range(size - 1, 0, -1):
        tree[node] = max(tree[2 * node], tree[2 * node + 1])

    answers: list[int] = []
    for group in groups:
        if tree[1] < group:
            answers.append(-1)
            continue

        node = 1
        while node < size:
            if tree[2 * node] >= group:
                node *= 2
            else:
                node = 2 * node + 1

        hotel = node - size
        tree[node] -= group
        node //= 2
        while node > 0:
            tree[node] = max(tree[2 * node], tree[2 * node + 1])
            node //= 2
        answers.append(hotel)
    return answers
```

### Why the expert code is correct

The root detects whether any hotel fits. At each level, choosing the left child
when feasible preserves the first-fit requirement; otherwise every left index
is impossible and the right child contains a feasible hotel.

**Complexity:** `O(n)` construction, `O(log n)` per group, and `O(n)` space.

## 6. What to remember

```text
first position satisfying threshold
store range maximum
descend left when feasible, otherwise right
```
