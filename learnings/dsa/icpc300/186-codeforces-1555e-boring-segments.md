# ICPC300 186: Codeforces 1555E - Boring Segments

**Source:** [Codeforces 1555E](https://codeforces.com/problemset/problem/1555/E)  
**Pattern:** weight-sorted sliding window with range-add minimum

## Exact contract

There are weighted integer segments `[l_i,r_i]` inside `[1,m]`. Choose some
segments whose union covers the whole interval `[1,m]`. Minimize the difference
between the maximum and minimum selected weights.

## First principles

Covering `[1,m]` is equivalent to covering every unit gap
`[1,2], [2,3], ..., [m-1,m]`. A segment `[l,r]` covers gap indices
`l..r-1`.

Sort segments by weight. If some selected set has minimum and maximum weights
`x` and `y`, then using every segment in the sorted window `[x,y]` also covers
the interval. Maintain the smallest right endpoint that covers all gaps for
each left endpoint. A lazy segment tree stores each gap's current coverage and
its global minimum.

## Cases that decide correctness

- Segment endpoints are inclusive, but the represented unit gaps are
  `[l,r)`.
- A zero-length segment covers no gap.
- Multiple equal-weight segments belong to the same zero-width weight window.
- Every gap must have positive coverage.
- Removing the left segment happens only after evaluating its current window.

## Brute force: enumerate selected subsets

```python
def boring_segments_brute(
    destination: int, segments: list[tuple[int, int, int]]
) -> int:
    if destination == 1:
        return 0
    answer = 10**30
    for subset in range(1, 1 << len(segments)):
        covered = [False] * (destination - 1)
        weights = []
        for index, (left, right, weight) in enumerate(segments):
            if not (subset >> index & 1):
                continue
            weights.append(weight)
            for gap in range(left - 1, right - 1):
                covered[gap] = True
        if all(covered):
            answer = min(answer, max(weights) - min(weights))
    return answer
```

This takes exponential time in the number of segments.

## Better: test every sorted weight window

Sorting removes arbitrary subsets: a feasible subset always sits inside a
feasible contiguous weight window. Recomputing coverage for all `O(n^2)`
windows is still too slow; two pointers reuse the previous window.

## Expert solution: add and remove segment coverage

```python
import sys


def solve() -> None:
    input_stream = sys.stdin.buffer
    segment_count, destination = map(int, input_stream.readline().split())
    segments: list[tuple[int, int, int]] = []
    for _ in range(segment_count):
        left, right, weight = map(int, input_stream.readline().split())
        segments.append((left, right, weight))
    segments.sort(key=lambda segment: segment[2])
    gap_count = destination - 1
    if gap_count == 0:
        print(0)
        return

    minimum = [0] * (4 * gap_count)
    lazy = [0] * (4 * gap_count)

    def add(
        node: int,
        left: int,
        right: int,
        query_left: int,
        query_right: int,
        difference: int,
    ) -> None:
        if query_right <= left or right <= query_left:
            return
        if query_left <= left and right <= query_right:
            minimum[node] += difference
            lazy[node] += difference
            return
        middle = (left + right) // 2
        add(node * 2, left, middle, query_left, query_right, difference)
        add(
            node * 2 + 1,
            middle,
            right,
            query_left,
            query_right,
            difference,
        )
        minimum[node] = lazy[node] + min(minimum[node * 2], minimum[node * 2 + 1])

    def change(segment: tuple[int, int, int], difference: int) -> None:
        left, right, _ = segment
        if left < right:
            add(1, 0, gap_count, left - 1, right - 1, difference)

    answer = 10**30
    right_index = 0
    for left_index, segment in enumerate(segments):
        while right_index < segment_count and minimum[1] == 0:
            change(segments[right_index], 1)
            right_index += 1
        if minimum[1] == 0:
            break
        answer = min(
            answer,
            segments[right_index - 1][2] - segment[2],
        )
        change(segment, -1)
    print(answer)


if __name__ == "__main__":
    solve()
```

The active sorted window covers the destination exactly when the root minimum
is positive. Two pointers inspect the minimum feasible right endpoint for every
left endpoint.

**Complexity:** `O(n log n + n log m)` time and `O(m)` space.
