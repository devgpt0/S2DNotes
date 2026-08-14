# ICPC300 020: CSES - Minimum Euclidean Distance

**Source:** [CSES - Minimum Euclidean Distance](https://cses.fi/problemset/task/2194/)  
**Pattern:** closest pair of points by divide and conquer  
**Goal:** Return the minimum squared Euclidean distance between two input
points. The source asks for the squared integer distance, not its square root.

## 1. Problem in plain words

For points `(1, 1)`, `(5, 2)`, and `(3, 1)`, the closest pair is `(1, 1)` and
`(3, 1)`. The required value is `(3-1)^2 + (1-1)^2 = 4`.

Computing a square root would add floating-point risk and would produce the
wrong source output. Compare and return squared distances throughout.

## 2. First principles

Split points by x-coordinate. The closest pair is either:

1. entirely in the left half;
2. entirely in the right half; or
3. one point from each half.

After solving both halves, let their best squared distance be `d`. A better
crossing pair must have each point within horizontal squared distance `< d`
of the split line. Keep those strip points sorted by y.

The packing lemma says each strip point needs comparison with only the next
seven y-ordered points: otherwise two of those points would already be closer
than `d` inside one half.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| Exactly two points | Their squared distance. |
| Duplicate coordinates | Answer `0` if supplied. |
| Closest pair crosses the split | The strip step must find it. |
| Equal x- or y-coordinates | Sorting and integer comparisons still work. |
| Large coordinates | Never use floating point. |

## 4. Brute force: test every pair

```python
Point = tuple[int, int]


def minimum_euclidean_distance_brute_force(points: list[Point]) -> int:
    if len(points) < 2:
        raise ValueError("at least two points are required")

    def distance_squared(first: Point, second: Point) -> int:
        return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2

    return min(
        distance_squared(points[first], points[second])
        for first in range(len(points))
        for second in range(first + 1, len(points))
    )
```

**Why it works:** the minimum pair is one of the `n(n-1)/2` pairs tested.

**Complexity:** `O(n^2)` time and `O(1)` auxiliary space.

## 5. Better approach: why a fixed window after x-sorting is not a solution

It is tempting to sort by x and compare each point with the next few points.
That is incorrect: arbitrarily many points may have nearly equal x-values but
very different y-values, and the closest useful neighbor may be far away in
x-sorted index order.

The y-sorted strip and its packing argument are what make a seven-neighbor
bound valid. Without that geometric invariant, the only safe direct scan is
quadratic. There is no honest generic middle algorithm to present here.

## 6. Expert solution: divide, merge by y, inspect the strip

Each recursive call returns both its best squared distance and its points
sorted by y. Merging the two y-orders in linear time keeps the whole recurrence
`T(n) = 2T(n/2) + O(n)`.

```python
Point = tuple[int, int]


def minimum_euclidean_distance(points: list[Point]) -> int:
    if len(points) < 2:
        raise ValueError("at least two points are required")

    def distance_squared(first: Point, second: Point) -> int:
        return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2

    infinity = 1 << 200
    points_by_x = sorted(points)

    def solve(x_order: list[Point]) -> tuple[int, list[Point]]:
        point_count = len(x_order)
        if point_count <= 3:
            best = infinity
            for first in range(point_count):
                for second in range(first + 1, point_count):
                    best = min(
                        best,
                        distance_squared(x_order[first], x_order[second]),
                    )
            return best, sorted(x_order, key=lambda point: (point[1], point[0]))

        middle = point_count // 2
        middle_x = x_order[middle][0]
        left_best, left_by_y = solve(x_order[:middle])
        right_best, right_by_y = solve(x_order[middle:])
        best = min(left_best, right_best)

        merged_by_y: list[Point] = []
        left_index = 0
        right_index = 0
        while left_index < len(left_by_y) and right_index < len(right_by_y):
            left_key = (left_by_y[left_index][1], left_by_y[left_index][0])
            right_key = (right_by_y[right_index][1], right_by_y[right_index][0])
            if left_key <= right_key:
                merged_by_y.append(left_by_y[left_index])
                left_index += 1
            else:
                merged_by_y.append(right_by_y[right_index])
                right_index += 1
        merged_by_y.extend(left_by_y[left_index:])
        merged_by_y.extend(right_by_y[right_index:])

        strip = [point for point in merged_by_y if (point[0] - middle_x) ** 2 < best]
        for first in range(len(strip)):
            for second in range(first + 1, min(first + 8, len(strip))):
                best = min(best, distance_squared(strip[first], strip[second]))

        return best, merged_by_y

    answer, _ = solve(points_by_x)
    return answer
```

### Why the expert code is correct

- Recursion checks every pair contained in one half.
- Any unexamined better pair must cross the split and have both endpoints in
  the strip; otherwise its horizontal distance alone is at least the current
  best distance.
- The packing lemma places the other endpoint among the next seven points in
  y-order, so the strip loop checks every potentially better crossing pair.
- These cases cover every point pair, and all comparisons use exact squared
  integer distances.

**Complexity:** `O(n log n)` time and `O(n)` auxiliary memory.

## 7. What to remember

Closest pair is not merely "sort by x." The reusable proof is: solve both
halves, merge by y, restrict to the split strip, then compare seven successors.
