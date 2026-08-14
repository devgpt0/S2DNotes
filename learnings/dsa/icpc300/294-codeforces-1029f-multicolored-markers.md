# ICPC300 294: Codeforces 1029F - Multicolored Markers

**Source:** [Codeforces 1029F - Multicolored Markers](https://codeforces.com/problemset/problem/1029/F)  
**Rating:** 2200  
**Pattern:** divisor search with a rectangular partition condition  
**Goal:** Arrange `first_count + second_count` unit markers as one rectangle,
with each color occupying a rectangle. Minimize the outer perimeter.

## 1. First principles

The two color rectangles fill the outer rectangle without overlap, so their
shared cut spans one full outer side. For outer dimensions `height * width`, a
valid cut therefore exists exactly when one color count is divisible by
`height` or by `width`.

Only factor pairs of the total area can be outer dimensions. Enumerating
divisors through the square root tests all candidates.

## 2. Cases that decide correctness

- Both color counts are positive.
- A one-row or one-column outer rectangle is valid.
- Testing one color is sufficient because the total is divisible by each outer
  side.
- Swapping height and width does not change perimeter.
- The minimum-perimeter factor pair need not permit the color cut.

## 3. Brute force: try every possible height

```python
def minimum_marker_perimeter_brute(first_count: int, second_count: int) -> int:
    if (
        type(first_count) is not int
        or type(second_count) is not int
        or first_count <= 0
        or second_count <= 0
    ):
        raise ValueError("marker counts must be positive integers")
    total = first_count + second_count
    answer = 2 * (1 + total)
    for height in range(1, total + 1):
        if total % height:
            continue
        width = total // height
        if first_count % height == 0 or first_count % width == 0:
            answer = min(answer, 2 * (height + width))
    return answer
```

**Complexity:** `O(first_count + second_count)` time and `O(1)` space.

## 4. Better approach: search dimensions near the square root

Perimeter is minimized near a square, so candidates may be checked outward
from `sqrt(total)`. A direct divisor loop has the same asymptotic bound and
simpler completeness reasoning.

## 5. Expert solution: enumerate factor pairs only

```python
from math import isqrt


def minimum_marker_perimeter(first_count: int, second_count: int) -> int:
    if (
        type(first_count) is not int
        or type(second_count) is not int
        or first_count <= 0
        or second_count <= 0
    ):
        raise ValueError("marker counts must be positive integers")
    total = first_count + second_count
    answer = 2 * (1 + total)
    for height in range(1, isqrt(total) + 1):
        if total % height:
            continue
        width = total // height
        if first_count % height == 0 or first_count % width == 0:
            answer = min(answer, 2 * (height + width))
    return answer
```

### Why the expert code is correct

Every possible outer rectangle appears as one factor pair. A full-height cut
exists when the height divides both color areas, and a full-width cut exists
when the width does; divisibility of the total makes testing one color enough.
The minimum over exactly these valid rectangles is the required perimeter.

**Complexity:** `O(sqrt(first_count + second_count))` time and `O(1)` space.

## 6. What to remember

```text
two rectangles fill one rectangle -> one shared full-side cut
outer dimensions -> divisors of total area
valid cut -> one outer side divides a color count
```
