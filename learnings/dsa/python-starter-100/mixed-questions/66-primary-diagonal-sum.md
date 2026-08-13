# 66. Sum a Matrix's Primary Diagonal

**What you learn:** Two-dimensional list indexes.

## Problem

Given a square matrix, sum the values from the top-left to the bottom-right.

## Example

```text
Input: matrix = [[1, 2], [3, 4]]
Output: 5
```

## Simple idea

Diagonal values use the same row and column index.

## Python solution

```python
def primary_diagonal_sum(matrix: list[list[int]]) -> int:
    size = len(matrix)

    for row in matrix:
        if len(row) != size:
            raise ValueError("matrix must be square")

    total = 0

    for index in range(size):
        total = total + matrix[index][index]

    return total
```

## Complexity

- Time: `O(n)`
- Extra space: `O(1)`

Try to write the solution yourself before reading the code.

