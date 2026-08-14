# Focus300 190: LeetCode 64 - Minimum Path Sum

**Source:** [LeetCode 64](https://leetcode.com/problems/minimum-path-sum/)  
**Difficulty:** Medium  
**Pattern:** rolling minimum-cost grid DP

## Exact contract

Given a nonempty rectangular grid of nonnegative integers, return the minimum
sum along a path from top-left to bottom-right using only right and down moves.
The starting and ending cell values are included.

## First principles

Every path into a cell comes from above or left, so its optimal cost is its own
value plus the smaller optimal predecessor cost. Scanning row-major guarantees
both predecessor states are already final.

## Cases that decide correctness

- A `1 x 1` grid returns its single value.
- The first row can arrive only from the left.
- The first column can arrive only from above.
- Zero-valued cells are valid and must not be treated as absent.
- The input grid is not mutated.

## Brute force: recursively enumerate every path

```python
def minimum_path_sum_brute(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or any(
            type(row) is not list or not row or len(row) != len(grid[0]) for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangular list")
    if any(type(value) is not int or value < 0 for row in grid for value in row):
        raise ValueError("grid values must be non-negative integers")

    def cost(row: int, column: int) -> int:
        if (row, column) == (len(grid) - 1, len(grid[0]) - 1):
            return grid[row][column]
        candidates: list[int] = []
        if row + 1 < len(grid):
            candidates.append(cost(row + 1, column))
        if column + 1 < len(grid[0]):
            candidates.append(cost(row, column + 1))
        return grid[row][column] + min(candidates)

    return cost(0, 0)
```

This explores every right/down path and is exponential without memoization.

## Better approach: memoize recursive cell costs

Caching each suffix cost reduces the recurrence to `O(rows * columns)` time
and space. Bottom-up iteration avoids recursion and rolls the storage.

## Expert solution: update one row of minimum costs

```python
def minimum_path_sum(grid: list[list[int]]) -> int:
    if (
        type(grid) is not list
        or not grid
        or any(
            type(row) is not list or not row or len(row) != len(grid[0]) for row in grid
        )
    ):
        raise TypeError("grid must be a nonempty rectangular list")
    if any(type(value) is not int or value < 0 for row in grid for value in row):
        raise ValueError("grid values must be non-negative integers")

    costs = [0] * len(grid[0])
    for row_index, row in enumerate(grid):
        for column, value in enumerate(row):
            if row_index == 0 and column == 0:
                costs[column] = value
            elif row_index == 0:
                costs[column] = costs[column - 1] + value
            elif column == 0:
                costs[column] += value
            else:
                costs[column] = min(costs[column], costs[column - 1]) + value
    return costs[-1]
```

At each cell, the old entry is the cost from above and the updated preceding
entry is the cost from the left. Keeping their minimum implements the complete
recurrence.

**Complexity:** `O(rows * columns)` time and `O(columns)` space.
