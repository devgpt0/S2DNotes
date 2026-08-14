# Focus300 018: LeetCode 85 - Maximal Rectangle

**Source:** [LeetCode 85](https://leetcode.com/problems/maximal-rectangle/)  
**Difficulty:** Hard  
**Pattern:** row histograms with a monotonic stack

## Exact contract

Given a nonempty rectangular matrix of strings `"0"` and `"1"`, return the
area of its largest axis-aligned rectangle containing only `"1"` cells.

## First principles

At each row, let `heights[column]` be the number of consecutive ones ending at
that row. Every all-one rectangle has one bottom row and becomes a consecutive
histogram rectangle there. Solving Largest Rectangle in Histogram after each
height update therefore considers every candidate rectangle.

## Cases that decide correctness

- A matrix containing only zeros returns zero.
- A single one returns one.
- A zero resets its column height immediately.
- The optimum may span several rows and columns.
- Ragged rows and characters other than `"0"` and `"1"` are invalid.

## Brute force: inspect every rectangle

```python
def maximal_rectangle_brute(matrix: list[list[str]]) -> int:
    if (
        not matrix
        or not matrix[0]
        or any(len(row) != len(matrix[0]) for row in matrix)
        or any(cell not in {"0", "1"} for row in matrix for cell in row)
    ):
        raise ValueError("matrix must be nonempty, rectangular, and binary")

    row_count = len(matrix)
    column_count = len(matrix[0])
    answer = 0
    for top in range(row_count):
        for bottom in range(top, row_count):
            for left in range(column_count):
                for right in range(left, column_count):
                    if all(
                        matrix[row][column] == "1"
                        for row in range(top, bottom + 1)
                        for column in range(left, right + 1)
                    ):
                        answer = max(answer, (bottom - top + 1) * (right - left + 1))
    return answer
```

This takes `O(rows^3 * columns^3)` time and `O(1)` auxiliary space.

## Better approach: histogram with quadratic range minima

```python
def maximal_rectangle_quadratic(matrix: list[list[str]]) -> int:
    if (
        not matrix
        or not matrix[0]
        or any(len(row) != len(matrix[0]) for row in matrix)
        or any(cell not in {"0", "1"} for row in matrix for cell in row)
    ):
        raise ValueError("matrix must be nonempty, rectangular, and binary")

    heights = [0] * len(matrix[0])
    answer = 0
    for row in matrix:
        for column, cell in enumerate(row):
            heights[column] = heights[column] + 1 if cell == "1" else 0
        for left in range(len(heights)):
            minimum = heights[left]
            for right in range(left, len(heights)):
                minimum = min(minimum, heights[right])
                answer = max(answer, minimum * (right - left + 1))
    return answer
```

This captures every bottom row in `O(rows * columns^2)` time.

## Expert solution: solve every histogram in linear time

```python
def maximal_rectangle(matrix: list[list[str]]) -> int:
    if (
        not matrix
        or not matrix[0]
        or any(len(row) != len(matrix[0]) for row in matrix)
        or any(cell not in {"0", "1"} for row in matrix for cell in row)
    ):
        raise ValueError("matrix must be nonempty, rectangular, and binary")

    heights = [0] * len(matrix[0])
    answer = 0
    for row in matrix:
        for column, cell in enumerate(row):
            heights[column] = heights[column] + 1 if cell == "1" else 0

        stack: list[tuple[int, int]] = []
        for index, height in enumerate([*heights, 0]):
            start = index
            while stack and stack[-1][1] > height:
                left, previous_height = stack.pop()
                answer = max(answer, previous_height * (index - left))
                start = left
            if not stack or stack[-1][1] < height:
                stack.append((start, height))
    return answer
```

The running heights encode exactly the rectangles ending at the current row.
The stack computes the widest interval for every limiting height, so taking the
maximum over all bottom rows returns the matrix optimum.

**Complexity:** `O(rows * columns)` time and `O(columns)` space.
