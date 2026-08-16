# Focus300 050: LeetCode 329 - Longest Increasing Path in a Matrix

**Source:** [LeetCode 329](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)  
**Difficulty:** Hard  
**Pattern:** topological layers in an implicit DAG

## Exact contract

Given a nonempty rectangular integer matrix, return the maximum number of cells
in a strictly increasing path. Consecutive cells must share an edge; diagonal
moves and wrapping outside the matrix are forbidden.

## First principles

Direct every legal move from a smaller cell to a larger neighbor. Strict
increase makes this graph acyclic. Local maxima have outdegree zero. Removing
all maxima layer by layer exposes their predecessors, and the number of layers
is the longest path length.


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

- A one-cell matrix returns one.
- Equal neighboring values cannot connect.
- Paths may turn between horizontal and vertical moves.
- Negative values do not change comparisons.
- The iterative expert solution avoids recursion depth proportional to cells.

## Brute force: start an uncached DFS from every cell

```python
def longest_increasing_path_brute(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")

    row_count = len(matrix)
    column_count = len(matrix[0])

    def search(row: int, column: int) -> int:
        answer = 1
        for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_step
            next_column = column + column_step
            if (
                0 <= next_row < row_count
                and 0 <= next_column < column_count
                and matrix[next_row][next_column] > matrix[row][column]
            ):
                answer = max(answer, 1 + search(next_row, next_column))
        return answer

    return max(
        search(row, column)
        for row in range(row_count)
        for column in range(column_count)
    )
```

Strict increase prevents cycles, but repeated suffix paths make this exponential.

## Better approach: memoize the path from each cell

```python
from functools import cache


def longest_increasing_path_memoized(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")

    row_count = len(matrix)
    column_count = len(matrix[0])

    @cache
    def search(row: int, column: int) -> int:
        return 1 + max(
            (
                search(next_row, next_column)
                for row_step, column_step in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if 0 <= (next_row := row + row_step) < row_count
                and 0 <= (next_column := column + column_step) < column_count
                and matrix[next_row][next_column] > matrix[row][column]
            ),
            default=0,
        )

    return max(
        search(row, column)
        for row in range(row_count)
        for column in range(column_count)
    )
```

This is `O(rows * columns)` time, but a worst-case path may exceed Python's
recursion depth.

## Expert solution: iterative topological peeling

```python
from collections import deque


def longest_increasing_path(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("matrix must be nonempty and rectangular")

    row_count = len(matrix)
    column_count = len(matrix[0])
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    outdegree = [[0] * column_count for _ in range(row_count)]
    queue: deque[tuple[int, int]] = deque()
    for row in range(row_count):
        for column in range(column_count):
            outdegree[row][column] = sum(
                0 <= row + row_step < row_count
                and 0 <= column + column_step < column_count
                and matrix[row + row_step][column + column_step] > matrix[row][column]
                for row_step, column_step in directions
            )
            if outdegree[row][column] == 0:
                queue.append((row, column))

    layers = 0
    while queue:
        layers += 1
        for _ in range(len(queue)):
            row, column = queue.popleft()
            for row_step, column_step in directions:
                previous_row = row + row_step
                previous_column = column + column_step
                if (
                    0 <= previous_row < row_count
                    and 0 <= previous_column < column_count
                    and matrix[previous_row][previous_column] < matrix[row][column]
                ):
                    outdegree[previous_row][previous_column] -= 1
                    if outdegree[previous_row][previous_column] == 0:
                        queue.append((previous_row, previous_column))
    return layers
```

Each layer removes current DAG sinks. A cell enters the queue only after every
larger continuation is removed, so its layer is one more than its longest
successor path. The final layer count is the global longest path.

**Complexity:** `O(rows * columns)` time and space.
