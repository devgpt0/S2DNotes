# ICPC300 103: CSES - Divisor Analysis

**Source:** [CSES - Divisor Analysis](https://cses.fi/problemset/task/2182/)  
**Pattern:** multiplicative divisor formulas and modular exponents  
**Goal:** Given the prime factorization `N = product(p_i^a_i)`, output modulo
`1_000_000_007` the number, sum, and product of all positive divisors of `N`.

## 1. Problem in plain words

A divisor independently chooses exponent `0..a_i` for every prime. This gives
the divisor count and turns the divisor sum into a product of geometric sums.

The product of divisors is subtler because the number itself is far too large
to construct. Add prime powers one factor at a time and update the product of
all divisors algebraically.

## 2. First principles

For one prime power `p^a`:

- exponent choices: `a + 1`;
- sum of choices: `1 + p + ... + p^a`.

Suppose the processed part has `d` divisors with product `P`. After adding
`p^a`, every old divisor appears with each exponent `0..a`. The new product is:

`P^(a+1) * p^(d * a(a+1)/2)`.

Exponents of nonzero residues modulo prime modulus `M` may be reduced modulo
`M-1` by Fermat's theorem.

## 3. Cases that decide correctness

| Case | Required behavior |
| --- | --- |
| One prime power | Use its direct geometric formulas. |
| Perfect square `N` | Middle square-root divisor is paired with itself. |
| At least one odd exponent | Total divisor count is even. |
| Huge exponents | Reduce modular powers, never construct `N`. |
| Empty factorization in reusable code | Represents `N = 1`, whose only divisor is `1`. |

## 4. Brute force: materialize every divisor

```python
MODULO = 1_000_000_007


def analyze_divisors_brute_force(
    factors: list[tuple[int, int]],
) -> tuple[int, int, int]:
    if any(prime < 2 or exponent < 1 for prime, exponent in factors):
        raise ValueError("factors require primes at least two and positive exponents")

    divisors = [1]
    for prime, exponent in factors:
        powers = [prime**power for power in range(exponent + 1)]
        divisors = [divisor * power for divisor in divisors for power in powers]

    product = 1
    for divisor in divisors:
        product = product * divisor % MODULO
    return len(divisors) % MODULO, sum(divisors) % MODULO, product
```

**Complexity:** proportional to the number of divisors, which can be enormous.

## 5. Better: count, geometric sum, and parity-aware product

Pair each divisor `d` with `N/d`. If the divisor count is even, the product is
`N^(count/2)`. If every exponent is even, `N` is a square and the product is
`sqrt(N)^count`. The code computes the needed exponents modulo `M-1` without
dividing a modular residue by two.

```python
MODULO = 1_000_000_007
EXPONENT_MODULO = MODULO - 1


def analyze_divisors_by_pairing(factors: list[tuple[int, int]]) -> tuple[int, int, int]:
    if any(prime < 2 or exponent < 1 for prime, exponent in factors):
        raise ValueError("factors require primes at least two and positive exponents")
    if any(prime % MODULO in (0, 1) for prime, _ in factors):
        raise ValueError("source prime bounds must stay below the modulus")

    divisor_count = 1
    divisor_count_exponent = 1
    divisor_sum = 1
    number = 1
    square_root = 1
    first_odd = next(
        (index for index, (_, exponent) in enumerate(factors) if exponent % 2 == 1),
        None,
    )

    half_count_exponent = 1
    for index, (prime, exponent) in enumerate(factors):
        divisor_count = divisor_count * (exponent + 1) % MODULO
        divisor_count_exponent = (
            divisor_count_exponent * (exponent + 1) % EXPONENT_MODULO
        )
        geometric_sum = (
            (pow(prime, exponent + 1, MODULO) - 1) * pow(prime - 1, MODULO - 2, MODULO)
        ) % MODULO
        divisor_sum = divisor_sum * geometric_sum % MODULO
        number = number * pow(prime, exponent, MODULO) % MODULO
        square_root = square_root * pow(prime, exponent // 2, MODULO) % MODULO

        factor = exponent + 1
        if first_odd == index:
            factor //= 2
        half_count_exponent = half_count_exponent * factor % EXPONENT_MODULO

    if first_odd is None:
        divisor_product = pow(square_root, divisor_count_exponent, MODULO)
    else:
        divisor_product = pow(number, half_count_exponent, MODULO)
    return divisor_count, divisor_sum, divisor_product
```

**Complexity:** `O(k log A)` time and `O(1)` auxiliary memory.

## 6. Expert solution: update the divisor product incrementally

This formula avoids branching on whether the represented number is a square.

```python
MODULO = 1_000_000_007
EXPONENT_MODULO = MODULO - 1


def analyze_divisors(factors: list[tuple[int, int]]) -> tuple[int, int, int]:
    if any(prime < 2 or exponent < 1 for prime, exponent in factors):
        raise ValueError("factors require primes at least two and positive exponents")
    if any(prime % MODULO in (0, 1) for prime, _ in factors):
        raise ValueError("source prime bounds must stay below the modulus")

    divisor_count = 1
    previous_count_exponent = 1
    divisor_sum = 1
    divisor_product = 1

    for prime, exponent in factors:
        geometric_sum = (
            (pow(prime, exponent + 1, MODULO) - 1) * pow(prime - 1, MODULO - 2, MODULO)
        ) % MODULO
        divisor_sum = divisor_sum * geometric_sum % MODULO

        triangular = exponent * (exponent + 1) // 2
        divisor_product = (
            pow(divisor_product, exponent + 1, MODULO)
            * pow(
                prime,
                previous_count_exponent * triangular % EXPONENT_MODULO,
                MODULO,
            )
        ) % MODULO

        divisor_count = divisor_count * (exponent + 1) % MODULO
        previous_count_exponent = (
            previous_count_exponent * (exponent + 1) % EXPONENT_MODULO
        )

    return divisor_count, divisor_sum, divisor_product
```

### Why the expert code is correct

- Independent exponent choices multiply both divisor counts and geometric sums.
- When adding `p^a`, each old divisor occurs in `a+1` new divisors, contributing
  the factor `old_product^(a+1)`.
- Across all old divisors, new prime exponents sum to
  `old_count * (0+...+a)`, producing the second product factor.
- The recurrence starts with the sole divisor of `1`, so induction covers the
  complete factorization.

**Complexity:** `O(k log A)` time and `O(1)` auxiliary memory.

## 7. What to remember

For divisor products, extend the factorization one prime at a time. The update
`P^(a+1) * p^(old_count * a(a+1)/2)` avoids constructing the number.
