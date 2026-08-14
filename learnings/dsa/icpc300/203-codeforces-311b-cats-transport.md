# ICPC300 203: Codeforces 311B - Cats Transport

**Source:** [Codeforces 311B - Cats Transport](https://codeforces.com/problemset/problem/311/B)  
**Difficulty:** 2300  
**Pattern:** sorted partition DP optimized by a monotone convex hull

## Exact contract

Hills lie on one route from hill `0`; `segment_lengths[i]` is the travel time
from hill `i` to `i+1`. Cat `(hill, time)` becomes ready there at `time`.
At most `group_count` keepers leave hill `0`, travel the route, and collect
consecutive groups of cats. Minimize total cat waiting time.

## First principles

For a cat at hill `h`, define `adjusted = time - distance[h]`: the latest
departure from hill `0` that reaches it exactly when ready. Sort adjusted
times. A keeper serving sorted cats `j+1..i` optimally leaves at `adjusted[i]`,
with cost

`adjusted[i] * (i-j) - (prefix[i] - prefix[j])`.

The DP transition separates into a query in `x = adjusted[i]` over lines with
slope `-j` and intercept `previous[j] + prefix[j]`.

## Cases that decide correctness

- Adjusted times may be negative.
- Sorting makes every optimal keeper group contiguous.
- Extra keepers may stay unused; more nonempty groups never increase cost.
- Equal adjusted times produce zero waiting inside their group.
- Hull slopes and query coordinates are both monotone.

## Brute force: enumerate partition cuts

```python
def cats_transport_brute(
    segment_lengths: list[int], cats: list[tuple[int, int]], group_count: int
) -> int:
    hill_count = len(segment_lengths) + 1
    if type(group_count) is not int or group_count < 1 or not cats:
        raise ValueError("cats and a positive group count are required")
    if any(type(length) is not int or length < 0 for length in segment_lengths):
        raise ValueError("segment lengths must be nonnegative integers")
    distance = [0] * hill_count
    for hill, length in enumerate(segment_lengths, 1):
        distance[hill] = distance[hill - 1] + length

    adjusted: list[int] = []
    for hill, time in cats:
        if type(hill) is not int or type(time) is not int or not 0 <= hill < hill_count:
            raise ValueError("invalid cat")
        adjusted.append(time - distance[hill])
    adjusted.sort()

    best: int | None = None
    for cuts in range(1 << (len(adjusted) - 1)):
        if cuts.bit_count() + 1 > group_count:
            continue
        cost = 0
        start = 0
        for index in range(len(adjusted)):
            if index == len(adjusted) - 1 or cuts >> index & 1:
                departure = adjusted[index]
                cost += sum(
                    departure - adjusted[cat] for cat in range(start, index + 1)
                )
                start = index + 1
        best = cost if best is None else min(best, cost)
    if best is None:
        raise RuntimeError("one group is always feasible")
    return best
```

This takes `O(m 2^m)` time for `m` cats.

## Better approach: quadratic partition DP

```python
def cats_transport_quadratic(
    segment_lengths: list[int], cats: list[tuple[int, int]], group_count: int
) -> int:
    hill_count = len(segment_lengths) + 1
    if type(group_count) is not int or group_count < 1 or not cats:
        raise ValueError("cats and a positive group count are required")
    if any(type(length) is not int or length < 0 for length in segment_lengths):
        raise ValueError("segment lengths must be nonnegative integers")
    distance = [0] * hill_count
    for hill, length in enumerate(segment_lengths, 1):
        distance[hill] = distance[hill - 1] + length

    adjusted = []
    for hill, time in cats:
        if type(hill) is not int or type(time) is not int or not 0 <= hill < hill_count:
            raise ValueError("invalid cat")
        adjusted.append(time - distance[hill])
    adjusted.sort()
    adjusted = [0, *adjusted]
    prefix = [0] * len(adjusted)
    for index in range(1, len(adjusted)):
        prefix[index] = prefix[index - 1] + adjusted[index]

    cat_count = len(cats)
    infinity = 10**30
    previous = [infinity] * (cat_count + 1)
    previous[0] = 0
    for groups in range(1, min(group_count, cat_count) + 1):
        current = [infinity] * (cat_count + 1)
        for right in range(groups, cat_count + 1):
            current[right] = min(
                previous[left]
                + adjusted[right] * (right - left)
                - (prefix[right] - prefix[left])
                for left in range(groups - 1, right)
            )
        previous = current
    return previous[cat_count]
```

The time is `O(p m^2)` and rolling space is `O(m)`.

## Expert solution: monotone convex hull DP

```python
from collections import deque


def cats_transport(
    segment_lengths: list[int], cats: list[tuple[int, int]], group_count: int
) -> int:
    hill_count = len(segment_lengths) + 1
    if type(group_count) is not int or group_count < 1 or not cats:
        raise ValueError("cats and a positive group count are required")
    if any(type(length) is not int or length < 0 for length in segment_lengths):
        raise ValueError("segment lengths must be nonnegative integers")
    distance = [0] * hill_count
    for hill, length in enumerate(segment_lengths, 1):
        distance[hill] = distance[hill - 1] + length

    adjusted = []
    for hill, time in cats:
        if type(hill) is not int or type(time) is not int or not 0 <= hill < hill_count:
            raise ValueError("invalid cat")
        adjusted.append(time - distance[hill])
    adjusted.sort()
    adjusted = [0, *adjusted]
    prefix = [0] * len(adjusted)
    for index in range(1, len(adjusted)):
        prefix[index] = prefix[index - 1] + adjusted[index]

    cat_count = len(cats)
    infinity = 10**30
    previous = [infinity] * (cat_count + 1)
    previous[0] = 0

    def value(line: tuple[int, int], coordinate: int) -> int:
        slope, intercept = line
        return slope * coordinate + intercept

    def obsolete(
        first: tuple[int, int], second: tuple[int, int], third: tuple[int, int]
    ) -> bool:
        first_slope, first_intercept = first
        second_slope, second_intercept = second
        third_slope, third_intercept = third
        return (second_intercept - first_intercept) * (second_slope - third_slope) >= (
            third_intercept - second_intercept
        ) * (first_slope - second_slope)

    for groups in range(1, min(group_count, cat_count) + 1):
        current = [infinity] * (cat_count + 1)
        first_left = groups - 1
        hull: deque[tuple[int, int]] = deque(
            [(-first_left, previous[first_left] + prefix[first_left])]
        )

        for right in range(groups, cat_count + 1):
            coordinate = adjusted[right]
            while len(hull) >= 2 and value(hull[0], coordinate) >= value(
                hull[1], coordinate
            ):
                hull.popleft()
            current[right] = (
                adjusted[right] * right - prefix[right] + value(hull[0], coordinate)
            )

            line = (-right, previous[right] + prefix[right])
            if previous[right] < infinity:
                while len(hull) >= 2 and obsolete(hull[-2], hull[-1], line):
                    hull.pop()
                hull.append(line)
        previous = current

    return previous[cat_count]
```

The hull stores every legal split `j` as its transition line. Decreasing slopes
and nondecreasing adjusted times make both insertion and query pointers
monotone, so every line enters and leaves once per DP layer.

**Complexity:** `O(pm + n)` time and `O(m+n)` space.
