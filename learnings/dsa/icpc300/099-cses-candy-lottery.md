# ICPC300 099: CSES - Candy Lottery

**Source:** [CSES - Candy Lottery](https://cses.fi/problemset/task/1727/)  
**Pattern:** expectation from a cumulative distribution

## Exact contract

There are `n` children. Independently, every child receives a uniformly random
integer number of candies from `1` through `k`. Print the expected largest
number of candies received by any child, with six digits after the decimal
point.

## First principles

Let `M` be the maximum. All `n` choices are at most `m` exactly when every
choice lies in `1..m`, so

`P(M <= m) = (m / k)^n`.

For a positive integer-valued variable bounded by `k`,

`E[M] = sum(P(M >= m), m = 1..k)`.

Thus each answer term is `1 - ((m - 1) / k)^n`.

## Cases that decide correctness

- The choices of different children are independent.
- The maximum is in `1..k`; there is no zero-candy outcome.
- For `n = 1`, the answer is `(k + 1) / 2`.
- For `k = 1`, the answer is exactly `1` for every `n`.
- Compute ratios before exponentiation; huge integer powers are unnecessary in
  the source solution.

## Brute force: enumerate every lottery outcome

```python
from itertools import product


def candy_lottery_enumeration(children: int, maximum_candies: int) -> float:
    total = 0
    outcomes = 0
    for received in product(range(1, maximum_candies + 1), repeat=children):
        total += max(received)
        outcomes += 1
    return total / outcomes
```

This is the definition of the expectation, but it takes
`O(k^n * n)` time.

## Better: count outcomes with each exact maximum

```python
from fractions import Fraction


def candy_lottery_exact(children: int, maximum_candies: int) -> Fraction:
    outcome_count = maximum_candies**children
    weighted_sum = 0
    for value in range(1, maximum_candies + 1):
        exact_count = value**children - (value - 1) ** children
        weighted_sum += value * exact_count
    return Fraction(weighted_sum, outcome_count)
```

There are `m^n - (m-1)^n` outcomes whose maximum is exactly `m`. This is
`O(k log n)` arithmetic operations, but its integers can contain millions of
digits at the largest source limits.

## Expert solution: sum tail probabilities

```python
import sys


def solve() -> None:
    children, maximum_candies = map(int, sys.stdin.readline().split())
    expected = 0.0
    for value in range(1, maximum_candies + 1):
        expected += 1.0 - ((value - 1) / maximum_candies) ** children
    print(f"{expected:.6f}")


if __name__ == "__main__":
    solve()
```

The tail-sum identity counts value `m` once precisely when the maximum reaches
at least `m`. The cumulative-distribution formula supplies that probability,
so their sum is exactly the required expectation.

**Complexity:** `O(k)` time and `O(1)` extra space.
