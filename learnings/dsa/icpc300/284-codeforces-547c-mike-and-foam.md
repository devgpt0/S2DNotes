# ICPC300 284: Codeforces 547C - Mike and Foam

**Source:** [Codeforces 547C - Mike and Foam](https://codeforces.com/problemset/problem/547/C)  
**Rating:** 2200  
**Pattern:** dynamic inclusion-exclusion over square-free divisors  
**Goal:** Toggle indexed positive integers active or inactive. After every
toggle, return the number of active unordered pairs with greatest common
divisor one.

## 1. First principles

For a value with distinct prime factors `p1..pk`, inclusion-exclusion counts
active values sharing none of those primes:

```text
coprime(value) = sum(mu(divisor) * active_multiples[divisor])
```

Only square-free divisors made from distinct prime factors participate, so one
toggle touches at most `2^k` counters.

## 2. Cases that decide correctness

- Toggling an active index removes it; toggling an inactive index adds it.
- Equal values at different indices are separate elements.
- Value one is coprime with every active value.
- On removal, divisor counters are decremented before counting remaining pairs.
- Pair counts are unordered and never include an element with itself.

## 3. Brute force: recount every active pair

```python
from math import gcd


def coprime_pair_counts_brute(values: list[int], toggles: list[int]) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")
    if any(not 0 <= index < len(values) for index in toggles):
        raise ValueError("toggle index out of range")

    active = [False] * len(values)
    answers: list[int] = []
    for index in toggles:
        active[index] = not active[index]
        answers.append(
            sum(
                active[first]
                and active[second]
                and gcd(values[first], values[second]) == 1
                for first in range(len(values))
                for second in range(first + 1, len(values))
            )
        )
    return answers
```

**Complexity:** `O(q n^2 log A)` time and `O(n)` space.

## 4. Better transition: count new pairs only

Maintain how many active values are divisible by each square-free divisor. On
insertion, inclusion-exclusion directly gives the number of new coprime
partners. On removal, delete the value from all counters first, then subtract
the partners that remain.

## 5. Expert solution: Mobius signs from distinct prime subsets

```python
from math import isqrt


def coprime_pair_counts(values: list[int], toggles: list[int]) -> list[int]:
    if not values or any(value <= 0 for value in values):
        raise ValueError("values must be positive")
    if any(not 0 <= index < len(values) for index in toggles):
        raise ValueError("toggle index out of range")

    limit = max(values)
    smallest_prime = list(range(limit + 1))
    for prime in range(2, isqrt(limit) + 1):
        if smallest_prime[prime] != prime:
            continue
        for multiple in range(prime * prime, limit + 1, prime):
            if smallest_prime[multiple] == multiple:
                smallest_prime[multiple] = prime

    divisor_signs: dict[int, list[tuple[int, int]]] = {}
    for value in set(values):
        remaining = value
        primes: list[int] = []
        while remaining > 1:
            prime = smallest_prime[remaining]
            primes.append(prime)
            while remaining % prime == 0:
                remaining //= prime
        pairs = [(1, 1)]
        for prime in primes:
            pairs += [(divisor * prime, -sign) for divisor, sign in pairs]
        divisor_signs[value] = pairs

    active_multiples = [0] * (limit + 1)
    active = [False] * len(values)
    pair_count = 0
    answers: list[int] = []
    for index in toggles:
        pairs = divisor_signs[values[index]]
        if active[index]:
            for divisor, _sign in pairs:
                active_multiples[divisor] -= 1
            pair_count -= sum(
                sign * active_multiples[divisor] for divisor, sign in pairs
            )
            active[index] = False
        else:
            pair_count += sum(
                sign * active_multiples[divisor] for divisor, sign in pairs
            )
            for divisor, _sign in pairs:
                active_multiples[divisor] += 1
            active[index] = True
        answers.append(pair_count)
    return answers
```

### Why the expert code is correct

Inclusion-exclusion over the value's distinct prime factors counts exactly the
active values divisible by none of them, which is equivalent to gcd one. An
insertion creates one pair with each such value. A removal first excludes
itself from all divisor counters and then deletes exactly its remaining
coprime pairs, so the maintained total is correct after every toggle.

**Complexity:** `O(A log log A + (n + q) 2^omega)` time and `O(A)` space.

## 6. What to remember

```text
gcd equals one -> share no prime factor
share no factor -> inclusion-exclusion over distinct primes
dynamic pairs -> add or remove only one element's partners
```
