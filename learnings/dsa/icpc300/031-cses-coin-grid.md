# ICPC300 031: CSES - Coin Grid

**Source:** [CSES - Coin Grid](https://cses.fi/problemset/task/1709/)  
**Pattern:** bipartite matching and Konig's minimum vertex cover

## Exact contract

Input gives `n` (`1 <= n <= 500`) and an `n x n` grid. Character `o` marks a
coin and `.` an empty square. In one move, choose one whole row or one whole
column and collect every coin on it. Output the minimum number of moves, then
describe each move as `1 r` for row `r` or `2 c` for column `c`, using
one-based indices.

## First principles

Make a bipartite graph with one vertex for every row and one for every column.
Each coin becomes an edge between its row and column. A set of moves collects
all coins exactly when its vertices touch every edge: it is a vertex cover.

Konig's theorem says that in a bipartite graph, the size of a minimum vertex
cover equals the size of a maximum matching. After finding a maximum matching,
start alternating searches from unmatched rows. If `ZL` and `ZR` are the
reached rows and columns, one minimum cover is `(rows - ZL) union ZR`.

## Cases that decide correctness

- An empty grid needs zero moves and no following lines.
- Selecting one row can cover many coins; coins are graph edges, not vertices.
- Alternating search uses unmatched edges from rows to columns and matched
  edges from columns back to rows.
- Several minimum covers may exist; any one is valid.

## Brute force: enumerate every row-and-column subset

```python
def minimum_coin_cover_brute(grid: list[str]) -> list[tuple[int, int]]:
    size = len(grid)
    coins = [
        (row, column)
        for row in range(size)
        for column in range(size)
        if grid[row][column] == "o"
    ]
    best_mask = 0
    best_size = 2 * size + 1

    for mask in range(1 << (2 * size)):
        selected = mask.bit_count()
        if selected >= best_size:
            continue
        if all(
            mask & (1 << row) or mask & (1 << (size + column)) for row, column in coins
        ):
            best_size = selected
            best_mask = mask

    moves = [(1, row + 1) for row in range(size) if best_mask & (1 << row)]
    moves.extend(
        (2, column + 1) for column in range(size) if best_mask & (1 << (size + column))
    )
    return moves
```

**Complexity:** `O(4^n n^2)` time and `O(n^2)` space for the coin list.

## Better: Kuhn matching and the alternating cover

```python
def minimum_coin_cover_kuhn(grid: list[str]) -> list[tuple[int, int]]:
    size = len(grid)
    graph = [[column for column, cell in enumerate(row) if cell == "o"] for row in grid]
    matched_column = [-1] * size

    def augment(row: int, seen_rows: list[bool]) -> bool:
        if seen_rows[row]:
            return False
        seen_rows[row] = True
        for column in graph[row]:
            owner = matched_column[column]
            if owner == -1 or augment(owner, seen_rows):
                matched_column[column] = row
                return True
        return False

    for row in range(size):
        augment(row, [False] * size)

    matched_row = [-1] * size
    for column, row in enumerate(matched_column):
        if row != -1:
            matched_row[row] = column

    reached_rows = [False] * size
    reached_columns = [False] * size
    stack = [row for row in range(size) if matched_row[row] == -1]
    for row in stack:
        reached_rows[row] = True

    while stack:
        row = stack.pop()
        for column in graph[row]:
            if matched_row[row] == column or reached_columns[column]:
                continue
            reached_columns[column] = True
            owner = matched_column[column]
            if owner != -1 and not reached_rows[owner]:
                reached_rows[owner] = True
                stack.append(owner)

    moves = [(1, row + 1) for row in range(size) if not reached_rows[row]]
    moves.extend((2, column + 1) for column in range(size) if reached_columns[column])
    return moves
```

Kuhn's algorithm is simple and exact, but takes `O(VE)` time in the worst
case.

## Expert solution: Hopcroft-Karp plus minimum-cover recovery

```python
from collections import deque
import sys


def minimum_vertex_cover(
    graph: list[list[int]], column_count: int
) -> list[tuple[int, int]]:
    row_count = len(graph)
    matched_row = [-1] * row_count
    matched_column = [-1] * column_count
    distance = [-1] * row_count

    def build_layers() -> int:
        queue: deque[int] = deque()
        shortest_augmenting = row_count + 1
        for row in range(row_count):
            if matched_row[row] == -1:
                distance[row] = 0
                queue.append(row)
            else:
                distance[row] = -1

        while queue:
            row = queue.popleft()
            if distance[row] + 1 > shortest_augmenting:
                continue
            for column in graph[row]:
                owner = matched_column[column]
                if owner == -1:
                    shortest_augmenting = distance[row] + 1
                elif distance[owner] == -1:
                    distance[owner] = distance[row] + 1
                    queue.append(owner)
        return shortest_augmenting

    def augment(row: int, shortest_augmenting: int) -> bool:
        for column in graph[row]:
            owner = matched_column[column]
            if owner == -1:
                if distance[row] + 1 != shortest_augmenting:
                    continue
            elif distance[owner] != distance[row] + 1 or not augment(
                owner,
                shortest_augmenting,
            ):
                continue
            matched_row[row] = column
            matched_column[column] = row
            return True
        distance[row] = -1
        return False

    while True:
        shortest_augmenting = build_layers()
        if shortest_augmenting > row_count:
            break
        for row in range(row_count):
            if matched_row[row] == -1:
                augment(row, shortest_augmenting)

    reached_rows = [False] * row_count
    reached_columns = [False] * column_count
    stack = [row for row in range(row_count) if matched_row[row] == -1]
    for row in stack:
        reached_rows[row] = True

    while stack:
        row = stack.pop()
        for column in graph[row]:
            if matched_row[row] == column or reached_columns[column]:
                continue
            reached_columns[column] = True
            owner = matched_column[column]
            if owner != -1 and not reached_rows[owner]:
                reached_rows[owner] = True
                stack.append(owner)

    cover = [(1, row + 1) for row in range(row_count) if not reached_rows[row]]
    cover.extend(
        (2, column + 1) for column in range(column_count) if reached_columns[column]
    )
    return cover


def solve() -> None:
    input_stream = sys.stdin.buffer
    size = int(input_stream.readline())
    graph = []
    for _ in range(size):
        row = input_stream.readline().strip()
        graph.append([column for column, cell in enumerate(row) if cell == ord("o")])

    cover = minimum_vertex_cover(graph, size)
    output = [str(len(cover))]
    output.extend(f"{kind} {index}" for kind, index in cover)
    print("\n".join(output))


if __name__ == "__main__":
    solve()
```

Hopcroft-Karp augments a maximal set of shortest alternating paths per phase.
The recovered cover touches every edge and has exactly the matching size, so
Konig's theorem proves it is minimum.

**Complexity:** `O(E sqrt(V))` time and `O(V + E)` space.
