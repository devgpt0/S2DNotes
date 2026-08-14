# ICPC300 246: Codeforces 1301F - Super Jaber

**Source:** [Codeforces 1301F](https://codeforces.com/problemset/problem/1301/F)  
**Difficulty:** 2400  
**Pattern:** BFS from color sets plus teleport decomposition

## Exact contract

Every cell of an `n` by `m` grid has one of `k` colors. A move costs one and
either enters an orthogonally adjacent cell or teleports between any two cells
of the same color. Answer shortest-distance queries between cells.

## First principles

Let `dist[c][v]` be the shortest distance from any cell of color `c` to cell
`v`. Compute one row with multi-source BFS. During that BFS, expand all cells
of any newly reached color once; this represents its complete teleport clique
without listing quadratic edges.

A shortest query path is either the Manhattan path or uses a teleport of some
color `c`. Splitting at that teleport gives

`dist[c][start] + 1 + dist[c][finish]`.

The two distance terms already include any other teleports used before or
after the chosen one.

## Cases that decide correctness

- Teleporting costs one, even between a cell and itself.
- A color can occur once or many times.
- A color absent from the grid contributes no teleport candidate.
- The Manhattan path remains a valid candidate.
- Each color clique must be expanded at most once per BFS.
- Packed integer arrays avoid Python-object memory overhead.

## Brute force: one implicit-graph BFS per query

```python
from collections import deque


def super_jaber_brute(
    grid: list[list[int]],
    queries: list[tuple[int, int, int, int]],
) -> list[int]:
    row_count = len(grid)
    column_count = len(grid[0])
    color_count = max(max(row) for row in grid) + 1
    cells_by_color: list[list[int]] = [[] for _ in range(color_count)]
    for row in range(row_count):
        for column in range(column_count):
            cell = row * column_count + column
            cells_by_color[grid[row][column]].append(cell)

    answers: list[int] = []
    for start_row, start_column, finish_row, finish_column in queries:
        start = start_row * column_count + start_column
        finish = finish_row * column_count + finish_column
        distance = [-1] * (row_count * column_count)
        distance[start] = 0
        queue = deque([start])
        expanded_color = [False] * color_count
        while queue:
            cell = queue.popleft()
            if cell == finish:
                break
            row, column = divmod(cell, column_count)
            next_distance = distance[cell] + 1
            neighbors = []
            if row:
                neighbors.append(cell - column_count)
            if row + 1 < row_count:
                neighbors.append(cell + column_count)
            if column:
                neighbors.append(cell - 1)
            if column + 1 < column_count:
                neighbors.append(cell + 1)
            color = grid[row][column]
            if not expanded_color[color]:
                expanded_color[color] = True
                neighbors.extend(cells_by_color[color])
            for neighbor in neighbors:
                if distance[neighbor] == -1:
                    distance[neighbor] = next_distance
                    queue.append(neighbor)
        answers.append(distance[finish])
    return answers
```

This is `O(qnm)` time and `O(nm+k)` extra space.

## Better insight: only the teleport color matters at query time

Precompute distances from every color set once. A query then checks `k`
possible teleport colors instead of traversing the grid.

## Expert solution: `k` multi-source BFS runs

```python
from array import array
from collections import deque
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    row_count, column_count, color_count = map(int, input_stream.readline().split())
    cell_count = row_count * column_count
    colors = array("i")
    cells_by_color: list[list[int]] = [[] for _ in range(color_count)]
    for row in range(row_count):
        row_colors = [value - 1 for value in map(int, input_stream.readline().split())]
        for column, color in enumerate(row_colors):
            cell = row * column_count + column
            colors.append(color)
            cells_by_color[color].append(cell)

    distance_by_color: list[array[int]] = []
    for source_color in range(color_count):
        distance = array("i", [-1]) * cell_count
        queue = deque(cells_by_color[source_color])
        for cell in cells_by_color[source_color]:
            distance[cell] = 0
        expanded_color = [False] * color_count
        expanded_color[source_color] = True

        while queue:
            cell = queue.popleft()
            row, column = divmod(cell, column_count)
            next_distance = distance[cell] + 1

            if row and distance[cell - column_count] == -1:
                distance[cell - column_count] = next_distance
                queue.append(cell - column_count)
            if row + 1 < row_count and distance[cell + column_count] == -1:
                distance[cell + column_count] = next_distance
                queue.append(cell + column_count)
            if column and distance[cell - 1] == -1:
                distance[cell - 1] = next_distance
                queue.append(cell - 1)
            if column + 1 < column_count and distance[cell + 1] == -1:
                distance[cell + 1] = next_distance
                queue.append(cell + 1)

            color = colors[cell]
            if not expanded_color[color]:
                expanded_color[color] = True
                for destination in cells_by_color[color]:
                    if distance[destination] == -1:
                        distance[destination] = next_distance
                        queue.append(destination)
        distance_by_color.append(distance)

    answers: list[str] = []
    query_count = int(input_stream.readline())
    for _ in range(query_count):
        start_row, start_column, finish_row, finish_column = map(
            int, input_stream.readline().split()
        )
        start_row -= 1
        start_column -= 1
        finish_row -= 1
        finish_column -= 1
        start = start_row * column_count + start_column
        finish = finish_row * column_count + finish_column
        answer = abs(start_row - finish_row) + abs(start_column - finish_column)
        for distance in distance_by_color:
            if distance[start] != -1:
                answer = min(answer, distance[start] + distance[finish] + 1)
        answers.append(str(answer))
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

Multi-source BFS gives each `dist[c][v]` exactly, and the path split considers
every possible teleport color.

**Complexity:** `O(knm+qk)` time and `O(knm)` space.
