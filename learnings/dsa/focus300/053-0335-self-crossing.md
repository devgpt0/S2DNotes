# Focus300 053: LeetCode 335 - Self Crossing

**Source:** [LeetCode 335 - Self Crossing](https://leetcode.com/problems/self-crossing/)  
**Difficulty:** Hard  
**Pattern:** constant-window spiral crossing cases  

## Exact contract

Starting at `(0, 0)`, move north, west, south, east, then repeat, using each
positive distance. Return whether any nonconsecutive path segments touch or
cross. Endpoint touching and collinear overlap count as crossings.

## First principles

The fixed counterclockwise directions make a noncrossing path either expand
outward or contract inward. The first crossing can only involve the newest
segment and one of the segments three, four, or five steps earlier, producing
three local geometric configurations.


## Classroom board: see the repeated work once

```text
brute force tries every choice.
the optimized solution keeps only the state that must survive to the
next step.
```



## Step-by-step transformation

1. Load the current candidates into a stack, queue, heap, or window.
2. Push or pop the structure while the current element keeps the invariant true.
3. Drop stale candidates and keep only the ones that can still affect the answer.
4. Read the final top, window score, or popped order as the output.

These problems transform the input by keeping just the active frontier of candidates instead of rescanning the whole array every time.


## Diagram: active frontier only

```text

            scan left to right
                |
                v
            keep active candidates
                |
                v
            pop stale work
                |
                v
            current best answer
```

These notes keep only the active frontier of useful candidates instead of rescanning the whole input.

## Cases that decide correctness

- Consecutive segments share an endpoint by construction and do not count.
- Touching a much earlier endpoint does count.
- Collinear overlap is a crossing.
- Fewer than four moves cannot self-cross.
- All distances must be strictly positive.

## Brute force: compare every new axis-aligned segment

```python
Point = tuple[int, int]
Segment = tuple[Point, Point]


def is_self_crossing_brute(distances: list[int]) -> bool:
    if any(type(distance) is not int or distance <= 0 for distance in distances):
        raise ValueError("distances must be positive integers")

    def intersects(first: Segment, second: Segment) -> bool:
        (ax, ay), (bx, by) = first
        (cx, cy), (dx, dy) = second
        first_horizontal = ay == by
        second_horizontal = cy == dy
        if first_horizontal and second_horizontal:
            return ay == cy and max(min(ax, bx), min(cx, dx)) <= min(
                max(ax, bx), max(cx, dx)
            )
        if not first_horizontal and not second_horizontal:
            return ax == cx and max(min(ay, by), min(cy, dy)) <= min(
                max(ay, by), max(cy, dy)
            )
        if first_horizontal:
            return min(ax, bx) <= cx <= max(ax, bx) and min(cy, dy) <= ay <= max(cy, dy)
        return min(cx, dx) <= ax <= max(cx, dx) and min(ay, by) <= cy <= max(ay, by)

    directions = ((0, 1), (-1, 0), (0, -1), (1, 0))
    point = (0, 0)
    segments: list[Segment] = []
    for index, distance in enumerate(distances):
        horizontal, vertical = directions[index % 4]
        next_point = (
            point[0] + horizontal * distance,
            point[1] + vertical * distance,
        )
        segment = (point, next_point)
        if any(intersects(segment, previous) for previous in segments[:-1]):
            return True
        segments.append(segment)
        point = next_point
    return False
```

**Complexity:** `O(n^2)` time and `O(n)` space.

## Better approach: retain only recent segments

The first-crossing geometry proves older segments can be discarded, giving
constant space, but explicit coordinate intersection still obscures the three
necessary inequalities.

## Expert solution: test the three first-crossing configurations

```python
def is_self_crossing(distances: list[int]) -> bool:
    if any(type(distance) is not int or distance <= 0 for distance in distances):
        raise ValueError("distances must be positive integers")
    for index in range(3, len(distances)):
        if (
            distances[index] >= distances[index - 2]
            and distances[index - 1] <= distances[index - 3]
        ):
            return True
        if (
            index >= 4
            and distances[index - 1] == distances[index - 3]
            and distances[index] + distances[index - 4] >= distances[index - 2]
        ):
            return True
        if (
            index >= 5
            and distances[index - 2] >= distances[index - 4]
            and distances[index] + distances[index - 4] >= distances[index - 2]
            and distances[index - 1] <= distances[index - 3]
            and distances[index - 1] + distances[index - 5] >= distances[index - 3]
        ):
            return True
    return False
```

The conditions respectively detect crossing the segment three back, touching
or overlapping the segment four back, and the inward-spiral overlap involving
the segment five back. Every first crossing has one of these forms.

**Complexity:** `O(n)` time and `O(1)` space.

