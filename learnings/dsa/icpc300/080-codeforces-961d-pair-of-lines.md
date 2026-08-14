# ICPC300 080: Codeforces 961D - Pair Of Lines

**Source:** [Codeforces 961D - Pair Of Lines](https://codeforces.com/problemset/problem/961/D)  
**Pattern:** deterministic candidate reduction by pigeonhole principle

## Exact contract

Input gives `n` distinct integer-coordinate points (`1 <= n <= 100000`).
Output `YES` if all points can be covered by at most two straight lines;
otherwise output `NO`.

## First principles

If two lines cover all points, among any first three points at least two lie on
the same covering line. Therefore one of only three candidate first lines is
correct: `(p0,p1)`, `(p0,p2)`, or `(p1,p2)`.

For a candidate, collect every point not on it. The candidate works exactly
when that remainder has at most two points or is collinear. Integer cross
products test collinearity exactly.

## Cases that decide correctness

- Any set of at most four points is coverable by two lines.
- A line may contain just one point when all other points share the other line.
- Vertical lines need no special case when using cross products.
- Testing only one arbitrary pair is insufficient; all three first-triple
  pairs are necessary.

## Brute force: enumerate every two-group partition

```python
def covered_by_two_lines_brute(points: list[tuple[int, int]]) -> bool:
    def collinear(group: list[tuple[int, int]]) -> bool:
        if len(group) <= 2:
            return True
        x1, y1 = group[0]
        x2, y2 = group[1]
        return all((x2 - x1) * (y - y1) == (y2 - y1) * (x - x1) for x, y in group[2:])

    for mask in range(1 << len(points)):
        first = [point for index, point in enumerate(points) if mask & (1 << index)]
        second = [
            point for index, point in enumerate(points) if mask & (1 << index) == 0
        ]
        if collinear(first) and collinear(second):
            return True
    return False
```

**Complexity:** `O(2^n n)` time and `O(n)` space.

## Better: enumerate every possible first line

```python
from itertools import combinations


def covered_by_two_lines_cubic(points: list[tuple[int, int]]) -> bool:
    if len(points) <= 4:
        return True

    def on_line(
        first: tuple[int, int], second: tuple[int, int], point: tuple[int, int]
    ) -> bool:
        return (second[0] - first[0]) * (point[1] - first[1]) == (
            second[1] - first[1]
        ) * (point[0] - first[0])

    for first_index, second_index in combinations(range(len(points)), 2):
        remainder = [
            point
            for point in points
            if not on_line(points[first_index], points[second_index], point)
        ]
        if len(remainder) <= 2 or all(
            on_line(remainder[0], remainder[1], point) for point in remainder[2:]
        ):
            return True
    return False
```

This reduces partitions to `O(n^2)` candidate lines but still takes `O(n^3)`
time.

## Expert solution: only three candidate first lines

```python
import sys


def on_line(
    first: tuple[int, int],
    second: tuple[int, int],
    point: tuple[int, int],
) -> bool:
    return (second[0] - first[0]) * (point[1] - first[1]) == (second[1] - first[1]) * (
        point[0] - first[0]
    )


def candidate_works(
    points: list[tuple[int, int]],
    first_index: int,
    second_index: int,
) -> bool:
    remainder = [
        point
        for point in points
        if not on_line(points[first_index], points[second_index], point)
    ]
    return len(remainder) <= 2 or all(
        on_line(remainder[0], remainder[1], point) for point in remainder[2:]
    )


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    point_count = data[0]
    points = [
        (data[1 + 2 * index], data[2 + 2 * index]) for index in range(point_count)
    ]
    if point_count <= 4:
        print("YES")
        return

    candidates = ((0, 1), (0, 2), (1, 2))
    print(
        "YES"
        if any(candidate_works(points, first, second) for first, second in candidates)
        else "NO"
    )


if __name__ == "__main__":
    solve()
```

Under any valid two-line cover, two of the first three points share a covering
line. That line appears in the candidate set, and its remainder test exactly
checks whether the other covering line exists.

**Complexity:** `O(n)` time and `O(n)` space for the remainder list.

