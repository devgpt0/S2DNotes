# ICPC300 205: Codeforces 1401E - Divide Square

**Source:** [Codeforces 1401E - Divide Square](https://codeforces.com/problemset/problem/1401/E)  
**Difficulty:** 2300  
**Pattern:** orthogonal intersection sweep with a Fenwick tree

## Exact contract

Inside `[0, 1_000_000]^2`, horizontal segments have form `(y, x1, x2)` and
vertical segments `(x, y1, y2)`, with inclusive endpoints. Every segment
touches at least one boundary parallel to its direction; horizontal `y` values
and vertical `x` values are distinct. Count the regions into which the segments
divide the square.

## First principles

Start with one region. A segment attached to one boundary creates one new
region for every perpendicular segment it crosses. If it spans between both
opposite boundaries, it creates one additional region before intersections.
Therefore

`regions = 1 + full_width + full_height + perpendicular_intersections`.

Sweep by `x`. Add a horizontal at `x1`, query active `y` values for each
vertical segment, and remove the horizontal after `x2`.

## Cases that decide correctness

- Endpoints are inclusive, so add events precede queries and removals follow.
- An endpoint intersection counts.
- A full-width or full-height segment contributes one even with no crossing.
- Same-orientation coordinates are distinct under the source contract.
- Boundary-touching is required for the region formula.

## Brute force: test every perpendicular pair

```python
BOUNDARY = 1_000_000


def divide_square_brute(
    horizontal: list[tuple[int, int, int]],
    vertical: list[tuple[int, int, int]],
) -> int:
    horizontal_y: set[int] = set()
    for y, left, right in horizontal:
        if (
            type(y) is not int
            or type(left) is not int
            or type(right) is not int
            or not 0 < y < BOUNDARY
            or not 0 <= left < right <= BOUNDARY
            or (left != 0 and right != BOUNDARY)
            or y in horizontal_y
        ):
            raise ValueError("invalid horizontal segment")
        horizontal_y.add(y)
    vertical_x: set[int] = set()
    for x, bottom, top in vertical:
        if (
            type(x) is not int
            or type(bottom) is not int
            or type(top) is not int
            or not 0 < x < BOUNDARY
            or not 0 <= bottom < top <= BOUNDARY
            or (bottom != 0 and top != BOUNDARY)
            or x in vertical_x
        ):
            raise ValueError("invalid vertical segment")
        vertical_x.add(x)

    answer = 1
    answer += sum(left == 0 and right == BOUNDARY for _, left, right in horizontal)
    answer += sum(bottom == 0 and top == BOUNDARY for _, bottom, top in vertical)
    answer += sum(
        left <= x <= right and bottom <= y <= top
        for y, left, right in horizontal
        for x, bottom, top in vertical
    )
    return answer
```

This is `O(nm)` time.

## Better approach: sweep with a sorted active list

Maintaining active horizontal `y` values in a Python list and using binary
search answers vertical queries, but insertion and removal remain linear. A
Fenwick tree over compressed `y` coordinates makes all three operations
logarithmic.

## Expert solution: event ordering plus Fenwick range counts

```python
from bisect import bisect_left, bisect_right

BOUNDARY = 1_000_000


def divide_square(
    horizontal: list[tuple[int, int, int]],
    vertical: list[tuple[int, int, int]],
) -> int:
    horizontal_y: set[int] = set()
    events: list[tuple[int, int, int, int]] = []
    answer = 1
    for y, left, right in horizontal:
        if (
            type(y) is not int
            or type(left) is not int
            or type(right) is not int
            or not 0 < y < BOUNDARY
            or not 0 <= left < right <= BOUNDARY
            or (left != 0 and right != BOUNDARY)
            or y in horizontal_y
        ):
            raise ValueError("invalid horizontal segment")
        horizontal_y.add(y)
        events.append((left, 0, y, 0))
        events.append((right, 2, y, 0))
        answer += left == 0 and right == BOUNDARY

    vertical_x: set[int] = set()
    for x, bottom, top in vertical:
        if (
            type(x) is not int
            or type(bottom) is not int
            or type(top) is not int
            or not 0 < x < BOUNDARY
            or not 0 <= bottom < top <= BOUNDARY
            or (bottom != 0 and top != BOUNDARY)
            or x in vertical_x
        ):
            raise ValueError("invalid vertical segment")
        vertical_x.add(x)
        events.append((x, 1, bottom, top))
        answer += bottom == 0 and top == BOUNDARY

    coordinates = sorted(horizontal_y)
    fenwick = [0] * (len(coordinates) + 1)

    def add(position: int, delta: int) -> None:
        index = bisect_left(coordinates, position) + 1
        while index < len(fenwick):
            fenwick[index] += delta
            index += index & -index

    def prefix(count: int) -> int:
        result = 0
        while count:
            result += fenwick[count]
            count -= count & -count
        return result

    for _, event_type, first, second in sorted(events):
        if event_type == 0:
            add(first, 1)
        elif event_type == 2:
            add(first, -1)
        else:
            lower = bisect_left(coordinates, first)
            upper = bisect_right(coordinates, second)
            answer += prefix(upper) - prefix(lower)
    return answer
```

At every vertical query, the Fenwick tree contains exactly horizontals whose
inclusive `x` interval covers the sweep coordinate. Its compressed range sum
counts precisely the crossing `y` coordinates.

**Complexity:** `O((n+m) log(n+m))` time and `O(n+m)` space.
