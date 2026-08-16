# Focus300 035: LeetCode 218 - The Skyline Problem

**Source:** [LeetCode 218 - The Skyline Problem](https://leetcode.com/problems/the-skyline-problem/)  
**Difficulty:** Hard  
**Pattern:** endpoint sweep with an active max-heap  

## Exact contract

Each building is `[left, right, height]` and covers the half-open horizontal
interval `[left, right)`. Return the skyline's critical points `(x, height)`:
the minimum sequence where height changes, ending at height zero.

## First principles

Skyline height can change only at a building endpoint. At an endpoint `x`, add
every building starting there, discard active buildings whose right endpoint
is at most `x`, and read the tallest remaining height.


## Classroom board: store the repeated state once

```text
brute force recomputes the same subproblem many times.
dp keeps the smallest useful state and extends it one step at a time.
```



## Step-by-step transformation

1. Turn the input into subproblems, prefixes, or states that can be reused.
2. Fill the base cases first so later states have something correct to build on.
3. Update each new state from earlier states while keeping the recurrence valid.
4. Read the answer from the final table entry or the best state collected at the end.

Dynamic-programming style notes transform the input by compressing many repeated choices into a small set of reusable states.


## Diagram: state table to answer

```text

            input
                |
                v
            base states
                |
                v
            reuse smaller states
                |
                v
            final dp answer
```

These notes compress repeated choices into reusable states, then read the answer from the last state that matters.

## Cases that decide correctness

- All events at one `x` must be processed before emitting a point.
- A building ending where another starts is handled by half-open intervals.
- Equal-height adjacent spans produce no redundant point.
- Nested buildings require lazy removal of expired heap entries.
- The final right endpoint emits height zero.

## Brute force: recompute the height at every endpoint

```python
Building = tuple[int, int, int]


def skyline_brute(buildings: list[Building]) -> list[tuple[int, int]]:
    for left, right, height in buildings:
        if (
            type(left) is not int
            or type(right) is not int
            or type(height) is not int
            or left >= right
            or height <= 0
        ):
            raise ValueError("invalid building")
    if not buildings:
        return []

    result = []
    for coordinate in sorted(
        {endpoint for left, right, _ in buildings for endpoint in (left, right)}
    ):
        height = max(
            (
                building_height
                for left, right, building_height in buildings
                if left <= coordinate < right
            ),
            default=0,
        )
        if not result or result[-1][1] != height:
            result.append((coordinate, height))
    return result
```

**Complexity:** `O(n^2)` time and `O(n)` space.

## Better approach: coordinate-compressed height painting

Compress all endpoints, paint each covered elementary interval with its maximum
height, then scan for changes. This remains `O(n^2)` in the worst case but
avoids testing irrelevant coordinates.

## Expert solution: sweep endpoints with a lazy max-heap

```python
from heapq import heappop, heappush


Building = tuple[int, int, int]


def skyline(buildings: list[Building]) -> list[tuple[int, int]]:
    for left, right, height in buildings:
        if (
            type(left) is not int
            or type(right) is not int
            or type(height) is not int
            or left >= right
            or height <= 0
        ):
            raise ValueError("invalid building")
    ordered = sorted(buildings)
    coordinates = sorted(
        {endpoint for left, right, _ in ordered for endpoint in (left, right)}
    )
    active: list[tuple[int, int]] = []
    result: list[tuple[int, int]] = []
    building_index = 0
    for coordinate in coordinates:
        while (
            building_index < len(ordered) and ordered[building_index][0] <= coordinate
        ):
            left, right, height = ordered[building_index]
            heappush(active, (-height, right))
            building_index += 1
        while active and active[0][1] <= coordinate:
            heappop(active)
        height = -active[0][0] if active else 0
        if not result or result[-1][1] != height:
            result.append((coordinate, height))
    return result
```

Every possible change coordinate is swept once. The heap root is the tallest
unexpired building; lazy deletion is safe because an expired non-root cannot
affect the skyline until it reaches the root.

**Complexity:** `O(n log n)` time and `O(n)` space.

