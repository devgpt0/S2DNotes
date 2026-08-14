# Focus300 092: LeetCode 675 - Cut Off Trees for Golf Event

**Source:** [LeetCode 675](https://leetcode.com/problems/cut-off-trees-for-golf-event/)  
**Difficulty:** Hard  
**Pattern:** ordered targets plus repeated unweighted shortest paths

## Exact contract

In a nonempty grid, `0` is blocked, `1` is ground, and each value above `1` is
a tree with a distinct height. Start at `(0, 0)`, move orthogonally through
nonzero cells, and cut every tree in increasing height order. Return the
minimum total steps, or `-1` if the next required tree is unreachable.

## First principles

Tree heights fix the visit order; there is no routing choice between targets.
The only subproblem is the shortest unweighted path from the current position
to the next tree. Distances add because every valid complete walk must contain
those same consecutive target pairs.

## Cases that decide correctness

- No trees requires zero steps, even when the starting cell is blocked.
- A blocked start makes any existing tree unreachable.
- Other trees are walkable before they are cut.
- Disconnected nonzero regions must return `-1` at the first failed segment.
- A target already under the player contributes zero steps.

## Brute force: enumerate simple paths for each required segment

```python
def cut_off_trees_brute(forest: list[list[int]]) -> int:
    if not forest or not all(type(row) is list and row for row in forest):
        raise ValueError("forest must be a nonempty rectangular grid")
    row_count = len(forest)
    column_count = len(forest[0])
    if row_count > 50 or column_count > 50:
        raise ValueError("forest dimensions must not exceed 50")
    if any(len(row) != column_count for row in forest):
        raise ValueError("forest must be rectangular")
    if any(
        type(value) is not int or not 0 <= value <= 1_000_000_000
        for row in forest
        for value in row
    ):
        raise ValueError("forest values must be integers in the source range")

    trees = sorted(
        (height, row, column)
        for row, values in enumerate(forest)
        for column, height in enumerate(values)
        if height > 1
    )
    heights = [height for height, _, _ in trees]
    if len(heights) != len(set(heights)):
        raise ValueError("tree heights must be distinct")
    if not trees:
        return 0
    if forest[0][0] == 0:
        return -1

    def shortest_path(start: tuple[int, int], target: tuple[int, int]) -> int:
        if start == target:
            return 0
        unreachable = row_count * column_count + 1
        best = unreachable
        visited = {start}

        def visit(row: int, column: int, steps: int) -> None:
            nonlocal best
            if steps >= best:
                return
            if (row, column) == target:
                best = steps
                return
            for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_delta
                next_column = column + column_delta
                next_cell = (next_row, next_column)
                if (
                    0 <= next_row < row_count
                    and 0 <= next_column < column_count
                    and forest[next_row][next_column] != 0
                    and next_cell not in visited
                ):
                    visited.add(next_cell)
                    visit(next_row, next_column, steps + 1)
                    visited.remove(next_cell)

        visit(start[0], start[1], 0)
        return -1 if best == unreachable else best

    total = 0
    current = (0, 0)
    for _, row, column in trees:
        target = (row, column)
        distance = shortest_path(current, target)
        if distance == -1:
            return -1
        total += distance
        current = target
    return total
```

Enumerating simple paths is exponential in the number of walkable cells.

## Better insight: each segment is an ordinary unweighted shortest path

Breadth-first search reaches a target with the fewest moves. Stopping as soon
as the target is discovered avoids exploring the rest of the grid.

## Expert solution: sort trees, then BFS between consecutive targets

```python
from collections import deque


def cut_off_trees(forest: list[list[int]]) -> int:
    if not forest or not all(type(row) is list and row for row in forest):
        raise ValueError("forest must be a nonempty rectangular grid")
    row_count = len(forest)
    column_count = len(forest[0])
    if row_count > 50 or column_count > 50:
        raise ValueError("forest dimensions must not exceed 50")
    if any(len(row) != column_count for row in forest):
        raise ValueError("forest must be rectangular")
    if any(
        type(value) is not int or not 0 <= value <= 1_000_000_000
        for row in forest
        for value in row
    ):
        raise ValueError("forest values must be integers in the source range")

    trees = sorted(
        (height, row, column)
        for row, values in enumerate(forest)
        for column, height in enumerate(values)
        if height > 1
    )
    heights = [height for height, _, _ in trees]
    if len(heights) != len(set(heights)):
        raise ValueError("tree heights must be distinct")
    if not trees:
        return 0
    if forest[0][0] == 0:
        return -1

    def distance(start: tuple[int, int], target: tuple[int, int]) -> int:
        if start == target:
            return 0
        queue = deque([(start[0], start[1], 0)])
        visited = {start}
        while queue:
            row, column, steps = queue.popleft()
            for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_delta
                next_column = column + column_delta
                next_cell = (next_row, next_column)
                if not (
                    0 <= next_row < row_count
                    and 0 <= next_column < column_count
                    and forest[next_row][next_column] != 0
                    and next_cell not in visited
                ):
                    continue
                if next_cell == target:
                    return steps + 1
                visited.add(next_cell)
                queue.append((next_row, next_column, steps + 1))
        return -1

    total = 0
    current = (0, 0)
    for _, row, column in trees:
        target = (row, column)
        steps = distance(current, target)
        if steps == -1:
            return -1
        total += steps
        current = target
    return total
```

Each BFS returns the exact segment distance, and the fixed height order makes
their sum globally optimal.

**Complexity:** with `T` trees and `R*C` cells, `O(T*R*C)` time and
`O(R*C)` auxiliary space.
