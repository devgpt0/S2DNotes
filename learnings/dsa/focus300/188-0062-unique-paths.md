# Focus300 188: LeetCode 62 - Unique Paths

**Source:** [LeetCode 62](https://leetcode.com/problems/unique-paths/)  
**Difficulty:** Medium  
**Pattern:** lattice-path dynamic programming and combinations

## Exact contract

Count paths from the top-left to bottom-right of a `rows x columns` grid when
each move goes one cell right or down. Both dimensions are between 1 and 100.

## First principles

Every path contains exactly `rows - 1` down moves and `columns - 1` right
moves. Dynamic programming counts ways into each cell from above and left;
equivalently, choosing which move positions are downward gives a binomial
coefficient.

## Cases that decide correctness

- A one-row or one-column grid has exactly one path.
- The starting cell contributes one empty prefix path.
- No diagonal or backward moves are allowed.
- Counts are exact integers with no modulus.
- Dimensions must be positive.

## Brute force: enumerate every move choice recursively

```python
def unique_paths_brute(rows: int, columns: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 100 or not 1 <= columns <= 100:
        raise ValueError("rows and columns must be between 1 and 100")

    def count(row: int, column: int) -> int:
        if row == rows - 1 or column == columns - 1:
            return 1
        return count(row + 1, column) + count(row, column + 1)

    return count(0, 0)
```

This explores `C(rows + columns - 2, rows - 1)` paths.

## Better approach: roll one DP row

```python
def unique_paths_dp(rows: int, columns: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 100 or not 1 <= columns <= 100:
        raise ValueError("rows and columns must be between 1 and 100")

    ways = [1] * columns
    for _ in range(1, rows):
        for column in range(1, columns):
            ways[column] += ways[column - 1]
    return ways[-1]
```

This is `O(rows * columns)` time and `O(columns)` space.

## Expert solution: choose the downward move positions

```python
from math import comb


def unique_paths(rows: int, columns: int) -> int:
    if type(rows) is not int or type(columns) is not int:
        raise TypeError("rows and columns must be integers")
    if not 1 <= rows <= 100 or not 1 <= columns <= 100:
        raise ValueError("rows and columns must be between 1 and 100")
    return comb(rows + columns - 2, rows - 1)
```

Every legal path is a unique ordering of the fixed multiset of down and right
moves, so the binomial coefficient counts paths bijectively.

**Complexity:** `O(min(rows, columns))` arithmetic steps and `O(1)` conceptual
state, excluding big-integer storage.
