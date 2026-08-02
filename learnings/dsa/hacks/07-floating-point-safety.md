# Floating-Point Safety

## First principles

Most decimal fractions have no exact finite binary representation. Arithmetic
therefore returns a nearby representable value. Comparisons must reflect the
problem's error tolerance, and exact geometric or monetary logic should use
integers when possible.

## Why it matters

Binary floating point cannot represent most decimal fractions exactly.

```text
0.1 + 0.2 != 0.3 exactly
```

## Technique

1. Prefer integer arithmetic after scaling when input has fixed decimal places.
2. Compare approximate values with an absolute and relative tolerance.
3. In floating binary search, run a fixed number of iterations.

## Python patterns

```python
from math import isclose

if isclose(first, second, rel_tol=1e-9, abs_tol=1e-12):
    ...
```

```python
# Fixed-iteration binary search avoids an unstable equality stop.
left, right = 0.0, upper_bound
for _ in range(100):
    middle = (left + right) / 2.0
    if feasible(middle):
        right = middle
    else:
        left = middle
answer = right
```

Scaled money when inputs have exactly two decimal digits:

```python
whole, fraction = token.decode().split('.')
cents = int(whole) * 100 + int(fraction.ljust(2, '0'))
```

## Pattern recognition

Be cautious with geometry, probabilities, decimal money, roots, and equality
conditions derived from division.

## Visual worked example: equality fails

```text
mathematics: 0.1 + 0.2 = 0.3
binary float:
0.1 + 0.2 -> 0.30000000000000004

wrong: abs(a - b) == 0
safer: abs(a - b) <= eps * max(1, abs(a), abs(b))
```

Choose `eps` from the required precision and accumulated operations; it is
not a universal constant for every problem.

## Traps

- Using one epsilon for values near zero and values near `10^12`.
- Sorting with an epsilon-based comparator, which can violate transitivity.
- Rounding intermediate values before the final output.
- Using `Decimal` automatically; it is exact for decimals but often much slower.
