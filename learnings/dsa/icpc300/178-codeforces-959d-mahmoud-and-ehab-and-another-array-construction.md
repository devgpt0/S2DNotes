# ICPC300 178: Codeforces 959D - Mahmoud and Ehab and another array construction

**Source:** [Codeforces 959D - Mahmoud and Ehab and another array construction](https://codeforces.com/problemset/problem/959/D)  
**Pattern:** lexicographic greedy with globally reserved prime factors

## Exact contract

Given an array `a` of integers in `[2, 10^6]`, construct the lexicographically
smallest array `b` such that `b >= a` lexicographically, every `b[i] >= 2`, and
every pair of values in `b` is coprime.

## First principles

Pairwise coprimality means no prime factor may appear in two chosen values.
Keep the input prefix exactly while its prime factors are unused. At the first
conflict, choose the smallest compatible value strictly greater than `a[i]`;
the result is now lexicographically greater, so every remaining position can
take the smallest value compatible with the reserved primes.

That smallest suffix value is always an unused prime: any composite is larger
than one of its own available prime factors.

## Cases that decide correctness

- The comparison with `a` is lexicographic, not componentwise.
- A repeated prime factor inside one number is reserved only once.
- The first changed value must be strictly greater than the input value.
- After that change, suffix values may be smaller than their input values.
- Values are at least two, so repeated `1`s are not an available shortcut.

## Brute force: enumerate bounded arrays lexicographically

```python
from itertools import product
from math import gcd


def another_array_brute(values: list[int], maximum: int) -> list[int]:
    if not values or any(type(value) is not int or value < 2 for value in values):
        raise ValueError("values must be integers of at least two")
    if type(maximum) is not int or maximum < 2:
        raise ValueError("maximum must be an integer of at least two")

    original = tuple(values)
    for candidate in product(range(2, maximum + 1), repeat=len(values)):
        if candidate < original:
            continue
        if all(
            gcd(candidate[first], candidate[second]) == 1
            for first in range(len(candidate))
            for second in range(first + 1, len(candidate))
        ):
            return list(candidate)
    raise ValueError("maximum is too small to contain a solution")
```

The bounded Cartesian product is useful only for tiny differential tests.

## Better approach: no separate intermediate

Trial division can implement the same lexicographic greedy on small values, but
does not change its invariant or asymptotic candidate search. The
smallest-prime-factor table is the production implementation of that greedy.

## Expert solution: smallest-prime-factor sieve and greedy construction

```python
from array import array

MAXIMUM_INPUT = 1_000_000
SIEVE_LIMIT = 2_000_000


def construct_pairwise_coprime_array(values: list[int]) -> list[int]:
    if not values or any(
        type(value) is not int or not 2 <= value <= MAXIMUM_INPUT for value in values
    ):
        raise ValueError("values must be integers in [2, 1_000_000]")

    smallest_prime = array("I", range(SIEVE_LIMIT + 1))
    for prime in range(2, int(SIEVE_LIMIT**0.5) + 1):
        if smallest_prime[prime] != prime:
            continue
        for multiple in range(prime * prime, SIEVE_LIMIT + 1, prime):
            if smallest_prime[multiple] == multiple:
                smallest_prime[multiple] = prime

    used = bytearray(SIEVE_LIMIT + 1)

    def distinct_factors(value: int) -> list[int]:
        factors: list[int] = []
        while value > 1:
            prime = smallest_prime[value]
            factors.append(prime)
            while value % prime == 0:
                value //= prime
        return factors

    answer: list[int] = []
    changed = False
    for index, value in enumerate(values):
        factors = distinct_factors(value)
        if not changed and all(not used[prime] for prime in factors):
            answer.append(value)
            for prime in factors:
                used[prime] = 1
            continue

        candidate = value + 1
        while candidate <= SIEVE_LIMIT:
            factors = distinct_factors(candidate)
            if all(not used[prime] for prime in factors):
                break
            candidate += 1
        if candidate > SIEVE_LIMIT:
            raise ValueError("source constraints no longer guarantee a candidate")

        answer.append(candidate)
        for prime in factors:
            used[prime] = 1
        changed = True

        next_prime = 2
        for _ in range(index + 1, len(values)):
            while smallest_prime[next_prime] != next_prime or used[next_prime]:
                next_prime += 1
            answer.append(next_prime)
            used[next_prime] = 1
        break

    return answer
```

Before the first change, choosing the input value is the only lexicographically
minimal choice. At the first conflict, exhaustive increasing search selects the
smallest legal greater value. The remaining unused primes are then the smallest
legal suffix values, proving the whole array is lexicographically minimal.

**Complexity:** `O(L log log L + n log L)` expected time and `O(L)` space for
`L = 2_000_000`; candidate searches factor the inspected integers by their
smallest prime factors.
