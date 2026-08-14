# ICPC300 048: CSES - Area of Rectangles

**Source:** [CSES - Area of Rectangles](https://cses.fi/problemset/task/1741/)  
**Pattern:** sweep line with a covered-length segment tree  
**Goal:** Compute the union area of axis-aligned rectangles. Overlapping area
must be counted once.

## 1. Problem in plain words

Adding individual rectangle areas double-counts overlaps. Sweep a vertical
line from left to right instead. Between consecutive rectangle x-coordinates,
the set of active y-intervals is constant, so that slab contributes:

`horizontal_width * union_length_of_active_y_intervals`.

All source coordinates are integers, and the answer is an exact integer.

## 2. First principles

Each rectangle `(x1, y1, x2, y2)` creates two events:

- at `x1`, add y-interval `[y1, y2)`;
- at `x2`, remove that interval.

Compress all y-boundaries. A segment tree stores two values for every range:

- how many active rectangles fully cover it;
- its currently covered geometric length.

If the cover count is positive, the whole range is covered. Otherwise, its
length is the sum of its children, or zero at a leaf.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Disjoint rectangles | Add their areas. |
| One rectangle inside another | Count only the outer area. |
| Rectangles share an edge | Add no overlap area. |
| Several events have the same x | Add the preceding slab before applying all. |
| Negative coordinates | Coordinate differences still give positive lengths. |

## 4. Brute force: mark integer unit cells

For small integer coordinates, each pair `(x, y)` represents unit square
`[x, x+1) x [y, y+1)`.

```python
Rectangle = tuple[int, int, int, int]


def rectangle_union_area_brute_force(rectangles: list[Rectangle]) -> int:
    covered: set[tuple[int, int]] = set()
    for left, bottom, right, top in rectangles:
        if left >= right or bottom >= top:
            raise ValueError("each rectangle must have positive area")
        for x_coordinate in range(left, right):
            for y_coordinate in range(bottom, top):
                covered.add((x_coordinate, y_coordinate))
    return len(covered)
```

**Complexity:** proportional to the total coordinate area of all rectangles,
which is infeasible when coordinates are large.

## 5. Better when there are few distinct boundaries: compressed grid

Coordinate compression replaces huge coordinate spans with cells between
consecutive rectangle boundaries. Marking still touches many cells, but its
cost depends on the number of distinct coordinates rather than their values.

```python
Rectangle = tuple[int, int, int, int]


def rectangle_union_area_compressed(rectangles: list[Rectangle]) -> int:
    if not rectangles:
        return 0

    x_coordinates: set[int] = set()
    y_coordinates: set[int] = set()
    for left, bottom, right, top in rectangles:
        if left >= right or bottom >= top:
            raise ValueError("each rectangle must have positive area")
        x_coordinates.update((left, right))
        y_coordinates.update((bottom, top))

    x_values = sorted(x_coordinates)
    y_values = sorted(y_coordinates)
    x_index = {value: index for index, value in enumerate(x_values)}
    y_index = {value: index for index, value in enumerate(y_values)}
    covered = [[False] * (len(y_values) - 1) for _ in range(len(x_values) - 1)]

    for left, bottom, right, top in rectangles:
        for x_position in range(x_index[left], x_index[right]):
            for y_position in range(y_index[bottom], y_index[top]):
                covered[x_position][y_position] = True

    area = 0
    for x_position, column in enumerate(covered):
        width = x_values[x_position + 1] - x_values[x_position]
        for y_position, is_covered in enumerate(column):
            if is_covered:
                height = y_values[y_position + 1] - y_values[y_position]
                area += width * height
    return area
```

**Complexity:** `O(nXY + XY)` time and `O(XY)` memory for `X` compressed
x-intervals and `Y` compressed y-intervals.

## 6. Expert solution: x-sweep and covered-y segment tree

```python
Rectangle = tuple[int, int, int, int]


def rectangle_union_area(rectangles: list[Rectangle]) -> int:
    if not rectangles:
        return 0

    events: list[tuple[int, int, int, int]] = []
    y_coordinates: set[int] = set()
    for left, bottom, right, top in rectangles:
        if left >= right or bottom >= top:
            raise ValueError("each rectangle must have positive area")
        events.append((left, 1, bottom, top))
        events.append((right, -1, bottom, top))
        y_coordinates.update((bottom, top))

    events.sort()
    y_values = sorted(y_coordinates)
    y_index = {value: index for index, value in enumerate(y_values)}
    interval_count = len(y_values) - 1
    cover_count = [0] * (4 * interval_count)
    covered_length = [0] * (4 * interval_count)

    def pull(node: int, left: int, right: int) -> None:
        if cover_count[node] > 0:
            covered_length[node] = y_values[right + 1] - y_values[left]
        elif left == right:
            covered_length[node] = 0
        else:
            covered_length[node] = (
                covered_length[2 * node] + covered_length[2 * node + 1]
            )

    def update(
        query_left: int,
        query_right: int,
        change: int,
        node: int = 1,
        left: int = 0,
        right: int | None = None,
    ) -> None:
        if right is None:
            right = interval_count - 1
        if query_left <= left and right <= query_right:
            cover_count[node] += change
            pull(node, left, right)
            return

        middle = (left + right) // 2
        if query_left <= middle:
            update(query_left, query_right, change, 2 * node, left, middle)
        if query_right > middle:
            update(
                query_left,
                query_right,
                change,
                2 * node + 1,
                middle + 1,
                right,
            )
        pull(node, left, right)

    area = 0
    previous_x = events[0][0]
    event_index = 0
    while event_index < len(events):
        x_coordinate = events[event_index][0]
        area += (x_coordinate - previous_x) * covered_length[1]

        while event_index < len(events) and events[event_index][0] == x_coordinate:
            _, change, bottom, top = events[event_index]
            update(y_index[bottom], y_index[top] - 1, change)
            event_index += 1
        previous_x = x_coordinate

    return area
```

### Why the expert code is correct

- Events make the active rectangle set constant between adjacent x-values.
- The segment-tree root is exactly the union length of active y-intervals:
  positive cover means fully covered, otherwise child lengths partition it.
- Width times that union length is exactly the current slab's union area.
- Half-open rectangle intervals make shared edges contribute zero area, and
  processing all equal-x events together prepares the next slab correctly.

**Complexity:** `O(n log n)` time and `O(n)` memory.

## 7. What to remember

For rectangle union area, sweep one axis and maintain the union length on the
other. A cover-count segment tree handles overlapping intervals correctly.
