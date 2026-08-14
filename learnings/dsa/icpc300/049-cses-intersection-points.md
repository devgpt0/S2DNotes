# ICPC300 049: CSES - Intersection Points

**Source:** [CSES - Intersection Points](https://cses.fi/problemset/task/1740/)  
**Pattern:** sweep line with a Fenwick tree  
**Goal:** Count intersection points between horizontal and vertical line
segments. The source excludes ambiguous overlapping collinear segments.

## 1. Problem in plain words

A horizontal segment at y-coordinate `y` intersects a vertical segment at
x-coordinate `x` exactly when `x` lies in the horizontal x-range and `y` lies
in the vertical y-range.

Pairwise testing is quadratic. Sweep x from left to right while maintaining
the y-coordinates of horizontal segments currently spanning the sweep line.

## 2. First principles

A horizontal segment from `x1` through `x2` creates two sweep events:

- add its y-coordinate at `x1`;
- remove its y-coordinate at `x2`.

A vertical segment at x-coordinate `x` asks how many active y-values lie in
its inclusive range `[y1, y2]`. A Fenwick tree stores active counts over
compressed y-coordinates.

At the same x-coordinate, process add events before queries and removals after
queries. This includes intersections at segment endpoints.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Segments cross in both interiors | Count one. |
| Vertical endpoint touches a horizontal segment | Count one. |
| Horizontal endpoint touches a vertical segment | Event order includes it. |
| Disjoint coordinate ranges | Count zero. |
| Negative or large coordinates | Compression preserves order, not magnitude. |

## 4. Brute force: test every horizontal-vertical pair

```python
Segment = tuple[int, int, int, int]


def count_intersection_points_brute_force(segments: list[Segment]) -> int:
    horizontal: list[tuple[int, int, int]] = []
    vertical: list[tuple[int, int, int]] = []

    for first_x, first_y, second_x, second_y in segments:
        if first_y == second_y and first_x != second_x:
            left, right = sorted((first_x, second_x))
            horizontal.append((left, right, first_y))
        elif first_x == second_x and first_y != second_y:
            bottom, top = sorted((first_y, second_y))
            vertical.append((first_x, bottom, top))
        else:
            raise ValueError("each segment must be nonzero and axis-aligned")

    answer = 0
    for left, right, y_coordinate in horizontal:
        for x_coordinate, bottom, top in vertical:
            if left <= x_coordinate <= right and bottom <= y_coordinate <= top:
                answer += 1
    return answer
```

**Complexity:** `O(HV)` time and `O(n)` memory for `H` horizontal and `V`
vertical segments.

## 5. Better: sweep with a sorted active list

Sweeping removes comparisons against horizontals whose x-range is irrelevant.
Binary search answers each vertical range query, but insertion and deletion in
a Python list remain linear. This is useful on moderate inputs and exposes the
event-order invariant before introducing a Fenwick tree.

```python
from bisect import bisect_left, bisect_right, insort

Segment = tuple[int, int, int, int]


def count_intersection_points_sorted_list(segments: list[Segment]) -> int:
    events: list[tuple[int, int, int, int]] = []
    for first_x, first_y, second_x, second_y in segments:
        if first_y == second_y and first_x != second_x:
            left, right = sorted((first_x, second_x))
            events.append((left, 0, first_y, first_y))
            events.append((right, 2, first_y, first_y))
        elif first_x == second_x and first_y != second_y:
            bottom, top = sorted((first_y, second_y))
            events.append((first_x, 1, bottom, top))
        else:
            raise ValueError("each segment must be nonzero and axis-aligned")

    active_y: list[int] = []
    answer = 0
    for _, event_type, first_y, second_y in sorted(events):
        if event_type == 0:
            insort(active_y, first_y)
        elif event_type == 1:
            answer += bisect_right(active_y, second_y) - bisect_left(active_y, first_y)
        else:
            index = bisect_left(active_y, first_y)
            if index == len(active_y) or active_y[index] != first_y:
                raise RuntimeError("removing an inactive horizontal segment")
            active_y.pop(index)
    return answer
```

**Complexity:** `O(n^2)` worst-case time because list updates shift elements,
and `O(n)` memory.

## 6. Expert solution: Fenwick tree over active y-coordinates

Only horizontal y-values need Fenwick positions. `bisect_left` and
`bisect_right` translate a vertical segment's arbitrary endpoints into the
range of compressed horizontal y-values it contains.

```python
from bisect import bisect_left, bisect_right

Segment = tuple[int, int, int, int]


def count_intersection_points(segments: list[Segment]) -> int:
    events: list[tuple[int, int, int, int]] = []
    horizontal_y: set[int] = set()

    for first_x, first_y, second_x, second_y in segments:
        if first_y == second_y and first_x != second_x:
            left, right = sorted((first_x, second_x))
            events.append((left, 0, first_y, first_y))
            events.append((right, 2, first_y, first_y))
            horizontal_y.add(first_y)
        elif first_x == second_x and first_y != second_y:
            bottom, top = sorted((first_y, second_y))
            events.append((first_x, 1, bottom, top))
        else:
            raise ValueError("each segment must be nonzero and axis-aligned")

    y_values = sorted(horizontal_y)
    fenwick = [0] * (len(y_values) + 1)

    def add(index: int, change: int) -> None:
        index += 1
        while index < len(fenwick):
            fenwick[index] += change
            index += index & -index

    def prefix_sum(index: int) -> int:
        total = 0
        index += 1
        while index > 0:
            total += fenwick[index]
            index -= index & -index
        return total

    answer = 0
    for _, event_type, first_y, second_y in sorted(events):
        if event_type == 0:
            add(bisect_left(y_values, first_y), 1)
        elif event_type == 2:
            add(bisect_left(y_values, first_y), -1)
        else:
            left_index = bisect_left(y_values, first_y)
            right_index = bisect_right(y_values, second_y) - 1
            if left_index <= right_index:
                answer += prefix_sum(right_index) - prefix_sum(left_index - 1)
    return answer
```

### Why the expert code is correct

- Immediately before a query event, the Fenwick tree contains exactly the
  horizontal segments whose inclusive x-ranges contain the query x-coordinate.
- Its range sum counts exactly those active y-values inside the vertical
  segment's inclusive y-range.
- Add-query-remove ordering at equal x handles both kinds of endpoint touch.
- Every valid intersection consists of one horizontal and one vertical segment
  and is counted by exactly that vertical segment's event.

**Complexity:** `O(n log n)` time and `O(n)` memory.

## 7. What to remember

Turn horizontal segments into active intervals over x, and vertical segments
into y-range queries. Event order decides whether endpoints are included.
