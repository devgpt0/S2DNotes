# Focus300 182: LeetCode 54 - Spiral Matrix

**Source:** [LeetCode 54](https://leetcode.com/problems/spiral-matrix/)  
**Difficulty:** Medium  
**Pattern:** shrinking rectangular boundaries

## Exact contract

Given a nonempty rectangular integer matrix, return all values in clockwise
spiral order starting at the top-left corner. Each cell appears exactly once.

## First principles

The next outer layer is its top row, right column, bottom row in reverse, and
left column in reverse. After emitting those sides, moving all four boundaries
inward leaves the same problem on a smaller rectangle.

## Cases that decide correctness

- A single row is emitted once from left to right.
- A single column is emitted once from top to bottom.
- Bottom and left traversals require boundary checks after shrinking.
- Rectangular matrices need not be square.
- The result contains exactly `rows * columns` values.

## Brute force: simulate direction changes with visited cells

```python
def spiral_order_brute(matrix: list[list[int]]) -> list[int]:
    if (
        type(matrix) is not list
        or not matrix
        or any(
            type(row) is not list or not row or len(row) != len(matrix[0])
            for row in matrix
        )
    ):
        raise TypeError("matrix must be a nonempty rectangular list")
    if any(type(value) is not int for row in matrix for value in row):
        raise TypeError("matrix values must be integers")

    rows = len(matrix)
    columns = len(matrix[0])
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    direction = 0
    row = 0
    column = 0
    seen: set[tuple[int, int]] = set()
    answer: list[int] = []
    for _ in range(rows * columns):
        answer.append(matrix[row][column])
        seen.add((row, column))
        row_step, column_step = directions[direction]
        next_row = row + row_step
        next_column = column + column_step
        if not (
            0 <= next_row < rows
            and 0 <= next_column < columns
            and (next_row, next_column) not in seen
        ):
            direction = (direction + 1) % 4
            row_step, column_step = directions[direction]
            next_row = row + row_step
            next_column = column + column_step
        row, column = next_row, next_column
    return answer
```

This is `O(rows * columns)` time and uses a same-sized visited set.

## Better approach: remove completed outer layers

Copying and rotating the unvisited submatrix makes the layer idea concise, but
repeated copies can become quadratic. Four integer boundaries encode the same
state without moving data.

## Expert solution: traverse four shrinking sides

```python
def spiral_order(matrix: list[list[int]]) -> list[int]:
    if (
        type(matrix) is not list
        or not matrix
        or any(
            type(row) is not list or not row or len(row) != len(matrix[0])
            for row in matrix
        )
    ):
        raise TypeError("matrix must be a nonempty rectangular list")
    if any(type(value) is not int for row in matrix for value in row):
        raise TypeError("matrix values must be integers")

    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    answer: list[int] = []
    while top <= bottom and left <= right:
        answer.extend(matrix[top][left : right + 1])
        top += 1
        for row in range(top, bottom + 1):
            answer.append(matrix[row][right])
        right -= 1
        if top <= bottom:
            answer.extend(reversed(matrix[bottom][left : right + 1]))
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                answer.append(matrix[row][left])
            left += 1
    return answer
```

Each boundary traversal emits one unvisited side and then excludes it. The
guards prevent a final row or column from being emitted twice.

**Complexity:** `O(rows * columns)` time and `O(1)` auxiliary space excluding
the output.
