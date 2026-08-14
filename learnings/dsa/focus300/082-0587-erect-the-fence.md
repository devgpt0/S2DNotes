# Focus300 082: LeetCode 587 - Erect the Fence

**Source:** [LeetCode 587](https://leetcode.com/problems/erect-the-fence/)  
**Difficulty:** Hard  
**Pattern:** convex hull with collinear boundary retention

## Exact contract

Given distinct integer-coordinate trees, return every tree on the boundary of
the minimum convex fence enclosing all trees. Collinear trees along a fence
edge are part of the answer. Output order is irrelevant to the source; the
implementations below return lexicographic order for deterministic tests.

## First principles

For three points `o`, `a`, and `b`, the cross product of vectors `oa` and `ob`
is positive for a counterclockwise turn, negative for a clockwise turn, and
zero for collinearity. A convex-hull scan removes only clockwise turns. Keeping
zero turns is what preserves every tree lying on an edge.

## Cases that decide correctness

- Zero, one, or two input points are all boundary points.
- If all trees are collinear, every tree must be returned.
- Collinear points between two extreme corners must not be discarded.
- Duplicate coordinates are outside the source contract and fail fast here.
- Exact integer cross products avoid floating-point slope errors.

## Brute force: find every supporting line

```python
from collections.abc import Sequence


Point = tuple[int, int]


def fence_trees_brute(trees: Sequence[Point]) -> list[Point]:
    if any(
        type(point) is not tuple
        or len(point) != 2
        or any(type(coordinate) is not int for coordinate in point)
        for point in trees
    ):
        raise TypeError("each tree must be a pair of integers")
    if len(set(trees)) != len(trees):
        raise ValueError("tree coordinates must be distinct")
    if len(trees) < 3:
        return sorted(trees)

    boundary: set[Point] = set()
    for first_index, first in enumerate(trees):
        for second in trees[first_index + 1 :]:
            signs = {
                (second[0] - first[0]) * (point[1] - first[1])
                - (second[1] - first[1]) * (point[0] - first[0])
                for point in trees
            }
            if all(sign >= 0 for sign in signs) or all(sign <= 0 for sign in signs):
                boundary.add(first)
                boundary.add(second)
    return sorted(boundary)
```

A pair belongs to a supporting line when all points lie on one side of its
infinite line. Enumerating all pairs takes `O(n^3)` time and `O(n)` space.

## Better approach: sort by polar angle

Graham scan also builds a hull with orientation tests after choosing a pivot
and sorting by polar angle. Retaining all boundary-collinear points requires
special handling of the final equal-angle group, which makes the two-pass
monotone chain simpler and less error-prone.

## Expert solution: monotone chain with strict popping

```python
from collections.abc import Sequence


Point = tuple[int, int]


def fence_trees(trees: Sequence[Point]) -> list[Point]:
    if any(
        type(point) is not tuple
        or len(point) != 2
        or any(type(coordinate) is not int for coordinate in point)
        for point in trees
    ):
        raise TypeError("each tree must be a pair of integers")
    if len(set(trees)) != len(trees):
        raise ValueError("tree coordinates must be distinct")

    points = sorted(trees)
    if len(points) < 3:
        return points

    def cross(origin: Point, first: Point, second: Point) -> int:
        return (first[0] - origin[0]) * (second[1] - origin[1]) - (
            first[1] - origin[1]
        ) * (second[0] - origin[0])

    lower: list[Point] = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) < 0:
            lower.pop()
        lower.append(point)

    upper: list[Point] = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) < 0:
            upper.pop()
        upper.append(point)

    return sorted(set(lower[:-1] + upper[:-1]))
```

The lower and upper scans reject exactly the points that would bend the fence
inward. Strict `< 0` popping preserves collinear edge points; the final set
removes corners visited by both scans.

**Complexity:** `O(n log n)` time for sorting and `O(n)` space.
