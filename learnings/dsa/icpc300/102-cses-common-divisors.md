# ICPC300 102: CSES - Common Divisors

**Source:** [CSES - Common Divisors](https://cses.fi/problemset/task/1081/)  
**Pattern:** divisor-frequency sieve  
**Goal:** Find the largest positive integer that divides at least two values in
the input array.

## 1. Problem in plain words

The answer equals the largest gcd of any pair, but checking every pair is too
slow. Reverse the question: for each possible divisor `d`, how many input
values are multiples of `d`?

Scanning divisors from largest to smallest lets us stop at the first count of
at least two.

## 2. First principles

Build `frequency[x]`, the number of occurrences of value `x`. The count of
array values divisible by `d` is:

`frequency[d] + frequency[2d] + frequency[3d] + ...`.

If this sum reaches two, some pair has gcd at least `d`. The first qualifying
`d` in descending order is exactly the maximum possible common divisor.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| Two equal maximum values | That value itself. |
| All pairs coprime | `1`. |
| A divisor belongs to many values | It still qualifies once count reaches two. |
| Larger divisor belongs to only one value | Continue downward. |
| Input has fewer than two values | Reject it. |

## 4. Brute force: gcd of every pair

```python
from math import gcd


def largest_common_divisor_brute_force(values: list[int]) -> int:
    if len(values) < 2 or any(value < 1 for value in values):
        raise ValueError("at least two positive values are required")
    return max(
        gcd(values[first], values[second])
        for first in range(len(values))
        for second in range(first + 1, len(values))
    )
```

**Complexity:** `O(n^2 log A)` time and `O(1)` auxiliary memory.

## 5. Better when values are sparse: enumerate each value's divisors

Count every divisor of every input value by trial division, then return the
largest divisor whose count is at least two.

```python
from collections import Counter
from math import isqrt


def largest_common_divisor_by_enumeration(values: list[int]) -> int:
    if len(values) < 2 or any(value < 1 for value in values):
        raise ValueError("at least two positive values are required")

    divisor_count: Counter[int] = Counter()
    for value in values:
        for divisor in range(1, isqrt(value) + 1):
            if value % divisor != 0:
                continue
            divisor_count[divisor] += 1
            paired = value // divisor
            if paired != divisor:
                divisor_count[paired] += 1
    return max(divisor for divisor, count in divisor_count.items() if count >= 2)
```

**Complexity:** `O(n sqrt(A))` time and `O(number of discovered divisors)`
memory.

## 6. Expert solution: scan multiples of each divisor

```python
def largest_common_divisor(values: list[int]) -> int:
    if len(values) < 2 or any(value < 1 for value in values):
        raise ValueError("at least two positive values are required")

    maximum = max(values)
    frequency = [0] * (maximum + 1)
    for value in values:
        frequency[value] += 1

    for divisor in range(maximum, 0, -1):
        divisible_count = 0
        for multiple in range(divisor, maximum + 1, divisor):
            divisible_count += frequency[multiple]
            if divisible_count >= 2:
                return divisor
    raise RuntimeError("divisor one must qualify")
```

### Why the expert code is correct

- The inner loop visits exactly all possible values divisible by `divisor`.
- Their frequencies sum to the number of input elements sharing that divisor.
- A count of two is equivalent to the existence of an input pair whose gcd is
  at least that divisor.
- Descending order makes the first qualifying divisor the largest one.

**Complexity:** `O(A log A + n)` time by the harmonic series and `O(A)` memory,
where `A` is the maximum input value.

## 7. What to remember

Replace pairwise gcd checks with a frequency question: count input multiples of
each candidate divisor, scanning candidates downward.
