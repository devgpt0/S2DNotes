# Focus300 189: LeetCode 63 - Unique Paths II

**Source:** [LeetCode 63](https://leetcode.com/problems/unique-paths-ii/)  
**Difficulty:** Medium  
**Pattern:** obstacle-aware rolling grid DP

## Exact contract

In a nonempty rectangular grid, `0` is open and `1` is an obstacle. Count paths
from top-left to bottom-right using only right and down moves without entering
obstacles. Dimensions are at most 100.

## First principles

An open cell receives paths from above and left; an obstacle receives zero.
While scanning left-to-right, one DP row stores the old value from above before
update and the new value from the left after update.

## Cases that decide correctness

- A blocked start or destination yields zero.
- Obstacles reset their DP entry to zero.
- A blocked cell can cut off every later cell in its row until another path
  arrives from above.
- One-row and one-column grids follow the same recurrence.
- Grid values other than integer zero and one are invalid.

## Brute force: recursively try both directions

```python
def unique_paths_with_obstacles_brute(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 100
        or any(
            type(row) is not list
            or not row
            or len(row) != len(grid[0])
            or len(row) > 100
            for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangle of side at most 100")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be integer zeroes and ones")

    def count(row: int, column: int) -> int:
        if row == len(grid) or column == len(grid[0]) or grid[row][column] == 1:
            return 0
        if (row, column) == (len(grid) - 1, len(grid[0]) - 1):
            return 1
        return count(row + 1, column) + count(row, column + 1)

    return count(0, 0)
```

Without memoization this explores exponentially many path prefixes.

## Better approach: store every cell's path count

A full `rows x columns` table applies the recurrence in `O(rows * columns)`
time and space. The expert version rolls that table into one row.

## Expert solution: reset blocked entries in one DP row

```python
def unique_paths_with_obstacles(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or len(grid) > 100
        or any(
            type(row) is not list
            or not row
            or len(row) != len(grid[0])
            or len(row) > 100
            for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangle of side at most 100")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be integer zeroes and ones")

    ways = [0] * len(grid[0])
    ways[0] = 1
    for row in grid:
        for column, blocked in enumerate(row):
            if blocked:
                ways[column] = 0
            elif column > 0:
                ways[column] += ways[column - 1]
    return ways[-1]
```

Before each update, `ways[column]` is the count from above; after adding the
left entry it is the count for the current cell. Obstacles erase both routes.

**Complexity:** `O(rows * columns)` time and `O(columns)` space.
