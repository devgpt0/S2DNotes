# ICPC300 300: Codeforces 1794D - Counting Factorizations

**Source:** [Codeforces 1794D - Counting Factorizations](https://codeforces.com/problemset/problem/1794/D)  
**Rating:** 2200  
**Pattern:** prime-value selection and multiplicity-generating DP  
**Goal:** From a multiset of `2n` values, select one copy of each of `n`
distinct prime values. Count distinct permutations of the `n` unselected
values, summed over all valid selections, modulo `998_244_353`.

## 1. First principles

For one selected set of prime values, the remaining multiset has `n` items and
contributes `n! / product(remaining_frequency!)` permutations.

Start with `n! / product(original_frequency!)`. Selecting a prime value of
frequency `count` changes its denominator from `count!` to `(count-1)!`, a
multiplicative factor of `count`. A one-dimensional DP chooses `n` distinct
prime values and multiplies these frequency factors.

## 2. Cases that decide correctness

- Repeated copies of one prime still provide only one distinct selectable
  prime value.
- Composite values may remain but cannot be selected.
- Fewer than `n` distinct prime values gives zero.
- Value `1` is not prime.
- Factorials and inverse factorials use the contest prime modulus.

## 3. Brute force: enumerate selected prime-value sets

```python
from collections import Counter
from itertools import combinations
from math import factorial, isqrt


MODULO = 998_244_353


def factorization_count_brute(values: list[int]) -> int:
    if (
        not values
        or len(values) % 2
        or any(type(value) is not int or value <= 0 for value in values)
    ):
        raise ValueError("values must contain a positive even-sized multiset")

    def is_prime(value: int) -> bool:
        if value < 2:
            return False
        return all(value % divisor for divisor in range(2, isqrt(value) + 1))

    half = len(values) // 2
    frequency = Counter(values)
    primes = [value for value in frequency if is_prime(value)]
    answer = 0
    for selected in combinations(primes, half):
        remaining = frequency.copy()
        for value in selected:
            remaining[value] -= 1
        permutations = factorial(half)
        for count in remaining.values():
            permutations //= factorial(count)
        answer += permutations
    return answer % MODULO
```

**Complexity:** exponential in the number of distinct prime values.

## 4. Better approach: subset DP over distinct primes

A bitmask may choose prime values and multiply their occurrence counts. Only
the number chosen matters, so a cardinality DP collapses `2^p` states to `n`.

## 5. Expert solution: frequency-weighted cardinality DP

```python
from collections import Counter


MODULO = 998_244_353


def factorization_count(values: list[int]) -> int:
    if (
        not values
        or len(values) % 2
        or any(type(value) is not int or value <= 0 for value in values)
    ):
        raise ValueError("values must contain a positive even-sized multiset")
    half = len(values) // 2
    maximum = max(values)
    is_prime = bytearray(b"\x01") * (maximum + 1)
    if maximum >= 0:
        is_prime[0] = 0
    if maximum >= 1:
        is_prime[1] = 0
    divisor = 2
    while divisor * divisor <= maximum:
        if is_prime[divisor]:
            start = divisor * divisor
            is_prime[start : maximum + 1 : divisor] = b"\x00" * (
                (maximum - start) // divisor + 1
            )
        divisor += 1

    factorial = [1] * (len(values) + 1)
    for value in range(1, len(factorial)):
        factorial[value] = factorial[value - 1] * value % MODULO
    inverse_factorial = [1] * len(factorial)
    inverse_factorial[-1] = pow(factorial[-1], MODULO - 2, MODULO)
    for value in range(len(values), 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % MODULO

    frequency = Counter(values)
    base = factorial[half]
    for count in frequency.values():
        base = base * inverse_factorial[count] % MODULO

    dp = [0] * (half + 1)
    dp[0] = 1
    for value, count in frequency.items():
        if not is_prime[value]:
            continue
        for chosen in range(half - 1, -1, -1):
            dp[chosen + 1] += dp[chosen] * count
            dp[chosen + 1] %= MODULO
    return base * dp[half] % MODULO
```

### Why the expert code is correct

The base contains the permutation denominator before selection. Choosing a
distinct prime value multiplies by its frequency, exactly replacing `count!`
with `(count-1)!`. The descending cardinality transition chooses each prime
value at most once, so `dp[n]` sums precisely all valid selections.

**Complexity:** `O(max_value log log max_value + n * distinct_primes)` time and
`O(max_value + n)` space.

## 6. What to remember

```text
remove one copy -> factorial denominator changes by its frequency
selected values must be distinct primes -> one transition per prime value
choose exactly n -> one-dimensional cardinality DP
```
