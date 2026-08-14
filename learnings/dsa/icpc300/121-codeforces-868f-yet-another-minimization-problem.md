# ICPC300 121: Codeforces 868F - Yet Another Minimization Problem

**Source:** [Codeforces 868F](https://codeforces.com/problemset/problem/868/F)  
**Pattern:** divide-and-conquer DP with a movable cost window

## Exact contract

Given `n <= 100000`, `k <= 20`, and an array whose values lie in `1..n`, split
the array into exactly `k` nonempty contiguous groups. A group's cost is the
number of equal-index pairs inside it: pairs `(i,j)` with `i < j` and
`a[i] = a[j]`. Output the minimum possible sum of group costs.

## First principles

Let `dp[g][r]` be the best cost for the first `r` values in `g` groups. If the
last group starts after split position `s`, then

`dp[g][r] = min(dp[g-1][s] + cost(s,r))` for `g-1 <= s < r`,

where `cost(s,r)` counts equal pairs in the half-open slice `a[s:r]`.
Adding a value to a maintained window creates one pair with each equal value
already inside; removing it destroys the same number after its frequency is
decremented.

This cost is Monge, so the best split positions are nondecreasing as `r`
increases. Divide-and-conquer optimization only searches the monotone range.

## Cases that decide correctness

- Groups are nonempty, so layer `g` starts at prefix length `g`.
- A value occurring `f` times contributes `f*(f-1)/2`, not `f*f`.
- The movable window represents exactly `a[s:r]` for the candidate split.
- Impossible previous states must remain infinity.
- The answer can exceed 32-bit range.

## Brute force: enumerate every cut set

```python
from itertools import combinations


def equal_pair_partition_brute(values: list[int], group_count: int) -> int:
    def segment_cost(left: int, right: int) -> int:
        return sum(
            values[first] == values[second]
            for first in range(left, right)
            for second in range(first + 1, right)
        )

    best = float("inf")
    for cuts in combinations(range(1, len(values)), group_count - 1):
        boundaries = (0, *cuts, len(values))
        cost = sum(
            segment_cost(boundaries[index], boundaries[index + 1])
            for index in range(group_count)
        )
        best = min(best, cost)
    return int(best)
```

There are `C(n-1,k-1)` cut sets, and each is evaluated directly.

## Better: quadratic transition DP

```python
def equal_pair_partition_quadratic(values: list[int], group_count: int) -> int:
    size = len(values)
    infinity = size * size + 1
    previous = [infinity] * (size + 1)
    previous[0] = 0

    for _ in range(group_count):
        current = [infinity] * (size + 1)
        for right in range(1, size + 1):
            frequencies: dict[int, int] = {}
            segment_cost = 0
            for left in range(right - 1, -1, -1):
                value = values[left]
                segment_cost += frequencies.get(value, 0)
                frequencies[value] = frequencies.get(value, 0) + 1
                current[right] = min(current[right], previous[left] + segment_cost)
        previous = current
    return previous[size]
```

Growing every candidate segment backward updates its cost in constant time,
but the `O(k n^2)` transitions are too slow for the source limits.

## Expert solution: monotone splits and one shared window

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    size, group_count = data[0:2]
    values = data[2:]
    infinity = size * size + 1
    previous = [infinity] * (size + 1)
    previous[0] = 0

    for group in range(1, group_count + 1):
        current = [infinity] * (size + 1)
        frequencies = [0] * (max(values) + 1)
        window_left = 0
        window_right = -1
        window_cost = 0

        def move_window(new_left: int, new_right: int) -> None:
            nonlocal window_left, window_right, window_cost
            while window_left > new_left:
                window_left -= 1
                value = values[window_left]
                window_cost += frequencies[value]
                frequencies[value] += 1
            while window_right < new_right:
                window_right += 1
                value = values[window_right]
                window_cost += frequencies[value]
                frequencies[value] += 1
            while window_left < new_left:
                value = values[window_left]
                frequencies[value] -= 1
                window_cost -= frequencies[value]
                window_left += 1
            while window_right > new_right:
                value = values[window_right]
                frequencies[value] -= 1
                window_cost -= frequencies[value]
                window_right -= 1

        def compute(left: int, right: int, split_left: int, split_right: int) -> None:
            if left > right:
                return
            middle = (left + right) // 2
            best_split = split_left
            upper_split = min(middle - 1, split_right)
            for split in range(split_left, upper_split + 1):
                move_window(split, middle - 1)
                candidate = previous[split] + window_cost
                if candidate < current[middle]:
                    current[middle] = candidate
                    best_split = split
            compute(left, middle - 1, split_left, best_split)
            compute(middle + 1, right, best_split, split_right)

        compute(group, size, group - 1, size - 1)
        previous = current

    print(previous[size])


if __name__ == "__main__":
    solve()
```

For each midpoint, the loop evaluates every split still allowed by monotonicity
with the exact current segment cost. The recursive split bounds preserve the
optimal candidate, so the result equals the full recurrence.

**Complexity:** `O(k n log n)` window moves and `O(n)` extra space.
