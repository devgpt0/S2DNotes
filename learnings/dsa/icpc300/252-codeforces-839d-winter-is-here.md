# ICPC300 252: Codeforces 839D - Winter is here

**Source:** [Codeforces 839D - Winter is here](https://codeforces.com/problemset/problem/839/D)  
**Rating:** 2200  
**Pattern:** divisor sieve with exact-GCD weighted inversion  
**Goal:** Over every nonempty subsequence, sum
`subsequence_length * gcd(subsequence)` modulo `1_000_000_007`.

## 1. First principles

If `count[d]` array elements are divisible by `d`, the sum of sizes over all
nonempty subsequences of those elements is

```text
count[d] * 2^(count[d] - 1)
```

Those subsequences have exact GCD equal to some multiple of `d`. Process `d`
downward and subtract the already known weighted counts of larger multiples.
Multiply the remaining exact count by `d` for its answer contribution.

## 2. Cases that decide correctness

- Equal values are distinct subsequence choices.
- A divisor with no divisible elements contributes zero.
- The empty subsequence contributes neither size nor GCD.
- Every nonempty subsequence has one exact positive GCD.
- Negative intermediate subtraction is reduced modulo the prime.

## 3. Brute force: enumerate every subsequence

```python
from math import gcd


MODULO = 1_000_000_007


def weighted_gcd_sum_brute(values: list[int]) -> int:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")
    answer = 0
    for chosen in range(1, 1 << len(values)):
        current_gcd = 0
        length = 0
        for index, value in enumerate(values):
            if chosen >> index & 1:
                current_gcd = gcd(current_gcd, value)
                length += 1
        answer += length * current_gcd
    return answer % MODULO
```

**Complexity:** `O(n 2^n log max(values))` time and `O(1)` extra space.

## 4. Better transition: count total selected positions by divisor

For `c` eligible indices, each index appears in exactly `2^(c-1)` subsets.
This counts the sum of subset sizes directly. Descending divisor subtraction
then converts divisibility counts into exact-GCD counts.

## 5. Expert solution: harmonic divisor inversion

```python
MODULO = 1_000_000_007


def weighted_gcd_sum(values: list[int]) -> int:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    maximum = max(values)
    frequency = [0] * (maximum + 1)
    for value in values:
        frequency[value] += 1
    powers_of_two = [1] * (len(values) + 1)
    for exponent in range(1, len(powers_of_two)):
        powers_of_two[exponent] = powers_of_two[exponent - 1] * 2 % MODULO

    exact_weighted_count = [0] * (maximum + 1)
    answer = 0
    for divisor in range(maximum, 0, -1):
        divisible_count = sum(
            frequency[multiple] for multiple in range(divisor, maximum + 1, divisor)
        )
        if divisible_count:
            exact_weighted_count[divisor] = (
                divisible_count * powers_of_two[divisible_count - 1]
            ) % MODULO
        for multiple in range(2 * divisor, maximum + 1, divisor):
            exact_weighted_count[divisor] -= exact_weighted_count[multiple]
        exact_weighted_count[divisor] %= MODULO
        answer += divisor * exact_weighted_count[divisor]
    return answer % MODULO
```

### Why the expert code is correct

The initial expression for divisor `d` is the total selected-position count of
all subsequences whose elements are divisible by `d`. Each such subsequence has
one exact GCD that is a multiple of `d`. Subtracting exact counts of larger
multiples leaves precisely subsequences with GCD `d`, already weighted by their
length, so multiplying by `d` gives their required sum.

**Complexity:** `O(M log M + n)` time and `O(M+n)` space for maximum `M`.

## 6. What to remember

```text
sum of subset sizes from c items -> c * 2^(c-1)
all elements divisible by d -> gcd is a multiple of d
exact gcd -> subtract larger multiples downward
```
