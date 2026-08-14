# ICPC300 022: Codeforces 1096G - Lucky Tickets

**Source:** [Codeforces 1096G - Lucky Tickets](https://codeforces.com/problemset/problem/1096/G)  
**Pattern:** polynomial exponentiation with NTT

## Exact contract

Input gives an even ticket length `n` (`2 <= n <= 200000`), a count `k`
(`1 <= k <= 10`), and `k` distinct allowed decimal digits. Leading zeroes are
allowed. Count length-`n` tickets whose first `n/2` digits and last `n/2`
digits have equal sums. Output the count modulo `998244353`.

## First principles

The two halves are independent. If `ways[x]` is the number of allowed
half-tickets with digit sum `x`, the answer is `sum(ways[x]^2)`.

Let `P(x)` contain coefficient `1` at every allowed digit. For
`h = n/2`, coefficient `x` of `P(x)^h` is exactly `ways[x]`. The only large
step is raising this small polynomial to a huge power.

## Cases that decide correctness

- Zero is an ordinary allowed digit and may appear first.
- Repeated use of an allowed digit is permitted.
- With one allowed digit, exactly one ticket exists and it is lucky.
- Coefficients are modular; unlike an existence problem, no coefficient may be
  replaced by a Boolean value.

## Brute force: enumerate every half-ticket

```python
from collections import Counter
from itertools import product


def count_lucky_brute(length: int, digits: list[int]) -> int:
    half = length // 2
    sum_counts = Counter(sum(ticket) for ticket in product(digits, repeat=half))
    return sum(count * count for count in sum_counts.values()) % 998_244_353
```

Enumerating halves rather than whole tickets already uses their independence,
but still takes `k^(n/2)` time.

## Better: dynamic programming by position and sum

```python
def count_lucky_dp(length: int, digits: list[int]) -> int:
    modulus = 998_244_353
    ways = [1]

    for _ in range(length // 2):
        next_ways = [0] * (len(ways) + 9)
        for current_sum, count in enumerate(ways):
            for digit in digits:
                next_ways[current_sum + digit] = (
                    next_ways[current_sum + digit] + count
                ) % modulus
        ways = next_ways

    return sum(count * count for count in ways) % modulus
```

This shares all prefixes with the same sum. Its `O(k n^2)` worst-case time is
useful for moderate `n`, but not the source limit.

## Expert solution: evaluate, power, interpolate

```python
import sys


MODULUS = 998_244_353
PRIMITIVE_ROOT = 3


def ntt(values: list[int], invert: bool) -> None:
    size = len(values)
    target = 0
    for index in range(1, size):
        bit = size >> 1
        while target & bit:
            target ^= bit
            bit >>= 1
        target ^= bit
        if index < target:
            values[index], values[target] = values[target], values[index]

    block_size = 2
    while block_size <= size:
        root = pow(PRIMITIVE_ROOT, (MODULUS - 1) // block_size, MODULUS)
        if invert:
            root = pow(root, MODULUS - 2, MODULUS)
        half = block_size // 2

        for block_start in range(0, size, block_size):
            factor = 1
            for offset in range(half):
                even = values[block_start + offset]
                odd = values[block_start + offset + half] * factor % MODULUS
                values[block_start + offset] = (even + odd) % MODULUS
                values[block_start + offset + half] = (even - odd) % MODULUS
                factor = factor * root % MODULUS
        block_size <<= 1

    if invert:
        inverse_size = pow(size, MODULUS - 2, MODULUS)
        for index, value in enumerate(values):
            values[index] = value * inverse_size % MODULUS


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    length, digit_count = data[0], data[1]
    digits = data[2 : 2 + digit_count]
    half = length // 2
    maximum_sum = max(digits) * half

    transform_size = 1
    while transform_size <= maximum_sum:
        transform_size <<= 1

    polynomial = [0] * transform_size
    for digit in digits:
        polynomial[digit] = 1

    ntt(polynomial, False)
    for index, value in enumerate(polynomial):
        polynomial[index] = pow(value, half, MODULUS)
    ntt(polynomial, True)

    answer = (
        sum(coefficient * coefficient for coefficient in polynomial[: maximum_sum + 1])
        % MODULUS
    )
    print(answer)


if __name__ == "__main__":
    solve()
```

The transform length is strictly greater than the degree of `P^h`, so the
cyclic multiplication performed by the NTT cannot wrap around. Pointwise
raising transformed values to `h` is therefore exactly polynomial
exponentiation.

**Complexity:** `O(n log n + n log n)` modular operations (the pointwise powers
add `O(n log n)` bit-exponent steps) and `O(n)` space.

