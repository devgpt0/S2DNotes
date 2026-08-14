# Advanced Number Theory: Extended GCD, CRT, Phi, Mobius, and BSGS

These tools appear when simple GCD, sieve, and modular arithmetic are already
insufficient. Each has a non-negotiable precondition; write it down first.

## Extended Euclidean algorithm

Extended GCD finds `x, y` with `a*x + b*y = gcd(a, b)`. It proves that
`a*x + b*y = c` has an integer solution exactly when `gcd(a, b)` divides `c`.

```python
def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    if first == 0 and second == 0:
        raise ValueError("at least one value must be non-zero")
    old_r, remainder = abs(first), abs(second)
    old_x, x = 1, 0
    old_y, y = 0, 1
    while remainder:
        quotient = old_r // remainder
        old_r, remainder = remainder, old_r - quotient * remainder
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return old_r, old_x if first >= 0 else -old_x, old_y if second >= 0 else -old_y


gcd_value, x_value, y_value = extended_gcd(30, 18)
print(gcd_value, 30 * x_value + 18 * y_value)
```

Output:

```text
6 6
```

If `gcd(a, m) == 1`, `x % m` is the modular inverse of `a` from this result.

## Chinese remainder theorem

For pairwise coprime moduli, CRT combines `x = ai (mod mi)` into one residue
modulo `M = product(mi)`. Combine two congruences at a time using extended GCD.
If moduli are not coprime, a solution exists only when the two residues agree
modulo the GCD; reduce before combining.

```python
def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    if first == 0 and second == 0:
        raise ValueError("at least one value must be non-zero")
    old_r, remainder = abs(first), abs(second)
    old_x, x = 1, 0
    old_y, y = 0, 1
    while remainder:
        quotient = old_r // remainder
        old_r, remainder = remainder, old_r - quotient * remainder
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return old_r, old_x if first >= 0 else -old_x, old_y if second >= 0 else -old_y


def combine_coprime(first_remainder: int, first_modulus: int, second_remainder: int, second_modulus: int) -> tuple[int, int]:
    gcd_value, inverse, _ = extended_gcd(first_modulus, second_modulus)
    if gcd_value != 1 or first_modulus <= 0 or second_modulus <= 0:
        raise ValueError("moduli must be positive and coprime")
    step = (second_remainder - first_remainder) * inverse % second_modulus
    modulus = first_modulus * second_modulus
    return (first_remainder + first_modulus * step) % modulus, modulus


print(combine_coprime(2, 3, 3, 5))
```

Output:

```text
(8, 15)
```

## Euler phi and Mobius

`phi(n)` counts values in `1..n` coprime to `n`. From the distinct prime
factors of `n`, start at `n` and apply `result -= result // prime`.

Mobius `mu(n)` is zero if a squared prime divides `n`; otherwise it is `(-1)^k`
for `k` distinct prime factors. Its key identity is `sum(mu(d) for d | n) = 1`
when `n == 1`, otherwise zero. This reverses divisor-sum relationships and is
common in coprime-pair counting.

## Baby-step giant-step

BSGS solves `base^x = target (mod modulus)` in `O(sqrt(modulus))` time and
memory. The usual form assumes `gcd(base, modulus) == 1`; handle the
non-coprime reduction separately. It is useful for discrete logarithm, not for
ordinary modular exponentiation.

## Checklist

- Linear Diophantine equation: test `c % gcd(a, b) == 0`.
- Modular inverse: test coprimality, not merely nonzero.
- CRT: distinguish pairwise-coprime and general moduli.
- `phi` and `mu` depend on distinct factors; factor exponents matter for
  detecting a square in Mobius.
