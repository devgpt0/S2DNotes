# Focus300 137: LeetCode 864 - Shortest Path to Get All Keys

**Source:** [LeetCode 864](https://leetcode.com/problems/shortest-path-to-get-all-keys/)  
**Difficulty:** Hard  
**Pattern:** BFS over position and key-mask states

## Exact contract

In a rectangular grid, `@` is the unique start, `#` is a wall, `a..f` are
keys, and `A..F` are locks passable only after collecting the matching key.
Move one orthogonal step per turn. Return the minimum steps to collect every
key, or `-1` if impossible.

## First principles

Position alone is not a complete state: returning to the same cell with more
keys can unlock new paths. A six-bit mask records collected keys. The resulting
state graph is unweighted, so BFS finds the minimum number of moves.

## Cases that decide correctness

- With no keys, the answer is zero at the start.
- Walking onto a key updates the mask before the next state is recorded.
- A lock without its key bit is impassable.
- The same cell may need exploration under different masks.
- Walls and grid boundaries are never states.

## Brute force: retain a visited-state set per route

```python
from collections import deque


def shortest_key_path_brute(grid: list[str]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 30
        or any(
            type(row) is not str or not row or len(row) != len(grid[0]) or len(row) > 30
            for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangular list of strings")
    allowed = set("@.#abcdefABCDEF")
    if any(character not in allowed for row in grid for character in row):
        raise ValueError("grid contains an invalid character")
    starts = [
        (row, column)
        for row, line in enumerate(grid)
        for column, character in enumerate(line)
        if character == "@"
    ]
    if len(starts) != 1:
        raise ValueError("grid must contain exactly one start")

    all_keys = 0
    for row in grid:
        for character in row:
            if "a" <= character <= "f":
                all_keys |= 1 << (ord(character) - ord("a"))
    start_row, start_column = starts[0]
    start_state = (start_row, start_column, 0)
    queue = deque([(start_row, start_column, 0, 0, frozenset({start_state}))])
    while queue:
        row, column, keys, distance, route = queue.popleft()
        if keys == all_keys:
            return distance
        for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_step
            next_column = column + column_step
            if not (0 <= next_row < len(grid) and 0 <= next_column < len(grid[0])):
                continue
            cell = grid[next_row][next_column]
            if cell == "#" or (
                "A" <= cell <= "F" and not keys & (1 << (ord(cell) - ord("A")))
            ):
                continue
            next_keys = keys
            if "a" <= cell <= "f":
                next_keys |= 1 << (ord(cell) - ord("a"))
            state = (next_row, next_column, next_keys)
            if state not in route:
                queue.append(
                    (next_row, next_column, next_keys, distance + 1, route | {state})
                )
    return -1
```

This enumerates simple paths in the state graph and can take exponential time
and space.

## Better approach: search between points of interest

Precompute distances between the start and keys under lock constraints, then
run subset DP. Direct state BFS is simpler because locks make those distances
depend on the current key mask.

## Expert solution: globally merge equal position-and-mask states

```python
from collections import deque


def shortest_key_path(grid: list[str]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 30
        or any(
            type(row) is not str or not row or len(row) != len(grid[0]) or len(row) > 30
            for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangular list of strings")
    allowed = set("@.#abcdefABCDEF")
    if any(character not in allowed for row in grid for character in row):
        raise ValueError("grid contains an invalid character")
    starts = [
        (row, column)
        for row, line in enumerate(grid)
        for column, character in enumerate(line)
        if character == "@"
    ]
    if len(starts) != 1:
        raise ValueError("grid must contain exactly one start")

    all_keys = 0
    for row in grid:
        for character in row:
            if "a" <= character <= "f":
                all_keys |= 1 << (ord(character) - ord("a"))
    start_row, start_column = starts[0]
    queue = deque([(start_row, start_column, 0, 0)])
    seen = {(start_row, start_column, 0)}
    while queue:
        row, column, keys, distance = queue.popleft()
        if keys == all_keys:
            return distance
        for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_step
            next_column = column + column_step
            if not (0 <= next_row < len(grid) and 0 <= next_column < len(grid[0])):
                continue
            cell = grid[next_row][next_column]
            if cell == "#" or (
                "A" <= cell <= "F" and not keys & (1 << (ord(cell) - ord("A")))
            ):
                continue
            next_keys = keys
            if "a" <= cell <= "f":
                next_keys |= 1 << (ord(cell) - ord("a"))
            state = (next_row, next_column, next_keys)
            if state not in seen:
                seen.add(state)
                queue.append((next_row, next_column, next_keys, distance + 1))
    return -1
```

The global seen set keeps the first, shortest arrival at each complete state.
Any later equal state has identical available moves and cannot improve it.

**Complexity:** `O(rows * columns * 2^keys)` time and space.
