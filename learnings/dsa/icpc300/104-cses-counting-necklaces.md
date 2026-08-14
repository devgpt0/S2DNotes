# ICPC300 104: CSES - Counting Necklaces

**Source:** [CSES - Counting Necklaces](https://cses.fi/problemset/task/2209/)  
**Pattern:** Burnside's lemma over cyclic rotations  
**Goal:** Count, modulo `1_000_000_007`, length-`n` necklaces using `m` colors,
where colorings that differ only by rotation are the same.

## 1. Problem in plain words

A necklace has no distinguished starting bead. For example, `RGB`, `GBR`, and
`BRG` describe one necklace.

Simply dividing `m^n` by `n` is wrong because periodic colorings are fixed by
more than one rotation. Burnside's lemma averages the number of colorings fixed
by each rotation.

## 2. First principles

Rotating by `r` positions partitions bead positions into `gcd(n, r)` cycles.
A coloring stays unchanged exactly when every position cycle has one color, so
that rotation fixes `m^gcd(n,r)` colorings.

Burnside gives:

`answer = (1/n) * sum(m^gcd(n,r), r=0..n-1)`.

Group rotations by `d = n / gcd(n,r)`. For each divisor `d` of `n`, exactly
`phi(d)` rotations have `gcd(n,r) = n/d`, producing the divisor formula:

`sum(phi(d) * m^(n/d), d divides n) / n`.

## 3. Cases that decide correctness

| Case | Required result |
| --- | --- |
| `n = 1` | `m`. |
| One color | `1` for every necklace length. |
| Prime `n` | Identity plus `n-1` one-cycle rotations. |
| Periodic coloring | Burnside weights its larger stabilizer correctly. |
| Modular division by `n` | Multiply by the modular inverse. |

## 4. Brute force: canonicalize every coloring

```python
from itertools import product


def count_necklaces_brute_force(length: int, color_count: int) -> int:
    if length < 1 or color_count < 1:
        raise ValueError("length and color count must be positive")

    necklaces: set[tuple[int, ...]] = set()
    for coloring in product(range(color_count), repeat=length):
        canonical = min(coloring[shift:] + coloring[:shift] for shift in range(length))
        necklaces.add(canonical)
    return len(necklaces)
```

**Complexity:** `O(m^n n^2)` tuple work and `O(m^n n)` memory.

## 5. Better: apply Burnside one rotation at a time

```python
from math import gcd

MODULO = 1_000_000_007


def count_necklaces_by_rotations(length: int, color_count: int) -> int:
    if length < 1 or color_count < 1 or length % MODULO == 0:
        raise ValueError("source bounds require positive values and invertible length")

    fixed_sum = (
        sum(
            pow(color_count, gcd(length, rotation), MODULO)
            for rotation in range(length)
        )
        % MODULO
    )
    return fixed_sum * pow(length, MODULO - 2, MODULO) % MODULO
```

**Complexity:** `O(n log n)` time and `O(1)` auxiliary memory.

## 6. Expert solution: group rotations by divisors

```python
from math import isqrt

MODULO = 1_000_000_007


def count_necklaces(length: int, color_count: int) -> int:
    if length < 1 or color_count < 1 or length % MODULO == 0:
        raise ValueError("source bounds require positive values and invertible length")

    prime_factors: list[int] = []
    remaining = length
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            prime_factors.append(candidate)
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        prime_factors.append(remaining)

    def euler_phi(value: int) -> int:
        result = value
        for prime in prime_factors:
            if value % prime == 0:
                result -= result // prime
        return result

    fixed_sum = 0
    for divisor in range(1, isqrt(length) + 1):
        if length % divisor != 0:
            continue
        fixed_sum += euler_phi(divisor) * pow(color_count, length // divisor, MODULO)
        paired = length // divisor
        if paired != divisor:
            fixed_sum += euler_phi(paired) * pow(color_count, length // paired, MODULO)
    return fixed_sum % MODULO * pow(length, MODULO - 2, MODULO) % MODULO
```

### Why the expert code is correct

- A rotation fixes exactly one independently chosen color per position cycle.
- Rotation by `r` has `gcd(n,r)` cycles.
- `phi(d)` counts exactly the rotations whose cycle count is `n/d`, so the
  divisor sum is the same fixed-coloring sum as direct Burnside.
- Dividing the group average by `n` counts each rotational orbit once.

**Complexity:** `O(sqrt(n) * number_of_prime_factors + log n)` time and
`O(number_of_prime_factors)` memory.

## 7. What to remember

For rotation-equivalent strings, Burnside averages fixed colorings. A rotation
by `r` has `gcd(n,r)` independent position cycles.
