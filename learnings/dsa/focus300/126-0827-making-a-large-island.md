# Focus300 126: LeetCode 827 - Making A Large Island

**Source:** [LeetCode 827](https://leetcode.com/problems/making-a-large-island/)  
**Difficulty:** Hard  
**Pattern:** component labeling and deduplicated neighbor aggregation

## Exact contract

Given an `n x n` binary grid, change at most one `0` to `1`. Return the largest
possible four-directionally connected island area. The input grid must remain
unchanged.

## First principles

Flipping one zero joins exactly the distinct existing components touching its
four sides, plus the new cell itself. Label every component once and store its
area. Then each zero needs only four label lookups; a set prevents counting the
same component twice when it touches from multiple sides.


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

- An all-ones grid returns `n*n` without requiring a flip.
- An all-zero grid returns `1`.
- Diagonal cells are not connected.
- One component may touch a zero on several sides and must be counted once.
- Flipping is optional, so an existing largest island remains a candidate.

## Brute force: flip each zero and flood-fill the whole grid

```python
from collections import deque


def largest_island_brute(grid: list[list[int]]) -> int:
    if type(grid) is not list or not 1 <= len(grid) <= 500:
        raise ValueError("grid size must be between 1 and 500")
    size = len(grid)
    if any(type(row) is not list or len(row) != size for row in grid):
        raise ValueError("grid must be square")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be binary integers")

    def largest_area(state: list[list[int]]) -> int:
        visited: set[tuple[int, int]] = set()
        best = 0
        for start_row in range(size):
            for start_column in range(size):
                start = (start_row, start_column)
                if state[start_row][start_column] == 0 or start in visited:
                    continue
                visited.add(start)
                queue = deque([start])
                area = 0
                while queue:
                    row, column = queue.popleft()
                    area += 1
                    for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        next_row = row + row_delta
                        next_column = column + column_delta
                        cell = (next_row, next_column)
                        if (
                            0 <= next_row < size
                            and 0 <= next_column < size
                            and state[next_row][next_column] == 1
                            and cell not in visited
                        ):
                            visited.add(cell)
                            queue.append(cell)
                best = max(best, area)
        return best

    zeros = [
        (row, column)
        for row in range(size)
        for column in range(size)
        if grid[row][column] == 0
    ]
    if not zeros:
        return size * size
    best = 0
    for row, column in zeros:
        state = [values.copy() for values in grid]
        state[row][column] = 1
        best = max(best, largest_area(state))
    return best
```

Up to `n^2` flips each scan `n^2` cells, for `O(n^4)` time.

## Better insight: flipping does not change existing component interiors

Precompute each component's label and area. Only the four labels around the
chosen zero affect its result.

## Expert solution: label once, aggregate per zero

```python
def largest_island(grid: list[list[int]]) -> int:
    if type(grid) is not list or not 1 <= len(grid) <= 500:
        raise ValueError("grid size must be between 1 and 500")
    size = len(grid)
    if any(type(row) is not list or len(row) != size for row in grid):
        raise ValueError("grid must be square")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be binary integers")

    labels = [row.copy() for row in grid]
    areas = {0: 0}
    next_label = 2
    for start_row in range(size):
        for start_column in range(size):
            if labels[start_row][start_column] != 1:
                continue
            labels[start_row][start_column] = next_label
            stack = [(start_row, start_column)]
            area = 0
            while stack:
                row, column = stack.pop()
                area += 1
                for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    next_row = row + row_delta
                    next_column = column + column_delta
                    if (
                        0 <= next_row < size
                        and 0 <= next_column < size
                        and labels[next_row][next_column] == 1
                    ):
                        labels[next_row][next_column] = next_label
                        stack.append((next_row, next_column))
            areas[next_label] = area
            next_label += 1

    best = max(areas.values())
    for row in range(size):
        for column in range(size):
            if labels[row][column] != 0:
                continue
            neighbor_labels: set[int] = set()
            for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_delta
                next_column = column + column_delta
                if 0 <= next_row < size and 0 <= next_column < size:
                    neighbor_labels.add(labels[next_row][next_column])
            best = max(best, 1 + sum(areas[label] for label in neighbor_labels))
    return best
```

Every original land cell is labeled once, and every zero examines at most four
component identifiers.

**Complexity:** `O(n^2)` time and `O(n^2)` space for the copied label grid.
