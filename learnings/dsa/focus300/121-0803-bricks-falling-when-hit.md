# Focus300 121: LeetCode 803 - Bricks Falling When Hit

**Source:** [LeetCode 803](https://leetcode.com/problems/bricks-falling-when-hit/)  
**Difficulty:** Hard  
**Pattern:** reverse-time connectivity with a virtual roof

## Exact contract

In a rectangular binary grid, a brick is stable when it is connected
orthogonally to the top row through bricks. Process distinct hit coordinates in
order. A hit removes its brick when present; every other brick that consequently
loses stability falls. Return the number of falling bricks after each hit,
excluding the brick directly removed.

## First principles

Deletion is difficult for disjoint-set union, but undoing deletions is easy.
Remove every effective hit first, connect the remaining bricks, then restore
hits in reverse. A virtual roof node represents stability. When one restored
brick increases the roof component from `before` to `after`, exactly
`after - before - 1` other bricks become connected; those are the bricks that
fell in forward time.


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

- Hitting an empty cell returns zero and must not restore a brick later.
- The directly hit brick is excluded by subtracting one.
- A top-row brick connects directly to the virtual roof.
- Restoring one brick may attach several previously disconnected components.
- Input grid and hit coordinates must not be mutated.

## Brute force: recompute stable bricks after every hit

```python
from collections import deque


def hit_bricks_brute(grid: list[list[int]], hits: list[list[int]]) -> list[int]:
    if not grid or not all(type(row) is list and row for row in grid):
        raise ValueError("grid must be a nonempty rectangular matrix")
    row_count = len(grid)
    column_count = len(grid[0])
    if (
        row_count > 200
        or column_count > 200
        or any(len(row) != column_count for row in grid)
    ):
        raise ValueError("grid dimensions must be rectangular and at most 200")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be binary integers")
    if type(hits) is not list or not 1 <= len(hits) <= 40_000:
        raise ValueError("hits length must be between 1 and 40,000")
    if any(
        type(hit) is not list
        or len(hit) != 2
        or type(hit[0]) is not int
        or type(hit[1]) is not int
        or not 0 <= hit[0] < row_count
        or not 0 <= hit[1] < column_count
        for hit in hits
    ):
        raise ValueError("every hit must be an in-bounds integer coordinate")
    if len({tuple(hit) for hit in hits}) != len(hits):
        raise ValueError("hit coordinates must be distinct")

    state = [row.copy() for row in grid]

    def stable_cells() -> set[tuple[int, int]]:
        stable = {
            (0, column) for column in range(column_count) if state[0][column] == 1
        }
        queue = deque(stable)
        while queue:
            row, column = queue.popleft()
            for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_delta
                next_column = column + column_delta
                cell = (next_row, next_column)
                if (
                    0 <= next_row < row_count
                    and 0 <= next_column < column_count
                    and state[next_row][next_column] == 1
                    and cell not in stable
                ):
                    stable.add(cell)
                    queue.append(cell)
        return stable

    answer: list[int] = []
    for row, column in hits:
        if state[row][column] == 0:
            answer.append(0)
            continue
        before = stable_cells()
        state[row][column] = 0
        fallen = before - stable_cells()
        fallen.discard((row, column))
        for fallen_row, fallen_column in fallen:
            state[fallen_row][fallen_column] = 0
        answer.append(len(fallen))
    return answer
```

Each hit may scan the entire grid, so this takes `O(H*R*C)` time.

## Better insight: reverse falling into component attachment

After all hits, build connectivity once. Restoring one hit changes only the
components adjacent to that cell, which union-find can merge incrementally.

## Expert solution: reverse hits with a virtual-roof DSU

```python
class DisjointSet:
    def __init__(self, size: int) -> None:
        self._parent = list(range(size))
        self._size = [1] * size

    def find(self, node: int) -> int:
        while self._parent[node] != node:
            self._parent[node] = self._parent[self._parent[node]]
            node = self._parent[node]
        return node

    def union(self, first: int, second: int) -> None:
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            return
        if self._size[first_root] < self._size[second_root]:
            first_root, second_root = second_root, first_root
        self._parent[second_root] = first_root
        self._size[first_root] += self._size[second_root]

    def component_size(self, node: int) -> int:
        return self._size[self.find(node)]


def hit_bricks(grid: list[list[int]], hits: list[list[int]]) -> list[int]:
    if not grid or not all(type(row) is list and row for row in grid):
        raise ValueError("grid must be a nonempty rectangular matrix")
    row_count = len(grid)
    column_count = len(grid[0])
    if (
        row_count > 200
        or column_count > 200
        or any(len(row) != column_count for row in grid)
    ):
        raise ValueError("grid dimensions must be rectangular and at most 200")
    if any(
        type(value) is not int or value not in (0, 1) for row in grid for value in row
    ):
        raise ValueError("grid values must be binary integers")
    if type(hits) is not list or not 1 <= len(hits) <= 40_000:
        raise ValueError("hits length must be between 1 and 40,000")
    if any(
        type(hit) is not list
        or len(hit) != 2
        or type(hit[0]) is not int
        or type(hit[1]) is not int
        or not 0 <= hit[0] < row_count
        or not 0 <= hit[1] < column_count
        for hit in hits
    ):
        raise ValueError("every hit must be an in-bounds integer coordinate")
    if len({tuple(hit) for hit in hits}) != len(hits):
        raise ValueError("hit coordinates must be distinct")

    state = [row.copy() for row in grid]
    effective: list[bool] = []
    for row, column in hits:
        present = state[row][column] == 1
        effective.append(present)
        if present:
            state[row][column] = 0

    roof = row_count * column_count
    disjoint_set = DisjointSet(roof + 1)

    def index(row: int, column: int) -> int:
        return row * column_count + column

    for row in range(row_count):
        for column in range(column_count):
            if state[row][column] == 0:
                continue
            cell = index(row, column)
            if row == 0:
                disjoint_set.union(cell, roof)
            if row > 0 and state[row - 1][column] == 1:
                disjoint_set.union(cell, index(row - 1, column))
            if column > 0 and state[row][column - 1] == 1:
                disjoint_set.union(cell, index(row, column - 1))

    answer = [0] * len(hits)
    for hit_index in range(len(hits) - 1, -1, -1):
        if not effective[hit_index]:
            continue
        row, column = hits[hit_index]
        before = disjoint_set.component_size(roof)
        state[row][column] = 1
        cell = index(row, column)
        if row == 0:
            disjoint_set.union(cell, roof)
        for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_delta
            next_column = column + column_delta
            if (
                0 <= next_row < row_count
                and 0 <= next_column < column_count
                and state[next_row][next_column] == 1
            ):
                disjoint_set.union(cell, index(next_row, next_column))
        after = disjoint_set.component_size(roof)
        answer[hit_index] = max(0, after - before - 1)
    return answer
```

The reverse roof-size increase counts precisely the other bricks that regained
stability through the restored hit.

**Complexity:** `O((R*C + H) * alpha(R*C))` time and `O(R*C + H)` space.
