# Convex Hull (Monotonic Chain)

## Idea

The convex hull is the smallest convex polygon containing all points. After
sorting points, build lower and upper chains while removing non-left turns.

## Visual model

```text
new point creates right turn -> middle point lies inside/below hull -> pop it
```

## Classroom board: pop an inside point

```text
current hull ends A->B; new point C creates a right turn
B bends inward, so B cannot be an outer corner
pop B and test A's previous edge with C again
```

## Steps

1. Sort and deduplicate points by `(x, y)`.
2. Scan left to right to build the lower hull.
3. Scan right to left to build the upper hull.
4. Remove each chain's repeated endpoint and concatenate.

## First-principles derivation

After sorting points, walk around the outside boundary. Whenever the last two
chosen edges make an unwanted turn, the middle point lies inside or on the
current boundary and cannot be a hull corner.

The stack invariant is that its consecutive triples always turn in the allowed
direction.

## Classroom board: remove an interior point

```text
points: (0,0), (2,0), (1,1), (2,2), (0,2)

sorted lower-hull scan:
add (0,0)
add (0,2)
next (1,1): turn is right for lower hull
pop (0,2), add (1,1)
add (2,0): right turn -> pop (1,1)
lower boundary now (0,0) -> (2,0)

upper scan adds (2,2) -> (0,2)
final hull: (0,0), (2,0), (2,2), (0,2)
```

The interior point `(1,1)` is removed because it cannot support the outer
boundary.

## Pattern recognition

Use it for outer boundary, farthest-pair preprocessing, minimum enclosing
direction problems, or removing points that cannot be extreme.

## Implementation: exclude collinear interior boundary points

The code uses `Point` and `cross` from the
[geometry-primitives note](01-geometry-primitives.md).

### C++

```cpp
std::vector<Point> convexHull(std::vector<Point> points) {
    std::sort(points.begin(), points.end(), [](Point a, Point b) { return std::tie(a.x, a.y) < std::tie(b.x, b.y); });
    points.erase(std::unique(points.begin(), points.end(), [](Point a, Point b) { return a.x == b.x && a.y == b.y; }), points.end());
    if (points.size() <= 1) return points;
    std::vector<Point> hull;
    for (Point point : points) {
        while (hull.size() >= 2 && cross(hull[hull.size() - 2], hull.back(), point) <= 0) hull.pop_back();
        hull.push_back(point);
    }
    size_t lowerSize = hull.size();
    for (int index = points.size() - 2; index >= 0; --index) {
        while (hull.size() > lowerSize && cross(hull[hull.size() - 2], hull.back(), points[index]) <= 0) hull.pop_back();
        hull.push_back(points[index]);
    }
    hull.pop_back();
    return hull;
}
```

### Python

```python
def convex_hull(points: list[Point]) -> list[Point]:
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower: list[Point] = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[Point] = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]
```

### Java

```java
static List<Point> convexHull(List<Point> input) {
    List<Point> points = input.stream().distinct()
        .sorted(Comparator.comparingLong(Point::x).thenComparingLong(Point::y)).toList();
    if (points.size() <= 1) return new ArrayList<>(points);
    List<Point> lower = new ArrayList<>();
    for (Point point : points) {
        while (lower.size() >= 2 && cross(lower.get(lower.size() - 2), lower.get(lower.size() - 1), point) <= 0) lower.remove(lower.size() - 1);
        lower.add(point);
    }
    List<Point> upper = new ArrayList<>();
    for (int index = points.size() - 1; index >= 0; index--) {
        Point point = points.get(index);
        while (upper.size() >= 2 && cross(upper.get(upper.size() - 2), upper.get(upper.size() - 1), point) <= 0) upper.remove(upper.size() - 1);
        upper.add(point);
    }
    lower.remove(lower.size() - 1);
    upper.remove(upper.size() - 1);
    lower.addAll(upper);
    return lower;
}
```

## Why it works

Sorted order guarantees the next hull edge moves forward. A non-left turn makes
the middle point non-extreme, so removing it cannot remove a required corner.

## Complexity

Time is `O(n log n)` for sorting and space is `O(n)`.

## Common mistakes

- Forgetting duplicate points.
- Using `< 0` versus `<= 0` without deciding whether collinear boundary points
  must remain.
- Repeating the first point at the end unexpectedly.
