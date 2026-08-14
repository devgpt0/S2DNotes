# ICPC300 229: Codeforces 803F - Coprime Subsequences

**Source:** [Codeforces 803F - Coprime Subsequences](https://codeforces.com/problemset/problem/803/F)  
**Rating:** 2200  
**Pattern:** divisor sieve with descending exact-GCD inversion  
**Goal:** Count nonempty subsequences whose greatest common divisor is one,
modulo `1_000_000_007`.

## 1. First principles

For every divisor `d`, count array elements divisible by `d`. Every nonempty
subsequence of those elements has a GCD that is a multiple of `d`, giving

```text
all_multiples[d] = 2^count[d] - 1
```

Process divisors downward. Subtract subsequences whose exact GCD is `2d, 3d,
...`; the remainder has exact GCD `d`. The requested answer is the value for
`d = 1`.

## 2. Cases that decide correctness

- Subsequences choose indices, so equal values remain distinct choices.
- The empty subsequence is excluded by subtracting one.
- Every subsequence has one exact positive GCD.
- Descending order makes all proper multiples already known.
- All subtraction is reduced modulo `1_000_000_007`.

## 3. Brute force: enumerate every nonempty subsequence

```python
from math import gcd


MODULO = 1_000_000_007


def coprime_subsequence_count_brute(values: list[int]) -> int:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")
    answer = 0
    for chosen in range(1, 1 << len(values)):
        current_gcd = 0
        for index, value in enumerate(values):
            if chosen >> index & 1:
                current_gcd = gcd(current_gcd, value)
        answer += current_gcd == 1
    return answer % MODULO
```

**Complexity:** `O(n 2^n log max(values))` time and `O(1)` extra space.

## 4. Better transition: count by divisibility, then recover exact GCDs

Counting subsequences directly by GCD is difficult, but counting those whose
every element is divisible by `d` is one power of two. Multiples form a divisor
poset, and descending subtraction performs its elementary Möbius inversion.

## 5. Expert solution: sieve counts and subtract multiples

```python
MODULO = 1_000_000_007


def coprime_subsequence_count(values: list[int]) -> int:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")

    maximum = max(values)
    frequency = [0] * (maximum + 1)
    for value in values:
        frequency[value] += 1

    powers_of_two = [1] * (len(values) + 1)
    for exponent in range(1, len(powers_of_two)):
        powers_of_two[exponent] = powers_of_two[exponent - 1] * 2 % MODULO

    exact = [0] * (maximum + 1)
    for divisor in range(maximum, 0, -1):
        divisible_count = sum(
            frequency[multiple] for multiple in range(divisor, maximum + 1, divisor)
        )
        exact[divisor] = powers_of_two[divisible_count] - 1
        for multiple in range(2 * divisor, maximum + 1, divisor):
            exact[divisor] -= exact[multiple]
        exact[divisor] %= MODULO
    return exact[1]
```

### Why the expert code is correct

`2^count[d]-1` counts exactly the nonempty subsequences in which every element
is divisible by `d`. Such a subsequence's exact GCD is one unique multiple of
`d`. Subtracting the already computed exact counts of larger multiples leaves
precisely exact GCD `d`; hence the final `exact[1]` is the requested count.

**Complexity:** `O(M log M + n)` time and `O(M+n)` space for maximum value `M`.

## 6. What to remember

```text
all elements divisible by d -> 2^count[d] - 1 subsequences
exact gcd d -> subtract exact counts of larger multiples
divisor loops -> harmonic O(M log M)
```
