# Focus300 105: LeetCode 741 - Cherry Pickup

**Source:** [LeetCode 741](https://leetcode.com/problems/cherry-pickup/)  
**Difficulty:** Hard  
**Pattern:** two synchronized grid walkers

## Exact contract

In an `n x n` grid, `0` is empty, `1` is a cherry, and `-1` is a thorn. Travel
from `(0, 0)` to `(n - 1, n - 1)` using down or right moves, then return using
up or left moves. A cherry can be collected only once. Return the maximum
cherries, or `0` when no complete trip exists.

## First principles

Reverse the return path: the problem becomes two walkers moving from the start
to the finish at the same time. At step `s`, a walker at row `r` must be at
column `s - r`. This removes one coordinate and turns two exponential path
choices into `O(n^3)` synchronized states.

## Cases that decide correctness

- A thorn invalidates a state for either walker.
- When both walkers occupy one cell, its cherry is counted once.
- Walkers may cross or share cells; only the current shared cell is deduplicated.
- An unreachable finish returns `0`, not a negative sentinel.
- Source grids are square, non-empty, contain only `-1`, `0`, and `1`, and have
  open start and finish cells.

## Brute force: enumerate every valid path pair

```python
def cherry_pickup_brute(grid: list[list[int]]) -> int:
    size = len(grid)
    if (
        size == 0
        or any(len(row) != size for row in grid)
        or any(cell not in {-1, 0, 1} for row in grid for cell in row)
    ):
        raise ValueError("grid must be non-empty, square, and contain -1, 0, or 1")

    paths: list[frozenset[tuple[int, int]]] = []

    def visit(row: int, column: int, path: list[tuple[int, int]]) -> None:
        if row >= size or column >= size or grid[row][column] == -1:
            return
        path.append((row, column))
        if row == column == size - 1:
            paths.append(frozenset(path))
        else:
            visit(row + 1, column, path)
            visit(row, column + 1, path)
        path.pop()

    visit(0, 0, [])
    answer = 0
    for first in paths:
        for second in paths:
            answer = max(
                answer,
                sum(grid[row][column] for row, column in first | second),
            )
    return answer
```

There are up to `binomial(2n - 2, n - 1)` monotone paths, so comparing every
pair is exponential.

## Better solution: memoize synchronized positions

```python
from functools import cache


def cherry_pickup_memo(grid: list[list[int]]) -> int:
    size = len(grid)
    if (
        size == 0
        or any(len(row) != size for row in grid)
        or any(cell not in {-1, 0, 1} for row in grid for cell in row)
    ):
        raise ValueError("grid must be non-empty, square, and contain -1, 0, or 1")
    impossible = -(10**9)

    @cache
    def collect(step: int, first_row: int, second_row: int) -> int:
        first_column = step - first_row
        second_column = step - second_row
        if not (
            0 <= first_row < size
            and 0 <= first_column < size
            and 0 <= second_row < size
            and 0 <= second_column < size
        ):
            return impossible
        if grid[first_row][first_column] == -1 or grid[second_row][second_column] == -1:
            return impossible

        cherries = grid[first_row][first_column]
        if first_row != second_row:
            cherries += grid[second_row][second_column]
        if step == 2 * size - 2:
            return cherries

        best_next = max(
            collect(step + 1, first_row, second_row),
            collect(step + 1, first_row + 1, second_row),
            collect(step + 1, first_row, second_row + 1),
            collect(step + 1, first_row + 1, second_row + 1),
        )
        return cherries + best_next

    return max(0, collect(0, 0, 0))
```

Memoization evaluates `O(n^3)` states but retains all of them.

## Expert solution: bottom-up DP with one step layer

```python
def cherry_pickup(grid: list[list[int]]) -> int:
    size = len(grid)
    if (
        size == 0
        or any(len(row) != size for row in grid)
        or any(cell not in {-1, 0, 1} for row in grid for cell in row)
    ):
        raise ValueError("grid must be non-empty, square, and contain -1, 0, or 1")
    impossible = -(10**9)
    previous = [[impossible] * size for _ in range(size)]
    previous[0][0] = grid[0][0] if grid[0][0] != -1 else impossible

    for step in range(1, 2 * size - 1):
        current = [[impossible] * size for _ in range(size)]
        low = max(0, step - size + 1)
        high = min(size - 1, step)
        for first_row in range(low, high + 1):
            first_column = step - first_row
            if grid[first_row][first_column] == -1:
                continue
            for second_row in range(low, high + 1):
                second_column = step - second_row
                if grid[second_row][second_column] == -1:
                    continue

                best_previous = impossible
                for old_first in (first_row, first_row - 1):
                    for old_second in (second_row, second_row - 1):
                        if old_first >= 0 and old_second >= 0:
                            best_previous = max(
                                best_previous,
                                previous[old_first][old_second],
                            )
                if best_previous == impossible:
                    continue
                cherries = grid[first_row][first_column]
                if first_row != second_row:
                    cherries += grid[second_row][second_column]
                current[first_row][second_row] = best_previous + cherries
        previous = current

    return max(0, previous[size - 1][size - 1])
```

Every transition considers the four pairs of previous moves. A layer contains
the best result for every pair of rows after the same number of steps, so old
layers are unnecessary.

**Complexity:** `O(n^3)` time and `O(n^2)` space.
