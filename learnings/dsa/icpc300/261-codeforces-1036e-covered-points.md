# ICPC300 261: Codeforces 1036E - Covered Points

**Source:** [Codeforces 1036E - Covered Points](https://codeforces.com/problemset/problem/1036/E)  
**Rating:** 2200  
**Pattern:** lattice-point counts plus exact rational intersections  
**Goal:** Count distinct integer-coordinate points covered by the given line
segments. The source excludes positive-length collinear overlaps.

## 1. First principles

A segment with displacement `(dx, dy)` contains
`gcd(abs(dx), abs(dy)) + 1` lattice points. Summing this for every segment
counts a lattice intersection once for every segment passing through it.

For every pair, use cross products to find its exact intersection. Record only
intersections that lie on both closed segments and have integer coordinates.
If `k` segments meet at one lattice point, subtract `k - 1`, not all
`C(k, 2)` pairs.

## 2. Cases that decide correctness

- Endpoints belong to their segments and may be shared intersections.
- A rational intersection with a non-integer coordinate changes nothing.
- Several segments may meet at the same lattice point.
- Cross-product numerators may be negative, so normalize the denominator sign.
- Parallel disjoint segments have no correction.
- A one-point collinear touch is an endpoint shared by both segments.
- Zero-length segments and positive-length collinear overlaps are invalid.

## 3. Brute force: enumerate every lattice point

```python
from math import gcd


Segment = tuple[int, int, int, int]


def covered_lattice_points_brute(segments: list[Segment]) -> int:
    if not segments:
        raise ValueError("segments must be nonempty")
    covered: set[tuple[int, int]] = set()
    for segment in segments:
        if len(segment) != 4 or any(type(value) is not int for value in segment):
            raise ValueError("each segment must contain four integers")
        x_first, y_first, x_second, y_second = segment
        dx = x_second - x_first
        dy = y_second - y_first
        steps = gcd(abs(dx), abs(dy))
        if steps == 0:
            raise ValueError("segment endpoints must differ")
        step_x = dx // steps
        step_y = dy // steps
        for offset in range(steps + 1):
            covered.add((x_first + offset * step_x, y_first + offset * step_y))
    return len(covered)
```

**Complexity:** `O(total lattice points)` time and space.

## 4. Better approach: subtract pair intersections

Subtracting one for every lattice intersection pair works when no three
segments concur. It over-subtracts a point shared by three or more segments,
so intersections must first be grouped by coordinate.

## 5. Expert solution: exact intersections grouped by point

```python
from math import gcd


Segment = tuple[int, int, int, int]


def covered_lattice_points(segments: list[Segment]) -> int:
    if not segments:
        raise ValueError("segments must be nonempty")
    total = 0
    for segment in segments:
        if len(segment) != 4 or any(type(value) is not int for value in segment):
            raise ValueError("each segment must contain four integers")
        x_first, y_first, x_second, y_second = segment
        dx = x_second - x_first
        dy = y_second - y_first
        steps = gcd(abs(dx), abs(dy))
        if steps == 0:
            raise ValueError("segment endpoints must differ")
        total += steps + 1

    intersections: dict[tuple[int, int], set[int]] = {}
    for first in range(len(segments)):
        ax, ay, bx, by = segments[first]
        rx = bx - ax
        ry = by - ay
        for second in range(first):
            cx, cy, dx, dy = segments[second]
            sx = dx - cx
            sy = dy - cy
            denominator = rx * sy - ry * sx
            if denominator == 0:
                if (cx - ax) * ry == (cy - ay) * rx:
                    first_projection = (ax, bx) if rx else (ay, by)
                    second_projection = (cx, dx) if rx else (cy, dy)
                    overlap_left = max(min(first_projection), min(second_projection))
                    overlap_right = min(max(first_projection), max(second_projection))
                    if overlap_left < overlap_right:
                        raise ValueError("collinear segments must not overlap")
                    common = {(ax, ay), (bx, by)} & {(cx, cy), (dx, dy)}
                    if overlap_left == overlap_right:
                        if len(common) != 1:
                            raise RuntimeError("missing collinear touch point")
                        point = common.pop()
                        touching = intersections.setdefault(point, set())
                        touching.add(first)
                        touching.add(second)
                continue
            t_numerator = (cx - ax) * sy - (cy - ay) * sx
            u_numerator = (cx - ax) * ry - (cy - ay) * rx
            if denominator < 0:
                denominator = -denominator
                t_numerator = -t_numerator
                u_numerator = -u_numerator
            if not (
                0 <= t_numerator <= denominator and 0 <= u_numerator <= denominator
            ):
                continue

            x_numerator = ax * denominator + rx * t_numerator
            y_numerator = ay * denominator + ry * t_numerator
            if x_numerator % denominator or y_numerator % denominator:
                continue
            point = (
                x_numerator // denominator,
                y_numerator // denominator,
            )
            touching = intersections.setdefault(point, set())
            touching.add(first)
            touching.add(second)

    return total - sum(len(touching) - 1 for touching in intersections.values())
```

### Why the expert code is correct

The gcd formula counts every lattice point on each segment. Exact cross
products identify precisely the duplicated lattice points and all segments
covering each one. Replacing `k` copies by one requires subtracting `k - 1`,
which the grouped correction does once per coordinate.

**Complexity:** `O(n^2)` time and `O(n^2)` intersection storage in the worst
case.

## 6. What to remember

```text
one segment -> gcd(dx, dy) + 1 lattice points
pair intersection -> exact cross-product fractions
many-way intersection -> subtract multiplicity minus one
```
