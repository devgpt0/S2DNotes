# Combinatorics and Inclusion-Exclusion

Counting starts by defining one object precisely. Decide whether order matters,
whether repetition is allowed, and whether objects are distinguishable.

## Core counts

| Situation | Count |
| --- | --- |
| choose `r` of `n`, no order | `C(n, r)` |
| arrange `r` distinct items from `n` | `n! / (n-r)!` |
| arrange a multiset of total `n` | `n! / product(count!)` |
| non-negative `x1 + ... + xk = n` | `C(n + k - 1, k - 1)` |
| positive `x1 + ... + xk = n` | `C(n - 1, k - 1)` |

`C(n, r) = 0` when `r < 0` or `r > n`. Use symmetry `C(n, r) = C(n, n-r)`.

## Combinations modulo a prime

For many queries with prime `modulus` and `maximum < modulus`, precompute
factorials and inverse factorials. Setup is `O(maximum + log modulus)` and each
query is `O(1)`.

```python
def combinations(maximum: int, modulus: int) -> tuple[list[int], list[int]]:
    if maximum < 0 or modulus <= 1:
        raise ValueError("maximum must be non-negative and modulus greater than one")
    factorial = [1] * (maximum + 1)
    inverse_factorial = [1] * (maximum + 1)
    for value in range(1, maximum + 1):
        factorial[value] = factorial[value - 1] * value % modulus
    inverse_factorial[maximum] = pow(factorial[maximum], modulus - 2, modulus)
    for value in range(maximum, 0, -1):
        inverse_factorial[value - 1] = inverse_factorial[value] * value % modulus
    return factorial, inverse_factorial


def choose(n: int, r: int, factorial: list[int], inverse_factorial: list[int], modulus: int) -> int:
    if r < 0 or r > n:
        return 0
    return factorial[n] * inverse_factorial[r] % modulus * inverse_factorial[n - r] % modulus


factorial, inverse_factorial = combinations(10, 1_000_000_007)
print(choose(5, 2, factorial, inverse_factorial, 1_000_000_007))
```

Output:

```text
10
```

This template deliberately requires a prime modulus and `maximum < modulus`.
For other cases, see Lucas theorem and prime-power binomial methods.

## Inclusion-exclusion

To count objects with none of several bad properties, add single bad sets,
subtract pair intersections, add triple intersections, and continue with
alternating signs.

For integers in `1..n` divisible by at least one of pairwise distinct primes,
sum `n // product(subset)` with sign `+` for odd subset sizes and `-` for even.
Deduplicate primes first; otherwise intersections are counted incorrectly.

## Derangements and useful identities

A derangement has no fixed positions. `D(0)=1`, `D(1)=0`, and
`D(n)=(n-1)(D(n-1)+D(n-2))`. Also remember Pascal's identity:
`C(n,r)=C(n-1,r-1)+C(n-1,r)`.

## Checklist

- Does order matter? Are objects distinguishable? Can positions be empty?
- Prove the formula with `n <= 4` before coding.
- For inverse factorials, verify the modulus and `n` bounds.
- Inclusion-exclusion needs intersection sizes, not only individual counts.

For worked contest patterns - gaps, bounded distributions, derangements, and
Catalan counts - continue with [PnC patterns](11-pnc-patterns.md).
