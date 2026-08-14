# Geometry and Lattice Points

Competitive geometry should stay in integer arithmetic whenever input points
are integral. Cross products avoid precision errors for orientation, area, and
convex hull.

## Vectors, dot product, and cross product

For vectors `u` and `v`, dot product `u.x*v.x + u.y*v.y` tests angles; cross
product `u.x*v.y - u.y*v.x` gives signed area and turn direction. A positive
cross is counter-clockwise, negative is clockwise, and zero is collinear.

```python
Point = tuple[int, int]


def cross(origin: Point, first: Point, second: Point) -> int:
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (first[1] - origin[1]) * (second[0] - origin[0])


print(cross((0, 0), (2, 0), (1, 1)))
```

Output:

```text
2
```

Never compare slopes by division when a cross-product comparison works; vertical
lines and floating-point rounding then disappear.

## Polygon area and boundary points

Shoelace gives twice the signed area of vertices in boundary order:
`area2 = abs(sum(xi*y(i+1) - yi*x(i+1)))`. For an integer segment, the number
of lattice intervals on its boundary is `gcd(abs(dx), abs(dy))`.

```python
from math import gcd


def doubled_polygon_area(points: list[Point]) -> int:
    if len(points) < 3:
        raise ValueError("a polygon needs at least three points")
    return abs(sum(x1 * y2 - y1 * x2 for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1])))


print(doubled_polygon_area([(0, 0), (4, 0), (0, 3)]))
print(gcd(6, 4))
```

Output:

```text
12
2
```

Pick's theorem for a simple lattice polygon is `area = interior + boundary / 2 - 1`.
Use doubled area to keep every calculation integral.

## Convex hull and intersections

Monotonic-chain convex hull sorts points and pops while the last turn violates
the chosen collinearity rule; it is `O(n log n)`. Segment intersection needs
orientation tests plus bounding-box checks for collinear cases. Decide whether
touching endpoints and collinear boundary points count before coding.

## Checklist

- Use `int`, not `float`, for orientation and polygon area from integer input.
- Document whether collinear hull points stay or are removed.
- Compare squared distances unless an actual distance is required.
- Handle a degenerate segment and duplicate points explicitly.
