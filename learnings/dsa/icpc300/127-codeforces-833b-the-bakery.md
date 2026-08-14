# ICPC300 127: Codeforces 833B - The Bakery

**Source:** [Codeforces 833B](https://codeforces.com/problemset/problem/833/B)  
**Pattern:** DP accelerated by range-add/range-maximum updates

## Exact contract

Split an array of `n` integers into exactly `k` nonempty contiguous segments.
The value of a segment is its number of distinct integers. Output the maximum
possible sum of segment values.

## First principles

For a fixed number of segments, maintain one candidate for every split `j`:

`previous[j] + distinct(a[j+1..r])`.

When the right endpoint advances to position `r` with value `x`, let `p` be
the previous position of `x`, or zero. Exactly the candidate splits
`j in [p,r-1]` gain one: their last segment did not previously contain `x`.
This is one range addition, followed by a range maximum over legal splits.

## Cases that decide correctness

- Segments are nonempty, so a prefix of length `r` only uses splits below `r`.
- The previous occurrence table resets for every DP layer.
- Splits before the previous equal value do not gain a new distinct element.
- Impossible DP states must not win a maximum after range additions.
- Exactly `k` segments are required, not at most `k`.

## Brute force: enumerate every cut set

```python
from itertools import combinations


def bakery_brute(values: list[int], segment_count: int) -> int:
    best = 0
    for cuts in combinations(range(1, len(values)), segment_count - 1):
        boundaries = (0, *cuts, len(values))
        score = sum(
            len(set(values[boundaries[index] : boundaries[index + 1]]))
            for index in range(segment_count)
        )
        best = max(best, score)
    return best
```

The number of partitions is `C(n-1,k-1)`.

## Better: quadratic dynamic programming

```python
def bakery_quadratic(values: list[int], segment_count: int) -> int:
    size = len(values)
    negative_infinity = -(10**9)
    previous = [negative_infinity] * (size + 1)
    previous[0] = 0
    for _ in range(segment_count):
        current = [negative_infinity] * (size + 1)
        for right in range(1, size + 1):
            distinct = set()
            for left in range(right - 1, -1, -1):
                distinct.add(values[left])
                current[right] = max(current[right], previous[left] + len(distinct))
        previous = current
    return previous[size]
```

This is the exact recurrence, but it evaluates all `O(n^2)` last segments per
layer.

## Expert solution: update every split candidate at once

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    size, segment_count = data[0:2]
    values = data[2:]
    negative_infinity = -(10**9)
    previous = [negative_infinity] * (size + 1)
    previous[0] = 0

    for _ in range(segment_count):
        segment_maximum = [negative_infinity] * (4 * (size + 1))
        lazy_add = [0] * (4 * (size + 1))

        def build(node: int, left: int, right: int) -> None:
            if right - left == 1:
                segment_maximum[node] = previous[left]
                return
            middle = (left + right) // 2
            build(node * 2, left, middle)
            build(node * 2 + 1, middle, right)
            segment_maximum[node] = max(
                segment_maximum[node * 2], segment_maximum[node * 2 + 1]
            )

        def add(
            node: int,
            left: int,
            right: int,
            query_left: int,
            query_right: int,
            value: int,
        ) -> None:
            if query_right <= left or right <= query_left:
                return
            if query_left <= left and right <= query_right:
                segment_maximum[node] += value
                lazy_add[node] += value
                return
            middle = (left + right) // 2
            add(node * 2, left, middle, query_left, query_right, value)
            add(node * 2 + 1, middle, right, query_left, query_right, value)
            segment_maximum[node] = lazy_add[node] + max(
                segment_maximum[node * 2], segment_maximum[node * 2 + 1]
            )

        def maximum(
            node: int,
            left: int,
            right: int,
            query_left: int,
            query_right: int,
            inherited_add: int = 0,
        ) -> int:
            if query_right <= left or right <= query_left:
                return negative_infinity
            if query_left <= left and right <= query_right:
                return inherited_add + segment_maximum[node]
            inherited_add += lazy_add[node]
            middle = (left + right) // 2
            return max(
                maximum(
                    node * 2,
                    left,
                    middle,
                    query_left,
                    query_right,
                    inherited_add,
                ),
                maximum(
                    node * 2 + 1,
                    middle,
                    right,
                    query_left,
                    query_right,
                    inherited_add,
                ),
            )

        build(1, 0, size + 1)
        current = [negative_infinity] * (size + 1)
        last_position: dict[int, int] = {}
        for right, value in enumerate(values, start=1):
            previous_position = last_position.get(value, 0)
            add(1, 0, size + 1, previous_position, right, 1)
            current[right] = maximum(1, 0, size + 1, 0, right)
            last_position[value] = right
        previous = current

    print(previous[size])


if __name__ == "__main__":
    solve()
```

The segment-tree leaf for split `j` always equals the previous-layer score
plus the distinct count of the current last segment. The update interval is
exactly the set of splits for which the new value was absent.

**Complexity:** `O(k n log n)` time and `O(n)` extra space.
