# ICPC300 173: Codeforces 895C - Square Subsets

**Source:** [Codeforces 895C - Square Subsets](https://codeforces.com/problemset/problem/895/C)  
**Pattern:** parity vectors over primes and linear algebra over `GF(2)`

## Exact contract

Given `n` integers in `[1, 70]`, count the nonempty index subsets whose product
is a perfect square. Equal values at different indices are distinct choices.
Return the count modulo `1_000_000_007`.

## First principles

An integer is a square exactly when every prime exponent is even. Replace each
value by a bit mask that records which of the 19 primes up to 70 have odd
exponents. A subset product is square exactly when the XOR of its masks is zero.

This gives two useful views:

- DP counts selections by their current XOR mask.
- Linear algebra counts vectors in the kernel of the mask matrix.

## Cases that decide correctness

- The empty subset has XOR zero and must be subtracted once.
- Every occurrence of a repeated value remains an independent index choice.
- Value `1` has mask zero, so each occurrence doubles every subset count.
- Prime powers contribute only the parity of their exponent.

## Brute force: enumerate index subsets

```python
from math import isqrt


def square_subsets_brute(values: list[int]) -> int:
    if not values or any(
        type(value) is not int or not 1 <= value <= 70 for value in values
    ):
        raise ValueError("values must be integers in [1, 70]")

    answer = 0
    for selection in range(1, 1 << len(values)):
        product = 1
        for index, value in enumerate(values):
            if selection >> index & 1:
                product *= value
        root = isqrt(product)
        answer += root * root == product
    return answer % 1_000_000_007
```

This is `O(n 2^n)` time and is useful only as a small-instance oracle.

## Better approach: frequency DP over parity masks

For a value occurring `c` times, there are `2^(c-1)` ways to choose an even
number of copies and the same number of ways to choose an odd number. Process
each distinct value once.

```python
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67)
MODULO = 1_000_000_007


def square_subsets_frequency_dp(values: list[int]) -> int:
    if not values or any(
        type(value) is not int or not 1 <= value <= 70 for value in values
    ):
        raise ValueError("values must be integers in [1, 70]")

    masks = [0] * 71
    for value in range(1, 71):
        remaining = value
        for bit, prime in enumerate(PRIMES):
            while remaining % prime == 0:
                masks[value] ^= 1 << bit
                remaining //= prime

    frequencies = [0] * 71
    for value in values:
        frequencies[value] += 1

    ways = {0: 1}
    for value, frequency in enumerate(frequencies):
        if frequency == 0:
            continue
        parity_choices = pow(2, frequency - 1, MODULO)
        following: dict[int, int] = {}
        value_mask = masks[value]
        for mask, count in ways.items():
            following[mask] = (following.get(mask, 0) + count * parity_choices) % MODULO
            changed = mask ^ value_mask
            following[changed] = (
                following.get(changed, 0) + count * parity_choices
            ) % MODULO
        ways = following
    return (ways.get(0, 0) - 1) % MODULO
```

At most `2^19` masks are reachable. The time is `O(70 * 2^19)` and the space
is `O(2^19)`.

## Expert solution: rank-nullity over `GF(2)`

The `n` masks are columns of a 19-row binary matrix. If its rank is `r`, its
kernel has dimension `n-r`, so exactly `2^(n-r)` index subsets XOR to zero.

```python
PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67)
MODULO = 1_000_000_007


def square_subsets(values: list[int]) -> int:
    if not values or any(
        type(value) is not int or not 1 <= value <= 70 for value in values
    ):
        raise ValueError("values must be integers in [1, 70]")

    basis = [0] * len(PRIMES)
    rank = 0
    for value in values:
        mask = 0
        remaining = value
        for bit, prime in enumerate(PRIMES):
            while remaining % prime == 0:
                mask ^= 1 << bit
                remaining //= prime

        while mask:
            bit = mask.bit_length() - 1
            if basis[bit]:
                mask ^= basis[bit]
            else:
                basis[bit] = mask
                rank += 1
                break

    return (pow(2, len(values) - rank, MODULO) - 1) % MODULO
```

Gaussian insertion preserves the span of all processed masks and increments
`rank` exactly for an independent vector. Rank-nullity then counts every
zero-XOR subset, including the empty subset removed at the end.

**Complexity:** `O(19n)` time and `O(19)` auxiliary space.
