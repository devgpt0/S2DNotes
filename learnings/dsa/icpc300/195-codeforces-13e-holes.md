# ICPC300 195: Codeforces 13E - Holes

**Source:** [Codeforces 13E - Holes](https://codeforces.com/problemset/problem/13/E)  
**Rating:** 2200  
**Pattern:** square-root decomposition with compressed jumps  
**Goal:** Maintain positive jump lengths. An update changes one length; a query
repeatedly moves from `index` to `index + jump[index]` and returns the last
in-array index and number of jumps before leaving the array.

The code uses zero-based indices; subtract one from source query positions.

## 1. First principles

Split indices into blocks. For every index precompute:

```text
next_index: first reached index outside this block, or n
jump_count: jumps needed to reach next_index
last_index: last visited index before that compressed jump leaves the block
```

Build these values from right to left. A query follows at most one compressed
jump per block. An update changes only summaries earlier in the same block.

## 2. Cases that decide correctness

- Jump lengths must be positive, so every path moves right and terminates.
- A jump directly outside counts as one jump.
- The returned index is the last position inside the array.
- Updating an index affects no later summary in its block.
- Both update and query positions are single indices.

## 3. Brute force: follow every jump

```python
def holes_brute(
    jumps: list[int],
    operations: list[tuple[int, int] | tuple[int, int, int]],
) -> list[tuple[int, int]]:
    if not jumps or any(jump <= 0 for jump in jumps):
        raise ValueError("jumps must be positive")

    current = jumps.copy()
    answers: list[tuple[int, int]] = []
    for operation in operations:
        kind = operation[0]
        if kind == 0:
            if len(operation) != 3:
                raise ValueError("update requires an index and jump")
            index, jump = operation[1:]
            if not 0 <= index < len(current) or jump <= 0:
                raise ValueError("invalid update")
            current[index] = jump
        elif kind == 1:
            if len(operation) != 2:
                raise ValueError("query requires one index")
            index = operation[1]
            if not 0 <= index < len(current):
                raise ValueError("invalid query")
            last = index
            count = 0
            while index < len(current):
                last = index
                index += current[index]
                count += 1
            answers.append((last, count))
        else:
            raise ValueError("operation kind must be zero or one")
    return answers
```

**Complexity:** `O(qn)` time and `O(n+q)` space.

## 4. Better transition: compress within stable blocks

A point update invalidates many earlier jump paths globally but only one block
if every summary stops at its block boundary. Queries then compose those stable
block summaries instead of individual jumps.

## 5. Expert solution: rebuilt block jump summaries

```python
from math import isqrt


def holes_sqrt(
    jumps: list[int],
    operations: list[tuple[int, int] | tuple[int, int, int]],
) -> list[tuple[int, int]]:
    if not jumps or any(jump <= 0 for jump in jumps):
        raise ValueError("jumps must be positive")

    size = len(jumps)
    block_size = isqrt(size) + 1
    current = jumps.copy()
    next_index = [size] * size
    jump_count = [1] * size
    last_index = list(range(size))

    def rebuild(block: int) -> None:
        left = block * block_size
        right = min(size, left + block_size)
        for index in range(right - 1, left - 1, -1):
            target = index + current[index]
            if target >= size or target // block_size != block:
                next_index[index] = min(target, size)
                jump_count[index] = 1
                last_index[index] = index
            else:
                next_index[index] = next_index[target]
                jump_count[index] = jump_count[target] + 1
                last_index[index] = last_index[target]

    block_count = (size + block_size - 1) // block_size
    for block in range(block_count):
        rebuild(block)

    answers: list[tuple[int, int]] = []
    for operation in operations:
        kind = operation[0]
        if kind == 0:
            if len(operation) != 3:
                raise ValueError("update requires an index and jump")
            index, jump = operation[1:]
            if not 0 <= index < size or jump <= 0:
                raise ValueError("invalid update")
            current[index] = jump
            rebuild(index // block_size)
        elif kind == 1:
            if len(operation) != 2:
                raise ValueError("query requires one index")
            index = operation[1]
            if not 0 <= index < size:
                raise ValueError("invalid query")
            last = index
            count = 0
            while index < size:
                count += jump_count[index]
                last = last_index[index]
                index = next_index[index]
            answers.append((last, count))
        else:
            raise ValueError("operation kind must be zero or one")
    return answers
```

### Why the expert code is correct

Right-to-left rebuilding makes every within-block target already correct. Each
summary therefore represents exactly the original jumps until the first block
exit. A query concatenates those exact disjoint path pieces. A point change can
only affect summaries earlier in its own block, all of which are rebuilt.

**Complexity:** `O((n+q) sqrt(n))` time and `O(n+q)` space.

## 6. What to remember

```text
forward jumps -> compute summaries right to left
point update -> rebuild one block
query -> one compressed transition per block
```
