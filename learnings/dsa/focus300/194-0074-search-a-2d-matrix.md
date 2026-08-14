# Focus300 194: LeetCode 74 - Search a 2D Matrix

**Source:** [LeetCode 74](https://leetcode.com/problems/search-a-2d-matrix/)  
**Difficulty:** Medium  
**Pattern:** binary search over a virtual flattened array

## Exact contract

Each matrix row is sorted in nondecreasing order, and the first value of every
row after the first is greater than the previous row's last value. Return
whether `target` occurs in the nonempty rectangular matrix.

## First principles

Those ordering rules make row-major matrix order globally sorted. Virtual flat
index `i` maps to `(i // columns, i % columns)`, so ordinary binary search works
without copying or flattening the matrix.

## Cases that decide correctness

- A one-cell matrix behaves like a one-element array.
- The target may lie between rows and be absent.
- Row boundaries do not need separate search logic.
- Duplicate values may occur within a row, but row transitions are strictly greater.
- Flattening physically would add unnecessary space.

## Brute force: scan every cell

```python
def matrix_contains_brute(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not all(type(row) is list and row for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")
    row_count = len(matrix)
    column_count = len(matrix[0])
    if row_count > 100 or column_count > 100 or any(
        len(row) != column_count for row in matrix
    ):
        raise ValueError("matrix dimensions must be rectangular and at most 100")
    if any(
        type(value) is not int or not -10_000 <= value <= 10_000
        for row in matrix
        for value in row
    ):
        raise ValueError("matrix values must be integers in the source range")
    if any(
        matrix[row][column] > matrix[row][column + 1]
        for row in range(row_count)
        for column in range(column_count - 1)
    ) or any(matrix[row - 1][-1] >= matrix[row][0] for row in range(1, row_count)):
        raise ValueError("matrix must satisfy the source ordering contract")
    if type(target) is not int or not -10_000 <= target <= 10_000:
        raise ValueError("target must be an integer in the source range")

    return any(target == value for row in matrix for value in row)
```

This takes `O(rows*columns)` time.

## Better insight: row-major coordinates preserve one global sorted order

Binary-search flat indices and convert only the midpoint to matrix coordinates.
No allocation is required.

## Expert solution: virtual flattened binary search

```python
def matrix_contains(matrix: list[list[int]], target: int) -> bool:
    if not matrix or not all(type(row) is list and row for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")
    row_count = len(matrix)
    column_count = len(matrix[0])
    if row_count > 100 or column_count > 100 or any(
        len(row) != column_count for row in matrix
    ):
        raise ValueError("matrix dimensions must be rectangular and at most 100")
    if any(
        type(value) is not int or not -10_000 <= value <= 10_000
        for row in matrix
        for value in row
    ):
        raise ValueError("matrix values must be integers in the source range")
    if any(
        matrix[row][column] > matrix[row][column + 1]
        for row in range(row_count)
        for column in range(column_count - 1)
    ) or any(matrix[row - 1][-1] >= matrix[row][0] for row in range(1, row_count)):
        raise ValueError("matrix must satisfy the source ordering contract")
    if type(target) is not int or not -10_000 <= target <= 10_000:
        raise ValueError("target must be an integer in the source range")

    left = 0
    right = row_count * column_count - 1
    while left <= right:
        middle = (left + right) // 2
        row, column = divmod(middle, column_count)
        value = matrix[row][column]
        if value == target:
            return True
        if value < target:
            left = middle + 1
        else:
            right = middle - 1
    return False
```

The virtual index interval contains exactly the still-possible globally sorted
cells after each comparison.

**Complexity:** `O(log(rows*columns))` search time and `O(1)` space after
validation.
