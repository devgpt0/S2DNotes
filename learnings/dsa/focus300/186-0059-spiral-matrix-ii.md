# Focus300 186: LeetCode 59 - Spiral Matrix II

**Source:** [LeetCode 59](https://leetcode.com/problems/spiral-matrix-ii/)  
**Difficulty:** Medium  
**Pattern:** shrinking rectangular boundaries

## Exact contract

For `1 <= n <= 20`, return an `n x n` matrix filled with `1..n^2` in clockwise
spiral order starting at the top-left corner.

## First principles

Each layer consists of a top row, right column, bottom row, and left column.
Filling those sides in order and shrinking their boundaries preserves the same
problem on the inner square.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- `n = 1` returns `[[1]]`.
- Every integer `1..n^2` appears exactly once.
- The final single row or column must not be filled twice.
- Direction changes occur before stepping outside or onto a filled cell.
- The output dimensions are exactly `n x n`.

## Brute force: simulate movement through unfilled cells

```python
def generate_spiral_matrix_brute(size: int) -> list[list[int]]:
    if type(size) is not int:
        raise TypeError("size must be an integer")
    if not 1 <= size <= 20:
        raise ValueError("size must be between 1 and 20")

    matrix = [[0] * size for _ in range(size)]
    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
    direction = 0
    row = 0
    column = 0
    for value in range(1, size * size + 1):
        matrix[row][column] = value
        row_step, column_step = directions[direction]
        next_row = row + row_step
        next_column = column + column_step
        if not (
            0 <= next_row < size
            and 0 <= next_column < size
            and matrix[next_row][next_column] == 0
        ):
            direction = (direction + 1) % 4
            row_step, column_step = directions[direction]
            next_row = row + row_step
            next_column = column + column_step
        row, column = next_row, next_column
    return matrix
```

This uses `O(n^2)` time and the output matrix as its visited marker.

## Better approach: generate one recursive layer at a time

Recursion can fill an outer square and call itself on the inner square, but its
coordinates and next value still encode four boundaries. Iteration keeps that
state explicit.

## Expert solution: fill four shrinking sides

```python
def generate_spiral_matrix(size: int) -> list[list[int]]:
    if type(size) is not int:
        raise TypeError("size must be an integer")
    if not 1 <= size <= 20:
        raise ValueError("size must be between 1 and 20")

    matrix = [[0] * size for _ in range(size)]
    top = 0
    bottom = size - 1
    left = 0
    right = size - 1
    value = 1
    while top <= bottom and left <= right:
        for column in range(left, right + 1):
            matrix[top][column] = value
            value += 1
        top += 1
        for row in range(top, bottom + 1):
            matrix[row][right] = value
            value += 1
        right -= 1
        if top <= bottom:
            for column in range(right, left - 1, -1):
                matrix[bottom][column] = value
                value += 1
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                matrix[row][left] = value
                value += 1
            left += 1
    return matrix
```

Each loop fills exactly the current outer layer. Boundary guards handle the
odd-sized center without duplicate writes.

**Complexity:** `O(n^2)` time and `O(1)` auxiliary space beyond the output.
