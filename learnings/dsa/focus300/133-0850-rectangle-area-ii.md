# Focus300 133: LeetCode 850 - Rectangle Area II

**Source:** [LeetCode 850](https://leetcode.com/problems/rectangle-area-ii/)  
**Difficulty:** Hard  
**Pattern:** sweep line with merged active intervals

## Exact contract

Given at most 200 axis-aligned rectangles `[x1, y1, x2, y2]` with integer
coordinates and positive width and height, return their union area modulo
`1_000_000_007`. Coordinates are between zero and `1_000_000_000`.

## First principles

Between consecutive vertical rectangle edges, the set of active y-intervals
does not change. The union area of that slab is its width times the merged
length of active y-intervals. Enter and exit events update the active multiset
at each edge.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Read the input and identify the smallest state that still determines the answer.
2. Process one element, node, or row at a time while preserving that state.
3. Discard work that can no longer change the result.
4. Convert the surviving state into the output the problem requests.

The examples and code below show this transformation on the specific problem instance.


## Diagram: input to output

```text

        input
            |
            v
        core invariant
            |
            v
        process one step at a time
            |
            v
        output
```

The note shows the main idea, the repeated work, and the small state that turns the input into the output.

## Cases that decide correctness

- Overlap contributes area only once.
- Rectangles touching only at an edge add no overlap area.
- Equal y-intervals from different rectangles need multiplicity counts.
- All events at one x-coordinate are processed together.
- Apply the modulus to the final accumulated integer area.

## Brute force: mark every integer unit cell

```python
MODULO = 1_000_000_007


def rectangle_union_area_brute(rectangles: list[list[int]]) -> int:
    if (
        type(rectangles) is not list
        or not 1 <= len(rectangles) <= 200
        or any(
            type(rectangle) is not list
            or len(rectangle) != 4
            or any(type(coordinate) is not int for coordinate in rectangle)
            for rectangle in rectangles
        )
    ):
        raise TypeError("rectangles must contain 1..200 integer coordinate lists")
    if any(
        not 0 <= left < right <= 1_000_000_000 or not 0 <= bottom < top <= 1_000_000_000
        for left, bottom, right, top in rectangles
    ):
        raise ValueError("each rectangle must have valid positive dimensions")

    cells = {
        (x_value, y_value)
        for left, bottom, right, top in rectangles
        for x_value in range(left, right)
        for y_value in range(bottom, top)
    }
    return len(cells) % MODULO
```

This uses time and space proportional to the numeric union area, which is
infeasible for large coordinates.

## Better approach: compress both coordinate axes

Map every rectangle edge to its rank, mark covered compressed cells, and sum
their real widths and heights. With at most `2n` coordinates per axis this is
`O(n^3)` marking time and `O(n^2)` space.

## Expert solution: sweep x while merging active y-ranges

```python
from collections import Counter


MODULO = 1_000_000_007


def rectangle_union_area(rectangles: list[list[int]]) -> int:
    if (
        type(rectangles) is not list
        or not 1 <= len(rectangles) <= 200
        or any(
            type(rectangle) is not list
            or len(rectangle) != 4
            or any(type(coordinate) is not int for coordinate in rectangle)
            for rectangle in rectangles
        )
    ):
        raise TypeError("rectangles must contain 1..200 integer coordinate lists")
    if any(
        not 0 <= left < right <= 1_000_000_000 or not 0 <= bottom < top <= 1_000_000_000
        for left, bottom, right, top in rectangles
    ):
        raise ValueError("each rectangle must have valid positive dimensions")

    events: list[tuple[int, int, int, int]] = []
    for left, bottom, right, top in rectangles:
        events.append((left, 1, bottom, top))
        events.append((right, -1, bottom, top))
    events.sort()

    def covered_length(active: Counter[tuple[int, int]]) -> int:
        intervals = sorted(interval for interval, count in active.items() if count)
        if not intervals:
            return 0
        total = 0
        current_left, current_right = intervals[0]
        for left, right in intervals[1:]:
            if left > current_right:
                total += current_right - current_left
                current_left, current_right = left, right
            else:
                current_right = max(current_right, right)
        return total + current_right - current_left

    active: Counter[tuple[int, int]] = Counter()
    area = 0
    previous_x = events[0][0]
    index = 0
    while index < len(events):
        x_value = events[index][0]
        area += (x_value - previous_x) * covered_length(active)
        while index < len(events) and events[index][0] == x_value:
            _, change, bottom, top = events[index]
            active[(bottom, top)] += change
            if active[(bottom, top)] == 0:
                del active[(bottom, top)]
            index += 1
        previous_x = x_value
    return area % MODULO
```

Each slab uses the exact union of active vertical intervals, so multiplying by
its width counts every covered point once regardless of overlap multiplicity.

**Complexity:** `O(n^2 log n)` time and `O(n)` space.
