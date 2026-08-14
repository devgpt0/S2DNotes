# ICPC300 280: Codeforces 1557D - Ezzat and Grid

**Source:** [Codeforces 1557D](https://codeforces.com/problemset/problem/1557/D)  
**Difficulty:** 2300  
**Pattern:** longest row chain with range-chmax DP

## Exact contract

The grid supplies inclusive column segments on numbered rows. Delete the fewest
rows so that every two consecutive remaining rows have an intersecting pair of
segments. Print the number and indices of deleted rows.

## First principles

Process rows in increasing order. For row `i`, query all its intervals for the
best chain ending at any earlier row whose interval covers a common column.
Then

`dp[i] = 1 + best_predecessor_length`.

After all queries for the row, range-chmax every one of its intervals with
`(dp[i],i)`. Delaying updates prevents a row from selecting itself.

## Cases that decide correctness

- Closed intervals intersect even at one endpoint.
- A row can have several overlapping or disjoint segments.
- Rows with no segments can form a length-one chain only.
- All queries for one row happen before its updates.
- Parent pointers reconstruct one longest kept row subsequence.

## Brute force: build every earlier-row transition

```python
def ezzat_grid_brute(
    row_count: int,
    segments: list[tuple[int, int, int]],
) -> list[int]:
    by_row: list[list[tuple[int, int]]] = [[] for _ in range(row_count)]
    for row, left, right in segments:
        by_row[row].append((left, right))

    dynamic = [1] * row_count
    parent = [-1] * row_count
    for row in range(row_count):
        for previous in range(row):
            intersects = any(
                max(left, old_left) <= min(right, old_right)
                for left, right in by_row[row]
                for old_left, old_right in by_row[previous]
            )
            if intersects and dynamic[previous] + 1 > dynamic[row]:
                dynamic[row] = dynamic[previous] + 1
                parent[row] = previous

    last = max(range(row_count), key=dynamic.__getitem__)
    kept: set[int] = set()
    while last != -1:
        kept.add(last)
        last = parent[last]
    return [row for row in range(row_count) if row not in kept]
```

This takes `O(n^2 s^2)` time in the densest interval distribution.

## Better insight: common columns identify every legal predecessor

Coordinate-compress interval endpoints. Updating every compressed point in an
interval is sufficient: two closed intervals share at least one endpoint from
the global coordinate set whenever they intersect.

## Expert solution: range maximum queries and range chmax updates

```python
from bisect import bisect_left, bisect_right
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    row_count, segment_count = map(int, input_stream.readline().split())
    by_row: list[list[tuple[int, int]]] = [[] for _ in range(row_count)]
    coordinates: list[int] = []
    for _ in range(segment_count):
        row, left, right = map(int, input_stream.readline().split())
        row -= 1
        by_row[row].append((left, right))
        coordinates.extend((left, right))
    ordered = sorted(set(coordinates))
    coordinate_count = len(ordered)
    maximum = [(0, -1)] * (4 * coordinate_count)
    lazy = [(0, -1)] * (4 * coordinate_count)

    def apply(node: int, value: tuple[int, int]) -> None:
        maximum[node] = max(maximum[node], value)
        lazy[node] = max(lazy[node], value)

    def push(node: int) -> None:
        if lazy[node] != (0, -1):
            apply(node * 2, lazy[node])
            apply(node * 2 + 1, lazy[node])
            lazy[node] = (0, -1)

    def update(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        value: tuple[int, int],
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            apply(node, value)
            return
        push(node)
        middle = (left + right) // 2
        update(node * 2, left, middle, query_left, query_right, value)
        update(node * 2 + 1, middle, right, query_left, query_right, value)
        maximum[node] = max(maximum[node * 2], maximum[node * 2 + 1])

    def query(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
    ) -> tuple[int, int]:
        if query_right <= left or right <= query_left:
            return (0, -1)
        if query_left <= left and right <= query_right:
            return maximum[node]
        push(node)
        middle = (left + right) // 2
        return max(
            query(node * 2, left, middle, query_left, query_right),
            query(node * 2 + 1, middle, right, query_left, query_right),
        )

    dynamic = [1] * row_count
    parent = [-1] * row_count
    best = (0, -1)
    for row in range(row_count):
        predecessor = (0, -1)
        compressed: list[tuple[int, int]] = []
        for left, right in by_row[row]:
            query_left = bisect_left(ordered, left)
            query_right = bisect_right(ordered, right)
            compressed.append((query_left, query_right))
            predecessor = max(
                predecessor,
                query(1, 0, coordinate_count, query_left, query_right),
            )
        dynamic[row] = predecessor[0] + 1
        parent[row] = predecessor[1]
        value = (dynamic[row], row)
        for query_left, query_right in compressed:
            update(
                1,
                0,
                coordinate_count,
                query_left,
                query_right,
                value,
            )
        best = max(best, value)

    kept: set[int] = set()
    row = best[1]
    while row != -1:
        kept.add(row)
        row = parent[row]
    removed = [row + 1 for row in range(row_count) if row not in kept]
    print(len(removed))
    print(*removed)


if __name__ == "__main__":
    solve()
```

The segment tree exposes exactly the best prior chain sharing a column with
the current row; parent links therefore recover an optimal retained chain.

**Complexity:** `O((n+m) log m)` time and `O(n+m)` space.
