# ICPC300 091: CSES - Removal Game

**Source:** [CSES - Removal Game](https://cses.fi/problemset/task/1097/)  
**Pattern:** interval minimax DP with one-dimensional compression

## Exact contract

Input gives `n` (`1 <= n <= 5000`) and `n` positive integers. Two players
alternate removing either the first or last remaining number and add it to
their score. Both play optimally. Output the maximum score the first player can
guarantee.

## First principles

For interval `[l,r]`, store the best score difference current player minus the
other player. Taking left yields `a[l] - difference[l+1,r]`; taking right yields
`a[r] - difference[l,r-1]`. Choose the larger.

If total sum is `S` and the final difference is `D`, the first score is
`(S+D)/2`. The recurrence uses only intervals one element shorter, so one array
is enough.

## Cases that decide correctness

- A one-element interval has difference equal to that element.
- The recurrence subtracts the opponent's future advantage.
- Update left endpoints in increasing order so `dp[l+1]` still represents the
  previous interval length.
- Scores require 64-bit arithmetic.

## Brute force: explore the complete game tree

```python
def removal_game_brute(values: list[int]) -> int:
    def difference(left: int, right: int) -> int:
        if left == right:
            return values[left]
        return max(
            values[left] - difference(left + 1, right),
            values[right] - difference(left, right - 1),
        )

    advantage = difference(0, len(values) - 1)
    return (sum(values) + advantage) // 2
```

**Complexity:** `O(2^n)` time and `O(n)` recursion space.

## Better: full interval table

```python
def removal_game_table(values: list[int]) -> int:
    size = len(values)
    difference = [[0] * size for _ in range(size)]
    for index, value in enumerate(values):
        difference[index][index] = value

    for length in range(2, size + 1):
        for left in range(size - length + 1):
            right = left + length - 1
            difference[left][right] = max(
                values[left] - difference[left + 1][right],
                values[right] - difference[left][right - 1],
            )
    return (sum(values) + difference[0][-1]) // 2
```

**Complexity:** `O(n^2)` time and `O(n^2)` space, which is excessive for
Python objects at `n = 5000`.

## Expert solution: one-dimensional interval DP

```python
import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    size = data[0]
    values = data[1:]
    difference = values.copy()

    for length in range(2, size + 1):
        for left in range(size - length + 1):
            right = left + length - 1
            difference[left] = max(
                values[left] - difference[left + 1],
                values[right] - difference[left],
            )

    print((sum(values) + difference[0]) // 2)


if __name__ == "__main__":
    solve()
```

Before an update, `difference[left]` and `difference[left+1]` are exactly the
two shorter intervals required by the recurrence. Thus compression changes no
state value.

**Complexity:** `O(n^2)` time and `O(n)` space.

