# ICPC300 276: Codeforces 1304F2 - Animal Observation (hard version)

**Source:** [Codeforces 1304F2](https://codeforces.com/problemset/problem/1304/F2)  
**Difficulty:** 2600  
**Pattern:** row DP with range-maximum transition decomposition

## Exact contract

For every adjacent row pair, choose one width-`k`, height-two rectangle. Maximize
the sum of grid cells covered by at least one chosen rectangle; overlaps count
once.

## First principles

Let `dp[p]` be the best union value through the previous row pair when its
rectangle starts at column `p`. For current start `j`, add its two-row sum and
subtract the overlap of intervals `p` and `j` on their shared row.

With shared-row prefix sums `S`, split previous starts into four ranges:

- `p <= j-k` or `p >= j+k`: no overlap, use `dp[p]`;
- `j-k < p <= j`: use `dp[p]-S[p+k]+S[j]`;
- `j <= p < j+k`: use `dp[p]+S[p]-S[j+k]`.

Each range is a static maximum query.

## Cases that decide correctness

- Adjacent chosen rectangles overlap only on their shared row.
- A shared cell is subtracted exactly once.
- Starts range from zero through `m-k` inclusive.
- The two middle ranges both include `p=j` and give the same value there.
- Grid values are nonnegative, but totals need wide integers.

## Brute force: try every previous start in the DP transition

```python
def animal_observation_brute(grid: list[list[int]], width: int) -> int:
    row_count = len(grid)
    column_count = len(grid[0])
    start_count = column_count - width + 1
    prefix = [[0] * (column_count + 1) for _ in range(row_count)]
    for row in range(row_count):
        for column, value in enumerate(grid[row]):
            prefix[row][column + 1] = prefix[row][column] + value

    def row_sum(row: int, start: int) -> int:
        return prefix[row][start + width] - prefix[row][start]

    previous = [row_sum(0, start) + row_sum(1, start) for start in range(start_count)]
    for row in range(1, row_count - 1):
        current = [0] * start_count
        for start in range(start_count):
            rectangle = row_sum(row, start) + row_sum(row + 1, start)
            best = 0
            for old_start in range(start_count):
                overlap_left = max(start, old_start)
                overlap_right = min(start + width, old_start + width)
                overlap = 0
                if overlap_left < overlap_right:
                    overlap = prefix[row][overlap_right] - prefix[row][overlap_left]
                best = max(best, previous[old_start] - overlap)
            current[start] = rectangle + best
        previous = current
    return max(previous)
```

This takes `O(nm^2)` time.

## Better insight: overlap algebra creates four range maxima

For one row transition, build maximum structures for `dp[p]`,
`dp[p]-S[p+k]`, and `dp[p]+S[p]`. Every new start then needs four logarithmic
queries rather than a scan.

## Expert solution: three iterative maximum trees per row

```python
import sys


NEGATIVE_INFINITY = -(10**30)


class RangeMaximum:
    def __init__(self, values: list[int]) -> None:
        self.base = 1
        while self.base < len(values):
            self.base *= 2
        self.tree = [NEGATIVE_INFINITY] * (2 * self.base)
        self.tree[self.base : self.base + len(values)] = values
        for node in range(self.base - 1, 0, -1):
            self.tree[node] = max(self.tree[node * 2], self.tree[node * 2 + 1])

    def query(self, left: int, right: int) -> int:
        if left >= right:
            return NEGATIVE_INFINITY
        answer = NEGATIVE_INFINITY
        left += self.base
        right += self.base
        while left < right:
            if left & 1:
                answer = max(answer, self.tree[left])
                left += 1
            if right & 1:
                right -= 1
                answer = max(answer, self.tree[right])
            left //= 2
            right //= 2
        return answer


def solve() -> None:
    input_stream = sys.stdin.buffer
    row_count, column_count, width = map(int, input_stream.readline().split())
    grid = [list(map(int, input_stream.readline().split())) for _ in range(row_count)]
    prefix = [[0] * (column_count + 1) for _ in range(row_count)]
    for row in range(row_count):
        for column, value in enumerate(grid[row]):
            prefix[row][column + 1] = prefix[row][column] + value

    def row_sum(row: int, start: int) -> int:
        return prefix[row][start + width] - prefix[row][start]

    start_count = column_count - width + 1
    previous = [row_sum(0, start) + row_sum(1, start) for start in range(start_count)]
    for row in range(1, row_count - 1):
        shared_prefix = prefix[row]
        plain_tree = RangeMaximum(previous)
        left_tree = RangeMaximum(
            [
                previous[start] - shared_prefix[start + width]
                for start in range(start_count)
            ]
        )
        right_tree = RangeMaximum(
            [previous[start] + shared_prefix[start] for start in range(start_count)]
        )
        current = [0] * start_count
        for start in range(start_count):
            best = max(
                plain_tree.query(0, start - width + 1),
                shared_prefix[start]
                + left_tree.query(max(0, start - width + 1), start + 1),
                -shared_prefix[start + width]
                + right_tree.query(start, min(start_count, start + width)),
                plain_tree.query(start + width, start_count),
            )
            current[start] = row_sum(row, start) + row_sum(row + 1, start) + best
        previous = current
    print(max(previous))


if __name__ == "__main__":
    solve()
```

The four ranges partition every previous start, and their transformed maxima
equal the direct overlap-subtracted transition.

**Complexity:** `O(nm log m)` time and `O(nm)` input-plus-prefix space.
