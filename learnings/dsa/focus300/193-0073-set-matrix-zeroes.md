# Focus300 193: LeetCode 73 - Set Matrix Zeroes

**Source:** [LeetCode 73](https://leetcode.com/problems/set-matrix-zeroes/)  
**Difficulty:** Medium  
**Pattern:** in-place row and column marker reuse

## Exact contract

For every cell that is initially zero, set its entire row and column to zero.
Modify the rectangular integer matrix in place; zeros created during the update
must not trigger additional rows or columns.

## First principles

The decision for each row and column is one bit: whether it originally contains
a zero. The first row and first column can store those marker bits, but their
own original-zero states must be saved separately because cell `(0, 0)` belongs
to both.


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

- A zero created during processing must not become a new marker.
- First-row and first-column zeros require separate flags.
- A `1 x 1` matrix works for both zero and nonzero values.
- Multiple original zeros may mark the same row or column.
- The function mutates the given row lists and returns `None`.

## Brute force: preserve the original matrix

```python
def set_matrix_zeroes_brute(matrix: list[list[int]]) -> None:
    if not matrix or not all(type(row) is list and row for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")
    row_count = len(matrix)
    column_count = len(matrix[0])
    if row_count > 200 or column_count > 200 or any(
        len(row) != column_count for row in matrix
    ):
        raise ValueError("matrix dimensions must be rectangular and at most 200")
    if any(
        type(value) is not int or not -(2**31) <= value <= 2**31 - 1
        for row in matrix
        for value in row
    ):
        raise ValueError("matrix values must be signed 32-bit integers")

    original = [row.copy() for row in matrix]
    for row in range(row_count):
        for column in range(column_count):
            if original[row][column] == 0:
                for other_column in range(column_count):
                    matrix[row][other_column] = 0
                for other_row in range(row_count):
                    matrix[other_row][column] = 0
```

The full copy is clear but uses `O(rows*columns)` auxiliary space.

## Better insight: the matrix already has room for marker bits

Record later-row markers in column zero and later-column markers in row zero,
then apply them only after the marking pass.

## Expert solution: first row and column as markers

```python
def set_matrix_zeroes(matrix: list[list[int]]) -> None:
    if not matrix or not all(type(row) is list and row for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")
    row_count = len(matrix)
    column_count = len(matrix[0])
    if row_count > 200 or column_count > 200 or any(
        len(row) != column_count for row in matrix
    ):
        raise ValueError("matrix dimensions must be rectangular and at most 200")
    if any(
        type(value) is not int or not -(2**31) <= value <= 2**31 - 1
        for row in matrix
        for value in row
    ):
        raise ValueError("matrix values must be signed 32-bit integers")

    first_row_zero = any(matrix[0][column] == 0 for column in range(column_count))
    first_column_zero = any(matrix[row][0] == 0 for row in range(row_count))

    for row in range(1, row_count):
        for column in range(1, column_count):
            if matrix[row][column] == 0:
                matrix[row][0] = 0
                matrix[0][column] = 0

    for row in range(1, row_count):
        for column in range(1, column_count):
            if matrix[row][0] == 0 or matrix[0][column] == 0:
                matrix[row][column] = 0

    if first_row_zero:
        for column in range(column_count):
            matrix[0][column] = 0
    if first_column_zero:
        for row in range(row_count):
            matrix[row][0] = 0
```

Markers are derived only from original interior zeros and are consumed after
marking finishes, preventing cascade effects.

**Complexity:** `O(rows*columns)` time and `O(1)` auxiliary space.
