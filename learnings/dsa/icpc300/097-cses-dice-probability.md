# ICPC300 097: CSES - Dice Probability

**Source:** [CSES - Dice Probability](https://cses.fi/problemset/task/1725/)  
**Pattern:** sum-distribution probability DP

## Exact contract

Input gives integers `n`, `a`, and `b`. Roll `n` independent fair six-sided
dice. Output the probability that their sum lies in the inclusive range
`[a,b]`, with six digits after the decimal point.

## First principles

After some dice, the total sum is a sufficient state. Appending one die sends
each probability equally to six next sums. After all dice, add probabilities
for sums from `a` through `b`.

## Cases that decide correctness

- Possible sums range from `n` through `6n`; clamp the requested interval.
- Outcomes are independent and each face has probability `1/6`.
- Ranges completely outside the possible sums have probability zero.
- Rolling arrays are safe because each layer depends only on the previous one.

## Brute force: enumerate all dice outcomes

```python
from itertools import product


def dice_probability_brute(dice_count: int, lower: int, upper: int) -> float:
    favorable = sum(
        lower <= sum(outcome) <= upper
        for outcome in product(range(1, 7), repeat=dice_count)
    )
    return favorable / 6**dice_count
```

**Complexity:** `O(6^n n)` time.

## Better: memoize remaining dice and required sum

```python
from functools import cache


def dice_probability_memo(dice_count: int, lower: int, upper: int) -> float:
    @cache
    def ways(remaining_dice: int, required_sum: int) -> int:
        if remaining_dice == 0:
            return int(required_sum == 0)
        return sum(
            ways(remaining_dice - 1, required_sum - face) for face in range(1, 7)
        )

    favorable = sum(ways(dice_count, total) for total in range(lower, upper + 1))
    return favorable / 6**dice_count
```

Memoization reduces work to `O(n^2)` reachable sum states but stores every
layer and uses recursion.

## Expert solution: rolling probability distribution

```python
import sys


def solve() -> None:
    dice_count, lower, upper = map(int, sys.stdin.readline().split())
    probability = [0.0] * (6 * dice_count + 1)
    probability[0] = 1.0

    for rolled in range(dice_count):
        next_probability = [0.0] * (6 * dice_count + 1)
        for current_sum in range(rolled, 6 * rolled + 1):
            share = probability[current_sum] / 6.0
            for face in range(1, 7):
                next_probability[current_sum + face] += share
        probability = next_probability

    lower = max(lower, dice_count)
    upper = min(upper, 6 * dice_count)
    answer = 0.0 if lower > upper else sum(probability[lower : upper + 1])
    print(f"{answer:.6f}")


if __name__ == "__main__":
    solve()
```

Each update applies the law of total probability across the six equally likely
last faces. Induction on rolled dice proves the array is the exact sum
distribution up to floating-point rounding.

**Complexity:** `O(n^2)` time and `O(n)` space because the sum range is `6n`.

