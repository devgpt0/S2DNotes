# Geometry Primitives

## Idea

The 2D cross product tells whether three points turn left, turn right, or are
collinear. It is the base of most exact integer geometry.

## Visual model

```text
cross(B-A, C-A) > 0  -> left turn
cross(B-A, C-A) < 0  -> right turn
cross(B-A, C-A) = 0  -> collinear
```

## Classroom board: read a cross-product sign

```text
A=(0,0), B=(2,0)
C=(1,1) lies above directed line A->B
cross(B-A, C-A) = 2*1 - 0*1 = 2 > 0 -> left turn
```

## Steps for segment intersection

1. Compute orientations of each segment's endpoints against the other segment.
2. Opposite orientations on both sides mean a proper intersection.
3. Handle zero orientations by checking whether the point lies inside the
   segment's bounding box.

## First-principles derivation

Two-dimensional geometry becomes exact algebra when directions are compared by
the cross product. Its sign tells whether three points turn left, turn right,
or remain collinear.

Use integer arithmetic whenever coordinates are integers; floating-point
angles introduce unnecessary precision errors.

## Classroom board: orientation by signed area

```text
A=(0,0), B=(3,0), C=(2,2)

AB = (3,0)
AC = (2,2)

cross(AB,AC) = 3*2 - 0*2 = 6 > 0
therefore A -> B -> C is a left turn

replace C with (2,-2):
cross = 3*(-2) - 0*2 = -6 < 0
therefore the turn is right
```

A zero cross product means the three points are collinear; bounding-box checks
are still needed to decide whether a point lies on a segment.

## Pattern recognition

Use cross products for orientation, line/segment intersection, polygon area,
convex hulls, and point-in-polygon tests.

## Implementation: closed segment intersection

### C++

```cpp
struct Point { long long x; long long y; };

long long cross(Point first, Point second, Point third) {
    return (second.x - first.x) * (third.y - first.y)
         - (second.y - first.y) * (third.x - first.x);
}

bool onSegment(Point first, Point second, Point point) {
    return cross(first, second, point) == 0
        && std::min(first.x, second.x) <= point.x && point.x <= std::max(first.x, second.x)
        && std::min(first.y, second.y) <= point.y && point.y <= std::max(first.y, second.y);
}

bool segmentsIntersect(Point a, Point b, Point c, Point d) {
    long long first = cross(a, b, c), second = cross(a, b, d);
    long long third = cross(c, d, a), fourth = cross(c, d, b);
    if (((first > 0 && second < 0) || (first < 0 && second > 0))
        && ((third > 0 && fourth < 0) || (third < 0 && fourth > 0))) return true;
    return (first == 0 && onSegment(a, b, c)) || (second == 0 && onSegment(a, b, d))
        || (third == 0 && onSegment(c, d, a)) || (fourth == 0 && onSegment(c, d, b));
}
```

### Python

```python
Point = tuple[int, int]


def cross(first: Point, second: Point, third: Point) -> int:
    return ((second[0] - first[0]) * (third[1] - first[1])
            - (second[1] - first[1]) * (third[0] - first[0]))


def on_segment(first: Point, second: Point, point: Point) -> bool:
    return (cross(first, second, point) == 0
            and min(first[0], second[0]) <= point[0] <= max(first[0], second[0])
            and min(first[1], second[1]) <= point[1] <= max(first[1], second[1]))


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool:
    first, second = cross(a, b, c), cross(a, b, d)
    third, fourth = cross(c, d, a), cross(c, d, b)
    proper = ((first > 0 > second or second > 0 > first)
              and (third > 0 > fourth or fourth > 0 > third))
    return (proper or (first == 0 and on_segment(a, b, c))
            or (second == 0 and on_segment(a, b, d))
            or (third == 0 and on_segment(c, d, a))
            or (fourth == 0 and on_segment(c, d, b)))
```

### Java

```java
record Point(long x, long y) {}

static long cross(Point first, Point second, Point third) {
    return (second.x() - first.x()) * (third.y() - first.y())
        - (second.y() - first.y()) * (third.x() - first.x());
}

static boolean onSegment(Point first, Point second, Point point) {
    return cross(first, second, point) == 0
        && Math.min(first.x(), second.x()) <= point.x() && point.x() <= Math.max(first.x(), second.x())
        && Math.min(first.y(), second.y()) <= point.y() && point.y() <= Math.max(first.y(), second.y());
}

static boolean segmentsIntersect(Point a, Point b, Point c, Point d) {
    long first = cross(a, b, c), second = cross(a, b, d);
    long third = cross(c, d, a), fourth = cross(c, d, b);
    boolean proper = ((first > 0 && second < 0) || (first < 0 && second > 0))
        && ((third > 0 && fourth < 0) || (third < 0 && fourth > 0));
    return proper || (first == 0 && onSegment(a, b, c)) || (second == 0 && onSegment(a, b, d))
        || (third == 0 && onSegment(c, d, a)) || (fourth == 0 && onSegment(c, d, b));
}
```

## Why it works

Properly crossing segments place each pair of endpoints on opposite sides of
the other line. Bounding-box checks cover touching and overlapping collinear
cases.

## Complexity

Time and space are `O(1)`.

## Common mistakes

- Using floating-point slopes for integer points.
- Ignoring collinear overlap and endpoint touching.
- Overflowing cross products; coordinate differences may require wider than
  64-bit arithmetic for extreme constraints.
