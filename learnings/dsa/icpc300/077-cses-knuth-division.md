# ICPC300 077: CSES - Knuth Division

**Source:** [CSES - Knuth Division](https://cses.fi/problemset/task/2088/)  
**Pattern:** Knuth-optimized interval dynamic programming

## Exact contract

Input gives `n` (`1 <= n <= 3000`) and `n` positive values. Recursively divide
the whole array into single-element segments. Dividing a segment costs the sum
of its values. Output the minimum possible total cost.

## First principles

Let `dp[l][r]` be the minimum cost to divide half-open segment `[l, r)`. Its
last division chooses `k`, pays the segment sum, and independently solves both
parts:

`dp[l][r] = sum(l,r) + min(dp[l][k] + dp[k][r])`.

The interval cost satisfies the quadrangle inequality, so optimal split points
are monotone: `opt[l][r-1] <= opt[l][r] <= opt[l+1][r]`. Knuth optimization
therefore checks only that narrow range.

## Cases that decide correctness

- A one-element segment needs no division and costs zero.
- Split positions are strictly inside the interval.
- Prefix sums make every interval sum constant-time.
- Costs require 64-bit storage; packed arrays avoid Python integer-object
  memory for the `O(n^2)` table.

## Brute force: recursively try every division tree

```python
def minimum_division_cost_brute(values: list[int]) -> int:
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    def divide(left: int, right: int) -> int:
        if right - left <= 1:
            return 0
        segment_sum = prefix[right] - prefix[left]
        return segment_sum + min(
            divide(left, split) + divide(split, right)
            for split in range(left + 1, right)
        )

    return divide(0, len(values))
```

The same intervals are recomputed across exponentially many division trees.

## Better: cubic interval DP

```python
def minimum_division_cost_cubic(values: list[int]) -> int:
    size = len(values)
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)
    best = [[0] * (size + 1) for _ in range(size + 1)]

    for length in range(2, size + 1):
        for left in range(size - length + 1):
            right = left + length
            best[left][right] = (
                prefix[right]
                - prefix[left]
                + min(
                    best[left][split] + best[split][right]
                    for split in range(left + 1, right)
                )
            )
    return best[0][size]
```

Memoizing intervals reduces exponential work to `O(n^3)` time and `O(n^2)`
space, still too slow for `n = 3000`.

## Expert solution: packed Knuth DP

```python
from array import array
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    size = data[0]
    values = data[1:]
    prefix = [0]
    for value in values:
        prefix.append(prefix[-1] + value)

    best = [array("Q", [0]) * (size + 1) for _ in range(size + 1)]
    optimal = [array("H", [0]) * (size + 1) for _ in range(size + 1)]
    for left in range(size):
        optimal[left][left + 1] = left + 1

    infinity = (1 << 64) - 1
    for length in range(2, size + 1):
        for left in range(size - length + 1):
            right = left + length
            first_split = optimal[left][right - 1]
            last_split = min(right - 1, optimal[left + 1][right])
            minimum = infinity
            chosen_split = first_split

            for split in range(first_split, last_split + 1):
                candidate = best[left][split] + best[split][right]
                if candidate < minimum:
                    minimum = candidate
                    chosen_split = split
            best[left][right] = minimum + prefix[right] - prefix[left]
            optimal[left][right] = chosen_split

    print(best[0][size])


if __name__ == "__main__":
    solve()
```

Knuth monotonicity guarantees the true split lies inside the two neighboring
optimal bounds. Each interval therefore examines only amortized constant many
splits while preserving the exact cubic recurrence.

**Complexity:** `O(n^2)` time and `O(n^2)` packed space.

