# ICPC300 078: CSES - Point in Polygon

**Source:** [CSES - Point in Polygon](https://cses.fi/problemset/task/2192/)  
**Pattern:** exact winding-number point classification

## Exact contract

Input gives a simple polygon with `n` integer-coordinate vertices and `m` query
points. For every query, output `INSIDE`, `OUTSIDE`, or `BOUNDARY`. Polygon
vertices are listed in boundary order and coordinates have absolute value at
most `10^9`.

## First principles

A point is on the boundary when it is collinear with an edge and lies inside
that edge's coordinate box. Otherwise, trace a horizontal ray. The winding
number changes when an edge crosses the ray upward on the point's left side or
downward on its right side. A nonzero winding number means inside.

All decisions use integer cross products, avoiding floating-point errors at
vertices and nearly horizontal edges.

## Cases that decide correctness

- Boundary testing must happen before ray crossings.
- Use half-open vertical comparisons so a polygon vertex is not counted twice.
- Horizontal edges never cross the ray but may contain the query.
- Concave polygons are valid; convex-only area tests are insufficient.

## Brute force: exact rational ray intersections

```python
from fractions import Fraction


def classify_point_fraction(
    polygon: list[tuple[int, int]],
    point: tuple[int, int],
) -> str:
    x, y = point
    crossings = 0
    for index, first in enumerate(polygon):
        second = polygon[(index + 1) % len(polygon)]
        x1, y1 = first
        x2, y2 = second
        cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if (
            cross == 0
            and min(x1, x2) <= x <= max(x1, x2)
            and min(y1, y2) <= y <= max(y1, y2)
        ):
            return "BOUNDARY"
        if (y1 > y) != (y2 > y):
            intersection_x = Fraction(x1 * (y2 - y1) + (y - y1) * (x2 - x1), y2 - y1)
            crossings += intersection_x > x
    return "INSIDE" if crossings % 2 else "OUTSIDE"
```

Fractions make the textbook ray definition exact but allocate many large
rational objects.

## Better: integer winding number

```python
def classify_point_winding(
    polygon: list[tuple[int, int]],
    point: tuple[int, int],
) -> str:
    x, y = point
    winding = 0
    for index, (x1, y1) in enumerate(polygon):
        x2, y2 = polygon[(index + 1) % len(polygon)]
        cross = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if (
            cross == 0
            and min(x1, x2) <= x <= max(x1, x2)
            and min(y1, y2) <= y <= max(y1, y2)
        ):
            return "BOUNDARY"
        if y1 <= y < y2 and cross > 0:
            winding += 1
        elif y2 <= y < y1 and cross < 0:
            winding -= 1
    return "INSIDE" if winding else "OUTSIDE"
```

This keeps the same `O(n)` scan but replaces rational arithmetic with exact
integer signs.

## Expert solution: batched integer classification

```python
import sys


def classify(polygon: list[tuple[int, int]], x: int, y: int) -> str:
    winding = 0
    previous_x, previous_y = polygon[-1]
    for current_x, current_y in polygon:
        cross = (current_x - previous_x) * (y - previous_y) - (
            current_y - previous_y
        ) * (x - previous_x)
        if (
            cross == 0
            and min(previous_x, current_x) <= x <= max(previous_x, current_x)
            and min(previous_y, current_y) <= y <= max(previous_y, current_y)
        ):
            return "BOUNDARY"
        if previous_y <= y < current_y and cross > 0:
            winding += 1
        elif current_y <= y < previous_y and cross < 0:
            winding -= 1
        previous_x, previous_y = current_x, current_y
    return "INSIDE" if winding else "OUTSIDE"


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count, query_count = data[0:2]
    offset = 2
    polygon = []
    for _ in range(vertex_count):
        polygon.append((data[offset], data[offset + 1]))
        offset += 2
    answers = []
    for _ in range(query_count):
        answers.append(classify(polygon, data[offset], data[offset + 1]))
        offset += 2
    print("\n".join(answers))


if __name__ == "__main__":
    solve()
```

The half-open winding rules count every genuine ray crossing once. Boundary
points are removed first, so nonzero winding is exactly the inside condition
for any simple polygon.

**Complexity:** `O(nm)` time and `O(n)` space for the polygon.

