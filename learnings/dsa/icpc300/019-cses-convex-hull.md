# ICPC300 019: CSES - Convex Hull

**Source:** [CSES - Convex Hull](https://cses.fi/problemset/task/2195/)  
**Pattern:** monotone chain with collinear boundary points  
**Goal:** Output every input point on the boundary of the convex hull in cyclic
order, including points lying between the corner vertices on a hull edge.

## 1. Problem in plain words

Imagine stretching a rubber band around all points. Every input point touched
by the band belongs in the answer. Unlike many convex-hull variants, the CSES
task requires collinear points along a boundary edge too, not only its two
endpoints.

For rectangle corners plus `(1, 0)` on the bottom edge, `(1, 0)` must appear in
the output. A collinear point strictly inside the rectangle must not.

## 2. First principles

For points `o`, `a`, and `b`, the signed cross product is:

`cross(o, a, b) = (a.x-o.x)(b.y-o.y) - (a.y-o.y)(b.x-o.x)`.

- positive: `o -> a -> b` turns counterclockwise;
- negative: it turns clockwise;
- zero: the three points are collinear.

Sort points lexicographically. The lower hull cannot contain a clockwise turn;
the upper hull obeys the same rule when scanned in reverse. To retain boundary
collinear points, pop only on a **strict** clockwise turn (`cross < 0`).

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Three or more collinear points on an edge | Include all of them once. |
| All points collinear | Return every point in line order. |
| Interior point | Exclude it. |
| Very large coordinates | Use integer cross products, not floating slopes. |
| Duplicate point supplied to this function | Reject it explicitly. |

## 4. Brute force: test every supporting line

A point pair lies on a supporting line when every other point is on one side
of their line or on the line. Mark both endpoints of every such pair. The
result is a lexicographically sorted boundary-point oracle; ordering the final
polygon is left to the faster algorithms.

```python
Point = tuple[int, int]


def convex_hull_boundary_brute_force(points: list[Point]) -> list[Point]:
    if len(set(points)) != len(points):
        raise ValueError("input points must be distinct")
    if len(points) <= 2:
        return sorted(points)

    def cross(origin: Point, first: Point, second: Point) -> int:
        return (first[0] - origin[0]) * (second[1] - origin[1]) - (
            first[1] - origin[1]
        ) * (second[0] - origin[0])

    boundary: set[Point] = set()
    for first_index in range(len(points)):
        for second_index in range(first_index + 1, len(points)):
            has_positive = False
            has_negative = False
            for point in points:
                turn = cross(points[first_index], points[second_index], point)
                has_positive |= turn > 0
                has_negative |= turn < 0
            if not (has_positive and has_negative):
                boundary.add(points[first_index])
                boundary.add(points[second_index])
    return sorted(boundary)
```

**Complexity:** `O(n^3)` time and `O(n)` output space.

## 5. Better: Jarvis march

Jarvis march chooses the next supporting direction by scanning every point.
When several points lie on that hull edge, append them in distance order. If
`h` points are on the boundary, the scan costs `O(nh)`.

```python
Point = tuple[int, int]


def convex_hull_jarvis(points: list[Point]) -> list[Point]:
    if len(set(points)) != len(points):
        raise ValueError("input points must be distinct")
    if len(points) <= 2:
        return sorted(points)

    def cross(origin: Point, first: Point, second: Point) -> int:
        return (first[0] - origin[0]) * (second[1] - origin[1]) - (
            first[1] - origin[1]
        ) * (second[0] - origin[0])

    def distance_squared(first: Point, second: Point) -> int:
        return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2

    ordered = sorted(points)
    if all(cross(ordered[0], ordered[-1], point) == 0 for point in ordered):
        return ordered

    start = ordered[0]
    current = start
    hull = [start]

    while True:
        candidate = next(point for point in points if point != current)
        for point in points:
            if point == current:
                continue
            turn = cross(current, candidate, point)
            if turn < 0 or (
                turn == 0
                and distance_squared(current, point)
                > distance_squared(current, candidate)
            ):
                candidate = point

        edge_points = [
            point
            for point in points
            if point != current and cross(current, candidate, point) == 0
        ]
        edge_points.sort(key=lambda point: distance_squared(current, point))
        for point in edge_points:
            if point != start:
                hull.append(point)

        current = candidate
        if current == start:
            return hull
```

**Complexity:** `O(nh + n log n)` time and `O(n)` memory.

## 6. Expert solution: monotone chain

Build lower and upper boundary chains. The all-collinear special case prevents
the two chains from returning every interior line point twice.

```python
Point = tuple[int, int]


def convex_hull(points: list[Point]) -> list[Point]:
    if len(set(points)) != len(points):
        raise ValueError("input points must be distinct")
    if len(points) <= 2:
        return sorted(points)

    def cross(origin: Point, first: Point, second: Point) -> int:
        return (first[0] - origin[0]) * (second[1] - origin[1]) - (
            first[1] - origin[1]
        ) * (second[0] - origin[0])

    ordered = sorted(points)
    if all(cross(ordered[0], ordered[-1], point) == 0 for point in ordered):
        return ordered

    lower: list[Point] = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) < 0:
            lower.pop()
        lower.append(point)

    upper: list[Point] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) < 0:
            upper.pop()
        upper.append(point)

    return lower[:-1] + upper[:-1]
```

### Why the expert code is correct

- Sorting gives the left-to-right order required for both monotone chains.
- A strict clockwise turn lies inside the convex envelope of its neighbors, so
  its middle point cannot remain on that chain and is safely removed.
- Counterclockwise turns remain, and zero turns remain specifically to satisfy
  the source requirement to output all boundary-collinear points.
- Lower and upper chains cover the entire boundary; dropping each final point
  removes their two duplicated endpoints.

**Complexity:** `O(n log n)` time for sorting and `O(n)` memory. Each point is
pushed and popped at most once per chain.

## 7. What to remember

The pop sign encodes the problem variant. Use `cross <= 0` to discard edge-
collinear points; CSES Convex Hull needs all boundary points, so use `cross < 0`.
