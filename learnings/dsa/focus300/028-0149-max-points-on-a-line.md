# Focus300 028: LeetCode 149 - Max Points on a Line

**Source:** [LeetCode 149](https://leetcode.com/problems/max-points-on-a-line/)  
**Difficulty:** Hard  
**Pattern:** normalized rational slopes per anchor

## Exact contract

Given unique integer-coordinate points, return the maximum number lying on one
straight line.

## First principles

Fix one anchor. Every other point on the same line has the same direction
vector `(dy,dx)` after dividing both components by their greatest common
divisor and normalizing sign. Integer pairs avoid floating-point rounding and
represent vertical lines naturally.

The best slope count for an anchor plus the anchor itself gives the best line
through that anchor. Every possible line is considered at one of its points.


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

- Zero, one, or two points return their count.
- Vertical and horizontal lines need canonical directions.
- Opposite direction vectors represent the same line.
- Large coordinates make floating slopes unsafe.
- Points are unique by source contract.

## Brute force: test every point against every pair-defined line

```python
def max_points_brute(points: list[list[int]]) -> int:
    if len(points) <= 2:
        return len(points)
    answer = 2
    for first in range(len(points)):
        x1, y1 = points[first]
        for second in range(first + 1, len(points)):
            x2, y2 = points[second]
            count = 0
            for x, y in points:
                if (x - x1) * (y2 - y1) == (y - y1) * (x2 - x1):
                    count += 1
            answer = max(answer, count)
    return answer
```

This takes `O(n^3)` time.

## Better insight: group all lines through one anchor by exact slope

An anchor reduces line identity to direction identity. GCD normalization makes
each remaining point one hash-map update, eliminating the third loop.

## Expert solution: GCD-normalized direction counts

```python
from collections import defaultdict
from math import gcd


def max_points(points: list[list[int]]) -> int:
    if len(points) <= 2:
        return len(points)
    answer = 2
    for anchor in range(len(points) - 1):
        slopes: dict[tuple[int, int], int] = defaultdict(int)
        x1, y1 = points[anchor]
        for x2, y2 in points[anchor + 1 :]:
            delta_x = x2 - x1
            delta_y = y2 - y1
            divisor = gcd(abs(delta_x), abs(delta_y))
            delta_x //= divisor
            delta_y //= divisor
            if delta_x < 0 or (delta_x == 0 and delta_y < 0):
                delta_x = -delta_x
                delta_y = -delta_y
            slopes[(delta_y, delta_x)] += 1
            answer = max(answer, slopes[(delta_y, delta_x)] + 1)
    return answer
```

Normalized integer directions are equal exactly when the anchor and both
points are collinear.

**Complexity:** `O(n^2 log C)` time for coordinate magnitude `C` and `O(n)`
space per anchor.
