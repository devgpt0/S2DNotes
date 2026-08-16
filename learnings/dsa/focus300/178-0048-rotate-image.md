# Focus300 178: LeetCode 48 - Rotate Image

**Source:** [LeetCode 48](https://leetcode.com/problems/rotate-image/)  
**Difficulty:** Medium  
**Pattern:** in-place four-way matrix cycles

## Exact contract

Rotate a non-empty `n x n` integer matrix 90 degrees clockwise in place. Do not
return a replacement matrix; the supplied nested list must contain the rotated
values when the function finishes.

## First principles

Coordinate `(row, column)` moves to `(column, n - 1 - row)`. Four applications
return to the starting coordinate, so process each layer as independent four-way
cycles and store one displaced value temporarily.


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

- A `1 x 1` matrix is unchanged.
- Odd sizes leave the center cell unchanged.
- Each four-way cycle must be processed once.
- Layer offsets run through `last - first - 1`.
- The matrix object and its row objects remain the mutation target.

## Brute force: rotate from a full copy

```python
def rotate_brute(matrix: list[list[int]]) -> None:
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("matrix must be non-empty and square")

    original = [row[:] for row in matrix]
    for row in range(size):
        for column in range(size):
            matrix[column][size - 1 - row] = original[row][column]
```

This takes `O(n^2)` time and `O(n^2)` extra space.

## Better transition: follow coordinate cycles directly

The rotation mapping forms disjoint cycles of four except at the odd-sized
center. Moving four values together removes the need for a copied matrix.

## Expert solution: layer-by-layer four-way swaps

```python
def rotate(matrix: list[list[int]]) -> None:
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("matrix must be non-empty and square")

    for first in range(size // 2):
        last = size - 1 - first
        for offset in range(last - first):
            top = matrix[first][first + offset]
            matrix[first][first + offset] = matrix[last - offset][first]
            matrix[last - offset][first] = matrix[last][last - offset]
            matrix[last][last - offset] = matrix[first + offset][last]
            matrix[first + offset][last] = top
```

The assignments move left to top, bottom to left, right to bottom, and saved top
to right, which is exactly one clockwise cycle.

**Complexity:** `O(n^2)` time and `O(1)` extra space.
