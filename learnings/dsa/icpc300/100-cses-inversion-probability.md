# ICPC300 100: CSES - Inversion Probability

**Source:** [CSES - Inversion Probability](https://cses.fi/problemset/task/1728/)  
**Pattern:** linearity of expectation over pairs

## Exact contract

There are `n` independent random variables. Variable `i` is uniformly chosen
from the integers `1..r_i`. An inversion is a pair `(i, j)` with `i < j` and
the first chosen value strictly greater than the second. Print the expected
number of inversions with six digits after the decimal point.

Input contains `n` on the first line and `r_1 ... r_n` on the second line.

## First principles

Create an indicator for every pair `(i, j)`. Its expectation is the
probability of that pair being an inversion. Linearity of expectation gives

`E[inversions] = sum(P(X_i > X_j), i < j)`.

The pair variables share positions and are not independent, but linearity does
not require independence.

## Cases that decide correctness

- Equal values are not inversions because the comparison is strict.
- Pair `(i, j)` has `r_i * r_j` equally likely value combinations.
- When `r_i = 1`, this position cannot be the larger member of an inversion.
- Count every unordered position pair once, in its original left-to-right
  order.
- Add pair probabilities as floating-point values only after computing their
  integer numerators.

## Brute force: enumerate every joint assignment

```python
from itertools import product


def inversion_probability_enumeration(limits: list[int]) -> float:
    inversion_sum = 0
    outcome_count = 0
    choices = [range(1, limit + 1) for limit in limits]
    for values in product(*choices):
        inversions = 0
        for left in range(len(values)):
            for right in range(left + 1, len(values)):
                inversions += values[left] > values[right]
        inversion_sum += inversions
        outcome_count += 1
    return inversion_sum / outcome_count
```

This directly averages inversion counts over `product(r_i)` assignments.

## Better: enumerate the values of each pair

```python
from fractions import Fraction


def inversion_probability_pairwise(limits: list[int]) -> Fraction:
    expected = Fraction(0)
    for left in range(len(limits)):
        for right in range(left + 1, len(limits)):
            favorable = 0
            for left_value in range(1, limits[left] + 1):
                for right_value in range(1, limits[right] + 1):
                    favorable += left_value > right_value
            expected += Fraction(favorable, limits[left] * limits[right])
    return expected
```

This applies linearity already, but explicitly checks all value pairs. Its
time is `O(sum_{i<j}(r_i r_j))`.

## Expert solution: count favorable value pairs in constant time

```python
import sys


def solve() -> None:
    input_data = list(map(int, sys.stdin.buffer.read().split()))
    count = input_data[0]
    limits = input_data[1:]
    if len(limits) != count:
        raise ValueError("expected exactly n limits")

    expected = 0.0
    for left in range(count):
        left_limit = limits[left]
        for right in range(left + 1, count):
            right_limit = limits[right]
            rising_end = min(left_limit - 1, right_limit)
            favorable = rising_end * (rising_end + 1) // 2
            favorable += (left_limit - 1 - rising_end) * right_limit
            expected += favorable / (left_limit * right_limit)

    print(f"{expected:.6f}")


if __name__ == "__main__":
    solve()
```

For a fixed right value `y`, there are `left_limit - y` larger left values
when that quantity is positive. Summing the resulting decreasing sequence is
equivalent to the triangular term above; any remaining left values each beat
all `right_limit` choices.

**Complexity:** `O(n^2)` time and `O(n)` input storage.
