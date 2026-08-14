# Focus300 061: LeetCode 407 - Trapping Rain Water II

**Source:** [LeetCode 407](https://leetcode.com/problems/trapping-rain-water-ii/)  
**Difficulty:** Hard  
**Pattern:** multi-source minimax Dijkstra from the boundary

## Exact contract

Given a rectangular grid of nonnegative elevations, return the water trapped
after rain. Water can escape through any boundary cell and adjacent movement is
orthogonal.

## First principles

For each cell, the lowest possible escape barrier is the minimum, over paths to
the boundary, of the maximum height on that path. Its water depth is that
barrier minus its own height when positive.

Processing all boundary cells in a min-heap grows the currently lowest closed
rim. When a cell is first reached, the popped rim is its optimal escape barrier;
push it back with effective height `max(rim, cell_height)`.

## Cases that decide correctness

- Boundary cells never retain water.
- Fewer than three rows or columns cannot enclose a cell.
- A low cell may still drain through a low path far away.
- The effective boundary height, not the raw neighbor height, propagates inward.
- Each cell should enter the heap once.

## Brute force: solve a minimax escape path for every interior cell

```python
import heapq


def trap_rain_water_brute(height_map: list[list[int]]) -> int:
    if not height_map or not height_map[0]:
        return 0
    row_count = len(height_map)
    column_count = len(height_map[0])

    def escape_height(start_row: int, start_column: int) -> int:
        best = [[10**30] * column_count for _ in range(row_count)]
        best[start_row][start_column] = height_map[start_row][start_column]
        heap = [(height_map[start_row][start_column], start_row, start_column)]
        while heap:
            barrier, row, column = heapq.heappop(heap)
            if barrier != best[row][column]:
                continue
            if row in (0, row_count - 1) or column in (0, column_count - 1):
                return barrier
            for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                next_row = row + row_delta
                next_column = column + column_delta
                next_barrier = max(barrier, height_map[next_row][next_column])
                if next_barrier < best[next_row][next_column]:
                    best[next_row][next_column] = next_barrier
                    heapq.heappush(heap, (next_barrier, next_row, next_column))
        raise RuntimeError("every grid cell reaches the boundary")

    water = 0
    for row in range(1, row_count - 1):
        for column in range(1, column_count - 1):
            water += escape_height(row, column) - height_map[row][column]
    return water
```

This runs a grid Dijkstra for every interior cell.

## Better insight: reverse all escape searches into one boundary flood

Every cell seeks the same boundary. Multi-source minimax Dijkstra shares that
work and finalizes cells in increasing escape-barrier order.

## Expert solution: priority flood from every boundary cell

```python
import heapq


def trap_rain_water(height_map: list[list[int]]) -> int:
    if not height_map or not height_map[0]:
        return 0
    row_count = len(height_map)
    column_count = len(height_map[0])
    if row_count < 3 or column_count < 3:
        return 0

    visited = [[False] * column_count for _ in range(row_count)]
    heap: list[tuple[int, int, int]] = []

    def add_boundary(row: int, column: int) -> None:
        if not visited[row][column]:
            visited[row][column] = True
            heapq.heappush(heap, (height_map[row][column], row, column))

    for row in range(row_count):
        add_boundary(row, 0)
        add_boundary(row, column_count - 1)
    for column in range(column_count):
        add_boundary(0, column)
        add_boundary(row_count - 1, column)

    water = 0
    while heap:
        boundary, row, column = heapq.heappop(heap)
        for row_delta, column_delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            next_row = row + row_delta
            next_column = column + column_delta
            if not (
                0 <= next_row < row_count
                and 0 <= next_column < column_count
                and not visited[next_row][next_column]
            ):
                continue
            visited[next_row][next_column] = True
            height = height_map[next_row][next_column]
            water += max(0, boundary - height)
            heapq.heappush(
                heap,
                (max(boundary, height), next_row, next_column),
            )
    return water
```

The first boundary that reaches a cell is its minimum possible escape barrier,
so its water depth is final at insertion.

**Complexity:** `O(rows*columns log(rows*columns))` time and
`O(rows*columns)` space.
