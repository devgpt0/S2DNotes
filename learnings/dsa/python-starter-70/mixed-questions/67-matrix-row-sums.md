# 67. Calculate Matrix Row Sums

**What you learn:** Nested list loops.

## Problem

Return the sum of each row in a matrix.

## Example

```text
Input: matrix = [[1, 2], [3, 4]]
Output: [3, 7]
```

## Simple idea

Calculate one total for each row and append it to the result.

## Python solution

```python
def matrix_row_sums(matrix: list[list[int]]) -> list[int]:
    sums: list[int] = []

    for row in matrix:
        row_total = 0

        for number in row:
            row_total = row_total + number

        sums.append(row_total)

    return sums
```

## Complexity

- Time: `O(rows × columns)`
- Extra space: `O(rows)`

Try to write the solution yourself before reading the code.

