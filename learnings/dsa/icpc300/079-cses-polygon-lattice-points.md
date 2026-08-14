# ICPC300 079: CSES - Polygon Lattice Points

**Source:** [CSES - Polygon Lattice Points](https://cses.fi/problemset/task/2193/)  
**Pattern:** shoelace formula, lattice edges, and Pick's theorem

## Exact contract

Input gives a simple polygon with `3 <= n <= 100000` integer-coordinate
vertices in boundary order. Output two integers: the number of integer lattice
points strictly inside the polygon and the number on its boundary.

## First principles

An edge with displacement `(dx, dy)` contains `gcd(|dx|, |dy|) + 1` lattice
points including both endpoints. Summing `gcd` over cyclic edges counts every
boundary vertex once, so it gives boundary count `B`.

The shoelace formula gives doubled area `A2`. Pick's theorem says
`A = I + B/2 - 1`, hence `I = (A2 - B + 2)/2`.

## Cases that decide correctness

- Use absolute shoelace area because either polygon orientation is allowed.
- Summing `gcd`, not `gcd + 1`, avoids counting each shared vertex twice.
- Horizontal and vertical edges work because `gcd(dx, 0) = |dx|`.
- Doubled area keeps all arithmetic integral and exact.

## Brute force: classify every lattice point in the bounding box

```python
def lattice_points_brute(polygon: list[tuple[int, int]]) -> tuple[int, int]:
    def classify(x: int, y: int) -> str:
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

    minimum_x = min(x for x, _ in polygon)
    maximum_x = max(x for x, _ in polygon)
    minimum_y = min(y for _, y in polygon)
    maximum_y = max(y for _, y in polygon)
    inside = 0
    boundary = 0
    for x in range(minimum_x, maximum_x + 1):
        for y in range(minimum_y, maximum_y + 1):
            location = classify(x, y)
            inside += location == "INSIDE"
            boundary += location == "BOUNDARY"
    return inside, boundary
```

Its work depends on coordinate range and can be enormous.

## Better for small coordinates: enumerate boundary points once

```python
from math import gcd


def lattice_points_with_boundary_set(
    polygon: list[tuple[int, int]],
) -> tuple[int, int]:
    boundary_points: set[tuple[int, int]] = set()
    for index, (x1, y1) in enumerate(polygon):
        x2, y2 = polygon[(index + 1) % len(polygon)]
        steps = gcd(abs(x2 - x1), abs(y2 - y1))
        step_x = (x2 - x1) // steps
        step_y = (y2 - y1) // steps
        for step in range(steps):
            boundary_points.add((x1 + step * step_x, y1 + step * step_y))

    minimum_x = min(x for x, _ in polygon)
    maximum_x = max(x for x, _ in polygon)
    minimum_y = min(y for _, y in polygon)
    maximum_y = max(y for _, y in polygon)

    def inside(x: int, y: int) -> bool:
        winding = 0
        previous_x, previous_y = polygon[-1]
        for current_x, current_y in polygon:
            cross = (current_x - previous_x) * (y - previous_y) - (
                current_y - previous_y
            ) * (x - previous_x)
            if previous_y <= y < current_y and cross > 0:
                winding += 1
            elif current_y <= y < previous_y and cross < 0:
                winding -= 1
            previous_x, previous_y = current_x, current_y
        return winding != 0

    interior = sum(
        (x, y) not in boundary_points and inside(x, y)
        for x in range(minimum_x, maximum_x + 1)
        for y in range(minimum_y, maximum_y + 1)
    )
    return interior, len(boundary_points)
```

This avoids repeatedly testing boundary collinearity, but still scans the
coordinate bounding box and materializes every boundary point.

## Expert solution: Pick's theorem in one edge scan

```python
from math import gcd
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    vertex_count = data[0]
    polygon = [
        (data[1 + 2 * index], data[2 + 2 * index]) for index in range(vertex_count)
    ]
    doubled_area = 0
    boundary = 0

    for index, (x1, y1) in enumerate(polygon):
        x2, y2 = polygon[(index + 1) % vertex_count]
        doubled_area += x1 * y2 - y1 * x2
        boundary += gcd(abs(x2 - x1), abs(y2 - y1))

    doubled_area = abs(doubled_area)
    interior = (doubled_area - boundary + 2) // 2
    print(interior, boundary)


if __name__ == "__main__":
    solve()
```

Shoelace supplies exact doubled area and the gcd sum supplies exact boundary
count. Pick's theorem then determines the only possible interior count.

**Complexity:** `O(n log C)` time for coordinate magnitude `C` and `O(n)`
input storage.

